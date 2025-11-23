from typing import Callable, Dict, List
from django.http import HttpRequest, HttpResponse, JsonResponse
from datetime import datetime, timedelta
from collections import defaultdict
import logging
from pathlib import Path


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


class RestrictAccessByTimeMiddleware:
    """
    Middleware to restrict chat access outside 6AM–9PM.
    """

    def __init__(
        self, get_response: Callable[[HttpRequest], HttpResponse]
    ) -> None:
        self.get_response: Callable[[HttpRequest], HttpResponse] = (
            get_response
        )

    def __call__(self, request: HttpRequest) -> HttpResponse:
        current_hour: int = datetime.now().hour

        if not (6 <= current_hour < 21):
            return JsonResponse(
                {'error': 'Chat access restricted outside 6AM–9PM'},
                status=403,
            )

        response: HttpResponse = self.get_response(request)
        return response


class OffensiveLanguageMiddleware:
    """
    Middleware to limit number of chat messages per IP.
    Restricts to 5 POST requests (messages) per minute.
    """

    def __init__(
        self, get_response: Callable[[HttpRequest], HttpResponse]
    ) -> None:
        self.get_response: Callable[[HttpRequest], HttpResponse] = (
            get_response
        )
        # Dictionary to track requests per IP: {ip: [timestamps]}
        self.ip_requests: Dict[str, List[datetime]] = defaultdict(list)

    def __call__(self, request: HttpRequest) -> HttpResponse:
        # Only enforce on POST requests to chats/messages
        if request.method == 'POST' and '/chats/messages' in request.path:
            ip: str = self.get_client_ip(request)
            now: datetime = datetime.now()

            # Clean up old requests outside the 1-minute window
            self.ip_requests[ip] = [
                ts
                for ts in self.ip_requests[ip]
                if now - ts < timedelta(minutes=1)
            ]

            # Check limit
            if len(self.ip_requests[ip]) >= 5:
                return JsonResponse(
                    {'error': 'Message limit exceeded. Max 5 per minute.'},
                    status=403,
                )

            # Record this request
            self.ip_requests[ip].append(now)

        # Continue normal flow
        response: HttpResponse = self.get_response(request)
        return response

    def get_client_ip(self, request: HttpRequest) -> str:
        """
        Extract client IP address from request headers.
        """
        x_forwarded_for: str | None = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', '')
