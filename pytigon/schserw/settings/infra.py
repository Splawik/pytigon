import os
import sys

from django.conf import settings

try:
    from django.utils.csp import CSP
except ImportError:
    CSP = None

from .base import (
    ENV,
    DEBUG,
    PRODUCTION_VERSION,
    DATA_PATH,
    LOG_PATH,
    MEDIA_ROOT,
    MEDIA_ROOT_PROTECTED,
    MEDIA_URL,
    MEDIA_URL_PROTECTED,
    TEMP_PATH,
    PRJ_PATH,
    BASE_PRJ_NAME,
    ROOT_PATH,
    SCRIPT_MODE,
    PLATFORM_TYPE,
    UPLOAD_PATH,
    DOC_PATH,
    DOC_PATH_PROTECTED,
    UPLOAD_PATH_PROTECTED,
)
from .features import MIDDLEWARE, INSTALLED_APPS, ALLAUTH, PWA
from pytigon.ext_lib.django_storage import OSFS_EXT
from pytigon_lib.schtools.platform_info import platform_name

# Logging verbosity level
if "-v" in sys.argv:
    i = sys.argv.index("-v")
    V = int(sys.argv[i + 1])
else:
    V = 1

if PRODUCTION_VERSION:
    if V == 3:
        level = "INFO"
    elif V == 2:
        level = "WARNING"
    elif V == 1:
        level = "ERROR"
    else:
        level = "CRITICAL"
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "standard": {
                "format": ("[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s"),
                "datefmt": "%Y-%m-%d %H:%M:%S",
            }
        },
        "handlers": {
            "logfile": {
                "level": level,
                "class": "logging.FileHandler",
                "filename": LOG_PATH + "/pytigon.log",
                "formatter": "standard",
            },
            "errorlogfile": {
                "level": level,
                "class": "logging.FileHandler",
                "filename": LOG_PATH + "/pytigon-err.log",
                "formatter": "standard",
            },
        },
        "loggers": {
            "django": {
                "handlers": ["logfile", "errorlogfile"],
                "level": level,
                "propagate": True,
            },
            "daphne": {
                "handlers": ["logfile", "errorlogfile"],
                "level": level,
                "propagate": True,
            },
            "httpclient": {
                "handlers": ["logfile", "errorlogfile"],
                "level": level,
                "propagate": True,
            },
            "pytigon": {
                "handlers": ["logfile", "errorlogfile"],
                "level": level,
                "propagate": True,
            },
            "pytigon_task": {
                "handlers": ["logfile", "errorlogfile"],
                "level": level,
                "propagate": True,
            },
        },
    }

    if ENV("LOGS_TO_DOCKER"):
        LOGGING["handlers"] = {
            "logfile": {
                "level": level,
                "class": "logging.StreamHandler",
                "formatter": "standard",
            },
            "errorlogfile": {
                "level": level,
                "class": "logging.StreamHandler",
                "formatter": "standard",
            },
        }
    elif ENV("PYTIGON_TASK"):
        LOGGING["handlers"]["logfile"]["filename"] = LOGGING["handlers"]["logfile"][
            "filename"
        ].replace(".log", "-task.log")
        LOGGING["handlers"]["errorlogfile"]["filename"] = LOGGING["handlers"]["errorlogfile"][
            "filename"
        ].replace(".log", "_task.log")
else:
    if V == 3:
        level = "DEBUG"
    elif V == 2:
        level = "INFO"
    elif V == 1:
        level = "WARNING"
    else:
        level = "ERROR"

    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
            },
        },
        "root": {
            "handlers": ["console"],
            "level": level,
        },
        "loggers": {
            "django": {
                "handlers": ["console"],
                "level": level,
                "propagate": False,
            },
        },
    }

if ENV("LOG_VIEWER"):
    LOGVIEWER = True
    INSTALLED_APPS.append("log_viewer")
    LOG_VIEWER_FILES = [
        "pytigon.log",
        "pytigon-err.log",
        "pytigon-task.log",
        "pytigon-err-task.log",
    ]
    LOG_VIEWER_FILES_DIR = LOG_PATH
    LOG_VIEWER_PATTERNS = ["["]
else:
    LOGVIEWER = False

ATOMIC_REQUESTS = True

INTERNAL_IPS = ("127.0.0.1", "127.0.0.2", "127.0.0.3", "localhost")

ALLOWED_HOSTS = ["*"]

PYTHON_INTERPRETER = sys.executable
PYTHON_CONSOLE = sys.executable

BOOTSTRAP5 = {"use_custom_controls": False, "wrapper_class": ""}

BOOTSTRAP_ADMIN_SIDEBAR_MENU = True
BOOTSTRAP_BUTTON_SIZE_CLASS = ""

BOOTSTRAP_TEMPLATE = ""
THREE_LEVEL_MENU = False

AUTO_RENDER_SELECT2_STATICS = False
SELECT2_THEME = "bootstrap-5"

ASGI_APPLICATION = "pytigon.schserw.routing.application"

