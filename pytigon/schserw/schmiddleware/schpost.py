"""Debugging and utility middleware for HTTP requests/responses.

Provides middleware classes for:
- Logging POST request data (ViewPost)
"""

import logging

from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)


class ViewRequests(MiddlewareMixin):
    """Log the HTTP method and path of each request."""

    def process_request(self, request):
        """Log request method and path.

        Args:
            request: The HTTP request object.
        """
        logger.debug("%s %s", request.method, request.path)


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


class ViewPost(MiddlewareMixin):
    """Middleware for logging POST request bodies (class-based version)."""

    def process_request(self, request):
        """Log POST data if the request method is POST.

        Args:
            request: The HTTP request object.
        """
        try:
            if request.method == "POST":
                logger.debug("=================== POST ======================")
                logger.debug(request.path)
                logger.debug(request.POST)
                logger.debug("===============================================")
        except Exception:
            logger.warning("Failed to log POST data", exc_info=True)
