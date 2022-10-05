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

import os
import sys
import random
import string
from fs.mountfs import MountFS
from fs.multifs import MultiFS
from fs.osfs import OSFS
from django.conf import settings
from pytigon_lib.schtools.main_paths import get_main_paths, get_prj_name
from pytigon_lib.schtools.env import get_environ
import os

ENV = get_environ()
BASE_PRJ_NAME = get_prj_name()

if not BASE_PRJ_NAME:
    BASE_PRJ_NAME = "_schall"

GEN_TIME = "0000.00.00 00:00:00"
USE_TZ = True

if (
    sys.argv
    and (
        (sys.argv[0].endswith("manage.py") and "runserver" in sys.argv)
        or "--debug" in sys.argv
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
    # DEBUG = True

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

PYTIGON_PATH = paths["PYTIGON_PATH"]
PLATFORM_TYPE = paths["PLATFORM_TYPE"]

ADMINS = []
MANAGERS = ADMINS

TIME_ZONE = "Europe/Warsaw"
LANGUAGE_CODE = "pl"
USE_I18N = True
SITE_ID = 1
LANGUAGES = [["en", "English"], ["pl", "Polish"]]
LOGIN_REDIRECT_URL = "/"
TEST_RUNNER = "django.test.runner.DiscoverRunner"


BASE_URL = "http://127.0.0.1:81"

URL_ROOT_FOLDER = ""
URL_ROOT_PREFIX = "/"
STATIC_URL = "static/"
MEDIA_URL = "site_media/"
MEDIA_URL_PROTECTED = "protected_site_media/"


APPEND_SLASH = False

from pytigon_lib.schtools.platform_info import platform_name

MEDIA_ROOT = os.path.join(os.path.join(DATA_PATH, BASE_PRJ_NAME), "media")
MEDIA_ROOT_PROTECTED = os.path.join(
    os.path.join(DATA_PATH, BASE_PRJ_NAME), "protected_media"
)
UPLOAD_PATH = os.path.join(MEDIA_ROOT, "upload")
UPLOAD_PATH_PROTECTED = os.path.join(MEDIA_ROOT, "protected_upload")

ADMIN_MEDIA_PREFIX = "/media/"

SECRET_KEY = ENV("SECRET_KEY")
if not SECRET_KEY:
    if (not PRODUCTION_VERSION) or DEBUG or ENV("EMBEDED_DJANGO_SERVER"):
        SECRET_KEY = "anawa"
    else:
        SECRET_KEY = "".join(
            random.choice(string.ascii_uppercase + string.digits) for _ in range(32)
        )

if ENV("GRAPHQL"):
    GRAPHQL = True
else:
    GRAPHQL = False


if ENV("REST"):
    REST = True
else:
    REST = False


ROOT_URLCONF = "pytigon.schserw.urls"

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "pytigon_lib.schdjangoext.django_settings.AppPackDirectoriesFinder",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            PYTIGON_PATH + "/templates",
            PYTIGON_PATH + "/appdata/plugins",
            DATA_PATH + "/plugins",
        ],
        "OPTIONS": {
            "context_processors": [
                "pytigon.schserw.schsys.context_processors.sch_standard",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.request",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.request",
            ],
            "loaders": [
                "pytigon_lib.schdjangoext.python_style_template_loader.Loader",
                "pytigon_lib.schdjangoext.python_style_template_loader.DBLoader",
                # "pytigon_lib.schdjangoext.python_style_template_loader.FSLoader",
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
            "builtins": ["pytigon.schserw.schsys.templatetags.defexfiltry"],
            "debug": DEBUG,
            # "string_if_invalid": "Invalid varialbe: %s!",
        },
    }
]

FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

if ENV("EMBEDED_DJANGO_SERVER"):
    MIDDLEWARE = [
        "django.middleware.common.CommonMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.locale.LocaleMiddleware",
        "pytigon.schserw.schmiddleware.csrf.DisableCSRF",
        # "pytigon.schserw.schmiddleware.schpost.view_post",
    ]
else:
    MIDDLEWARE = [
        "corsheaders.middleware.CorsMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.locale.LocaleMiddleware",
        "django.contrib.auth.middleware.RemoteUserMiddleware",
        # "pytigon.schserw.schmiddleware.schpost.view_post",
    ]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]


INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.messages",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.admin",
    "django.contrib.sites",
    "django.forms",
    "django_select2",
    "mailer",
    "django_bootstrap5",
    "corsheaders",
    "widget_tweaks",
    "pytigon.schserw.schsys",
]

if GRAPHQL:
    INSTALLED_APPS.append("graphene_django")
    INSTALLED_APPS.append("oauth2_provider")

if REST:
    INSTALLED_APPS.append("rest_framework")
    if not "oauth2_provider" in INSTALLED_APPS:
        INSTALLED_APPS.append("oauth2_provider")

    REST_FRAMEWORK = {
        "DEFAULT_AUTHENTICATION_CLASSES": [
            "oauth2_provider.contrib.rest_framework.OAuth2Authentication",
        ]
    }

