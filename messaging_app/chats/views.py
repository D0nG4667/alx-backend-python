from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsOwner  # custom permission


class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        'participants__email',
        'participants__first_name',
        'participants__last_name',
    ]
    ordering_fields = ['created_at']

    def get_queryset(self): # type: ignore
        """
        Restrict conversations to those where the current user is a participant.
        """
        return Conversation.objects.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
        participant_ids = request.data.get('participants', [])
        if not participant_ids:
            return Response(
                {'error': 'Participants list is required.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        participants = User.objects.filter(id__in=participant_ids)
        if not participants.exists():
            return Response(
                {'error': 'No valid participants found.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Ensure the requesting user is always included
        conversation = Conversation.objects.create()
        conversation.participants.set(list(participants) + [request.user])
        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['message_body', 'sender__email', 'recipient__email']
    ordering_fields = ['sent_at']

    def get_queryset(self):  # type: ignore[override]
        """
        Restrict messages to those where the current user is sender or recipient.
        """
        user = self.request.user
        return Message.objects.filter(sender=user) | Message.objects.filter(
            recipient=user
        )

    def create(self, request, *args, **kwargs):
        sender_id = request.data.get('sender')
        recipient_id = request.data.get('recipient')
        conversation_id = request.data.get('conversation')
        message_body = request.data.get('message_body')

        if not all([sender_id, recipient_id, conversation_id, message_body]):
            return Response(
                {'error': 'All fields are required.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        sender = get_object_or_404(User, id=sender_id)
        recipient = get_object_or_404(User, id=recipient_id)
        conversation = get_object_or_404(Conversation, id=conversation_id)

        # Ensure the sender is the current user
        if sender != request.user:
            return Response(
                {'error': 'You can only send messages as yourself.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        message = Message.objects.create(
            sender=sender,
            recipient=recipient,
            conversation=conversation,
            message_body=message_body,
        )

        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
