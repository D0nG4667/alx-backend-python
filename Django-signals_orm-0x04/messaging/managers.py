from django.db import models


class UnreadMessagesManager(models.Manager):
    def unread_for_user(self, user):
        """
        Return unread messages for a given user.
        Optimized with .only() to fetch minimal fields.
        """
        return self.filter(receiver=user, read=False).only(
            'id', 'sender', 'content', 'timestamp'
        )
