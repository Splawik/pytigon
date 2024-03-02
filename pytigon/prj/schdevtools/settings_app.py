import os
import sys
import json
from urllib.parse import urlparse

PRJ_TITLE = "Developer tools"
PRJ_NAME = "schdevtools"
THEMES = ["tablet_modern", "tablet_modern", "smartfon_standard"]

_lp = os.path.dirname(os.path.abspath(__file__))

if "PYTIGON_ROOT_PATH" in os.environ:
    _rp = os.environ["PYTIGON_ROOT_PATH"]
else:
    _rp = os.path.abspath(os.path.join(_lp, "..", ".."))

if not _lp in sys.path:
    sys.path.insert(0, _lp)
if not _rp in sys.path:
    sys.path.insert(0, _rp)

from pytigon_lib import init_paths

init_paths(PRJ_NAME, _lp)

from pytigon_lib.schdjangoext.django_init import get_app_config
from pytigon_lib.schtools.platform_info import platform_name

from pytigon.schserw.settings import *

from apps import APPS, APPS_EXT, PUBLIC, MAIN_PRJ

try:
    from global_db_settings import setup_databases
except:
    setup_databases = None

MEDIA_ROOT = os.path.join(os.path.join(DATA_PATH, PRJ_NAME), "media")
UPLOAD_PATH = os.path.join(MEDIA_ROOT, "upload")
LOCAL_ROOT_PATH = os.path.abspath(os.path.join(_lp, ".."))
ROOT_PATH = _rp
URL_ROOT_PREFIX = ""
if not LOCAL_ROOT_PATH in sys.path:
    sys.path.append(LOCAL_ROOT_PATH)

if ENV("PUBLISH_IN_SUBFOLDER") and not MAIN_PRJ:
    URL_ROOT_FOLDER = "schdevtools"
    URL_ROOT_PREFIX = URL_ROOT_FOLDER + "/"
    STATIC_URL = URL_ROOT_FOLDER + "/static/"
    MEDIA_URL = URL_ROOT_FOLDER + "/site_media/"
    MEDIA_URL_PROTECTED = URL_ROOT_FOLDER + "/site_media_protected/"
BOOTSTRAP_TEMPLATE = "bootswatch/materia"
# BOOTSTRAP_TEMPLATE = "bootswatch/united"
THREE_LEVEL_MENU = True


PWA_APP_NAME = "SCDevTools"
PWA_APP_DESCRIPTION = "Pytigon developer tools"
PWA_APP_THEME_COLOR = "#0A0302"
PWA_APP_BACKGROUND_COLOR = "#ffffff"
PWA_APP_DISPLAY = "standalone"
PWA_APP_SCOPE = "/" + URL_ROOT_PREFIX
PWA_APP_ORIENTATION = "any"
PWA_APP_START_URL = "/" + URL_ROOT_PREFIX
PWA_APP_STATUS_BAR_COLOR = "default"
PWA_APP_DIR = "ltr"
PWA_APP_LANG = "pl-PL"
PWA_APP_ROOT_URL = "/" + URL_ROOT_PREFIX

PWA_APP_ICONS = [
    {"src": PWA_APP_ROOT_URL + "static/images/pytigon.png", "sizes": "160x160"}
]
PWA_APP_ICONS_APPLE = [
    {"src": PWA_APP_ROOT_URL + "static/images/pytigon.png", "sizes": "160x160"}
]
PWA_APP_SPLASH_SCREEN = [
    {
        "src": PWA_APP_ROOT_URL + "static/images/pytigon.png",
        "media": "(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)",
    }
]

PWA_SERVICE_WORKER_PATH = os.path.join(_lp, "static", PRJ_NAME, "sw.js")

WEBPUSH_SETTINGS = {
    "VAPID_PUBLIC_KEY": "BC50NYho7GMYXtR2tmVyMZyWWRsQRkyX0cuNU-eLcJ8Bmkijj4rbSbw8Q-oH0-fxuggofrcdxTyehu08IX4x8CM",
    "VAPID_PRIVATE_KEY": "ZapnVc3zzzhrM3TPFa_RKFrJ_YymFybgS8F_ZlxAf2I",
    "VAPID_ADMIN_EMAIL": "auto@pytigon.cloud",
}


GUI_COMMAND_LINE = "--no_splash --websocket_id=/schbuilder/clock/channel/"
NUMBER_OF_WORKERS = 1
NO_ASGI = True

INSTALLED_APPS.append("explorer")

EXPLORER_CONNECTIONS = {"Default": "default"}
EXPLORER_DEFAULT_CONNECTION = "default"


