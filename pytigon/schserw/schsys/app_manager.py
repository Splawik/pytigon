import functools
import importlib
import logging
import sys
import traceback

from django.conf import settings
from django.urls import get_script_prefix

try:
    from django.contrib.auth.models import Permission
except Exception:
    Permission = None

from pytigon_lib.schdjangoext.django_init import get_app_name

_logger = logging.getLogger(__name__)

try:
    if settings.ALLAUTH:
        from allauth.socialaccount.adapter import get_adapter
        from allauth.socialaccount.providers import registry
    else:
        registry = None
except (AttributeError, ImportError):
    registry = None


def has_user_perm(user, perm):
    if "|" in perm:
        arg, fun_path = perm.split("|", 1)
        module_path, fun_name = fun_path.rsplit(".", 1)
        module = importlib.import_module(module_path)
        fun = getattr(module, fun_name)
        return fun(user, arg)

    else:
        return user.has_perm(perm)


class AppInfo:
    """Class to hold application information."""

    def __init__(
        self,
        app_title="",
        app_perms="",
        index="",
        app_name="",
        module_name="",
        module_title="",
        sys_module_name="",
        user_param="",
    ):
        self.app_title = app_title
        self.app_perms = app_perms
        self.index = index
        self.app_name = app_name
        self.module_name = module_name
        self.module_title = module_title
        self.sys_module_name = sys_module_name
        self.user_param = user_param

    def __str__(self):
        return (
            f"sys_module_name: {self.sys_module_name}\n"
            f"module_name: {self.module_name}\n"
            f"module_title: {self.module_title}\n"
            f"app_name: {self.app_name}\n"
            f"app_title: {self.app_title}\n"
        )


class AppItemInfo(AppInfo):
    """Class to hold application item information."""

    def __init__(self, app_info, url="", description="", right="", icon=""):
        super().__init__(
            app_info.app_title,
            app_info.app_perms,
            app_info.index,
            app_info.app_name,
            app_info.module_name,
            app_info.module_title,
            app_info.sys_module_name,
            app_info.user_param,
        )
        self.url = url
        self.description = description
        self.right = right
        self.icon = icon

    def get_app_info(self):
        """Get the AppInfo object."""
        return AppInfo(
            self.app_title,
            self.app_perms,
            self.index,
            self.app_name,
            self.module_name,
            self.module_title,
            self.sys_module_name,
            self.user_param,
        )

    def __str__(self):
        return super().__str__() + "\n" + f"description: {self.description}\n"


@functools.lru_cache(maxsize=128)
def _get_apps_cached(prj, host):
    """Module-level cached app list builder.

    Cached on ``(prj, host)`` so it is shared across requests and does not
    hold references to request/user objects.
    """
    ret = []

    if prj:
        _temp = importlib.import_module(prj + ".apps")
        apps = _temp.APPS
    else:
        apps = None

    for _app in settings.INSTALLED_APPS:
        if apps:
            test = False
            name = _app if isinstance(_app, str) else _app.name
            if name.startswith(prj):
                test = True
            else:
                for app in apps:
                    if name in app:
                        test = True
                        break
            if not test:
                continue

        app = get_app_name(_app)
        if host == "127.0.0.2" and app == "schserw.schsys":
            continue
        try:
            module_title = None
            module_name = None
            title = None
            perms = None
            url = None
            elementy = app.split(".")
            appname = elementy[-1]
            module = importlib.import_module(elementy[0])
            module2 = getattr(module, elementy[-1]) if len(elementy) > 1 else module
            if module2:
                module_title = module2.ModuleTitle
                try:
                    module_name = module2.ModuleName
                except Exception:
                    module_name = module_title
                title = module2.Title
                perms = module2.Perms
                index = module2.Index
                user_param = module2.UserParam if hasattr(module2, "UserParam") else {}

                app_info = AppInfo()
                app_info.app_title = title
                app_info.app_perms = perms
                app_info.index = index
                app_info.app_name = appname
                app_info.module_name = module_name
                app_info.module_title = module_title
                app_info.sys_module_name = elementy[0]
                app_info.user_param = user_param
                ret.append(app_info)
        except Exception:
            _logger.debug("Error loading app info for %s", _app, exc_info=True)
    return ret


