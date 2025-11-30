from __future__ import annotations
from typing import Any
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Message(models.Model):
    id = models.BigAutoField(primary_key=True)
    sender = models.ForeignKey(
        User, related_name='msg_sent_messages', on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        User, related_name='msg_received_messages', on_delete=models.CASCADE
    )
    content = models.TextField()
    timestamp: Any = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'Message from {self.sender} to {self.receiver}'


class MessageHistory(models.Model):
    message = models.ForeignKey(
        Message, related_name='msg_history', on_delete=models.CASCADE
    )
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'History for Message {self.message.id} at {self.edited_at}'


class Notification(models.Model):
    user = models.ForeignKey(
        User, related_name='msg_notifications', on_delete=models.CASCADE
    )
    message = models.ForeignKey(
        Message, related_name='msg_notifications', on_delete=models.CASCADE
    )
    created_at: Any = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'Notification for {self.user} - Message {self.message.id}'
