from __future__ import annotations
from typing import TYPE_CHECKING
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
    edited_by = models.ForeignKey(
        User,
        related_name='edited_messages',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text='Tracks which user last edited the message',
    )
    parent_message = models.ForeignKey(
        'self',
        related_name='replies',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        help_text='Reference to the parent message if this is a reply',
    )

    if TYPE_CHECKING:
        # Let type checkers know about reverse relation
        replies: models.Manager['Message']

    def get_thread(self):
        """
        Recursively fetch all replies to this message.
        """
        replies = []
        for reply in (
            self.replies.all()
            .select_related('sender', 'receiver')
            .prefetch_related('replies')
        ):
            replies.append(
                {
                    'id': reply.id,
                    'sender': reply.sender.username,
                    'receiver': reply.receiver.username,
                    'content': reply.content,
                    'timestamp': reply.timestamp,
                    'replies': reply.get_thread(),
                }
            )
        return replies

    def __str__(self) -> str:
        return f'Message from {self.sender} to {self.receiver}'


class MessageHistory(models.Model):
    message = models.ForeignKey(
        Message, related_name='msg_history', on_delete=models.CASCADE
    )
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(
        User,
        related_name='message_history',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text='User who performed the edit',
    )

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
