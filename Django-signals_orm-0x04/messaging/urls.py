from django.urls import path
from . import views

urlpatterns = [
    path('delete-user/', views.delete_user, name='delete_user'),
    # Add more app-specific routes here
]
