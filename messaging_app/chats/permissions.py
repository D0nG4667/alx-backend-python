from rest_framework import permissions


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission:
    - Only authenticated users can access the API
    - Only participants of a conversation can view, send, update, or delete messages
    """

    def has_permission(self, request, view):
        # Ensure user is authenticated globally
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj): # type: ignore
        """
        Object-level check:
        - For Conversation objects: user must be in participants
        - For Message objects: user must be in the conversation participants
        """
        if hasattr(obj, "participants"):
            return request.user in obj.participants.all()

        if hasattr(obj, "conversation"):
            return request.user in obj.conversation.participants.all()

        return False