OAUTH2_PROVIDER = {
    #'SCOPES': {
    #    'read': 'Read scope',
    #    'write': 'Write scope',
    # },
    "PKCE_REQUIRED": False,
}


try:
    import mptt

    MPTT = True
    LOGVIEWER = True
    INSTALLED_APPS.append("mptt")
    INSTALLED_APPS.append("django_filters")
    INSTALLED_APPS.append("log_viewer")
except:
    MPTT = False
    LOGVIEWER = False

try:
    import allauth

    ALLAUTH = True
    INSTALLED_APPS.append("allauth")
    INSTALLED_APPS.append("allauth.account")
    INSTALLED_APPS.append("allauth.socialaccount")
    AUTHENTICATION_BACKENDS.append(
        "allauth.account.auth_backends.AuthenticationBackend"
    )
except:
    ALLAUTH = False

try:
    import compressor

    INSTALLED_APPS.append("compressor")
    STATICFILES_FINDERS.append("compressor.finders.CompressorFinder")
except:
    INSTALLED_APPS.append("_schserverless.schnocompress")

if ENV("PWA"):
    INSTALLED_APPS.append("pwa")
    INSTALLED_APPS.append("webpush")

    if DEBUG:
        WEBPUSH_SETTINGS = {
            "VAPID_PUBLIC_KEY": "BC50NYho7GMYXtR2tmVyMZyWWRsQRkyX0cuNU-eLcJ8Bmkijj4rbSbw8Q-oH0-fxuggofrcdxTyehu08IX4x8CM",
            "VAPID_PRIVATE_KEY": "ZapnVc3zzzhrM3TPFa_RKFrJ_YymFybgS8F_ZlxAf2I",
            "VAPID_ADMIN_EMAIL": "auto@pytigon.cloud",
        }
    PWA = True
else:
    PWA = False

if PLATFORM_TYPE != "webserver":
    MIDDLEWARE.insert(
        #        0, "pytigon.schserw.schmiddleware.whitenoise2.WhiteNoiseMiddleware2"
        0,
        "whitenoise.middleware.WhiteNoiseMiddleware",
    )
    INSTALLED_APPS.append("whitenoise.runserver_nostatic")

INSTALLED_APPS.append("django.contrib.staticfiles")

if (
    not ENV("PYTIGON_WITHOUT_CHANNELS")
    and platform_name() != "Android"
    and platform_name() != "Emscripten"
):
    try:
        import channels
        import twisted

        INSTALLED_APPS.append("channels")
    except:
        pass
try:
    from multiprocessing import synchronize

    INSTALLED_APPS.append("django_q")
except:
    pass

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

CHANNELS_URL_TAB = []

HIDE_APPS = []

PRJS = []

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
                "format": "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            }
        },
        "handlers": {
            "logfile": {
                "level": level,
                "class": "logging.FileHandler",
                "filename": LOG_PATH + "/pytigon.log",
                # "maxBytes": 50000,
                # "backupCount": 2,
                "formatter": "standard",
            },
            "errorlogfile": {
                "level": level,
                "class": "logging.FileHandler",
                "filename": LOG_PATH + "/pytigon-err.log",
                # "maxBytes": 50000,
                # "backupCount": 2,
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
        LOGGING["handlers"]["errorlogfile"]["filename"] = LOGGING["handlers"][
            "errorlogfile"
        ]["filename"].replace(".log", "_task.log")

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

LOG_VIEWER_FILES = [
    "pytigon.log",
    "pytigon-err.log",
    "pytigon-task.log",
    "pytigon-err-task.log",
]
LOG_VIEWER_FILES_DIR = LOG_PATH
LOG_VIEWER_PATTERNS = [
    "[",
]

LOCALE_PATHS = [
    os.path.join(SERW_PATH, "locale"),
    os.path.join(PRJ_PATH, get_prj_name(), "locale"),
]

# CSRF_USE_SESSIONS = True

ATOMIC_REQUESTS = True

INTERNAL_IPS = ("127.0.0.1", "127.0.0.2", "127.0.0.3", "localhost")

ALLOWED_HOSTS = ["*"]

PYTHON_INTERPRETER = sys.executable
PYTHON_CONSOLE = sys.executable

BOOTSTRAP5 = {"use_custom_controls": False, "wrapper_class": ""}

BOOTSTRAP_ADMIN_SIDEBAR_MENU = True
BOOTSTRAP_BUTTON_SIZE_CLASS = ""

BOOTSTRAP_TEMPLATE = ""

# SEARCH_PATH = "/schwiki/%s/search/"

AUTO_RENDER_SELECT2_STATICS = False
SELECT2_THEME = "bootstrap-5"


ASGI_APPLICATION = "pytigon.schserw.routing.application"

if PLATFORM_TYPE == "webserver":
    if ENV("CHANNELS_REDIS"):
        CHANNELS_REDIS_SERVER, CHANNELS_REDIS_PORT = (
            ENV("CHANNELS_REDIS").split(":") + ["6379"]
        )[:2]
    else:
        CHANNELS_REDIS_SERVER = "127.0.0.1"
        CHANNELS_REDIS_PORT = "6379"

    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            # "ROUTING": "schserw.routing.channel_routing",
            "CONFIG": {"hosts": [(CHANNELS_REDIS_SERVER, int(CHANNELS_REDIS_PORT))]},
        }
    }
