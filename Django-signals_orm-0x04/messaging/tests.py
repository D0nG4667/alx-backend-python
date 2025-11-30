from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from .models import Message, MessageHistory, Notification
from django.urls import reverse

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


class DeleteUserSignalTest(TestCase):
    def setUp(self) -> None:
        # Create sender and receiver
        self.sender = User.objects.create_user(
            username='sender', email='sender@example.com', password='pass123'
        )
        self.receiver = User.objects.create_user(
            username='receiver',
            email='receiver@example.com',
            password='pass123',
        )

        # Create a message
        self.message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content='Hello Receiver!',
        )

        # Create a notification for the receiver
        self.notification = Notification.objects.create(
            user=self.receiver, message=self.message
        )

        # Create a message history entry
        self.history = MessageHistory.objects.create(
            message=self.message,
            old_content='Old content',
            edited_by=self.sender,
        )

        # Client for simulating requests
        self.client = Client()
        self.client.login(username='sender', password='pass123')

    def test_delete_user_cleans_related_data(self) -> None:
        """
        Deleting a user should remove their account and all related
        messages, notifications, and histories.
        """
        self.client.force_login(self.sender)  # ensures authenticated

        response = self.client.get(reverse('messages:delete_user'))
        self.assertEqual(response.status_code, 200)

        # Verify sender is deleted
        self.assertFalse(User.objects.filter(username='sender').exists())

        # Verify related messages are deleted
        self.assertFalse(Message.objects.filter(sender=self.sender).exists())

        # Verify related notifications are deleted
        self.assertFalse(
            Notification.objects.filter(user=self.receiver).exists()
        )

        # Verify related histories are deleted
        self.assertFalse(
            MessageHistory.objects.filter(message=self.message).exists()
        )
