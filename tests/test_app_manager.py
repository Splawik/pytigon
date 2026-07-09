"""Tests for pytigon.schserw.schsys.app_manager module."""

from unittest.mock import MagicMock

import pytest
from django.http import HttpRequest


class TestHasUserPerm:
    def test_user_has_perm_direct(self):
        from pytigon.schserw.schsys.app_manager import has_user_perm

        user = MagicMock()
        user.has_perm.return_value = True
        assert has_user_perm(user, "app.perm") is True
        user.has_perm.assert_called_with("app.perm")


class TestAppManager:
    @pytest.fixture
    def http_request(self):
        r = HttpRequest()
        r.META = {
            "HTTP_USER_AGENT": "Mozilla/5.0",
            "HTTP_ACCEPT": "text/html",
        }
        r.GET = {}
        r.path = "/app/schsystab/form/list/"
        r.session = {}
        r.LANGUAGE_CODE = "en"
        r.user = MagicMock()
        r.user.has_perm.return_value = False
        import datetime

        r.user.date_joined = datetime.datetime(2024, 1, 1)
        return r

    def test_app_manager_creation(self, http_request):
        from pytigon.schserw.schsys.app_manager import AppManager

        mgr = AppManager(http_request)
        assert mgr is not None
        assert mgr.appname() is not None
        assert mgr.appid() is not None

    def test_login_providers(self, http_request):
        from pytigon.schserw.schsys.app_manager import AppManager

        mgr = AppManager(http_request)
        providers = mgr.login_providers()
        assert isinstance(providers, list)
