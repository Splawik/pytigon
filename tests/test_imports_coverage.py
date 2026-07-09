"""Import-based coverage tests for various pytigon modules."""

import pytest


class TestImportsForCoverage:
    def test_import_schema(self):
        """Simple import to trigger module-level code in schema.py."""
        from pytigon.schserw.schsys.schema import Query, UserMutation

        assert Query is not None
        assert UserMutation is not None

    def test_import_catch(self):
        """Import catch node."""
        from pytigon.schserw.schsys.templatetags.catch import CatchNode, do_catch

        assert CatchNode is not None
        assert do_catch is not None

    def test_import_collapse(self):
        """Import collapse node."""
        from pytigon.schserw.schsys.templatetags.collapse import CollapseNode

        assert CollapseNode is not None

    def test_import_htmlwidget(self):
        """Import htmlwidget node."""
        from pytigon.schserw.schsys.templatetags.htmlwidget import HtmlWidgetNode

        assert HtmlWidgetNode is not None

    def test_import_schjwt(self):
        """Import schjwt middleware."""
        from pytigon.schserw.schmiddleware.schjwt import (
            JWTUserMiddleware,
            get_user,
        )

        assert JWTUserMiddleware is not None
        assert get_user is not None

    def test_import_schpost(self):
        """Import schpost middleware."""
        from pytigon.schserw.schmiddleware.schpost import ViewPost, ViewRequests

        assert ViewPost is not None
        assert ViewRequests is not None

    def test_import_csrf(self):
        """Import csrf middleware."""
        from pytigon.schserw.schmiddleware.csrf import DisableCSRF

        assert DisableCSRF is not None

    def test_import_vary(self):
        """Import vary middleware."""
        from pytigon.schserw.schmiddleware.vary import VaryMiddleware

        assert VaryMiddleware is not None

    def test_import_remotebackend(self):
        """Import remotebackend."""
        from pytigon.schserw.schsys.remotebackend import RemoteUserBackendMod

        assert RemoteUserBackendMod is not None

    def test_import_commands_handlers(self):
        """Import command handlers."""
        from pytigon.commands.handlers.manage import ManageCommandHandler
        from pytigon.commands.handlers.run import RunCommandHandler
        from pytigon.commands.handlers.runserver import RunServerCommandHandler
        from pytigon.commands.handlers.python import PythonCommandHandler
        from pytigon.commands.handlers.init import InitCommandHandler
        from pytigon.commands.handlers.tools import ToolCommandHandler
        from pytigon.commands.handlers.default import DefaultCommandHandler

        assert ManageCommandHandler is not None
        assert RunCommandHandler is not None
        assert RunServerCommandHandler is not None
        assert PythonCommandHandler is not None
        assert InitCommandHandler is not None
        assert ToolCommandHandler is not None
        assert DefaultCommandHandler is not None

    def test_import_app_manager(self):
        """Import all app_manager classes."""
        from pytigon.schserw.schsys.app_manager import (
            AppInfo,
            AppItemInfo,
            AppManager,
            has_user_perm,
        )

        assert AppInfo is not None
        assert AppItemInfo is not None
        assert AppManager is not None
        assert has_user_perm is not None

    def test_import_cache_message_storage(self):
        """Import cache message storage."""
        from pytigon.schserw.schsys.cache_message_storage import CacheStorage

        assert CacheStorage is not None

    def test_import_context_processors(self):
        """Import all context processor functions."""
        from pytigon.schserw.schsys.context_processors import (
            Env,
            RulesPermWrapper,
            RulesWrapper,
            browser_type,
            client_type,
            default_template,
            default_template2,
            get_fragment,
            sch_standard,
            standard_web_browser,
            test_mobile,
            test_tablet,
        )

        assert sch_standard is not None
        assert test_mobile is not None
        assert browser_type is not None

    def test_import_views(self):
        """Import views functions."""
        from pytigon.schserw.schsys.views import (
            change_password,
            change_profile_variant,
            datedialog,
            dstatic,
            favicon,
            get_messages,
            listdialog,
            ok,
            plugin_template,
            plugins,
            search,
            site_media_protected,
            start,
            sw,
            tabdialog,
            treedialog,
        )

        assert change_password is not None
        assert ok is not None
        assert start is not None

    def test_import_urls(self):
        """Import urls module."""
        from pytigon.schserw import urls as schserw_urls
        from pytigon.schserw.schsys import urls as schsys_urls

        assert schserw_urls.urlpatterns is not None
        assert schsys_urls.urlpatterns is not None

    def test_import_features_settings(self):
        """Import features settings."""
        import pytigon.schserw.settings.features as features_mod

        assert features_mod.INSTALLED_APPS is not None
        assert features_mod.MIDDLEWARE is not None

    def test_import_infra_settings(self):
        """Import infra settings."""
        import pytigon.schserw.settings.infra as infra_mod

        assert infra_mod.LOGGING is not None
        assert infra_mod.STORAGES is not None

    def test_import_base_settings(self):
        """Import base settings."""
        import pytigon.schserw.settings.base as base_mod

        assert base_mod.DEBUG is not None
        assert base_mod.DATABASES is not None
