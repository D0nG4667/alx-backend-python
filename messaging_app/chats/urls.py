from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from django.urls import path, include
from .views import ConversationViewSet, MessageViewSet

# Base routers
routers = DefaultRouter()
routers.register(r'conversations', ConversationViewSet, basename='conversation')

# Nested routers for messages under conversations
nested_routers = NestedDefaultRouter(routers, r'conversations', lookup='conversation')
nested_routers.register(r'messages', MessageViewSet, basename='conversation-messages')

urlpatterns = [
    path('', include(routers.urls)),
    path('', include(nested_routers.urls)),
]
