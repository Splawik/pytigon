import logging

from django.contrib.auth import get_user_model
from django.utils.functional import SimpleLazyObject
from graphql_jwt.utils import get_http_authorization, get_payload

logger = logging.getLogger(__name__)


def get_user(request, username):
    """Retrieve and cache the user object based on the username."""
    cached = getattr(request, "_cached_user", None)
    if cached is None or cached.is_anonymous:
        request._cached_user = (
            get_user_model().objects.filter(username=username).first()
        )
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
