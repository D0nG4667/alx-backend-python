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

    def has_object_permission(self, request, view, obj):  # type: ignore
        """
        Object-level check:
        Applies to all methods: GET, POST, PUT, PATCH, DELETE
        """

        # For Conversation objects
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()

        # For Message objects
        if hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()

        return False


class IsOwner(permissions.BasePermission):
    """
    Custom permission:
    - Only the owner of a resource can update or delete it
    - Read operations are allowed for authenticated users
    """

    def has_permission(self, request, view):
        # Ensure user is authenticated globally
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):  # type: ignore
        """
        Object-level check:
        - Read operations allowed for authenticated users
        - Write operations only allowed for the owner
        """

        if request.method in permissions.SAFE_METHODS:
            return True

        # Assuming the object has an 'owner' attribute
        return obj.owner == request.user