if PLATFORM_TYPE == "webserver":
    if ENV("CHANNELS_REDIS"):
        CHANNELS_REDIS_SERVER, CHANNELS_REDIS_PORT = (ENV("CHANNELS_REDIS").split(":") + ["6379"])[
            :2
        ]
    else:
        CHANNELS_REDIS_SERVER = "127.0.0.1"
        CHANNELS_REDIS_PORT = "6379"

    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {"hosts": [(CHANNELS_REDIS_SERVER, int(CHANNELS_REDIS_PORT))]},
        }
    }
else:
    CHANNEL_LAYERS = {"default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}}

STORAGES = {
    "default": {
        "BACKEND": "pytigon.ext_lib.django_storage.FSStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

COMPRESS_STORAGE = "compressor.storage.GzipCompressorFileStorage"

STATIC_FS = None
ROOT_FS = None


def DEFAULT_FILE_STORAGE_FS():
    global STATIC_FS, ROOT_FS
    from fs.mountfs import MountFS
    from fs.multifs import MultiFS

    _m = MountFS()
    ROOT_FS = _m
    _m.mount("pytigon", OSFS_EXT(settings.ROOT_PATH))
    STATIC_FS = MultiFS()
    STATIC_FS.add_fs("static_main", OSFS_EXT(settings.STATIC_ROOT))
    p = os.path.join(PRJ_PATH, BASE_PRJ_NAME, "static")
    if os.path.exists(p):
        STATIC_FS.add_fs("static_prj", OSFS_EXT(p))
    _m.mount("static", STATIC_FS)
    _m.mount("app", OSFS_EXT(settings.LOCAL_ROOT_PATH))
    _m.mount("data", OSFS_EXT(settings.DATA_PATH))
    try:
        _m.mount("temp", OSFS_EXT(settings.TEMP_PATH))
    except Exception:
        pass
    try:
        _m.mount("site_media", OSFS_EXT(settings.MEDIA_ROOT))
        _m.mount("site_media_protected", OSFS_EXT(settings.MEDIA_ROOT_PROTECTED))
    except Exception:
        print("mount error: site_media paths not available")

    try:
        _m.mount("doc", OSFS_EXT(settings.DOC_PATH))
        _m.mount("doc_protected", OSFS_EXT(settings.DOC_PATH_PROTECTED))

        _m.mount("upload", OSFS_EXT(settings.UPLOAD_PATH))
        _m.mount(
            "filer_public",
            OSFS_EXT(os.path.join(settings.UPLOAD_PATH, "filer_public")),
        )
        _m.mount(
            "filer_private",
            OSFS_EXT(os.path.join(settings.UPLOAD_PATH, "filer_private")),
        )
        _m.mount(
            "filer_public_thumbnails",
            OSFS_EXT(os.path.join(settings.UPLOAD_PATH, "filer_public_thumbnails")),
        )
        _m.mount(
            "filer_private_thumbnails",
            OSFS_EXT(os.path.join(settings.UPLOAD_PATH, "filer_private_thumbnails")),
        )
    except Exception:
        print("mount error: doc/upload paths not available")

    if sys.argv and (sys.argv[0].endswith("pytigon") or sys.argv[0].endswith("ptig")):
        if platform_name() == "Windows":
            _m.mount("osfs", OSFS_EXT("c:\\"))
        else:
            _m.mount("osfs", OSFS_EXT("/"))

    if SCRIPT_MODE:
        cwd = os.path.abspath(os.getcwd())
        _m.mount("cwd", cwd)

    return _m


THUMBNAIL_DEFAULT_STORAGE = "pytigon.ext_lib.django_storage.ThumbnailFileSystemStorage"

if ENV("THUMBNAIL_PROTECTED"):
    THUMBNAIL_MEDIA_ROOT = os.path.join(MEDIA_ROOT_PROTECTED, "thumb")
    THUMBNAIL_MEDIA_URL = MEDIA_URL_PROTECTED + "thumb/"
else:
    THUMBNAIL_MEDIA_ROOT = os.path.join(MEDIA_ROOT, "thumb")
    THUMBNAIL_MEDIA_URL = MEDIA_URL + "thumb/"

THUMBNAIL_BASEDIR = THUMBNAIL_MEDIA_ROOT

if not os.path.exists(THUMBNAIL_MEDIA_ROOT):
    os.makedirs(THUMBNAIL_MEDIA_ROOT)

THUMBNAIL_ALIASES = {
    "": {
        "small": {"size": (50, 50), "crop": True},
        "large": {"size": (800, 600), "crop": True},
    },
}

DATA_UPLOAD_MAX_MEMORY_SIZE = 26214400
OFFLINE_SUPPORT = False
PYODIDE = False
CORS_ORIGIN_WHITELIST = ("null",)

if platform_name() == "Android":
    CORS_ORIGIN_ALLOW_ALL = True

try:
    CACHES = {"default": ENV.cache()}
    SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
except Exception:
    pass

MESSAGE_STORAGE = "pytigon.schserw.schsys.cache_message_storage.CacheStorage"

SOCIALACCOUNT_ADAPTER = "pytigon_lib.schdjangoext.allauth.SocialAccountAdapter"
if DEBUG:
    ACCOUNT_DEFAULT_HTTP_PROTOCOL = "http"
    ACCOUNT_EMAIL_REQUIRED = False
else:
    ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"
    ACCOUNT_EMAIL_REQUIRED = True
    ACCOUNT_EMAIL_VERIFICATION = "mandatory"
    ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
    ACCOUNT_USERNAME_REQUIRED = True

ACCOUNT_AUTHENTICATION_METHOD = "username_email"

SOCIALACCOUNT_LOGIN_ON_GET = True

GRAPHENE = {
    "SCHEMA": "pytigon.schserw.schsys.schema.schema",
}

GRAPHENE_PUBLIC = False

try:
    import dj_email_url

    email_config = dj_email_url.config()
    vars().update(email_config)
except Exception:
    pass

if ENV("EMBEDED_DJANGO_SERVER"):
    Q_CLUSTER = {
        "name": "DjangORM",
        "workers": 1,
        "timeout": 360,
        "retry": 480,
        "queue_limit": 10,
        "bulk": 10,
        "orm": "default",
    }
else:
    Q_CLUSTER = {
        "name": "DjangORM",
        "workers": 2,
        "timeout": 360,
        "retry": 480,
        "queue_limit": 50,
        "bulk": 10,
        "orm": "default",
    }

SENTRY_ENABLED = False
if ENV("SENTRY_ENABLED"):
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    SENTRY_ENABLED = True

    sentry_sdk.init(
        dsn=ENV("SENTRY_DSN"),
        integrations=[DjangoIntegration()],
        auto_session_tracking=False,
        environment="production",
    )

PROMETHEUS_ENABLED = False
if ENV("PROMETHEUS_ENABLED"):
    PROMETHEUS_ENABLED = True
    INSTALLED_APPS.append("django_prometheus")

if False:
    if CSP is not None:
        SECURE_CSP = {
            "default-src": [CSP.SELF],
            "script-src": [
                CSP.SELF,
                CSP.NONCE,
                "blob:",
                "https://*.jsdelivr.net",
                "http://*.jsdelivr.net",
                "https://*.googleapis.com",
                "http://*.googleapis.com",
            ],
            "style-src": [
                CSP.SELF,
                CSP.UNSAFE_INLINE,
                "https://fonts.googleapis.com",
            ],
            "font-src": [CSP.SELF, "https://fonts.gstatic.com", "data:"],
            "img-src": [
                CSP.SELF,
                "data:",
                "http://*.tile.osm.org/",
                "https://*.tile.osm.org/",
                "http://*.bossanova.uk/",
                "https://*.bossanova.uk/",
                "http://*.tile.openstreetmap.org",
                "https://*.tile.openstreetmap.org",
            ],
            "worker-src": [CSP.SELF, "blob:"],
            "connect-src": [
                CSP.SELF,
                "https://*.tile.openstreetmap.org",
                "http://*.tile.openstreetmap.org",
            ],
        }
    else:
        SECURE_CSP = {}

if CSP is not None:
    SECURE_CSP = {
        "default-src": [CSP.SELF],
        "script-src": [
            CSP.SELF,
            CSP.NONCE,
            "blob:",
            "https://*.jsdelivr.net",
            "http://*.jsdelivr.net",
            "https://*.googleapis.com",
            "http://*.googleapis.com",
            "'sha256-HHh/PGb5Jp8ck+QB/v7zeWzuHf3vYssM0CBPvYgEHR4='",
        ],
        "style-src": [
            CSP.SELF,
            CSP.UNSAFE_INLINE,
            "https://*.jsdelivr.net",
            "http://*.jsdelivr.net",
            "http://googleapis.com",
            "http://*.googleapis.com",
            "https://googleapis.com",
            "https://*.googleapis.com",
        ],
        "font-src": [
            CSP.SELF,
            "http://gstatic.com",
            "http://*.gstatic.com",
            "https://gstatic.com",
            "https://*.gstatic.com",
            "data:",  # Przekazane jako zwykły ciąg znaków
        ],
        "img-src": [
            CSP.SELF,
            "data:",  # Przekazane jako zwykły ciąg znaków
            "blob:",  # Przekazane jako zwykły ciąg znaków (wymagane przez MapLibre)
            "http://*.tile.osm.org",
            "https://*.tile.osm.org",
            "http://*.bossanova.uk",
            "https://*.bossanova.uk",
            "http://*.tile.openstreetmap.org",
            "https://*.tile.openstreetmap.org",
        ],
        "worker-src": [
            CSP.SELF,
            "blob:",  # Przekazane jako zwykły ciąg znaków
        ],
        "connect-src": [
            CSP.SELF,
            "https://cdn.jsdelivr.net/",
            "https://tile.openstreetmap.org",
            "http://tile.openstreetmap.org",
            "https://*.tile.openstreetmap.org",
            "http://*.tile.openstreetmap.org",
        ],
    }
else:
    SECURE_CSP = {}
