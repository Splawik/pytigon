from django.utils.deprecation import MiddlewareMixin
from django.core.exceptions import MiddlewareNotUsed


class VaryMiddleware(MiddlewareMixin):
    """
    Middleware to set the 'Vary' header in the HTTP response based on the request.
    """

    def process_request(self, request):
        """
        Initialize the `set_vary` attribute on the request object.
        """
        request.set_vary = None

    def process_response(self, request, response):
        """
        Set the 'Vary' header in the response if `set_vary` is specified in the request.

        Args:
            request: The HTTP request object.
            response: The HTTP response object.

        Returns:
            HttpResponse: The modified response object with the 'Vary' header set if applicable.
        """
        try:
            if request.set_vary is not None:
                response.headers["Vary"] = request.set_vary
            return response
        except Exception as e:
            # Log the error and re-raise to avoid silently failing
            raise MiddlewareNotUsed(f"Error processing response: {e}")
