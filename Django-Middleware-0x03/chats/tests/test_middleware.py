from pathlib import Path
import pytest
from django.test import Client

LOG_FILE = Path(__file__).resolve().parent.parent.parent / 'requests.log'


@pytest.mark.django_db
def test_request_logging_middleware() -> None:
    """
    Ensure RequestLoggingMiddleware logs requests to requests.log
    """

    # Clean up any existing log file
    # if LOG_FILE.exists():
    #     LOG_FILE.write_text("")

    client = Client()

    # Hit an endpoint (adjust path to one that exists in your app)
    response = client.get('/api/v1/messages/')

    # Allow for 200, 404, or 401 depending on endpoint permissions
    assert response.status_code in (200, 401, 404)

    # Verify log file was created
    assert LOG_FILE.exists()

    # Read log file contents
    logs = LOG_FILE.read_text()

    # Assert log contains expected fields
    assert 'User:' in logs
    assert 'Path:' in logs
    assert '/api/v1/messages/' in logs
