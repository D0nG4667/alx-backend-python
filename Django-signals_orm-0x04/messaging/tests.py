from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Message, Notification

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
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content='Hello Receiver!',
        )

        notification = Notification.objects.filter(
            user=self.receiver, message=message
        ).first()
        self.assertIsNotNone(notification)
        self.assertEqual(notification.user, self.receiver)
        self.assertEqual(notification.message, message)
