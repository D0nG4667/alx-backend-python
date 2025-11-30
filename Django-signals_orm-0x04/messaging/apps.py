from django.apps import AppConfig


class MessagingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'messaging'

    def ready(self) -> None:
        # Import signals when app is ready
        import messaging.signals  # noqa
