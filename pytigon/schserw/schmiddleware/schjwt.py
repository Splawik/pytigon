from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import get_user_model
from django.utils.functional import SimpleLazyObject
from graphql_jwt.utils import get_http_authorization, get_payload


def get_user(request, username):
    """Retrieve and cache the user object based on the username."""
    if not hasattr(request, "_cached_user") or request._cached_user.is_anonymous:
        users = get_user_model().objects.filter(username=username)
        request._cached_user = users[0] if users.exists() else None
    return request._cached_user


class JWTUserMiddleware(MiddlewareMixin):
    """Middleware to authenticate users using JWT tokens."""

    def process_request(self, request):
        """Process the request and set the user based on the JWT token."""
        token = get_http_authorization(request)
        if not token:
            return

        try:
            payload = get_payload(token)
            username = payload.get("username")
            if username:
                request.user = SimpleLazyObject(lambda: get_user(request, username))
        except Exception as e:
            # Log the exception if needed
            pass
