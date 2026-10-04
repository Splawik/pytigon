"""Production guard middleware for the default administrator account.

Two responsibilities, both active only on a production web server:

* run the one-shot startup check (a loud log line, or a 503 when
  ``PYTIGON_STRICT_DEFAULT_ADMIN`` is enabled);
* force a password change for the bootstrap administrator until its password
  differs from the bootstrap default.

It is a deliberate no-op in the embedded desktop mode, so a local
single-user application never sees a login or a password prompt.
"""

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect

from pytigon.schserw.schsys import default_admin

# Paths that must stay reachable while forcing a password change, otherwise the
# redirect would loop.
_EXEMPT_SUFFIXES = (
    "/schsys/do_login/",
    "/schsys/do_logout/",
    "/schsys/change_password/",
    "/schsys/password_change/",
)

_BLOCKED_BODY = (
    "Server refused to start: the default administrator password has not been "
    "changed. See the server log for instructions."
)


class DefaultAdminGuardMiddleware:
    """Warn, block, or force a password change for the bootstrap administrator."""

    def __init__(self, get_response):
        """Store the next middleware/callable and per-process state.

        Args:
            get_response: The next callable in the middleware chain.
        """
        self.get_response = get_response
        self._startup_checked = False
        self._blocked = False

    def __call__(self, request):
        """Run the startup guard once, then enforce the password policy.

        Args:
            request: The incoming HTTP request.

        Returns:
            The downstream response, a redirect to the password-change page, or
            a 503 when strict mode blocked the server.
        """
        if not self._startup_checked:
            self._startup_checked = True
            self._blocked = default_admin.startup_check() == "blocked"

        if self._blocked:
            return HttpResponse(_BLOCKED_BODY, status=503)

        if self._should_force_change(request):
            from pytigon_lib.schdjangoext.tools import make_href

            return HttpResponseRedirect(make_href("/schsys/password_change/"))

        return self.get_response(request)

    def _should_force_change(self, request) -> bool:
        """Return whether this request must be redirected to change the password."""
        if not getattr(settings, "FORCE_PASSWORD_CHANGE_IN_PRODUCTION", True):
            return False
        if not default_admin.is_production_webserver():
            return False

        user = getattr(request, "user", None)
        if user is None or not user.is_authenticated:
            return False
        if self._is_exempt(getattr(request, "path", "")):
            return False

        return default_admin.user_has_default_password(user)

    @staticmethod
    def _is_exempt(path: str) -> bool:
        """Return whether *path* must be served even during a forced change."""
        if path.endswith(_EXEMPT_SUFFIXES):
            return True
        for prefix in (
            getattr(settings, "STATIC_URL", None),
            getattr(settings, "MEDIA_URL", None),
        ):
            if prefix and path.startswith(prefix):
                return True
        return False
