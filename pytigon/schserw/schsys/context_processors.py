"""Module contains standard context processors"""

import datetime
import time
import uuid
from urllib.parse import urlparse

from django.conf import settings
from django.utils.functional import SimpleLazyObject

try:
    from django.contrib.auth.context_processors import PermWrapper
except ImportError:
    PermWrapper = None

from pytigon_lib.schdjangoext.django_init import get_app_name
from pytigon_lib.schtools.env import get_environ

from .app_manager import AppItemInfo, AppManager

# Safe settings attributes exposed to templates — secrets like SECRET_KEY,
# DATABASES, etc. are NOT included.
_SAFE_SETTINGS_ATTRS = frozenset(
    {
        "DEBUG",
        "URL_ROOT_FOLDER",
        "URL_ROOT_PREFIX",
        "STATIC_URL",
        "MEDIA_URL",
        "MEDIA_URL_PROTECTED",
        "UPLOAD_URL",
        "DOC_URL",
        "APPEND_SLASH",
        "PRJ_NAME",
        "PRJ_TITLE",
        "LANGUAGE_CODE",
        "TIME_ZONE",
        "USE_I18N",
        "USE_TZ",
        "SITE_ID",
        "LANGUAGES",
        "LOGIN_REDIRECT_URL",
        "COMPRESS_ENABLED",
        "PWA",
        "OFFLINE_SUPPORT",
        "PYODIDE",
        "BOOTSTRAP_BUTTON_SIZE_CLASS",
        "GEN_TIME",
        "BASE_URL",
        "RULES_ENABLED",
        "GRAPHQL",
        "REST",
        "MAILER",
        "ALLAUTH",
        "SHOW_LOGIN_WIN",
        "PUBLIC",
        "PRODUCTION_VERSION",
        "THREE_LEVEL_MENU",
        "SELECT2_THEME",
        "BOOTSTRAP5",
        "BOOTSTRAP_TEMPLATE",
    }
)


class SafeSettingsProxy:
    """Proxy that only exposes whitelisted settings attributes to templates.

    Prevents accidental leakage of secrets (SECRET_KEY, DATABASES, etc.)
    through the template context.
    """

    def __getattr__(self, name):
        if name in _SAFE_SETTINGS_ATTRS:
            return getattr(settings, name)
        raise AttributeError(name)

    def __dir__(self):
        return sorted(_SAFE_SETTINGS_ATTRS)

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
    if "HTTP_ACCEPT" in request.META and request.META.get("HTTP_USER_AGENT"):
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


def _extract_path_info(request):
    r = urlparse(request.path)
    rr = r.path.split("/")
    last_fragment = (rr[-1] if rr[-1] else rr[-2] if len(rr) > 1 else "") if len(rr) > 0 else r.path
    return r, rr, last_fragment


def _extract_form_state(request, last_fragment):
    return {
        "form_edit": last_fragment in ("edit", "add"),
        "form_add": last_fragment == "add",
        "form_delete": last_fragment == "delete",
        "form_info": request.path.endswith("/view/"),
        "form_grid": "/grid" in request.path,
        "form_ext": "_ext" in request.path,
        "form_list": "form/list" in request.path,
    }


def _extract_view_state(request, rr):
    readonly = "/_" in request.path
    return {
        "readonly": readonly,
        "ro": "_" if readonly else "",
        "show_title_bar": any(x in request.path for x in ("/sublist", "/get", "_set")),
        "get": ("gettree" if "/gettree" in request.path else "get") if "/get" in request.path else "",
    }


def _extract_url_info(rr):
    url_base = "/" + settings.URL_ROOT_FOLDER if settings.URL_ROOT_FOLDER else ""
    i = 0
    app_path = url_base + "/"
    for pos in rr:
        if pos == settings.URL_ROOT_FOLDER:
            app_path = "/".join(rr[: i + 2]) + "/"
            break
        i += 1
    return url_base, app_path


def _extract_project_info(request):
    url_base = "/" + settings.URL_ROOT_FOLDER if settings.URL_ROOT_FOLDER else ""
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
    return url_app_base, prj


def _extract_browser_info(request):
    lng = request.LANGUAGE_CODE[:2].lower() if hasattr(request, "LANGUAGE_CODE") else "en"
    b_type = browser_type(request)
    c_type = client_type(request)
    x = b_type.split("_")
    b_type = x[0]
    b_type2 = x[1] if len(x) > 1 else "standard"
    d_template = default_template2(b_type)
    if lng and lng != "en":
        d_template = d_template.replace(".html", "_" + lng + ".html")
    return b_type, b_type2, c_type, d_template, lng


def _extract_theme(settings):
    if hasattr(settings, "BOOTSTRAP_TEMPLATE"):
        return settings.BOOTSTRAP_TEMPLATE.replace("/", "_")
    return ""


def sch_standard(request):
    standard = standard_web_browser(request)
    _r, rr, last_fragment = _extract_path_info(request)

    form_state = _extract_form_state(request, last_fragment)
    view_state = _extract_view_state(request, rr)
    show_form = form_state["form_edit"] or form_state["form_delete"] or form_state["form_info"]

    url_base, app_path = _extract_url_info(rr)
    url_app_base, prj = _extract_project_info(request)

    b_type, b_type2, c_type, d_template, lng = _extract_browser_info(request)

    if settings.GEN_TIME:
        gmt_str = settings.GEN_TIME
    else:
        gmt = time.gmtime()
        gmt_str = f"{gmt[0]:04d}.{gmt[1]:02d}.{gmt[2]:02d} {gmt[3]:02d}:{gmt[4]:02d}:{gmt[5]:02d}"

    user_agent = request.META.get("HTTP_USER_AGENT", "")

    ret = {
        "standard_web_browser": standard,
        **form_state,
        **view_state,
        "show_form": show_form,
        "URL_ROOT_FOLDER": settings.URL_ROOT_FOLDER,
        "base_path": url_base + "/",
        "app_path": app_path,
        "URL_APP_BASE": url_app_base,
        "browser_type": b_type,
        "client_type": c_type,
        "application_type": b_type2,
        "default_template": d_template,
        "prj_name": settings.PRJ_NAME,
        "prj_title": settings.PRJ_TITLE,
        "uuid": "x" + str(uuid.uuid4()),
        "lang": lng,
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
        "theme": _extract_theme(settings),
        "settings": SimpleLazyObject(SafeSettingsProxy),
        "fragment": get_fragment(request) if standard else "",
        "extra_param": request.GET.get("extra_param", ""),
        "datetime": datetime,
    }
    if hasattr(request, "session") and "client_param" in request.session:
        ret.update(request.session["client_param"])

    if settings.DEBUG:
        ret["context"] = ret

    if PermWrapper:
        from pytigon_lib.schviews.schrules import is_rules_active
        if is_rules_active():
            ret["perms"] = RulesPermWrapper(request)

    return ret
