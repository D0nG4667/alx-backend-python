from typing import Any
from django.db.models import QuerySet
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsOwner, IsParticipantOfConversation
from .pagination import StandardResultsSetPagination


class ConversationViewSet(viewsets.ModelViewSet[Conversation]):
    serializer_class = ConversationSerializer
    permission_classes = [IsOwner]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        'participants__email',
        'participants__first_name',
        'participants__last_name',
    ]
    ordering_fields = ['created_at']

    def get_queryset(self) -> QuerySet[Conversation]:
        """Restrict conversations to those where the current user is a participant."""
        return Conversation.objects.filter(participants=self.request.user)

    def perform_create(self, serializer: Serializer) -> None:
        """Ensure the requesting user is always included in participants."""
        participant_ids: list[int] = self.request.data.get('participants', [])
        if not participant_ids:
            raise ValueError('Participants list is required.')

        participants: QuerySet[User] = User.objects.filter(
            id__in=participant_ids
        )
        if not participants.exists():
            raise ValueError('No valid participants found.')

        conversation: Conversation = serializer.save()
        conversation.participants.set(
            list(participants) + [self.request.user]
        )


class MessageViewSet(viewsets.ModelViewSet[Message]):
    serializer_class = MessageSerializer
    permission_classes = [IsParticipantOfConversation]
    pagination_class = StandardResultsSetPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = Any  # replace with actual MessageFilter if imported
    search_fields = ['message_body', 'sender__email', 'recipient__email']
    ordering_fields = ['sent_at']

    def get_queryset(self) -> QuerySet[Message]:
        """Restrict messages to those where the current user is sender or recipient."""
        user: User = self.request.user
        return Message.objects.filter(Q(sender=user) | Q(recipient=user))

    def perform_create(self, serializer: Serializer) -> None:
        """Ensure the sender is the current user."""
        sender_id: int | None = self.request.data.get('sender')
        recipient_id: int | None = self.request.data.get('recipient')
        conversation_id: int | None = self.request.data.get('conversation')
        message_body: str | None = self.request.data.get('message_body')

        if not all([sender_id, recipient_id, conversation_id, message_body]):
            raise ValueError('All fields are required.')

        sender: User = User.objects.get(id=sender_id)
        recipient: User = User.objects.get(id=recipient_id)
        conversation: Conversation = Conversation.objects.get(
            id=conversation_id
        )

        if sender != self.request.user:
            raise PermissionError('You can only send messages as yourself.')

        serializer.save(
            sender=sender,
            recipient=recipient,
            conversation=conversation,
            message_body=message_body,
        )