else:
    CHANNEL_LAYERS = {"default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}}

DEFAULT_FILE_STORAGE = "pytigon.ext_lib.django_storage.FSStorage"
STATICFILES_STORAGE = "pytigon.ext_lib.django_storage.StaticFSStorage"

if ENV("COMPRESS_ENABLED"):
    COMPRESS_ENABLED = True
else:
    COMPRESS_ENABLED = False

COMPRESS_STORAGE = "compressor.storage.GzipCompressorFileStorage"

STATIC_FS = None


def STATIC_FILE_STORAGE_FS():
    static_fs = MultiFS()
    static_fs.add_fs("static_main", OSFS(settings.STATIC_ROOT), write=True)
    p = os.path.join(PRJ_PATH, BASE_PRJ_NAME, "static")
    if os.path.exists(p):
        static_fs.add_fs("static_prj", OSFS(p))
    return static_fs


def DEFAULT_FILE_STORAGE_FS():
    global STATIC_FS
    _m = MountFS()
    _m.mount("pytigon", OSFS(settings.ROOT_PATH))
    STATIC_FS = MultiFS()
    STATIC_FS.add_fs("static_main", OSFS(settings.STATIC_ROOT))
    p = os.path.join(PRJ_PATH, BASE_PRJ_NAME, "static")
    if os.path.exists(p):
        STATIC_FS.add_fs("static_prj", OSFS(p))
    _m.mount("static", STATIC_FS)
    _m.mount("app", OSFS(settings.LOCAL_ROOT_PATH))
    _m.mount("data", OSFS(settings.DATA_PATH))
    try:
        _m.mount("temp", OSFS(settings.TEMP_PATH))
    except:
        pass
    try:
        _m.mount("media", OSFS(settings.MEDIA_ROOT))
    except:
        pass
    try:
        _m.mount("upload", OSFS(settings.UPLOAD_PATH))
        _m.mount(
            "filer_public", OSFS(os.path.join(settings.UPLOAD_PATH, "filer_public"))
        )
        _m.mount(
            "filer_private", OSFS(os.path.join(settings.UPLOAD_PATH, "filer_private"))
        )
        _m.mount(
            "filer_public_thumbnails",
            OSFS(os.path.join(settings.UPLOAD_PATH, "filer_public_thumbnails")),
        )
        _m.mount(
            "filer_private_thumbnails",
            OSFS(os.path.join(settings.UPLOAD_PATH, "filer_private_thumbnails")),
        )
    except:
        pass

    if sys.argv and sys.argv[0].endswith("pytigon"):
        if platform_name() == "Windows":
            _m.mount("osfs", OSFS("c:\\"))
        else:
            _m.mount("osfs", OSFS("/"))

    return _m


DATA_UPLOAD_MAX_MEMORY_SIZE = 26214400
OFFLINE_SUPPORT = False
PYODIDE = False
CORS_ORIGIN_WHITELIST = ("null",)

if platform_name() == "Android":
    CORS_ORIGIN_ALLOW_ALL = True

try:
    CACHES = {"default": ENV.cache()}
    SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
except:
    CACHES = {
        "default": {
            "BACKEND": "diskcache.DjangoCache",
            "LOCATION": TEMP_PATH,
            "TIMEOUT": 3000,
            "OPTIONS": {"size_limit": 2**30},  # 1 gigabyte
        },
    }

SOCIALACCOUNT_ADAPTER = "pytigon_lib.schdjangoext.allauth.SocialAccountAdapter"
if DEBUG:
    ACCOUNT_DEFAULT_HTTP_PROTOCOL = "http"
    ACCOUNT_EMAIL_REQUIRED = False
else:
    ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"
    ACCOUNT_EMAIL_REQUIRED = True
    ACCOUNT_EMAIL_VERIFICATION = "mandatory"
    ACCOUNT_EMAIL_CONFIRMATION_COOLDOWN = 1
    ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
    ACCOUNT_USERNAME_REQUIRED = True

SOCIALACCOUNT_LOGIN_ON_GET = True

GRAPHENE = {
    "SCHEMA": "pytigon.schserw.schsys.schema.schema",
}

GRAPHENE_PUBLIC = False

EMAIL_BACKEND = "mailer.backend.DbBackend"
try:
    import dj_email_url

    email_config = dj_email_url.config()
    vars().update(email_config)
except:
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

# try:
#    from pytigon.schserw import *
# except:
#    pass
