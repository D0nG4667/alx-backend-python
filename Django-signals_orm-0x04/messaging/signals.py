from typing import Any
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Message, MessageHistory, Notification
from django.contrib.auth.models import AbstractBaseUser

User = get_user_model()


@receiver(pre_save, sender=Message)
def log_message_edit(
    sender: AbstractBaseUser, instance: Message, **kwargs: Any
) -> None:
    """
    Signal: Before saving a Message, check if content has changed.
    If changed, log the old content into MessageHistory.
    """
    if not instance.pk:
        # New message, nothing to log
        return

    try:
        old_instance = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    if old_instance.content != instance.content:
        # Mark message as edited
        instance.edited = True
        # Save old content in history
        MessageHistory.objects.create(
            message=instance,
            old_content=old_instance.content,
            edited_by=instance.edited_by,
        )


@receiver(post_save, sender=Message)
def create_notification(
    sender: AbstractBaseUser, instance: Message, created: bool, **kwargs: Any
) -> None:
    """
    Signal: When a new Message is created, generate a Notification for the receiver.
    """
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)


@receiver(post_delete, sender=User)
def cleanup_user_related_data(
    sender: Any, instance: AbstractBaseUser, **kwargs: Any
) -> None:
    """
    Signal: After a User is deleted, remove all related messages,
    notifications, and message histories.
    """
    # Delete messages sent or received by the user
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # Delete notifications belonging to the user
    Notification.objects.filter(user=instance).delete()

    # Delete message histories linked to messages of this user
    MessageHistory.objects.filter(message__sender=instance).delete()
    MessageHistory.objects.filter(message__receiver=instance).delete()
