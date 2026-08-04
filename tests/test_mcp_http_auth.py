"""Regression tests for MCP streamable HTTP authorisation gate.

Covers the auth-gated wrapper in ``pytigon.schserw.mcp.http``. The critical
regression is the non-tuple authenticator result path, which previously used a
misspelled local (``is_authenticate``), leaving ``is_authenticated`` unbound and
raising ``UnboundLocalError`` for a valid, authenticated user.
"""

import asyncio

import pytest
from django.http import HttpRequest
from django.http import QueryDict


def _make_user(is_authenticated=True):
    class _User:
        def __init__(self, value):
            self.is_authenticated = value

    return _User(is_authenticated)


@pytest.fixture
def http_module():
    from pytigon.schserw.mcp import http

    return http


async def _run(coro):
    return await coro


async def _collect_messages(app, scope):
    messages = []

    async def send(message):
        messages.append(message)

    async def receive():
        return {}

    await app(scope, receive, send)
    return messages


@pytest.mark.django_db
def test_single_user_authenticated_calls_through(http_module, monkeypatch):
    """A non-tuple authenticator result is not a documented DRF shape, but the
    wrapper must handle it safely: a truthy user with ``is_authenticated=True``
    must pass the gate and reach the MCP handler with ``scope["user"]`` set."""

    captured = {}

    async def fake_authenticate(scope):
        return _make_user(True)

    async def fake_mcp(scope, receive, send):
        captured["user"] = scope.get("user")

    monkeypatch.setattr(http_module, "_authenticate", fake_authenticate)
    monkeypatch.setattr(http_module, "mcp_streamable_http", fake_mcp)

    scope = {"type": "http", "path": "/mcp", "headers": []}
    asyncio.run(_collect_messages(http_module.mcp_streamable_http_protected, scope))

    assert captured["user"] is not None
    assert captured["user"].is_authenticated is True


@pytest.mark.django_db
def test_non_authenticated_user_is_denied(http_module, monkeypatch):
    """A user whose ``is_authenticated`` is False must be rejected with 401."""

    async def fake_authenticate(scope):
        return _make_user(False)

    async def fake_unauthorized(send, message="Unauthorized"):
        await send(
            {"type": "http.response.start", "status": 401, "headers": []}
        )
        await send({"type": "http.response.body", "body": b""})

    monkeypatch.setattr(http_module, "_authenticate", fake_authenticate)
    monkeypatch.setattr(http_module, "_unauthorized", fake_unauthorized)

    scope = {"type": "http", "path": "/mcp", "headers": []}
    messages = asyncio.run(
        _collect_messages(http_module.mcp_streamable_http_protected, scope)
    )

    start = messages[0]
    assert start["status"] == 401


@pytest.mark.django_db
def test_none_user_is_denied(http_module, monkeypatch):
    """An unauthenticated (``None``) result must be rejected with 401."""

    async def fake_authenticate(scope):
        return None

    async def fake_unauthorized(send, message="Unauthorized"):
        await send(
            {"type": "http.response.start", "status": 401, "headers": []}
        )
        await send({"type": "http.response.body", "body": b""})

    monkeypatch.setattr(http_module, "_authenticate", fake_authenticate)
    monkeypatch.setattr(http_module, "_unauthorized", fake_unauthorized)

    scope = {"type": "http", "path": "/mcp", "headers": []}
    messages = asyncio.run(
        _collect_messages(http_module.mcp_streamable_http_protected, scope)
    )

    start = messages[0]
    assert start["status"] == 401


@pytest.mark.django_db
def test_tuple_result_authentication(http_module, monkeypatch):
    """The typical DRF authenticator tuple result ``(user, auth)`` must pass
    the gate for an authenticated user."""

    captured = {}

    async def fake_authenticate(scope):
        return (_make_user(True), object())

    async def fake_mcp(scope, receive, send):
        captured["user"] = scope.get("user")

    monkeypatch.setattr(http_module, "_authenticate", fake_authenticate)
    monkeypatch.setattr(http_module, "mcp_streamable_http", fake_mcp)

    scope = {"type": "http", "path": "/mcp", "headers": []}
    asyncio.run(_collect_messages(http_module.mcp_streamable_http_protected, scope))

    assert captured["user"] is not None


@pytest.mark.django_db
def test_client_credentials_tuple_with_none_user_passes(http_module, monkeypatch):
    """A valid OAuth2 ``client_credentials`` token authenticates with no user:
    the DRF authenticator returns ``(None, token)``. This must be allowed,
    not rejected with 401 (regression for production client_credentials)."""

    captured = {}

    async def fake_authenticate(scope):
        return (None, object())

    async def fake_mcp(scope, receive, send):
        captured["called"] = True
        captured["user"] = scope.get("user")

    monkeypatch.setattr(http_module, "_authenticate", fake_authenticate)
    monkeypatch.setattr(http_module, "mcp_streamable_http", fake_mcp)

    scope = {"type": "http", "path": "/mcp", "headers": []}
    messages = asyncio.run(
        _collect_messages(http_module.mcp_streamable_http_protected, scope)
    )

    assert captured["called"] is True
    assert captured["user"] is None
    assert all(m.get("type") != "http.response.start" for m in messages)


@pytest.mark.django_db
def test_auth_request_is_full_httprequest(http_module):
    """The auth shim must be a real ``django.http.HttpRequest`` so that newer
    django-oauth-toolkit versions (>= 3.4) can call ``request.GET`` and
    ``request.build_absolute_uri()`` inside ``OAuthLibCore.verify_request``
    without raising (regression: prod returned 401 because the old shim raised
    ``AttributeError`` that was silently swallowed)."""

    scope = {
        "type": "http",
        "method": "GET",
        "path": "/mcp",
        "query_string": b"",
        "scheme": "https",
        "server": (b"pytigon.cloud", 443),
        "headers": [
            (b"authorization", b"Bearer tok123"),
            (b"host", b"pytigon.cloud"),
        ],
    }
    req = http_module._AuthRequest(scope)

    assert isinstance(req, HttpRequest)
    assert isinstance(req.GET, QueryDict)
    assert req.GET.get("access_token") is None  # no access_token in query string
    assert req.build_absolute_uri("/mcp") == "https://pytigon.cloud/mcp"
    assert req.META.get("HTTP_HOST") == "pytigon.cloud"
    assert req.META.get("wsgi.url_scheme") == "https"
    assert req.META.get("HTTP_AUTHORIZATION") == "Bearer tok123"

    no_host = http_module._AuthRequest({**scope, "headers": [(b"authorization", b"Bearer t")]})
    # must not crash even without an explicit host header
    assert no_host.build_absolute_uri("/mcp").startswith("https://")


