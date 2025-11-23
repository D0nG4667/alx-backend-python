from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Allow access only if the object belongs to the requesting user.
    """

    def has_object_permission(self, request, view, obj):
        # Assuming Message and Conversation models have a `user` or `owner` field
        return obj.user == request.user