if platform_name() != "Android":
    INSTALLED_APPS.append("easy_thumbnails")

    THUMBNAIL_PROCESSORS = (
        "easy_thumbnails.processors.colorspace",
        "easy_thumbnails.processors.autocrop",
        #'easy_thumbnails.processors.scale_and_crop',
        #'filer.thumbnail_processors.scale_and_crop_with_subject_location',
        "easy_thumbnails.processors.filters",
    )
from pytigon_lib.schtools.install_init import init

init(PRJ_NAME, ROOT_PATH, DATA_PATH, PRJ_PATH, STATIC_ROOT, [MEDIA_ROOT, UPLOAD_PATH])

START_PAGE = "None"
SHOW_LOGIN_WIN = True
PACKS = []

for app in APPS:
    if "." in app:
        pack = app.split(".")[0]
        if not pack in PACKS:
            PACKS.append(pack)
            p1 = os.path.join(LOCAL_ROOT_PATH, pack)
            if not p1 in sys.path:
                sys.path.append(p1)
            p2 = os.path.join(PRJ_PATH_ALT, pack)
            if not p2 in sys.path:
                sys.path.append(p2)

    if not app in [x if type(x) == str else x.label for x in INSTALLED_APPS]:
        a = get_app_config(app)
        if not app in INSTALLED_APPS:
            INSTALLED_APPS.append(get_app_config(app))
        aa = app.split(".")
        for root_path in [PRJ_PATH, PRJ_PATH_ALT]:
            base_path = os.path.join(root_path, aa[0])
            if os.path.exists(base_path):
                TEMPLATES[0]["DIRS"].append(os.path.join(base_path, "templates"))
                if len(aa) == 2:
                    if not base_path in sys.path:
                        sys.path.append(base_path)
                    locale_path = os.path.join(base_path, "locale")
                    if locale_path not in LOCALE_PATHS:
                        if os.path.exists(locale_path):
                            LOCALE_PATHS.append(os.path.join(base_path, "locale"))

for app in APPS_EXT:
    if not app in INSTALLED_APPS:
        INSTALLED_APPS.append(app)

TEMPLATES[0]["DIRS"].insert(0, os.path.join(DATA_PATH, PRJ_NAME, "templates"))
TEMPLATES[0]["DIRS"].insert(
    0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
)
TEMPLATES[0]["DIRS"].insert(
    0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "plugins")
)
LOCALE_PATHS.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "locale"))

_NAME = os.path.join(DATA_PATH, "%s/%s.db" % (PRJ_NAME, PRJ_NAME))

DATABASES["default"] = {
    "ENGINE": "django.db.backends.sqlite3",
    "NAME": _NAME,
}

if setup_databases:
    db_setup = setup_databases(PRJ_NAME)
    db_local = DATABASES["default"]
    for key, value in db_setup[0].items():
        DATABASES[key] = value
    DATABASES["local"] = db_local
    if db_setup[1]:
        AUTHENTICATION_BACKENDS = db_setup[1]
else:
    if "DATABASE_URL" in os.environ:
        db_local = DATABASES["default"]
        DATABASES["default"] = ENV.db()
        DATABASES["local"] = db_local
    else:
        DATABASES["local"] = {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": _NAME.replace(".db", "_local.db"),
        }


CHANNELS_URL_TAB += [
    (URL_ROOT_PREFIX + "schbuilder/clock/channel/", "schbuilder.consumers.Clock"),
    (
        URL_ROOT_PREFIX + "schbuilder/webserver/channel/",
        "schbuilder.consumers.WebServer",
    ),
    (
        URL_ROOT_PREFIX + "schbuilder/django_manage/channel/",
        "schbuilder.consumers.DjangoManage",
    ),
    (
        URL_ROOT_PREFIX + "schcommander/shell/channel/",
        "schcommander.consumers.ShellConsumer",
    ),
    (
        URL_ROOT_PREFIX + "schtasks/show_task_events/channel/",
        "schtasks.consumers.TaskEventsConsumer",
    ),
]


try:
    from settings_app_local import *
except:
    pass

GEN_TIME = "2024.03.02 19:21:06"
OFFLINE_SUPPORT = True


for key, value in os.environ.items():
    if key.startswith("PYTIGON_"):
        key2 = key[8:]
        if value.startswith("[") or value.startswith("{") or value.startswith(":"):
            try:
                globals()[key2] = json.loads(
                    value[1 if value.startswith(":") else 0 :]
                    .replace("'", '"')
                    .replace("[|]", "!")
                    .replace('["]', '\\"')
                )
            except:
                print("invalid json syntax for environment variable: %s", key)
        else:
            globals()[key2] = value
