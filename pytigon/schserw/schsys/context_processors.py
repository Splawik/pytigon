#!/usr/bin/python
# -*- coding: utf-8 -*-
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation; either version 3, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.

# Pytigon - wxpython and django application framework

# author: "Slawomir Cholaj (slawomir.cholaj@gmail.com)"
# copyright: "Copyright (C) ????/2012 Slawomir Cholaj"
# license: "LGPL 3.0"
# version: "0.1a"


"""Module contains standard context processors

"""


import uuid
import time
from urllib.parse import urlparse

import traceback
import sys


from django.conf import settings
from django.urls import get_script_prefix

try:
    from django.contrib.auth.models import Permission
    from django.contrib.auth.context_processors import PermWrapper
except:
    pass

from pytigon_lib.schdjangoext.django_init import get_app_name
from pytigon_lib.schtools.env import get_environ

if settings.ALLAUTH:
    from allauth.socialaccount.providers import registry
    from allauth.socialaccount.adapter import get_adapter
else:
    registry = None

# browser_type: 0 - python client 1 - web client 2 - hybrid - web client in
# python client 3 - python client -> web client


mobiles = (
    """sony,symbian,nokia,samsung,mobile,windows ce,epoc,opera mini,nitro,j2me,midp-,cldc-,netfront,mot,up.browser,
up.link,audiovox,blackberry,ericsson,panasonic,philips,sanyo,sharp,sie-,portalmmm,blazer,avantgo,danger,palm,series60,
palmsource,pocketpc,smartphone,rover,ipaq,au-mic,alcatel,ericy,up.link,docomo,vodafone/,wap1.,wap2.,plucker,480x640,sec,
fennec,android,google wireless transcoder,nintendo,webtv,playstation""".replace(
        "\n", ""
    )
    .replace("\r", "")
    .split(",")
)


def test_mobile(request):
    if "HTTP_X_OPERAMINI_FEATURES" in request.META:
        return True
    if "HTTP_ACCEPT" in request.META and request.META["HTTP_USER_AGENT"]:
        s = request.META["HTTP_ACCEPT"].lower()
        if "application/vnd.wap.xhtml+xml" in s:
            return True
    if "HTTP_USER_AGENT" in request.META and request.META["HTTP_USER_AGENT"]:
        s = request.META["HTTP_USER_AGENT"].lower()
        for ua in mobiles:
            if ua in s:
                return True
    return False


def test_tablet(request):
    if "HTTP_USER_AGENT" in request.META and request.META["HTTP_USER_AGENT"]:
        s = request.META["HTTP_USER_AGENT"].lower()
        if "xtablet" in s:
            return True
    return False


def standard_web_browser(request):
    if "browser_type" in request.GET:
        return int(request.GET["browser_type"])
    if not "HTTP_USER_AGENT" in request.META:
        return 0
    if (
        request
        and "HTTP_USER_AGENT" in request.META
        and request.META["HTTP_USER_AGENT"]
        and request.META["HTTP_USER_AGENT"].lower().startswith("py")
    ):
        if "WebKit" in request.META["HTTP_USER_AGENT"]:
            return 3
        else:
            return 0
    else:
        if "HYBRID_BROWSER" in request.session or "hybrid" in request.GET:
            return 2
        elif "only_table" in request.GET:
            return 6
        elif "only_content" in request.GET:
            return 5
        elif "to_print" in request.GET:
            return 9
        else:
            return 1


def get_fragment(request):
    fragment = "page"
    if "fragment" in request.GET:
        fragment = request.GET.get("fragment")
    else:
        if "only_content" in request.GET:
            fragment = "page"
        if "only_table" in request.GET:
            fragment = "table-content"
    return fragment


def client_type(request):
    if standard_web_browser(request):
        if test_mobile(request):
            if test_tablet(request):
                return "tablet"
            else:
                return "smartfon"
        else:
            return "desktop"
    else:
        return "schweb"


def browser_type(request):
    if hasattr(settings, "THEMES"):
        themes = settings.THEMES
    else:
        themes = ["auto", "auto", "auto"]

    if standard_web_browser(request):
        if test_mobile(request):
            if test_tablet(request):
                if themes[1] == "auto" or not themes[1]:
                    return "tablet_standard"
                else:
                    return themes[1]
            else:
                if themes[2] == "auto" or not themes[2]:
                    return "smartfon_standard"
                else:
                    return themes[2]
        else:
            if themes[0] == "auto" or not themes[0]:
                return "desktop_standard"
            else:
                return themes[0]
    else:
        return "schweb"


