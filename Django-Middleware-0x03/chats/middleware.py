import logging
from datetime import datetime
from pathlib import Path
from typing import Callable
from django.http import HttpRequest, HttpResponse


class RequestLoggingMiddleware:
    """
    Middleware that logs each user request with timestamp, user, and request path.
    """

    def __init__(
        self, get_response: Callable[[HttpRequest], HttpResponse]
    ) -> None:
        self.get_response: Callable[[HttpRequest], HttpResponse] = (
            get_response
        )

        # Configure logger for request logging
        self.logger: logging.Logger = logging.getLogger('requests_logger')
        if not self.logger.handlers:  # Prevent duplicate handlers
            log_file: Path = Path('requests.log')
            handler: logging.FileHandler = logging.FileHandler(log_file)
            formatter: logging.Formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

    def __call__(self, request: HttpRequest) -> HttpResponse:
        # Determine user identity
        user: str = (
            request.user.username
            if request.user.is_authenticated
            else 'Anonymous'
        )

        # Log request details
        log_message: str = (
            f'{datetime.now()} - User: {user} - Path: {request.path}'
        )
        self.logger.info(log_message)

        # Continue request/response cycle
        response: HttpResponse = self.get_response(request)
        return response
