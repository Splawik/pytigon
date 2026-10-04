"""Per-application access control for application URLs.

Some applications are tools rather than end-user features: the file manager
(``schcommander``) exposes the virtual filesystem — the project directory and
the data directory — and the installer/builder can execute code. Those
applications are generated export artefacts and must not be edited, so their
views are protected here, at the URL-prefix level, covering both the views that
go through ``form_with_perms`` and the plain Django views declared directly in
the application's ``urls.py``.

Two lists drive the policy, both overridable through the environment:

* ``settings.STAFF_ONLY_APPS`` — requires ``request.user.is_staff``, also on a
  ``PUBLIC`` site.
* ``settings.LOGIN_ONLY_APPS`` — requires an authenticated user, relaxed when
  the whole site is ``PUBLIC``.

Anonymous requests are answered with 401 (or redirected to ``LOGIN_URL`` when
one is configured); authenticated users without the required permission get 403.
"""

import logging

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.http import urlencode

logger = logging.getLogger(__name__)

DENIED_BODY = b"Access denied: this application requires an authorised user."


def _setting_list(name, default=()):
    """Return a setting as a tuple of non-empty strings."""
    value = getattr(settings, name, None)
    if value is None:
        value = default
    if isinstance(value, str):
        value = value.split(",")
    return tuple(item.strip() for item in value if item and item.strip())


def _app_prefixes(setting_name, default=()):
    """Return the set of first path segments covered by *setting_name*."""
    return set(_setting_list(setting_name, default))


def _first_segment(request):
    """Return the first path segment below the URL root prefix."""
    path = request.path_info or "/"
    root = getattr(settings, "URL_ROOT_PREFIX", "/") or "/"
    if root != "/" and path.startswith(root):
        path = path[len(root):]
    path = path.lstrip("/")
    if not path:
        return ""
    return path.split("/", 1)[0]


class AppAccessMiddleware:
    """Require a logged-in (or staff) user for whole applications."""

    def __init__(self, get_response):
        """Store the next callable in the middleware chain.

        Args:
            get_response: The next middleware or view.
        """
        self.get_response = get_response

    def __call__(self, request):
        """Enforce the per-application policy, then continue the chain.

        Args:
            request: The incoming HTTP request.

        Returns:
            The downstream response, or a redirect/denial response.

        Raises:
            PermissionDenied: When the user lacks the required permission.
        """
        app = _first_segment(request)
        if app:
            staff_only = _app_prefixes("STAFF_ONLY_APPS", ("schinstall", "schbuilder"))
            login_only = _app_prefixes("LOGIN_ONLY_APPS", ("schcommander",))
            user = getattr(request, "user", None)
            authenticated = bool(
                user is not None and getattr(user, "is_authenticated", False)
            )

            if app in staff_only:
                # Administrative applications stay closed even on a PUBLIC site.
                if not authenticated or not getattr(user, "is_staff", False):
                    return self._deny(request, authenticated)
            elif app in login_only and not getattr(settings, "PUBLIC", False):
                if not authenticated:
                    return self._deny(request, False)

        return self.get_response(request)

    def _deny(self, request, authenticated):
        """Return the denial response for an unauthorised request."""
        if not authenticated:
            login_url = getattr(settings, "LOGIN_URL", None)
            if login_url:
                query = urlencode({"next": request.get_full_path()})
                separator = "&" if "?" in login_url else "?"
                return HttpResponseRedirect(f"{login_url}{separator}{query}")
            return HttpResponse(DENIED_BODY, status=401)
        raise PermissionDenied
