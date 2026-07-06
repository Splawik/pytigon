"""Debugging and utility middleware for HTTP requests/responses.

Provides middleware classes for:
- Logging POST request data (ViewPost)
"""

import logging

logger = logging.getLogger(__name__)


class ViewRequests:
    """Log the HTTP method and path of each request."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.debug("%s %s", request.method, request.path)
        return self.get_response(request)


def view_post(get_response):
    """Middleware factory for logging POST request bodies.

    Args:
        get_response: The next middleware or view in the chain.

    Returns:
        Callable middleware function.
    """

    def middleware(request):
        try:
            if request.method == "POST":
                logger.debug("=================== POST ======================")
                logger.debug(request.path)
                logger.debug(request.POST)
                logger.debug("===============================================")
        except Exception:
            logger.warning("Failed to log POST data", exc_info=True)
        response = get_response(request)
        return response

    return middleware


class ViewPost:
    """Middleware for logging POST request bodies (class-based version)."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            if request.method == "POST":
                logger.debug("=================== POST ======================")
                logger.debug(request.path)
                logger.debug(request.POST)
                logger.debug("===============================================")
        except Exception:
            logger.warning("Failed to log POST data", exc_info=True)
        return self.get_response(request)
