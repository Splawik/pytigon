"""Tests for the default-administrator production guard (point 1.2).

The bootstrap account ``auto`` / ``anawa`` is a documented default, not a
secret: a local desktop installation must work without a login, and a package
brings data owned by this account. These tests lock in that the guard is a
no-op locally and behaves correctly on a production web server.
"""

import logging

import pytest
from django.test import RequestFactory, override_settings

from pytigon.schserw.schmiddleware.default_admin import DefaultAdminGuardMiddleware
from pytigon.schserw.schsys import checks, default_admin

PROD = {
    "PRODUCTION_VERSION": True,
    "DEBUG": False,
    "PLATFORM_TYPE": "webserver",
    "DEFAULT_ADMIN_USERNAME": "auto",
    "DEFAULT_ADMIN_PASSWORD": "anawa",
    "PYTIGON_STRICT_DEFAULT_ADMIN": False,
    "FORCE_PASSWORD_CHANGE_IN_PRODUCTION": True,
}


class FakeUser:
    """Minimal stand-in for an authenticated bootstrap administrator."""

    is_authenticated = True
    USERNAME_FIELD = "username"
    username = "auto"
    pk = 1

    def __init__(self, password="hash-default", default=True):
        self.password = password
        self._default = default

    def check_password(self, raw):
        return self._default and raw == "anawa"


@pytest.fixture(autouse=True)
def _reset_guard():
    default_admin.reset_startup_check()
    yield
    default_admin.reset_startup_check()


class TestIsProductionWebserver:
    def test_true_in_production(self):
        with override_settings(**PROD):
            assert default_admin.is_production_webserver() is True

    def test_false_in_debug(self):
        with override_settings(**{**PROD, "DEBUG": True}):
            assert default_admin.is_production_webserver() is False

    def test_false_for_embedded_desktop(self):
        with override_settings(**{**PROD, "PLATFORM_TYPE": "standard"}):
            assert default_admin.is_production_webserver() is False

    def test_false_outside_production_version(self):
        with override_settings(**{**PROD, "PRODUCTION_VERSION": False}):
            assert default_admin.is_production_webserver() is False


class TestUserHasDefaultPassword:
    def test_true_for_bootstrap_account(self):
        with override_settings(**PROD):
            assert default_admin.user_has_default_password(FakeUser()) is True

    def test_false_after_password_change(self):
        with override_settings(**PROD):
            user = FakeUser(password="changed", default=False)
            assert default_admin.user_has_default_password(user) is False

    def test_false_for_other_account(self):
        with override_settings(**{**PROD, "DEFAULT_ADMIN_USERNAME": "someone"}):
            assert default_admin.user_has_default_password(FakeUser()) is False

    def test_false_for_anonymous(self):
        with override_settings(**PROD):

            class Anon:
                is_authenticated = False

            assert default_admin.user_has_default_password(Anon()) is False

    def test_cache_is_invalidated_by_password_change(self):
        with override_settings(**PROD):
            user = FakeUser()
            assert default_admin.user_has_default_password(user) is True
            user.password = "changed-hash"
            user._default = False
            assert default_admin.user_has_default_password(user) is False


class TestStartupCheck:
    def test_warns_once_in_production(self, monkeypatch, caplog):
        calls = []
        monkeypatch.setattr(
            default_admin,
            "default_admin_is_active",
            lambda *a, **k: calls.append(1) or True,
        )
        with override_settings(**PROD):
            with caplog.at_level(logging.CRITICAL):
                assert default_admin.startup_check() == "warned"
                # The guard is one-shot: later calls are cheap no-ops.
                assert default_admin.startup_check() == "ok"
            assert len(calls) == 1
        assert any("SECURITY" in r.message for r in caplog.records)

    def test_ok_when_password_changed(self, monkeypatch):
        monkeypatch.setattr(
            default_admin, "default_admin_is_active", lambda *a, **k: False
        )
        with override_settings(**PROD):
            assert default_admin.startup_check() == "ok"

    def test_strict_raises_when_blocked(self, monkeypatch):
        from django.core.exceptions import ImproperlyConfigured

        monkeypatch.setattr(
            default_admin, "default_admin_is_active", lambda *a, **k: True
        )
        with override_settings(**{**PROD, "PYTIGON_STRICT_DEFAULT_ADMIN": True}):
            with pytest.raises(ImproperlyConfigured):
                default_admin.startup_check(raise_if_blocked=True)

    def test_strict_returns_blocked_for_middleware(self, monkeypatch):
        monkeypatch.setattr(
            default_admin, "default_admin_is_active", lambda *a, **k: True
        )
        with override_settings(**{**PROD, "PYTIGON_STRICT_DEFAULT_ADMIN": True}):
            assert default_admin.startup_check() == "blocked"

    def test_noop_for_desktop(self, monkeypatch):
        called = []
        monkeypatch.setattr(
            default_admin,
            "default_admin_is_active",
            lambda *a, **k: called.append(1) or True,
        )
        with override_settings(**{**PROD, "PLATFORM_TYPE": "standard"}):
            assert default_admin.startup_check() == "ok"
        assert called == []


