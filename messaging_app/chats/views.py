from rest_framework import viewsets, status, filters  
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]  
    search_fields = [
        'participants__email',
        'participants__first_name',
        'participants__last_name',
    ]
    ordering_fields = ['created_at']

    def create(self, request, *args, **kwargs):
        participant_ids = request.data.get('participants', [])
        if not participant_ids:
            return Response(
                {'error': 'Participants list is required.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        participants = User.objects.filter(user_id__in=participant_ids)
        if not participants.exists():
            return Response(
                {'error': 'No valid participants found.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]  
    search_fields = ['message_body', 'sender__email', 'recipient__email']
    ordering_fields = ['sent_at']

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

        sender = get_object_or_404(User, user_id=sender_id)
        recipient = get_object_or_404(User, user_id=recipient_id)
        conversation = get_object_or_404(Conversation, conversation_id=conversation_id)

        message = Message.objects.create(
            sender=sender,
            recipient=recipient,
            conversation=conversation,
            message_body=message_body,
        )

        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
