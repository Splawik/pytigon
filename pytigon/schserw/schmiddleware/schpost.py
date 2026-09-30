"""Debugging and utility middleware for HTTP requests/responses.

Provides middleware classes for:
- Logging POST request data (ViewPost)
"""

import logging

logger = logging.getLogger(__name__)

# Values for these keys are replaced with "***" before a POST body is logged,
# otherwise debug logging writes plaintext passwords and tokens to disk.
_REDACTED_KEYS = frozenset(
    {
        "password",
        "password1",
        "password2",
        "new_password",
        "old_password",
        "new_password1",
        "new_password2",
        "passwd",
        "pass",
        "token",
        "access_token",
        "refresh_token",
        "secret",
        "secret_key",
        "api_key",
        "apikey",
        "authorization",
        "csrfmiddlewaretoken",
        "key",
    }
)


def _redacted(post_data):
    """Return the POST data with credential-looking values masked.

    Args:
        post_data: A QueryDict or other mapping of POST parameters.

    Returns:
        dict: The same keys, with sensitive values masked.
    """
    if post_data is None:
        return {}
    safe = {}
    for key in post_data:
        name = str(key)
        safe[name] = "***" if name.lower() in _REDACTED_KEYS else post_data[key]
    return safe


class ViewRequests:
    """Log the HTTP method and path of each request."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.debug("%s %s", request.method, request.path)
        return self.get_response(request)


def _log_post(request):
    """Log a POST request's path and body, swallowing logging failures."""
    try:
        if request.method == "POST":
            logger.debug("=================== POST ======================")
            logger.debug(request.path)
            logger.debug("body: %s", _redacted(request.POST))
            logger.debug("===============================================")
    except Exception:
        logger.warning("Failed to log POST data", exc_info=True)


def view_post(get_response):
    """Middleware factory for logging POST request bodies.

    Args:
        get_response: The next middleware or view in the chain.

    Returns:
        Callable middleware function.
    """

    def middleware(request):
        _log_post(request)
        return get_response(request)

    return middleware


class ViewPost:
    """Middleware for logging POST request bodies (class-based version).

    Equivalent to :func:`view_post` but usable in ``MIDDLEWARE`` as a class.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _log_post(request)
        return self.get_response(request)
