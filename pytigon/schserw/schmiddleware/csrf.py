"""Middleware to disable CSRF protection for embedded Django server.

This middleware is used when running Pytigon as an embedded Django server,
where CSRF protection is not needed because the client is a desktop
application rather than a web browser.
"""

from django.utils.deprecation import MiddlewareMixin


class DisableCSRF(MiddlewareMixin):
    """Disable CSRF checks by setting _dont_enforce_csrf_checks on the request."""

    def process_request(self, request):
        """Set the flag that tells Django to skip CSRF validation.

        Args:
            request: The HTTP request object.
        """
        request._dont_enforce_csrf_checks = True
