from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Message, MessageHistory, Notification

User = get_user_model()


class NotificationSignalTest(TestCase):
    def setUp(self) -> None:
        self.sender = User.objects.create_user(
            email='sender@example.com',
            username='sender',
            password='pass123',
            first_name='Sender',
            last_name='User',
        )
        self.receiver = User.objects.create_user(
            email='receiver@example.com',
            username='receiver',
            password='pass123',
            first_name='Receiver',
            last_name='User',
        )

    def test_notification_created_on_message(self) -> None:
        """Creating a message should create a notification for the receiver"""
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content='Hello Receiver!',
        )

        notification = Notification.objects.filter(
            user=self.receiver, message=message
        ).first()
        self.assertIsNotNone(notification)
        if notification is not None:
            self.assertEqual(notification.user, self.receiver)
            self.assertEqual(notification.message, message)


class MessageEditSignalTest(TestCase):
    def setUp(self) -> None:
        self.sender = User.objects.create_user(
            email='sender@example.com',
            username='sender',
            password='pass123',
            first_name='Sender',
            last_name='User',
        )
        self.receiver = User.objects.create_user(
            email='receiver@example.com',
            username='receiver',
            password='pass123',
            first_name='Receiver',
            last_name='User',
        )
        self.message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content='Original content',
        )

    def test_message_edit_creates_history(self) -> None:
        """Message edit should create a history record with old content"""
        self.message.content = 'Updated content'
        self.message.save()

        history = MessageHistory.objects.filter(message=self.message).first()
        self.assertIsNotNone(history)

        if history is not None:
            self.assertEqual(history.old_content, 'Original content')
            self.assertTrue(self.message.edited)