def default_template(b_type):
    return "%s.html" % b_type


def default_template2(b_type):
    return "theme/%s.html" % b_type


def has_user_perm(user, perm):
    if "|" in perm:
        arg, fun_path = perm.split("|", 1)
        module_path, fun_name = fun_path.rsplit(".", 1)
        module = __import__(module_path, fromlist=[None])
        fun = getattr(module, fun_name)
        return fun(user, arg)

    else:
        return user.has_perm(perm)


class AppInfo:
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
            + f"module_name: {self.module_name}\n"
            + f"module_title: {self.module_title}\n"
            + f"app_name: {self.app_name}\n"
            + f"app_title: {self.app_title}\n"
        )


class AppItemInfo(AppInfo):
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


class AppManager:
    def __init__(self, request):
        self.request = request

    def appname(self):
        path = self.request.path
        elementy = path.split("/")
        base_url = get_script_prefix()
        nr = base_url.count("/")
        return elementy[nr]

    def appid(self):
        path = self.request.path
        elementy = path.split("/")
        base_url = get_script_prefix()
        nr = base_url.count("/")
        if elementy[nr] == "schwiki":
            return elementy[nr + 1]
        else:
            return elementy[nr]

    def get_main_title(self):
        apps = self._get_apps()
        for app in apps:
            if app[4] == "main":
                return app[0]
        return ""

    def _get_apps(self, prj=None):
        ret = []

        if prj:
            _temp = __import__(prj + ".apps")
            apps = _temp.apps.APPS
        else:
            apps = None

        for _app in settings.INSTALLED_APPS:
            if apps:
                test = False
                name = _app if type(_app) == str else _app.name
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
            if self.request.get_host() == "127.0.0.2" and app == "schserw.schsys":
                continue
            try:
                module_title = None
                module_name = None
                title = None
                perms = None
                url = None
                elementy = app.split(".")
                appname = elementy[-1]
                module = __import__(elementy[0])
                if len(elementy) > 1:
                    module2 = getattr(module, elementy[-1])
                else:
                    module2 = module
                if module2:
                    module_title = module2.ModuleTitle
                    try:
                        module_name = module2.ModuleName
                    except:
                        module_name = module_title
                    title = module2.Title
                    perms = module2.Perms
                    index = module2.Index
                    if hasattr(module2, "UserParam"):
                        user_param = module2.UserParam
                    else:
                        user_param = {}

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
            except:
                pass
        return ret

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

    def get_app_items(self, prj=settings.PRJ_NAME):
        apps = self._get_apps(prj)
        ret = []
        for app in apps:
            if app.app_name != None and app.app_name != "":
                # try:
                module = __import__(app.sys_module_name)
                if app.sys_module_name != app.app_name:
                    module2 = getattr(module, app.app_name)
                else:
                    module2 = module
                if module2:
                    for pos in module2.Urls:
                        # Urls: url, title, right, icon
                        app_info = AppItemInfo(app)
                        app_info.url = app.app_name + "/" + pos[0]
                        app_info.description = pos[1]
                        app_info.right = pos[2]
                        app_info.icon = pos[3]
                        ret.append(app_info)

                    if hasattr(module2, "AdditionalUrls"):
                        # AdditionalUrls: url, title, right, icon, module,
                        if callable(module2.AdditionalUrls):
                            urls2 = module2.AdditionalUrls(
                                prj, self.request.LANGUAGE_CODE[:2].lower()
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
            # except:
            #    pass
        return ret

    def get_apps_width_perm(self, prj=settings.PRJ_NAME):
        ret = []
        items = self.get_app_items(prj)
        no_empty_apps = []
        for item in items:
            if not item.app_name in no_empty_apps:
                no_empty_apps.append(item.app_name)
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

    def get_app_items_width_perm(self, prj=settings.PRJ_NAME):
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

    def get_main_tools_app_items_width_perm(self, prj=settings.PRJ_NAME):
        ret = self.get_app_items_width_perm(prj)
        if settings.THREE_LEVEL_MENU:
            return [item for item in ret if item.module_name == "main tools"]
        else:
            return [item for item in ret if item.module_name != "config"]

    def get_not_main_tools_app_items_width_perm(self, prj=settings.PRJ_NAME):
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
                except:
                    print(sys.exc_info()[0])
                    print(traceback.print_exc())
        return ret


class Env:
    def __init__(self, env):
        self.env = env

    def __getitem__(self, name):
        return self.env(name)


class CanCanWrapper:
    def __init__(self, action, request):
        self.action = action
        self.request = request

    def call(self, obj):
        return self.request.ability.can(self.action, obj)


class CanCanPermWrapper(PermWrapper):
    def __init__(self, request):
        super().__init__(request.user)
        self.request = request

    def __getitem__(self, app_label):
        if app_label.startswith("can_"):
            return CanCanWrapper(app_label[4:], self.request)
        else:
            return super().__getitem(app_label)


def sch_standard(request):
    """Context processor function

    Args:
        requst - django reuqest

    Returns dict with vars:
        standard_web_browser - 0 - wxPython client, 1 - standard browser, 2 - hybrid (webkit embeded in wxPython
        application, 3 - webkit in wxPython frame (no hybrid), 5 - render only content (for javascript ajax),
        6 - render only table content (for javascript ajax)

        app_manager - AppManager(request)browser_type=1

        form_edit - True if request in edit mode

        form_add - True if request in new form mode,

        form_delete - True if request in delete mode

        form_ext -  True if request in form mode

        form_list - True if request in list view mode

        readonly - True if readonly mode

        ro - '_' in readonly mode else ''

        form_info - True if request in form info mode

        form_grid - True if request in form grid mode

        URL_ROOT_FOLDER - url root folder

        URL_BASE - url base folder

        show_form - True if request in show form mode

        browser_type - 'desktop_standard', 'tablet_standard', 'smartfon_standard', 'schweb'

        application_type - 'standard',

        default_template - default template for browser

        default_template2 - default template for browser

        prj_name - prj name

        prj_title - prj title

        show_title_bar - show title bar

        get - True if request in get mode

        settings - settings module

        uuid - uniquie id

        lang: two letters language

        DEBUG: settings.DEBUG
    """

    # parameters = request.session.get('standard_parameters', None).copy()
    # if parameters:
    #    parameters['app_manager'] =  AppManager(request)
    #    parameters['settings'] = settings
    #    return parameters

    standard = standard_web_browser(request)

    r = urlparse(request.path)
    rr = r.path.split("/")
    if len(rr) > 0:
        if rr[-1]:
            last_fragment = rr[-1]
        else:
            if len(rr) > 1:
                last_fragment = rr[-2]
            else:
                last_fragment = ""
    else:
        last_fragment = r.path

    if last_fragment == "edit" or last_fragment == "add":
        form_edit = True
    else:
        form_edit = False
    if last_fragment == "add":
        form_add = True
    else:
        form_add = False
    if last_fragment == "delete":
        form_delete = True
    else:
        form_delete = False

    if request.path.endswith("/view/"):
        form_info = True
    else:
        form_info = False

    if form_edit or form_delete or form_info:
        show_form = True
    else:
        show_form = False
    if "/grid" in request.path:
        form_grid = True
    else:
        form_grid = False
    if "_ext" in request.path:
        form_ext = True
    else:
        form_ext = False
    if "/_" in request.path:
        readonly = True
        ro = "_"
    else:
        readonly = False
        ro = ""
    if "form/list" in request.path:
        list_view = True
    else:
        list_view = False
    if "_set" in request.path or "/sublist" in request.path or "/get" in request.path:
        show_title_bar = True
    else:
        show_title_bar = False
    if "/get" in request.path:
        if "/gettree" in request.path:
            get = "gettree"
        else:
            get = "get"
    else:
        get = ""
    if settings.URL_ROOT_FOLDER and len(settings.URL_ROOT_FOLDER) > 0:
        url_base = "/" + settings.URL_ROOT_FOLDER
    else:
        url_base = ""

    i = 0
    app_path = url_base + "/"
    for pos in rr:
        if pos == settings.URL_ROOT_FOLDER:
            app_path = "/".join(rr[: i + 2]) + "/"
            break
        i += 1

    url_app_base = url_base
    prj = None
    if len(settings.PRJS) > 0:
        for _prj in settings.PRJS:
            if not _prj.startswith("_"):
                if ("/" + _prj + "/") in request.path:
                    url_app_base = url_base + "/" + _prj
                    prj = _prj
                    break
    if not prj:
        prj = settings.PRJ_NAME

    lng = request.LANGUAGE_CODE[:2].lower()

    b_type = browser_type(request)
    c_type = client_type(request)

    x = b_type.split("_")
    b_type = x[0]
    if len(x) > 1:
        b_type2 = x[1]
    else:
        b_type2 = "standard"

    if standard == 2:
        # d_template = default_template("hybrid")
        d_template = default_template2(b_type)
    elif standard == 5:
        # d_template = default_template("only_content")
        d_template = default_template2(b_type)
    elif standard == 6:
        # d_template = default_template("only_table")
        d_template = default_template2(b_type)
    elif standard == 9:
        # d_template = default_template("to_print")
        d_template = default_template2(b_type)
    else:
        d_template = default_template2(b_type)
        # d_template = d_template

    if lng and lng != "en":
        d_template = d_template.replace(".html", "_" + lng + ".html")
        # d_template2 = d_template2.replace(".html", "_" + lng + ".html")

    if settings.GEN_TIME:
        gmt_str = settings.GEN_TIME
    else:
        gmt = time.gmtime()
        gmt_str = "%04d.%02d.%02d %02d:%02d:%02d" % (
            gmt[0],
            gmt[1],
            gmt[2],
            gmt[3],
            gmt[4],
            gmt[5],
        )

    if "HTTP_USER_AGENT" in request.META and request.META["HTTP_USER_AGENT"]:
        user_agent = request.META["HTTP_USER_AGENT"]
    else:
        user_agent = ""

    # if "only_content" in request.GET and request.GET["only_content"]:
    #    content_limited_to = request.GET["only_content"]
    # else:
    #    content_limited_to = ""
    # if "fragment" in request.GET and request.GET["fragment"] == "min":
    #    content_limited_to = request.GET["only_content"]

    if hasattr(settings, "BOOTSTRAP_TEMPLATE"):
        theme = settings.BOOTSTRAP_TEMPLATE.replace("/", "_")
    else:
        theme = ""

    if "extra_param" in request.GET:
        extra_param = request.GET.get("extra_param")
    else:
        extra_param = ""

    ret = {
        "standard_web_browser": standard,
        "form_edit": form_edit,
        "form_add": form_add,
        "form_delete": form_delete,
        # "form_ext": form_ext,
        "form_list": list_view,
        "readonly": readonly,
        "ro": ro,
        # "content_limited_to": content_limited_to,
        "form_info": form_info,
        "form_grid": form_grid,
        "URL_ROOT_FOLDER": settings.URL_ROOT_FOLDER,
        "base_path": url_base + "/",
        "app_path": app_path,
        "URL_APP_BASE": url_app_base,
        "show_form": show_form,
        "browser_type": b_type,
        "client_type": c_type,
        "application_type": b_type2,
        "default_template": d_template,
        # "default_template2": d_template2,
        "prj_name": settings.PRJ_NAME,
        "prj_title": settings.PRJ_TITLE,
        "show_title_bar": show_title_bar,
        "get": get,
        "uuid": "x" + str(uuid.uuid4()),
        "lang": request.LANGUAGE_CODE[:2].lower(),
        "prj": prj,
        "offline_support": settings.OFFLINE_SUPPORT,
        "gen_time": gmt_str,
        "btn_size": settings.BOOTSTRAP_BUTTON_SIZE_CLASS,
        "SHOW_LOGIN_WIN": False,
        "env": Env(get_environ()),
        "pyodide": settings.PYODIDE,
        "user_agent": user_agent,
        "errors": False,
        "app_manager": AppManager(request),
        "theme": theme,
        "settings": settings,
        "fragment": get_fragment(request) if standard else "",
        "extra_param": extra_param,
    }
    if "client_param" in request.session:
        ret.update(request.session["client_param"])

    ret["app_manager"] = AppManager(request)
    ret["settings"] = settings

    if settings.DEBUG:
        ret["context"] = ret

    if hasattr(settings, "CANCAN") and settings.CANCAN:
        ret["perms"] = CanCanPermWrapper(request)

    # print("FRAGMENT: ", get_fragment(request))
    # print("TEMPLATE: ", d_template)

    return ret
