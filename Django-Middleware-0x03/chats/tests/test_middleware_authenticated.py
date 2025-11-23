from pathlib import Path
import pytest
from django.test import Client
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from django.http import HttpResponse

LOG_FILE = Path(__file__).resolve().parent.parent.parent / 'requests.log'


@pytest.mark.django_db
def test_request_logging_authenticated_user() -> None:
    """
    Ensure RequestLoggingMiddleware logs authenticated user requests to requests.log
    """

    # Clean up any existing log file
    if LOG_FILE.exists():
        LOG_FILE.write_text("")

    User = get_user_model()
    user = User.objects.create_user(
        username='testuser', password='securepassword123'
    )

    # Create a DRF token for the user
    token = Token.objects.create(user=user)

    # Attach token to client requests (set default header)
    client = Client()
    client.defaults['HTTP_AUTHORIZATION'] = f'Token {token.key}'

    # Hit an endpoint (adjust path to one that exists in your app)
    response: HttpResponse = client.get('/api/v1/messages/')
    assert response.status_code in (200, 401, 404)

    # Verify log file was created
    assert LOG_FILE.exists()

    # Read log file contents
    logs = LOG_FILE.read_text()

    # Assert log contains the authenticated username and path
    assert 'User: testuser' in logs
    assert '/api/v1/messages/' in logs
