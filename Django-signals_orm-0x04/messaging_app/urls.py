"""
URL configuration for messaging_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.http import JsonResponse
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from rest_framework.authtoken.views import obtain_auth_token


def api_home(request):
    return JsonResponse(
        {
            'message': 'Welcome to the Messaging API',
            'versions': {
                'v1': '/api/v1/',
            },
        }
    )


def api_v1_home(request):
    return JsonResponse(
        {
            'version': 'v1',
            'endpoints': {
                'messages': '/api/v1/messages/',
                'auth_browsable': '/api/v1/auth/',
                'auth_token': '/api/v1/token/',
                'schema': '/api/v1/schema/',
                'swagger_ui': '/api/v1/docs/',
                'redoc': '/api/v1/redoc/',
            },
        }
    )


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    # API root and versioned root
    path('api/', api_home, name='api_home'),  # ✅ API home page
    path('api/v1/', api_v1_home, name='api_v1_home'),
    # Versioned endpoints
    path('api/v1/chats/', include('chats.urls')),
    path(
        'api/v1/auth/', include('rest_framework.urls')
    ),  # browsable API login/logout
    path('api/v1/token/', obtain_auth_token),  # token-based authentication
    # schema / docs
    path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    path(
        'api/v1/docs/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui',
    ),
    path(
        'api/v1/redoc/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc',
    ),
    path(
        'api/v1/messages/',
        include(('messaging.urls', 'messages'), namespace='messages'),
    ),
]
