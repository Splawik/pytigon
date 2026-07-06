"""Module contains standard context processors"""

import datetime
import time
import uuid
from urllib.parse import urlparse

from django.conf import settings

try:
    from django.contrib.auth.context_processors import PermWrapper
except Exception:
    PermWrapper = None

from pytigon_lib.schdjangoext.django_init import get_app_name
from pytigon_lib.schtools.env import get_environ

from .app_manager import AppItemInfo, AppManager

MOBILE_USER_AGENTS = (
    "sony,symbian,nokia,samsung,mobile,windows ce,epoc,opera mini,nitro,j2me,midp-,"
    "cldc-,netfront,mot,up.browser,up.link,audiovox,blackberry,ericsson,panasonic,"
    "philips,sanyo,sharp,sie-,portalmmm,blazer,avantgo,danger,palm,series60,palmsource,"
    "pocketpc,smartphone,rover,ipaq,au-mic,alcatel,ericy,up.link,docomo,vodafone/,"
    "wap1.,wap2.,plucker,480x640,sec,fennec,android,google wireless transcoder,"
    "nintendo,webtv,playstation"
).split(",")


def test_mobile(request):
    if "HTTP_X_OPERAMINI_FEATURES" in request.META:
        return True
    if "HTTP_ACCEPT" in request.META and request.META["HTTP_USER_AGENT"]:
        s = request.META["HTTP_ACCEPT"].lower()
        if "application/vnd.wap.xhtml+xml" in s:
            return True
    if "HTTP_USER_AGENT" in request.META and request.META["HTTP_USER_AGENT"]:
        s = request.META["HTTP_USER_AGENT"].lower()
        for ua in MOBILE_USER_AGENTS:
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
    if "HTTP_USER_AGENT" not in request.META:
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
        if (
            hasattr(request, "session")
            and "HYBRID_BROWSER" in request.session
            or "hybrid" in request.GET
        ):
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
    themes = settings.THEMES if hasattr(settings, "THEMES") else ["auto", "auto", "auto"]

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
    return f"{b_type}.html"


def default_template2(b_type):
    return f"theme/{b_type}.html"


class Env:
    def __init__(self, env):
        self.env = env

    def __getitem__(self, name):
        return self.env(name)


if PermWrapper:

    class RulesWrapper:
        def __init__(self, action, request):
            self.action = action
            self.request = request

        def call(self, obj):
            from pytigon_lib.schviews.schrules import user_can
            return user_can(self.request.user, self.action, type(obj), obj)

    class RulesPermWrapper(PermWrapper):
        def __init__(self, request):
            super().__init__(request.user)
            self.request = request

        def __getitem__(self, app_label):
            if app_label.startswith("can_"):
                return RulesWrapper(app_label[4:], self.request)
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

    standard = standard_web_browser(request)

    r = urlparse(request.path)
    rr = r.path.split("/")
    last_fragment = (rr[-1] if rr[-1] else rr[-2] if len(rr) > 1 else "") if len(rr) > 0 else r.path

    form_edit = True if last_fragment == "edit" or last_fragment == "add" else False
    form_add = True if last_fragment == "add" else False
    form_delete = True if last_fragment == "delete" else False

    form_info = True if request.path.endswith("/view/") else False

    show_form = True if form_edit or form_delete or form_info else False
    form_grid = True if "/grid" in request.path else False
    form_ext = True if "_ext" in request.path else False
    if "/_" in request.path:
        readonly = True
        ro = "_"
    else:
        readonly = False
        ro = ""
    list_view = True if "form/list" in request.path else False
    if "_set" in request.path or "/sublist" in request.path or "/get" in request.path:
        show_title_bar = True
    else:
        show_title_bar = False
    get = ("gettree" if "/gettree" in request.path else "get") if "/get" in request.path else ""
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

    lng = request.LANGUAGE_CODE[:2].lower() if hasattr(request, "LANGUAGE_CODE") else "en"

    b_type = browser_type(request)
    c_type = client_type(request)

    x = b_type.split("_")
    b_type = x[0]
    b_type2 = x[1] if len(x) > 1 else "standard"

    d_template = default_template2(b_type)

    if lng and lng != "en":
        d_template = d_template.replace(".html", "_" + lng + ".html")

    if settings.GEN_TIME:
        gmt_str = settings.GEN_TIME
    else:
        gmt = time.gmtime()
        gmt_str = f"{gmt[0]:04d}.{gmt[1]:02d}.{gmt[2]:02d} {gmt[3]:02d}:{gmt[4]:02d}:{gmt[5]:02d}"

    if "HTTP_USER_AGENT" in request.META and request.META["HTTP_USER_AGENT"]:
        user_agent = request.META["HTTP_USER_AGENT"]
    else:
        user_agent = ""

    if hasattr(settings, "BOOTSTRAP_TEMPLATE"):
        theme = settings.BOOTSTRAP_TEMPLATE.replace("/", "_")
    else:
        theme = ""

    extra_param = request.GET.get("extra_param") if "extra_param" in request.GET else ""

    ret = {
        "standard_web_browser": standard,
        "form_edit": form_edit,
        "form_add": form_add,
        "form_delete": form_delete,
        "form_list": list_view,
        "readonly": readonly,
        "ro": ro,
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
        "prj_name": settings.PRJ_NAME,
        "prj_title": settings.PRJ_TITLE,
        "show_title_bar": show_title_bar,
        "get": get,
        "uuid": "x" + str(uuid.uuid4()),
        "lang": request.LANGUAGE_CODE[:2].lower()
        if hasattr(request, "LANGUAGE_CODE") and request.LANGUAGE_CODE
        else "en",
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
        "datetime": datetime,
    }
    if hasattr(request, "session") and "client_param" in request.session:
        ret.update(request.session["client_param"])

    ret["settings"] = settings

    if settings.DEBUG:
        ret["context"] = ret

    if PermWrapper:
        from pytigon_lib.schviews.schrules import is_rules_active
        if is_rules_active():
            ret["perms"] = RulesPermWrapper(request)

    return ret
