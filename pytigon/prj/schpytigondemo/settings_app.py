import os
import sys
from urllib.parse import urlparse

PRJ_TITLE = "Pytigon demo"
PRJ_NAME = "schpytigondemo"
THEMES = ["tablet_modern", "auto", "tablet_standard"]

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
    URL_ROOT_FOLDER = "schpytigondemo"
    URL_ROOT_PREFIX = URL_ROOT_FOLDER + "/"
    STATIC_URL = URL_ROOT_FOLDER + "/static/"
    MEDIA_URL = URL_ROOT_FOLDER + "/site_media/"
    MEDIA_URL_PROTECTED = URL_ROOT_FOLDER + "/site_media_protected/"

from pytigon_lib.schtools.install_init import init

init(PRJ_NAME, ROOT_PATH, DATA_PATH, PRJ_PATH, STATIC_ROOT, [MEDIA_ROOT, UPLOAD_PATH])

START_PAGE = "None"
SHOW_LOGIN_WIN = False
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
                    LOCALE_PATHS.append(os.path.join(base_path, "locale"))


INSTALLED_APPS.append('explorer')

if platform_name()!='Android':
    INSTALLED_APPS.append('easy_thumbnails')
    INSTALLED_APPS.append('filer')

    THUMBNAIL_PROCESSORS = (
        'easy_thumbnails.processors.colorspace',
        'easy_thumbnails.processors.autocrop',
        #'easy_thumbnails.processors.scale_and_crop',
        'filer.thumbnail_processors.scale_and_crop_with_subject_location',
        'easy_thumbnails.processors.filters',
    )

FILER_DEBUG = True

EXPLORER_CONNECTIONS = { 'Default': 'default' } 
EXPLORER_DEFAULT_CONNECTION = 'default'

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

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": _NAME,
    },
}

if setup_databases:
    db_setup = setup_databases(PRJ_NAME)
    db_local = DATABASES["default"]

    DATABASES = db_setup[0]
    DATABASES["local"] = db_local

    if db_setup[1]:
        AUTHENTICATION_BACKENDS = db_setup[1]
else:
    if "DATABASE_URL" in os.environ:
        db_url = os.environ["DATABASE_URL"]
        db_local = DATABASES["default"]
        DATABASES = {
            "default": ENV.db(),
        }
        DATABASES["local"] = db_local


CHANNELS_URL_TAB += [
    (
        URL_ROOT_PREFIX + "schsimplecontrols_demo/teleconference/channel/",
        "schsimplecontrols_demo.consumers.teleconference",
    ),
    (URL_ROOT_PREFIX + "channels_demo/clock/channel/", "channels_demo.consumers.clock"),
    (
        URL_ROOT_PREFIX + "schcommander/shell/channel/",
        "schcommander.consumers.ShellConsumer",
    ),
    (
        URL_ROOT_PREFIX + "schcommander/shell/channel/",
        "schcommander.consumers.ShellConsumer",
    ),
    (
        URL_ROOT_PREFIX + "schcommander/shell/channel/",
        "schcommander.consumers.ShellConsumer",
    ),
    (
        URL_ROOT_PREFIX + "schcommander/shell/channel/",
        "schcommander.consumers.ShellConsumer",
    ),
    (
        URL_ROOT_PREFIX + "schcommander/shell/channel/",
        "schcommander.consumers.ShellConsumer",
    ),
    (
        URL_ROOT_PREFIX + "schcommander/shell/channel/",
        "schcommander.consumers.ShellConsumer",
    ),
    (
        URL_ROOT_PREFIX + "schcommander/shell/channel/",
        "schcommander.consumers.ShellConsumer",
    ),
    (
        URL_ROOT_PREFIX + "schcommander/shell/channel/",
        "schcommander.consumers.ShellConsumer",
    ),
    (
        URL_ROOT_PREFIX + "schcommander/shell/channel/",
        "schcommander.consumers.ShellConsumer",
    ),
    (
        URL_ROOT_PREFIX + "schcommander/shell/channel/",
        "schcommander.consumers.ShellConsumer",
    ),
]


try:
    from settings_app_local import *
except:
    pass

GEN_TIME = "2022.11.20 10:53:02"
OFFLINE_SUPPORT = True

for key, value in os.environ.items():
    if key.startswith("PYTIGON_"):
        key2 = key[8:]
        if key2 in globals():
            globals()[key2] = type(globals()[key2])(value)
        else:
            globals()[key2] = value

#BOOTSTRAP_TEMPLATE = "bootswatch/zephyr"
#BOOTSTRAP_TEMPLATE = "bootswatch/minty"
#BOOTSTRAP_TEMPLATE = "bootswatch/pulse"
#BOOTSTRAP_TEMPLATE = "bootswatch/journal"
#BOOTSTRAP_TEMPLATE = "bootswatch/united"
#BOOTSTRAP_TEMPLATE = "bootswatch/cosmo"
#BOOTSTRAP_TEMPLATE = "bootswatch/litera"
#BOOTSTRAP_TEMPLATE = "bootswatch/default"
#BOOTSTRAP_TEMPLATE = "bootswatch/sandstone"

#BOOTSTRAP_TEMPLATE = "bootswatch/flatly"
#BOOTSTRAP_TEMPLATE = "bootswatch/yeti"
BOOTSTRAP_TEMPLATE = "bootswatch/materia"


XMLRPC_PORT = 7080
#PYODIDE = True
#PYODIDE = False
