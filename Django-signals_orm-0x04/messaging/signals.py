from typing import Any
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Message, MessageHistory, Notification


@receiver(pre_save, sender=Message)
def log_message_edit(sender: Any, instance: Message, **kwargs: Any) -> None:
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
            message=instance, old_content=old_instance.content
        )


@receiver(post_save, sender=Message)
def create_notification(
    sender: Any, instance: Message, created: bool, **kwargs: Any
) -> None:
    """
    Signal: When a new Message is created, generate a Notification for the receiver.
    """
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)
