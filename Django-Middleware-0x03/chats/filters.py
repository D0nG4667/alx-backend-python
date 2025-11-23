import django_filters
from .models import Message


class MessageFilter(django_filters.FilterSet):
    """
    Filter messages by sender, recipient, or time range.
    """

    sender = django_filters.NumberFilter(field_name='sender__id', lookup_expr='exact')
    recipient = django_filters.NumberFilter(
        field_name='recipient__id', lookup_expr='exact'
    )
    start_date = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='gte')
    end_date = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['sender', 'recipient', 'start_date', 'end_date']
