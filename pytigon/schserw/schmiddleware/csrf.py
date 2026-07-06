"""Middleware to disable CSRF protection for embedded Django server.

This middleware is used when running Pytigon as an embedded Django server,
where CSRF protection is not needed because the client is a desktop
application rather than a web browser.
"""


class DisableCSRF:
    """Disable CSRF checks by setting _dont_enforce_csrf_checks on the request."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request._dont_enforce_csrf_checks = True
        return self.get_response(request)
