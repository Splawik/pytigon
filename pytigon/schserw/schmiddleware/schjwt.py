import logging

from django.contrib.auth import get_user_model
from django.utils.functional import SimpleLazyObject
from graphql_jwt.utils import get_http_authorization, get_payload

logger = logging.getLogger(__name__)


def get_user(request, username):
    """Retrieve and cache the user object based on the username."""
    if not hasattr(request, "_cached_user") or request._cached_user.is_anonymous:
        users = get_user_model().objects.filter(username=username)
        request._cached_user = users[0] if users.exists() else None
    return request._cached_user


class JWTUserMiddleware:
    """Middleware to authenticate users using JWT tokens."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = get_http_authorization(request)
        if token:
            try:
                payload = get_payload(token)
                username = payload.get("username")
                if username:
                    request.user = SimpleLazyObject(lambda: get_user(request, username))
            except Exception:
                logger.debug("JWT authentication failed", exc_info=True)
        return self.get_response(request)
