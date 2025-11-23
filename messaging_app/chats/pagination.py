from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    """
    Custom pagination: 20 messages per page.
    """

    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
