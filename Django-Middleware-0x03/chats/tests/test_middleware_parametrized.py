from pathlib import Path
import pytest
from django.test import Client
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from django.http import HttpResponse

LOG_FILE = Path(__file__).resolve().parent.parent.parent / 'requests.log'


@pytest.mark.django_db
@pytest.mark.parametrize(
    'is_authenticated, expected_user, expected_status',
    [
        (False, 'Anonymous', 401),  # anonymous should get 401 Unauthorized
        (True, 'testuser', 200),  # authenticated should get 200 OK
    ],
)
def test_request_logging_middleware(
    is_authenticated: bool, expected_user: str, expected_status: int
) -> None:
    """
    Parametrized test to ensure RequestLoggingMiddleware logs both
    anonymous and authenticated user requests to requests.log.
    """

    # Clean up any existing log file
    if LOG_FILE.exists():
        LOG_FILE.write_text("")

    client = Client()

    if is_authenticated:
        User = get_user_model()
        user = User.objects.create_user(
            username='testuser', password='securepassword123'
        )
        # Create a DRF token for the user
        token = Token.objects.create(user=user)
        # Attach token to client requests
        client.defaults['HTTP_AUTHORIZATION'] = f'Token {token.key}'

    # Hit the endpoint
    response: HttpResponse = client.get('/api/v1/messages/')
    assert response.status_code == expected_status

    # Verify log file was created
    assert LOG_FILE.exists()

    # Read log file contents
    logs = LOG_FILE.read_text()

    # Assert log contains the expected user identity and path
    assert f'User: {expected_user}' in logs
    assert '/api/v1/messages/' in logs
