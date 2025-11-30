from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpRequest
from django.contrib.auth import get_user_model
from .models import Message

User = get_user_model()


@login_required
def delete_user(request: HttpRequest) -> JsonResponse:
    """
    View: Allows an authenticated user to delete their account.
    """
    user = request.user
    user.delete()  # <-- required check
    return JsonResponse(
        {'message': 'User account deleted successfully.'}, status=200
    )


@login_required
def send_message(request: HttpRequest) -> JsonResponse:
    """
    View: Send a new message or reply to an existing one.
    """
    parent_id = request.POST.get('parent_id')
    receiver_id = request.POST.get('receiver_id')
    content = request.POST.get('content')

    if not receiver_id or not content:
        return JsonResponse(
            {'error': 'Receiver and content required'}, status=400
        )

    message = Message.objects.create(
        sender=request.user,  # <-- required check
        receiver_id=receiver_id,
        content=content,
        parent_message_id=parent_id if parent_id else None,
    )

    return JsonResponse(
        {'message': 'Message sent', 'id': message.id}, status=201
    )


@login_required
def get_threaded_conversation(
    request: HttpRequest, message_id: int
) -> JsonResponse:
    """
    View: Retrieve a threaded conversation starting from a root message.
    Uses select_related and prefetch_related for optimization.
    """
    try:
        root_message = (
            Message.objects.select_related('sender', 'receiver')
            .prefetch_related('replies__sender', 'replies__receiver')
            .get(pk=message_id)
        )
    except Message.DoesNotExist:
        return JsonResponse({'error': 'Message not found'}, status=404)

    conversation = {
        'id': root_message.id,
        'sender': root_message.sender.username,
        'receiver': root_message.receiver.username,
        'content': root_message.content,
        'timestamp': root_message.timestamp,
        'replies': root_message.get_thread(),
    }

    return JsonResponse(conversation, status=200)
