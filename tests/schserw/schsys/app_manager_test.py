import pytest
from django.http import HttpRequest, HttpResponse

from pytigon.schserw.schsys.app_manager import AppInfo, AppItemInfo, AppManager, has_user_perm


class TestAppInfo:
    def test_init_with_defaults(self):
        info = AppInfo()
        assert info.app_title == ""
        assert info.app_perms == ""

    def test_init_with_values(self):
        info = AppInfo(
            app_title="Test App",
            app_perms="test.perm",
            app_name="test_app",
            module_name="Test Module",
            module_title="Test Title",
            sys_module_name="test",
            user_param={"key": "value"},
        )
        assert info.app_title == "Test App"
        assert info.sys_module_name == "test"
        assert info.user_param == {"key": "value"}

    def test_str_representation(self):
        info = AppInfo(
            app_title="Test App",
            module_name="Test Module",
            module_title="Test Title",
            app_name="test_app",
            sys_module_name="test",
        )
        s = str(info)
        assert "sys_module_name: test" in s
        assert "module_name: Test Module" in s
        assert "app_name: test_app" in s


class TestAppItemInfo:
    def test_init_and_url(self):
        app_info = AppInfo(
            app_title="Test",
            app_perms="perm",
            index="idx",
            app_name="app",
            module_name="mod",
            module_title="Mod Title",
            sys_module_name="sys",
            user_param={},
        )
        item = AppItemInfo(app_info, url="/test/", description="desc", right="right", icon="icon")
        assert item.url == "/test/"
        assert item.description == "desc"
        assert item.right == "right"
        assert item.icon == "icon"

    def test_get_app_info_returns_appinfo(self):
        app_info = AppInfo(
            app_title="Test",
            app_perms="perm",
            app_name="app",
            module_name="mod",
            module_title="Mod Title",
            sys_module_name="sys",
        )
        item = AppItemInfo(app_info)
        result = item.get_app_info()
        assert isinstance(result, AppInfo)
        assert result.app_title == "Test"
        assert result.app_name == "app"

    def test_str_includes_description(self):
        app_info = AppInfo(app_title="T", sys_module_name="s")
        item = AppItemInfo(app_info, description="test desc")
        assert "test desc" in str(item)
