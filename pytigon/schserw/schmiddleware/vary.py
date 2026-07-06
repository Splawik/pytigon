"""Middleware for setting the HTTP Vary header.

The Vary header tells caching proxies which request headers affect
the response. This middleware allows views to set the Vary header
value on the request object, which is then applied to the response.
"""

import logging

logger = logging.getLogger(__name__)


class VaryMiddleware:
    """Middleware to set the 'Vary' header based on request attributes.

    Views can set `request.set_vary` to a header value, and this
    middleware will add it to the response's 'Vary' header.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.set_vary = None
        response = self.get_response(request)
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
