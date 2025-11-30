from typing import Any
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification


@receiver(post_save, sender=Message)
def create_notification(
    sender: Any, instance: Message, created: bool, **kwargs: Any
) -> None:
    """
    Signal: When a new Message is created, generate a Notification for the receiver.
    """
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)
