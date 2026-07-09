"""Tests for pytigon.schserw.schsys.context_processors module."""

from unittest.mock import MagicMock

import pytest
from django.http import HttpRequest


class TestContextProcessors:
    """Tests for context processor functions."""

    @pytest.fixture
    def http_request(self):
        r = HttpRequest()
        r.META = {
            "HTTP_USER_AGENT": "Mozilla/5.0 (X11; Linux x86_64) Firefox/130.0",
            "HTTP_ACCEPT": "text/html",
        }
        r.GET = {}
        r.path = "/app/schsystab/form/edit/"
        r.LANGUAGE_CODE = "en"
        return r

    def test_test_mobile_desktop_browser(self, http_request):
        from pytigon.schserw.schsys.context_processors import test_mobile

        assert test_mobile(http_request) is False

    def test_test_mobile_android(self, http_request):
        from pytigon.schserw.schsys.context_processors import test_mobile

        http_request.META["HTTP_USER_AGENT"] = "Mozilla/5.0 Android Mobile"
        assert test_mobile(http_request) is True

    def test_test_mobile_iphone(self, http_request):
        from pytigon.schserw.schsys.context_processors import test_mobile

        http_request.META["HTTP_USER_AGENT"] = "Mozilla/5.0 iPhone Mobile"
        assert test_mobile(http_request) is True

    def test_test_mobile_no_user_agent(self, http_request):
        from pytigon.schserw.schsys.context_processors import test_mobile

        del http_request.META["HTTP_USER_AGENT"]
        del http_request.META["HTTP_ACCEPT"]
        assert test_mobile(http_request) is False

    def test_test_tablet_false(self, http_request):
        from pytigon.schserw.schsys.context_processors import test_tablet

        assert test_tablet(http_request) is False

    def test_test_tablet_true(self, http_request):
        from pytigon.schserw.schsys.context_processors import test_tablet

        http_request.META["HTTP_USER_AGENT"] = "Mozilla/5.0 XTablet"
        assert test_tablet(http_request) is True

    def test_standard_web_browser_normal(self, http_request):
        from pytigon.schserw.schsys.context_processors import standard_web_browser

        assert standard_web_browser(http_request) == 1

    def test_standard_web_browser_only_table(self, http_request):
        from pytigon.schserw.schsys.context_processors import standard_web_browser

        http_request.GET["only_table"] = "1"
        assert standard_web_browser(http_request) == 6

    def test_standard_web_browser_only_content(self, http_request):
        from pytigon.schserw.schsys.context_processors import standard_web_browser

        http_request.GET["only_content"] = "1"
        assert standard_web_browser(http_request) == 5

    def test_standard_web_browser_to_print(self, http_request):
        from pytigon.schserw.schsys.context_processors import standard_web_browser

        http_request.GET["to_print"] = "1"
        assert standard_web_browser(http_request) == 9

    def test_standard_web_browser_browser_type_param(self, http_request):
        from pytigon.schserw.schsys.context_processors import standard_web_browser

        http_request.GET["browser_type"] = "4"
        assert standard_web_browser(http_request) == 4

    def test_get_fragment_default(self, http_request):
        from pytigon.schserw.schsys.context_processors import get_fragment

        assert get_fragment(http_request) == "page"

    def test_get_fragment_from_query(self, http_request):
        from pytigon.schserw.schsys.context_processors import get_fragment

        http_request.GET["fragment"] = "custom"
        assert get_fragment(http_request) == "custom"

    def test_get_fragment_only_table(self, http_request):
        from pytigon.schserw.schsys.context_processors import get_fragment

        http_request.GET["only_table"] = "1"
        assert get_fragment(http_request) == "table-content"

    def test_client_type_desktop(self, http_request):
        from pytigon.schserw.schsys.context_processors import client_type

        assert client_type(http_request) == "desktop"

    def test_client_type_mobile(self, http_request):
        from pytigon.schserw.schsys.context_processors import client_type

        http_request.META["HTTP_USER_AGENT"] = "Android Mobile"
        assert client_type(http_request) == "smartfon"

    def test_client_type_tablet(self, http_request):
        from pytigon.schserw.schsys.context_processors import client_type

        http_request.META["HTTP_USER_AGENT"] = "Android XTablet"
        assert client_type(http_request) == "tablet"

    def test_browser_type_desktop(self, http_request):
        from pytigon.schserw.schsys.context_processors import browser_type

        assert browser_type(http_request) == "desktop_standard"

    def test_browser_type_mobile(self, http_request):
        from pytigon.schserw.schsys.context_processors import browser_type

        http_request.META["HTTP_USER_AGENT"] = "Android Mobile"
        assert browser_type(http_request) == "smartfon_standard"

    def test_browser_type_tablet(self, http_request):
        from pytigon.schserw.schsys.context_processors import browser_type

        http_request.META["HTTP_USER_AGENT"] = "Mozilla/5.0 android xtablet"
        assert browser_type(http_request) == "tablet_standard"

    def test_default_template(self):
        from pytigon.schserw.schsys.context_processors import default_template

        assert default_template("desktop") == "desktop.html"

    def test_default_template2(self):
        from pytigon.schserw.schsys.context_processors import default_template2

        assert default_template2("desktop") == "theme/desktop.html"

    def test_env_class(self):
        from pytigon.schserw.schsys.context_processors import Env

        def my_env(name):
            return f"value_of_{name}"

        e = Env(my_env)
        assert e["test"] == "value_of_test"

    def test_sch_standard_returns_dict(self, http_request):
        from pytigon.schserw.schsys.context_processors import sch_standard

        result = sch_standard(http_request)
        assert isinstance(result, dict)
        assert "standard_web_browser" in result
        assert "browser_type" in result
        assert "client_type" in result
        assert "prj_name" in result
        assert "prj_title" in result
        assert "uuid" in result
        assert "form_edit" in result
        assert "form_add" in result
        assert "form_delete" in result
        assert "form_list" in result
        assert "readonly" in result
        assert "ro" in result
        assert "form_info" in result
        assert "form_grid" in result
        assert "show_form" in result
        assert "URL_ROOT_FOLDER" in result
        assert "base_path" in result
        assert "URL_APP_BASE" in result
        assert "app_path" in result
        assert "default_template" in result
        assert "application_type" in result
        assert "gen_time" in result
        assert "lang" in result
        assert "settings" in result
        assert "app_manager" in result
        assert "env" in result
        assert "pyodide" in result
        assert "offline_support" in result

    def test_sch_standard_edit_path(self, http_request):
        from pytigon.schserw.schsys.context_processors import sch_standard

        http_request.path = "/app/schsystab/form/edit/"
        result = sch_standard(http_request)
        assert result["form_edit"] is True
        assert result["show_form"] is True

    def test_sch_standard_add_path(self, http_request):
        from pytigon.schserw.schsys.context_processors import sch_standard

        http_request.path = "/app/schsystab/form/add/"
        result = sch_standard(http_request)
        assert result["form_edit"] is True
        assert result["form_add"] is True
        assert result["show_form"] is True

    def test_sch_standard_delete_path(self, http_request):
        from pytigon.schserw.schsys.context_processors import sch_standard

        http_request.path = "/app/schsystab/form/delete/"
        result = sch_standard(http_request)
        assert result["form_delete"] is True
        assert result["show_form"] is True

    def test_sch_standard_readonly_path(self, http_request):
        from pytigon.schserw.schsys.context_processors import sch_standard

        http_request.path = "/app/schsystab/form/_list/"
        result = sch_standard(http_request)
        assert result["readonly"] is True
        assert result["ro"] == "_"

    def test_sch_standard_list_view(self, http_request):
        from pytigon.schserw.schsys.context_processors import sch_standard

        http_request.path = "/app/schsystab/form/list/"
        result = sch_standard(http_request)
        assert result["form_list"] is True

    def test_sch_standard_form_grid(self, http_request):
        from pytigon.schserw.schsys.context_processors import sch_standard

        http_request.path = "/app/schsystab/form/grid"
        result = sch_standard(http_request)
        assert result["form_grid"] is True

    def test_sch_standard_form_ext(self, http_request):
        from pytigon.schserw.schsys.context_processors import sch_standard

        http_request.path = "/app/schsystab/form/_ext/edit/"
        result = sch_standard(http_request)
        assert result["form_ext"] is True

    def test_sch_standard_form_info(self, http_request):
        from pytigon.schserw.schsys.context_processors import sch_standard

        http_request.path = "/app/schsystab/form/view/"
        result = sch_standard(http_request)
        assert result["form_info"] is True
        assert result["show_form"] is True

    def test_sch_standard_get_param(self, http_request):
        from pytigon.schserw.schsys.context_processors import sch_standard

        http_request.path = "/app/schsystab/form/get/"
        result = sch_standard(http_request)
        assert result["get"] == "get"

    def test_sch_standard_show_title_bar(self, http_request):
        from pytigon.schserw.schsys.context_processors import sch_standard

        http_request.path = "/app/schsystab/form/_set/"
        result = sch_standard(http_request)
        assert result["show_title_bar"] is True

    def test_sch_standard_gettree(self, http_request):
        from pytigon.schserw.schsys.context_processors import sch_standard

        http_request.path = "/app/schsystab/form/gettree/"
        result = sch_standard(http_request)
        assert result["get"] == "gettree"

    def test_sch_standard_extra_param(self, http_request):
        from pytigon.schserw.schsys.context_processors import sch_standard

        http_request.GET["extra_param"] = "test_value"
        result = sch_standard(http_request)
        assert result["extra_param"] == "test_value"

    def test_sch_standard_theme(self, http_request):
        from pytigon.schserw.schsys.context_processors import sch_standard

        result = sch_standard(http_request)
        assert "theme" in result
        assert "btn_size" in result

    def test_sch_standard_offline_support(self, http_request):
        from pytigon.schserw.schsys.context_processors import sch_standard

        result = sch_standard(http_request)
        assert "offline_support" in result

    def test_sch_standard_errors(self, http_request):
        from pytigon.schserw.schsys.context_processors import sch_standard

        result = sch_standard(http_request)
        assert result["errors"] is False

    def test_sch_standard_user_agent(self, http_request):
        from pytigon.schserw.schsys.context_processors import sch_standard

        result = sch_standard(http_request)
        assert result["user_agent"] == http_request.META["HTTP_USER_AGENT"]