class AppManager:
    """Class to manage applications."""

    def __init__(self, request):
        self.request = request

    def appname(self):
        """Get the application name from the request path."""
        path = self.request.path
        elementy = path.split("/")
        base_url = get_script_prefix()
        nr = base_url.count("/")
        return elementy[nr]

    def appid(self):
        """Get the application ID from the request path."""
        path = self.request.path
        elementy = path.split("/")
        base_url = get_script_prefix()
        nr = base_url.count("/")
        if elementy[nr] == "schwiki":
            return elementy[nr + 1]
        else:
            return elementy[nr]

    def get_main_title(self):
        """Get the main title of the application."""
        apps = self._get_apps()
        for app in apps:
            if app[4] == "main":
                return app[0]
        return ""

    def _get_apps(self, prj=None):
        return _get_apps_cached(prj, self.request.get_host())

    def get_apps(self, prj=None):
        ret = []
        items = self.get_app_items(prj)
        for item in items:
            append = True
            for pos in ret:
                if pos.app_name == item.app_name:
                    append = False
                    break
            if append:
                ret.append(item.get_app_info())
        return ret

    def get_menu_id(self):
        i = 0
        apps = self.get_apps_width_perm()
        for app in apps:
            if app.app_name == self.appid():
                return i
            i += 1
        return 0

    def get_app_items(self, prj=None):
        if prj is None:
            prj = settings.PRJ_NAME
        apps = self._get_apps(prj)
        ret = []
        for app in apps:
            if app.app_name is not None and app.app_name != "":
                module = importlib.import_module(app.sys_module_name)
                if app.sys_module_name != app.app_name:
                    module2 = getattr(module, app.app_name)
                else:
                    module2 = module
                if module2:
                    for pos in module2.Urls:
                        app_info = AppItemInfo(app)
                        app_info.url = app.app_name + "/" + pos[0]
                        app_info.description = pos[1]
                        app_info.right = pos[2]
                        app_info.icon = pos[3]
                        ret.append(app_info)

                    if hasattr(module2, "AdditionalUrls"):
                        if callable(module2.AdditionalUrls):
                            urls2 = module2.AdditionalUrls(
                                prj,
                                self.request.LANGUAGE_CODE[:2].lower()
                                if hasattr(self.request, "LANGUAGE_CODE")
                                else "en",
                            )
                        else:
                            urls2 = module2.AdditionalUrls
                        for pos in urls2:
                            app_info = AppItemInfo(app)
                            app_info.sys_module_name = (
                                pos[4] if pos[4] else app.sys_module_name
                            )
                            app_info.module_title = (
                                pos[5] if pos[5] else app.module_title
                            )
                            app_info.app_name = pos[6] if pos[6] else app.app_name
                            app_info.app_title = pos[7] if pos[7] else app.app_title
                            app_info.url = pos[0]
                            app_info.description = pos[1]
                            app_info.right = pos[2]
                            app_info.icon = pos[3]
                            app_info.app_perms = None
                            app_info.user_param = None
                            if app_info.module_name == "config":
                                app_info.module_name = app_info.sys_module_name

                            id = -1
                            test = 0
                            i = 0
                            for pos in ret:
                                if pos.module_name == app_info.module_name:
                                    if test == 0:
                                        id = i
                                    if pos.app_name == app_info.app_name:
                                        test = 1
                                        id = i
                                i += 1
                            if id >= 0:
                                ret.insert(id + 1, app_info)
                            else:
                                ret.append(app_info)
        return ret

    def get_apps_width_perm(self, prj=None):
        if prj is None:
            prj = settings.PRJ_NAME
        ret = []
        items = self.get_app_items(prj)
        no_empty_apps = set()
        for item in items:
            no_empty_apps.add(item.app_name)
        for item in self.get_apps(prj):
            if item.app_name in settings.HIDE_APPS:
                continue
            if item.app_name in no_empty_apps:
                if item.app_perms:
                    if self.request.user.has_module_perms(item.app_name):
                        ret.append(item)
                else:
                    ret.append(item)
        return ret

    def get_app_items_width_perm(self, prj=None):
        if prj is None:
            prj = settings.PRJ_NAME
        ret = []
        for item in self.get_app_items(prj):
            if item.app_name in settings.HIDE_APPS:
                continue
            if not item.app_perms or self.request.user.has_module_perms(item.app_name):
                if item.right:
                    if has_user_perm(self.request.user, item.right):
                        ret.append(item)
                else:
                    ret.append(item)
            else:
                if (
                    len(
                        Permission.objects.filter(content_type__app_label=item.app_name)
                    )
                    == 0
                ):
                    if item.right:
                        if has_user_perm(self.request.user, item.right):
                            ret.append(item)
                    else:
                        ret.append(item)
        return ret

    def get_main_tools_app_items_width_perm(self, prj=None):
        if prj is None:
            prj = settings.PRJ_NAME
        ret = self.get_app_items_width_perm(prj)
        if settings.THREE_LEVEL_MENU:
            return [item for item in ret if item.module_name == "main tools"]
        else:
            return [item for item in ret if item.module_name != "config"]

    def get_not_main_tools_app_items_width_perm(self, prj=None):
        if prj is None:
            prj = settings.PRJ_NAME
        ret = self.get_app_items_width_perm(prj)
        if settings.THREE_LEVEL_MENU:
            return [item for item in ret if item.module_name != "main tools"]
        else:
            return [item for item in ret if item.module_name == "config"]

    def login_providers(self):
        ret = []

        if registry:
            for key, value in registry.provider_map.items():
                adapter = get_adapter()
                try:
                    adapter.get_provider(None, key)
                    ret.append((key, value.name, value))
                except Exception:
                    _logger.debug("Failed to get provider %s", key, exc_info=True)
        return ret
