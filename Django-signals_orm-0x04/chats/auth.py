#!/usr/bin/env python3
"""
Custom authentication views for messaging_app using JWT (SimpleJWT).
"""

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Extend the default JWT serializer to add custom claims if needed.
    Example: include user's email or role in the token payload.
    """

    def validate(self, attrs):
        data = super().validate(attrs)

        # Add custom claims
        data['email'] = self.user.email
        data['username'] = self.user.username

        # If you have roles/groups:
        data['roles'] = [group.name for group in self.user.groups.all()]

        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    JWT login view that uses the custom serializer.
    """

    serializer_class = CustomTokenObtainPairSerializer


# You can still use the default TokenRefreshView directly in urls.py
# Example:
# path("api/token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
# path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
