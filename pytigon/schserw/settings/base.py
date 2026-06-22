import os
import sys
from fs.mountfs import MountFS
from fs.multifs import MultiFS

from django.conf import settings

from pytigon.ext_lib.django_storage import OSFS_EXT

from pytigon_lib.schtools.main_paths import get_main_paths, get_prj_name
from pytigon_lib.schtools.platform_info import platform_name
from pytigon_lib.schtools.env import get_environ

ENV = get_environ()
BASE_PRJ_NAME = get_prj_name()

if not BASE_PRJ_NAME:
    BASE_PRJ_NAME = "_schall"

GEN_TIME = "0000.00.00 00:00:00"
USE_TZ = True
DATE_INPUT_FORMATS = [
    "%Y-%m-%d",
]

if (
    sys.argv
    and (
        (sys.argv[0].endswith("manage.py") and "runserver" in sys.argv)
        or "--dev" in sys.argv
    )
) or ENV("PYTIGON_DEBUG"):
    DEBUG = True
    DB_DEBUG = True
    PRODUCTION_VERSION = False
else:
    DEBUG = False
    DB_DEBUG = False
    PRODUCTION_VERSION = True

if sys.argv and (sys.argv[0].endswith("pytigon") or sys.argv[0].endswith("ptig")):
    PRODUCTION_VERSION = False

if ENV("PUBLIC"):
    PUBLIC = True
else:
    PUBLIC = False

SHOW_LOGIN_WIN = True

paths = get_main_paths()

SERW_PATH = paths["SERW_PATH"]
DATA_PATH = paths["DATA_PATH"]
LOG_PATH = paths["LOG_PATH"]
TEMP_PATH = paths["TEMP_PATH"]
PRJ_PATH = paths["PRJ_PATH"]
PRJ_PATH_ALT = paths["PRJ_PATH_ALT"]
STATIC_ROOT = paths["STATIC_PATH"]
STATICFILES_DIRS = paths["STATICFILES_DIRS"]
ROOT_PATH = paths["ROOT_PATH"]

if ENV("SCRIPT_MODE"):
    SCRIPT_MODE = True
    cwd = os.path.abspath(os.getcwd())
    STATIC_ROOT = os.path.join(cwd, "static")
else:
    SCRIPT_MODE = False

PYTIGON_PATH = paths["PYTIGON_PATH"]
PLATFORM_TYPE = paths["PLATFORM_TYPE"]

DATABASES = {}
ADMINS = []
MANAGERS = ADMINS

TIME_ZONE = ENV("TIME_ZONE", default="Europe/Warsaw")
LANGUAGE_CODE = ENV("LANGUAGE_CODE", default="pl")
USE_I18N = True
SITE_ID = 1
LANGUAGES = [
    ["en", "English"],
    ["pl", "Polish"],
]
LOGIN_REDIRECT_URL = "/"
TEST_RUNNER = "django.test.runner.DiscoverRunner"

if DEBUG:
    EXECUTE_DB_CODE = "import"
else:
    EXECUTE_DB_CODE = "exec_and_cache"
EXECUTE_DB_CODE_CACHE_TIMEOUT = 900

BASE_URL = "http://127.0.0.1:81"

URL_ROOT_FOLDER = ""
URL_ROOT_PREFIX = "/"

STATIC_URL = "static/"
MEDIA_URL = "site_media/"
MEDIA_URL_PROTECTED = "site_media_protected/"
UPLOAD_URL = "site_media/upload/"
UPLOAD_URL_PROTECTED = "site_media_protected/upload/"
DOC_URL = "site_media/doc/"
DOC_URL_PROTECTED = "site_media_protected/doc/"

APPEND_SLASH = False

MEDIA_ROOT = os.path.join(os.path.join(DATA_PATH, BASE_PRJ_NAME), "media")
MEDIA_ROOT_PROTECTED = os.path.join(
    os.path.join(DATA_PATH, BASE_PRJ_NAME), "media_protected"
)
UPLOAD_PATH = os.path.join(MEDIA_ROOT, "upload")
UPLOAD_PATH_PROTECTED = os.path.join(MEDIA_ROOT_PROTECTED, "upload")
DOC_PATH = os.path.join(MEDIA_ROOT, "doc")
DOC_PATH_PROTECTED = os.path.join(MEDIA_ROOT_PROTECTED, "doc")


SECRET_KEY = ENV("SECRET_KEY")
if not SECRET_KEY:
    if (not PRODUCTION_VERSION) or DEBUG or ENV("EMBEDED_DJANGO_SERVER"):
        from django.core.management.utils import get_random_secret_key
        SECRET_KEY = get_random_secret_key()
    else:
        raise ValueError(
            "SECRET_KEY must be set in production. "
            "Set the SECRET_KEY environment variable."
        )

if ENV("GRAPHQL"):
    GRAPHQL = True
else:
    GRAPHQL = False

if ENV("REST"):
    REST = True
else:
    REST = False

if ENV("RULES_ENABLED"):
    RULES_ENABLED = True
else:
    RULES_ENABLED = False

if ENV("MAILER"):
    MAILER = True
else:
    MAILER = False

if ENV("ALLAUTH"):
    ALLAUTH = True
else:
    ALLAUTH = False

if ENV("COMPRESS_ENABLED"):
    COMPRESS_ENABLED = True
else:
    COMPRESS_ENABLED = False

if ENV("PWA"):
    PWA = True
else:
    PWA = False
