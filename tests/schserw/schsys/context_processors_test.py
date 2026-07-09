# Tests for mobile/tablet detection and other standalone functions
# Note: these fixtures must not shadow pytest's built-in "request" fixture

import pytest
from django.http import HttpRequest

from pytigon.schserw.schsys.context_processors import (
    Env,
    browser_type,
    client_type,
    default_template,
    default_template2,
    get_fragment,
    standard_web_browser,
    test_mobile as _test_mobile,
    test_tablet as _test_tablet,
)


class TestMobileDetection:
    def test_no_user_agent_returns_false(self):
        request = HttpRequest()
        assert _test_mobile(request) is False

    def test_opera_mini_headers_returns_true(self):
        request = HttpRequest()
        request.META["HTTP_X_OPERAMINI_FEATURES"] = "something"
        assert _test_mobile(request) is True

    def test_mobile_user_agent_android(self):
        request = HttpRequest()
        request.META["HTTP_USER_AGENT"] = "Mozilla/5.0 Android"
        request.META["HTTP_ACCEPT"] = "text/html"
        assert _test_mobile(request) is True

    def test_desktop_user_agent_returns_false(self):
        request = HttpRequest()
        request.META["HTTP_USER_AGENT"] = "Mozilla/5.0 (Windows NT 10.0)"
        request.META["HTTP_ACCEPT"] = "text/html"
        assert _test_mobile(request) is False


class TestTabletDetection:
    def test_xtablet_user_agent(self):
        request = HttpRequest()
        request.META["HTTP_USER_AGENT"] = "Mozilla/5.0 xtablet"
        assert _test_tablet(request) is True

    def test_no_user_agent_returns_false(self):
        request = HttpRequest()
        assert _test_tablet(request) is False


class TestStandardWebBrowser:
    def test_no_user_agent_returns_0(self):
        request = HttpRequest()
        assert standard_web_browser(request) == 0

    def test_browser_type_from_get(self):
        request = HttpRequest()
        request.GET._mutable = True
        request.GET["browser_type"] = "2"
        assert standard_web_browser(request) == 2

    def test_python_client_returns_0(self):
        request = HttpRequest()
        request.META["HTTP_USER_AGENT"] = "py client"
        assert standard_web_browser(request) == 0

    def test_python_client_webkit_returns_3(self):
        request = HttpRequest()
        request.META["HTTP_USER_AGENT"] = "py client with WebKit"
        assert standard_web_browser(request) == 3

    def test_standard_browser_returns_1(self):
        request = HttpRequest()
        request.META["HTTP_USER_AGENT"] = "Mozilla/5.0"
        assert standard_web_browser(request) == 1


class TestGetFragment:
    def test_default_fragment(self):
        request = HttpRequest()
        assert get_fragment(request) == "page"

    def test_fragment_from_get(self):
        request = HttpRequest()
        request.GET._mutable = True
        request.GET["fragment"] = "custom"
        assert get_fragment(request) == "custom"

    def test_only_table_fragment(self):
        request = HttpRequest()
        request.GET._mutable = True
        request.GET["only_table"] = "1"
        assert get_fragment(request) == "table-content"


class TestClientType:
    def test_python_client_returns_schweb(self):
        request = HttpRequest()
        assert client_type(request) == "schweb"


class TestDefaultTemplate:
    def test_default_template(self):
        assert default_template("test") == "test.html"

    def test_default_template2(self):
        assert default_template2("desktop") == "theme/desktop.html"


class TestEnv:
    def test_getitem(self):
        env = Env(lambda name: f"value_for_{name}")
        assert env["TEST_KEY"] == "value_for_TEST_KEY"
