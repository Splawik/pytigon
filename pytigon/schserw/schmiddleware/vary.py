"""Middleware for setting the HTTP Vary header.

The Vary header tells caching proxies which request headers affect
the response. This middleware allows views to set the Vary header
value on the request object, which is then applied to the response.
"""

import logging

from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)


class VaryMiddleware(MiddlewareMixin):
    """Middleware to set the 'Vary' header based on request attributes.

    Views can set `request.set_vary` to a header value, and this
    middleware will add it to the response's 'Vary' header.
    """

    def process_request(self, request):
        """Initialize the `set_vary` attribute on the request object.

        Args:
            request: The HTTP request object.
        """
        request.set_vary = None

    def process_response(self, request, response):
        """Set the 'Vary' header in the response if `set_vary` is specified.

        Args:
            request: The HTTP request object.
            response: The HTTP response object.

        Returns:
            HttpResponse: The modified response object with the
                'Vary' header set if applicable.
        """
        try:
            if request.set_vary is not None:
                response.headers["Vary"] = request.set_vary
        except Exception:
            logger.warning(
                "Failed to set Vary header to '%s'",
                getattr(request, "set_vary", None),
                exc_info=True,
            )
        return response
