"""Tests for the per-application access middleware (plan point 1.4).

The file manager (``schcommander``) exposes the virtual filesystem — project and
data directories — through plain Django views in the generated projects, which
must not be edited. These tests cover the framework-level guard.
"""

import pytest
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.test import RequestFactory, override_settings

from pytigon.schserw.schmiddleware.app_access import AppAccessMiddleware


class _User:
    def __init__(self, authenticated, staff=False):
        self.is_authenticated = authenticated
        self.is_staff = staff and authenticated


@pytest.fixture
def rf():
    """A RequestFactory instance (pytest-django's ``rf`` is not available here)."""
    return RequestFactory()


def _middleware(response=None):
    def get_response(request):
        return response if response is not None else HttpResponse("downstream")

    return AppAccessMiddleware(get_response)


SETTINGS = {
    "URL_ROOT_PREFIX": "/",
    "STAFF_ONLY_APPS": ("schinstall", "schbuilder"),
    "LOGIN_ONLY_APPS": ("schcommander",),
    "PUBLIC": False,
    "LOGIN_URL": None,
}


def _get(rf, path, user):
    request = rf.get(path)
    request.user = user
    return _middleware()(request)


class TestFileManagerRequiresLogin:
    """schcommander exposes the VFS, so anonymous access must be refused."""

    @pytest.mark.parametrize(
        "path",
        [
            "/schcommander/grid//",
            "/schcommander/open/data/settings_app.py/",
            "/schcommander/open/app/pytigon/schserw/settings_app.py/",
            "/schcommander/save/data/install.ini/",
            "/schcommander/view/data/base.db/",
            "/schcommander/convert_html/app/readme.txt/",
        ],
    )
    def test_anonymous_is_refused(self, rf, path):
        with override_settings(**SETTINGS):
            response = _get(rf, path, _User(authenticated=False))
        assert response.status_code == 401

    def test_anonymous_redirects_to_login_when_configured(self, rf):
        settings = {**SETTINGS, "LOGIN_URL": "/schsys/change_password/"}
        with override_settings(**settings):
            response = _get(rf, "/schcommander/grid//", _User(authenticated=False))
        assert response.status_code == 302
        assert response["Location"].startswith("/schsys/change_password/?")

    def test_authenticated_user_passes(self, rf):
        with override_settings(**SETTINGS):
            response = _get(rf, "/schcommander/grid//", _User(authenticated=True))
        assert response.status_code == 200
        assert response.content == b"downstream"


class TestStaffOnlyApplications:
    @pytest.mark.parametrize("path", ["/schinstall/", "/schbuilder/grid/"])
    def test_anonymous_is_refused(self, rf, path):
        with override_settings(**SETTINGS):
            response = _get(rf, path, _User(authenticated=False))
        assert response.status_code == 401

    def test_authenticated_non_staff_is_forbidden(self, rf):
        with override_settings(**SETTINGS):
            with pytest.raises(PermissionDenied):
                _get(rf, "/schinstall/", _User(authenticated=True, staff=False))

    def test_staff_passes(self, rf):
        with override_settings(**SETTINGS):
            response = _get(rf, "/schinstall/", _User(authenticated=True, staff=True))
        assert response.status_code == 200

    def test_staff_only_ignored_on_public_site(self, rf):
        """Administrative applications stay closed even on a PUBLIC site."""
        with override_settings(**{**SETTINGS, "PUBLIC": True}):
            response = _get(rf, "/schinstall/", _User(authenticated=False))
        assert response.status_code == 401


class TestOrdinaryApplications:
    @pytest.mark.parametrize(
        "path",
        [
            "/schtools/",
            "/pytigon/",
            "/",
            "/schbrowser/",
            "/accounts/login/",
            "/static/pytigon/pytigon-lib.css",
        ],
    )
    def test_other_urls_are_untouched(self, rf, path):
        with override_settings(**SETTINGS):
            response = _get(rf, path, AnonymousUser())
        assert response.status_code == 200


class TestPublicSite:
    def test_public_site_relaxes_file_manager(self):
        """A PUBLIC site is an explicit operator choice, so the guard steps aside."""
        with override_settings(**{**SETTINGS, "PUBLIC": True}):
            response = _get(RequestFactory(), "/schcommander/grid//", AnonymousUser())
        assert response.status_code == 200


class TestUrlRootPrefix:
    def test_prefix_is_stripped_before_matching(self, rf):
        with override_settings(**{**SETTINGS, "URL_ROOT_PREFIX": "/app/"}):
            response = _get(rf, "/app/schcommander/grid//", _User(authenticated=False))
        assert response.status_code == 401

    def test_prefixed_request_to_other_app_passes(self, rf):
        with override_settings(**{**SETTINGS, "URL_ROOT_PREFIX": "/app/"}):
            response = _get(rf, "/app/schtools/", _User(authenticated=False))
        assert response.status_code == 200


class TestCustomLists:
    def test_operator_can_add_an_application(self, rf):
        settings = {**SETTINGS, "LOGIN_ONLY_APPS": ("schcommander", "mydocs")}
        with override_settings(**settings):
            response = _get(rf, "/mydocs/", _User(authenticated=False))
        assert response.status_code == 401

    def test_operator_can_relax_the_default(self, rf):
        with override_settings(**{**SETTINGS, "LOGIN_ONLY_APPS": ()}):
            response = _get(rf, "/schcommander/grid//", _User(authenticated=False))
        assert response.status_code == 200

    def test_comma_separated_string_is_accepted(self, rf):
        with override_settings(**{**SETTINGS, "LOGIN_ONLY_APPS": "alpha, beta"}):
            assert _get(rf, "/alpha/", _User(False)).status_code == 401
            assert _get(rf, "/beta/", _User(False)).status_code == 401
