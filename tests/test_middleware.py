"""Tests for pytigon.schserw.schmiddleware modules."""

from unittest.mock import MagicMock, patch

import pytest
from django.http import HttpRequest, HttpResponse


class TestDisableCSRF:
    def test_disable_csrf_sets_flag(self):
        from pytigon.schserw.schmiddleware.csrf import DisableCSRF

        def get_response(req):
            return HttpResponse("OK")

        middleware = DisableCSRF(get_response)
        request = HttpRequest()
        response = middleware(request)
        assert response.status_code == 200
        assert hasattr(request, "_dont_enforce_csrf_checks")
        assert request._dont_enforce_csrf_checks is True


class TestJWTUserMiddleware:
    def test_jwt_middleware_initialization(self):
        from pytigon.schserw.schmiddleware.schjwt import JWTUserMiddleware

        def get_response(req):
            return HttpResponse("OK")

        middleware = JWTUserMiddleware(get_response)
        assert middleware.get_response is get_response

    def test_jwt_middleware_no_auth_header(self):
        from pytigon.schserw.schmiddleware.schjwt import JWTUserMiddleware
        from django.contrib.auth.models import AnonymousUser

        def get_response(req):
            return HttpResponse("OK")

        middleware = JWTUserMiddleware(get_response)
        request = HttpRequest()
        request.META = {}
        response = middleware(request)
        assert response.status_code == 200

    def test_jwt_get_user_new(self):
        from pytigon.schserw.schmiddleware.schjwt import get_user

        request = MagicMock()
        del request._cached_user

        mock_user = MagicMock()
        mock_user.is_anonymous = False

        with patch(
            "pytigon.schserw.schmiddleware.schjwt.get_user_model",
            return_value=MagicMock(
                objects=MagicMock(
                    filter=MagicMock(
                        return_value=MagicMock(
                            first=MagicMock(return_value=mock_user),
                        )
                    )
                )
            ),
        ):
            result = get_user(request, "testuser")
            assert result is mock_user
            assert request._cached_user is mock_user


class TestVaryMiddleware:
    def test_vary_middleware(self):
        from pytigon.schserw.schmiddleware.vary import VaryMiddleware

        def get_response(req):
            resp = HttpResponse("OK")
            return resp

        middleware = VaryMiddleware(get_response)
        request = HttpRequest()
        request.META = {
            "HTTP_USER_AGENT": "Test",
            "HTTP_ACCEPT": "text/html",
        }
        request.GET = {}
        response = middleware(request)
        assert response.status_code == 200


class TestSchPostMiddleware:
    def test_schpost_middleware(self):
        from pytigon.schserw.schmiddleware.schpost import ViewPost

        def get_response(req):
            return HttpResponse("OK")

        middleware = ViewPost(get_response)
        request = MagicMock()
        request.META = {
            "HTTP_USER_AGENT": "Test",
            "HTTP_ACCEPT": "text/html",
        }
        request.GET = {}
        request.path = "/test/"
        request.method = "GET"
        request.body = b""
        response = middleware(request)
        assert response is not None