class TestSystemCheck:
    def test_warning_when_active(self, monkeypatch):
        monkeypatch.setattr(
            default_admin, "default_admin_is_active", lambda *a, **k: True
        )
        with override_settings(**PROD):
            result = checks.default_admin_credentials(None)
        assert result and result[0].id == "pytigon.W001"

    def test_empty_when_changed(self, monkeypatch):
        monkeypatch.setattr(
            default_admin, "default_admin_is_active", lambda *a, **k: False
        )
        with override_settings(**PROD):
            assert checks.default_admin_credentials(None) == []

    def test_empty_for_desktop(self, monkeypatch):
        monkeypatch.setattr(
            default_admin, "default_admin_is_active", lambda *a, **k: True
        )
        with override_settings(**{**PROD, "PLATFORM_TYPE": "standard"}):
            assert checks.default_admin_credentials(None) == []


class TestMiddleware:
    @staticmethod
    def _middleware():
        return DefaultAdminGuardMiddleware(lambda request: "response")

    def test_redirects_bootstrap_admin(self, monkeypatch):
        monkeypatch.setattr(
            default_admin, "startup_check", lambda *a, **k: "ok"
        )
        monkeypatch.setattr(
            default_admin, "user_has_default_password", lambda user: True
        )
        request = RequestFactory().get("/some/page/")
        request.user = FakeUser()
        with override_settings(**PROD):
            response = self._middleware()(request)
        assert response.status_code == 302
        assert "password_change" in response["Location"]

    def test_exempt_change_password_page(self, monkeypatch):
        monkeypatch.setattr(
            default_admin, "startup_check", lambda *a, **k: "ok"
        )
        monkeypatch.setattr(
            default_admin, "user_has_default_password", lambda user: True
        )
        request = RequestFactory().get("/schsys/change_password/")
        request.user = FakeUser()
        with override_settings(**PROD):
            assert self._middleware()(request) == "response"

    def test_exempt_password_change_page(self, monkeypatch):
        monkeypatch.setattr(
            default_admin, "startup_check", lambda *a, **k: "ok"
        )
        monkeypatch.setattr(
            default_admin, "user_has_default_password", lambda user: True
        )
        request = RequestFactory().get("/schsys/password_change/")
        request.user = FakeUser()
        with override_settings(**PROD):
            assert self._middleware()(request) == "response"

    def test_noop_for_desktop(self, monkeypatch):
        monkeypatch.setattr(
            default_admin, "startup_check", lambda *a, **k: "ok"
        )
        monkeypatch.setattr(
            default_admin, "user_has_default_password", lambda user: True
        )
        request = RequestFactory().get("/some/page/")
        request.user = FakeUser()
        with override_settings(**{**PROD, "PLATFORM_TYPE": "standard"}):
            assert self._middleware()(request) == "response"

    def test_force_change_disabled(self, monkeypatch):
        monkeypatch.setattr(
            default_admin, "startup_check", lambda *a, **k: "ok"
        )
        monkeypatch.setattr(
            default_admin, "user_has_default_password", lambda user: True
        )
        request = RequestFactory().get("/some/page/")
        request.user = FakeUser()
        with override_settings(**{**PROD, "FORCE_PASSWORD_CHANGE_IN_PRODUCTION": False}):
            assert self._middleware()(request) == "response"

    def test_strict_blocks_with_503(self, monkeypatch):
        monkeypatch.setattr(
            default_admin, "default_admin_is_active", lambda *a, **k: True
        )
        request = RequestFactory().get("/")
        request.user = FakeUser()
        with override_settings(**{**PROD, "PYTIGON_STRICT_DEFAULT_ADMIN": True}):
            response = self._middleware()(request)
        assert response.status_code == 503
