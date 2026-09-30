import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.utils.functional import SimpleLazyObject
from graphql_jwt.exceptions import JSONWebTokenError
from graphql_jwt.utils import get_http_authorization, get_payload

logger = logging.getLogger(__name__)


def get_user(request, username):
    """Retrieve and cache the user object based on the username.

    Returns ``AnonymousUser`` when the username does not resolve to a usable
    (existing and active) account, so that ``request.user.is_authenticated``
    is always a real boolean attribute.
    """
    # Deliberately not "_auth_user" / "_cached_user": those names belong to
    # Django's own authentication machinery and reusing them makes this
    # middleware fight with django.contrib.auth.
    cached = getattr(request, "_schjwt_user", None)
    if cached is None:
        user = get_user_model().objects.filter(username=username).first()
        if user is None:
            logger.info("JWT referenced a non-existent username")
        elif not user.is_active:
            logger.info("JWT referenced an inactive account")
            user = None
        cached = user if user is not None else AnonymousUser()
        request._schjwt_user = cached
    return cached


class JWTUserMiddleware:
    """Middleware to authenticate users using JWT tokens."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = get_http_authorization(request)
        if token:
            try:
                payload = get_payload(token)
            except (JSONWebTokenError, ValueError, TypeError, KeyError):
                # Logged without the token itself: it is a bearer credential.
                logger.info("JWT authentication failed", exc_info=True)
            else:
                username = payload.get("username")
                if username:
                    request.user = SimpleLazyObject(
                        lambda: get_user(request, username)
                    )
        return self.get_response(request)
