from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpRequest
from django.contrib.auth import get_user_model

User = get_user_model()


@login_required
def delete_user(request: HttpRequest) -> JsonResponse:
    """
    View: Allows an authenticated user to delete their account.
    """
    user = request.user
    user.delete()  # <-- required check
    return JsonResponse(
        {'message': 'User account deleted successfully.'}, status=200
    )
