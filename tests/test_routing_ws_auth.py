"""Tests for the WebSocket authorisation guard in schserw/routing.py.

The consumers themselves live in the generated application projects, which are
export artefacts and must not be edited, so the guard is applied by the
framework while the routes are built. These tests exercise that guard.
"""

import asyncio

import pytest
from django.test import override_settings

from pytigon.schserw.routing import (
    _WS_FORBIDDEN,
    _WS_UNAUTHENTICATED,
    _websocket_is_staff_only,
    guard_websocket,
)

NORMAL_PATH = "schtools/anywidget/channel/"
STAFF_PATH = "schcommander/shell/channel/"


class _User:
    def __init__(self, authenticated, staff=False):
        self.is_authenticated = authenticated
        self.is_staff = staff and authenticated


def _consumer(calls):
    async def inner(scope, receive, send):
        calls.append(scope["path"])
        await send({"type": "websocket.accept"})

    return inner


def _connect(app, user, path=NORMAL_PATH):
    """Drive the ASGI application for one connection and return sent messages."""
    sent = []

    async def receive():
        return {"type": "websocket.connect"}

    async def send(message):
        sent.append(message)

    asyncio.run(app({"type": "websocket", "path": path, "user": user}, receive, send))
    return sent


PROTECTED = {
    "WEBSOCKET_REQUIRE_AUTH": True,
    "PUBLIC": False,
    "WEBSOCKET_STAFF_ONLY": ("schcommander/", "schbuilder/", "schtasks/", "schai/"),
    "WEBSOCKET_PUBLIC_PATHS": (),
}


class TestStaffOnlyDetection:
    def test_dangerous_paths_are_staff_only(self):
        with override_settings(**PROTECTED):
            assert _websocket_is_staff_only(STAFF_PATH) is True
            assert _websocket_is_staff_only("schbuilder/django/manage/channel/") is True

    def test_ordinary_paths_are_not_staff_only(self):
        with override_settings(**PROTECTED):
            assert _websocket_is_staff_only(NORMAL_PATH) is False


class TestGuardRequiresAuthentication:
    def test_anonymous_is_rejected(self):
        calls = []
        with override_settings(**PROTECTED):
            app = guard_websocket(NORMAL_PATH, _consumer(calls))
            sent = _connect(app, _User(authenticated=False))
        assert calls == []
        assert sent == [{"type": "websocket.close", "code": _WS_UNAUTHENTICATED}]

    def test_missing_user_is_rejected(self):
        calls = []
        with override_settings(**PROTECTED):
            app = guard_websocket(NORMAL_PATH, _consumer(calls))
            sent = _connect(app, None)
        assert calls == []
        assert sent[0]["code"] == _WS_UNAUTHENTICATED

    def test_authenticated_user_passes(self):
        calls = []
        with override_settings(**PROTECTED):
            app = guard_websocket(NORMAL_PATH, _consumer(calls))
            sent = _connect(app, _User(authenticated=True))
        assert calls == [NORMAL_PATH]
        assert sent == [{"type": "websocket.accept"}]


class TestGuardRequiresStaff:
    def test_anonymous_is_rejected(self):
        calls = []
        with override_settings(**PROTECTED):
            app = guard_websocket(STAFF_PATH, _consumer(calls))
            sent = _connect(app, _User(authenticated=False), path=STAFF_PATH)
        assert calls == []
        assert sent[0]["code"] == _WS_UNAUTHENTICATED

    def test_non_staff_user_is_forbidden(self):
        calls = []
        with override_settings(**PROTECTED):
            app = guard_websocket(STAFF_PATH, _consumer(calls))
            sent = _connect(app, _User(authenticated=True, staff=False), path=STAFF_PATH)
        assert calls == []
        assert sent == [{"type": "websocket.close", "code": _WS_FORBIDDEN}]

    def test_staff_user_passes(self):
        calls = []
        with override_settings(**PROTECTED):
            app = guard_websocket(STAFF_PATH, _consumer(calls))
            sent = _connect(app, _User(authenticated=True, staff=True), path=STAFF_PATH)
        assert calls == [STAFF_PATH]
        assert sent == [{"type": "websocket.accept"}]


class TestPublicMode:
    def test_public_site_allows_anonymous_on_ordinary_paths(self):
        calls = []
        with override_settings(**{**PROTECTED, "PUBLIC": True}):
            app = guard_websocket(NORMAL_PATH, _consumer(calls))
            sent = _connect(app, _User(authenticated=False))
        assert calls == [NORMAL_PATH]
        assert sent == [{"type": "websocket.accept"}]

    def test_public_site_still_protects_staff_only_paths(self):
        """A PUBLIC site must not expose the interactive shell."""
        calls = []
        with override_settings(**{**PROTECTED, "PUBLIC": True}):
            app = guard_websocket(STAFF_PATH, _consumer(calls))
            sent = _connect(app, _User(authenticated=False), path=STAFF_PATH)
        assert calls == []
        assert sent[0]["code"] == _WS_UNAUTHENTICATED

    def test_explicit_public_path_stays_anonymous(self):
        calls = []
        settings = {**PROTECTED, "WEBSOCKET_PUBLIC_PATHS": ("schtools/publicfeed/",)}
        with override_settings(**settings):
            app = guard_websocket("schtools/publicfeed/channel/", _consumer(calls))
            sent = _connect(
                app, _User(authenticated=False), path="schtools/publicfeed/channel/"
            )
        assert calls == ["schtools/publicfeed/channel/"]
        assert sent == [{"type": "websocket.accept"}]

    def test_authentication_can_be_disabled(self):
        calls = []
        with override_settings(**{**PROTECTED, "WEBSOCKET_REQUIRE_AUTH": False}):
            app = guard_websocket(NORMAL_PATH, _consumer(calls))
            sent = _connect(app, _User(authenticated=False))
        assert calls == [NORMAL_PATH]
        assert sent == [{"type": "websocket.accept"}]


class TestCloseCodes:
    def test_codes_are_in_the_private_range(self):
        assert 4000 <= _WS_UNAUTHENTICATED <= 4999
        assert 4000 <= _WS_FORBIDDEN <= 4999


class TestRouteBuilding:
    def test_built_routes_are_wrapped(self, monkeypatch):
        """Routes built from CHANNELS_URL_TAB must carry the guard."""
        from pytigon.schserw import routing

        class Consumer:
            @classmethod
            def as_asgi(cls):
                async def inner(scope, receive, send):  # pragma: no cover
                    await send({"type": "websocket.accept"})

                return inner

        module = type(routing)("fake_consumers_module")
        module.Consumer = Consumer
        monkeypatch.setattr(
            routing.importlib, "import_module", lambda name: module, raising=False
        )
        monkeypatch.setattr(
            routing.settings,
            "CHANNELS_URL_TAB",
            [(STAFF_PATH, "fake_consumers_module.Consumer")],
            raising=False,
        )

        routes = routing._build_websocket_routes()
        assert len(routes) == 1

        calls = []
        route_app = routes[0].callback
        # The guard rejects before delegating, so the consumer is never reached.
        sent = _connect(route_app, _User(authenticated=False), path=STAFF_PATH)
        assert sent[0]["code"] == _WS_UNAUTHENTICATED
        assert calls == []
