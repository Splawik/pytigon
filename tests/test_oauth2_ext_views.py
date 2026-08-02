"""Tests for the custom OAuth2 token view (application-scoped scopes).

The test-suite settings do not register ``oauth2_provider`` in
``INSTALLED_APPS``, so we import the view against lightweight stubs of the
``oauth2_provider`` symbols it uses. This keeps the test hermetic without
enabling the full REST/OAuth stack for the whole suite.
"""

import json
import sys
import types
from unittest import mock

import pytest
from django.http import HttpRequest


@pytest.fixture
def token_view():
    # Build minimal stubs for the oauth2_provider symbols used by the view.
    fake_access_token = type("AccessToken", (), {})
    fake_access_token.DoesNotExist = type("DoesNotExist", (Exception,), {})

    models_mod = types.ModuleType("oauth2_provider.models")
    models_mod.get_access_token_model = lambda: fake_access_token

    signals_mod = types.ModuleType("oauth2_provider.signals")
    signals_mod.app_authorized = mock.Mock()

    base_mod = types.ModuleType("oauth2_provider.views.base")

    def _create_token_response(self, request, *args, **kwargs):
        raise NotImplementedError

    base_mod.TokenView = type(
        "TokenView",
        (),
        {"post": lambda self, *a, **k: None, "create_token_response": _create_token_response},
    )

    # Insert stubs so importing the real module does not reach the DB layer.
    sys.modules["oauth2_provider"] = types.ModuleType("oauth2_provider")
    sys.modules["oauth2_provider.models"] = models_mod
    sys.modules["oauth2_provider.signals"] = signals_mod
    sys.modules["oauth2_provider.views"] = types.ModuleType("oauth2_provider.views")
    sys.modules["oauth2_provider.views.base"] = base_mod

    from pytigon.schserw.oauth2_ext.views import ApplicationScopesTokenView

    return ApplicationScopesTokenView()


def _make_request():
    request = HttpRequest()
    request.method = "POST"
    request.POST = {}
    request.META = {}
    return request


class _FakeApplication:
    pass


class _FakeToken:
    def __init__(self, scope="read", has_custom_scope=False):
        self.scope = scope
        app = _FakeApplication()
        if has_custom_scope:
            app.pytigonoauth2application = type("Ext", (), {"scope": "custom:write"})()
        else:
            app.pytigonoauth2application = type("Ext", (), {"scope": ""})()
        self.application = app
        self.saved = False

    def save(self):
        self.saved = True


class TestApplicationScopesTokenView:
    def _fake_access_class(self, monkeypatch, token):
        from pytigon.schserw.oauth2_ext import views as v

        def get(*args, **kwargs):
            return token

        fake_token_class = type(
            "AccessToken",
            (),
            {
                "DoesNotExist": v.AccessToken.DoesNotExist,
                "objects": type("O", (), {"get": staticmethod(get)})(),
            },  # noqa: E501
        )
        monkeypatch.setattr(v, "AccessToken", fake_token_class)
        return fake_token_class

    def _run(
        self,
        token_view,
        monkeypatch,
        body,
        status=200,
        fake_token=None,
        access_token="tok123",
        headers=None,
    ):
        request = _make_request()
        monkeypatch.setattr(
            token_view,
            "create_token_response",
            lambda req, *a, **k: ("url", headers or {}, json.dumps(body), status),
        )
        if fake_token is not None:
            self._fake_access_class(monkeypatch, fake_token)
        return token_view.post(request)

    def test_success_without_custom_scope(self, token_view, monkeypatch):
        token = _FakeToken(scope="read", has_custom_scope=False)
        resp = self._run(
            token_view,
            monkeypatch,
            body={"access_token": "tok123", "scope": "read"},
            fake_token=token,
        )
        assert resp.status_code == 200
        assert json.loads(resp.content)["scope"] == "read"

    def test_success_with_custom_scope(self, token_view, monkeypatch):
        token = _FakeToken(scope="read", has_custom_scope=True)
        resp = self._run(
            token_view,
            monkeypatch,
            body={"access_token": "tok123", "scope": "read"},
            fake_token=token,
        )
        assert resp.status_code == 200
        data = json.loads(resp.content)
        assert data["scope"] == "custom:write"
        assert token.scope == "custom:write"

    def test_non_200_status_passthrough(self, token_view, monkeypatch):
        resp = self._run(
            token_view,
            monkeypatch,
            body={"error": "invalid_request"},
            status=400,
        )
        assert resp.status_code == 400
        assert json.loads(resp.content)["error"] == "invalid_request"

    def test_invalid_json_body_returns_400(self, token_view, monkeypatch):
        request = _make_request()

        def bad_body(req, *a, **k):
            return ("url", {}, "not-json{{{", 200)

        monkeypatch.setattr(token_view, "create_token_response", bad_body)
        resp = token_view.post(request)
        assert resp.status_code == 400

    def test_missing_access_token_returns_404(self, token_view, monkeypatch):
        from pytigon.schserw.oauth2_ext import views as v

        def get(*args, **kwargs):
            raise v.AccessToken.DoesNotExist()

        fake_token_class = type(
            "AccessToken",
            (),
            {
                "DoesNotExist": v.AccessToken.DoesNotExist,
                "objects": type("O", (), {"get": staticmethod(get)})(),
            },  # noqa: E501
        )
        monkeypatch.setattr(v, "AccessToken", fake_token_class)

        request = _make_request()
        monkeypatch.setattr(
            token_view,
            "create_token_response",
            lambda req, *a, **k: (
                "url",
                {},
                json.dumps({"access_token": "missing", "scope": "read"}),
                200,
            ),
        )
        resp = token_view.post(request)
        assert resp.status_code == 404

    def test_unexpected_error_returns_500(self, token_view, monkeypatch):
        request = _make_request()

        def boom(req, *a, **k):
            raise RuntimeError("unexpected")

        monkeypatch.setattr(token_view, "create_token_response", boom)
        resp = token_view.post(request)
        assert resp.status_code == 500

    def test_app_authorized_signal_sent(self, token_view, monkeypatch):
        from unittest import mock

        from pytigon.schserw.oauth2_ext import views as v

        sent = mock.Mock()
        monkeypatch.setattr(v, "app_authorized", sent)

        token = _FakeToken(scope="read", has_custom_scope=False)
        self._run(
            token_view,
            monkeypatch,
            body={"access_token": "tok123", "scope": "read"},
            fake_token=token,
        )
        assert sent.send.called
