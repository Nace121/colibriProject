from django.contrib.auth import logout
from django.core.exceptions import ValidationError

class ClearBadSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            _ = request.user.is_authenticated
        except (ValidationError, ValueError, TypeError):
            # Session contient un ancien _auth_user_id incompatible
            logout(request)
        return self.get_response(request)
