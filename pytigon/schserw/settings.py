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
import datetime
from fs.mountfs import MountFS
from fs.multifs import MultiFS
from fs.osfs import OSFS
from django.conf import settings
from os import environ
from pytigon_lib.schtools.main_paths import get_main_paths, get_prj_name
import django_cache_url

prj_name = get_prj_name()
if not prj_name:
    prj_name = "_schall"

GEN_TIME = "0000.00.00 00:00:00"

if (
    sys.argv
    and (
        (sys.argv[0].endswith("manage.py") and "runserver" in sys.argv)
        or "--debug" in sys.argv
    )
) or "PYTIGON_DEBUG" in environ:
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
STATICFILES_DIR = paths["STATICFILES_DIR"]
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
STATIC_URL = "/static/"
MEDIA_URL = "/site_media/"
MEDIA_URL_PROTECTED = "/protected_site_media/"

APPEND_SLASH = False

STATICFILES_DIRS = []
if STATICFILES_DIR != STATIC_ROOT:
    STATICFILES_DIRS.append(STATICFILES_DIR)

from pytigon_lib.schtools.platform_info import platform_name

MEDIA_ROOT = os.path.join(os.path.join(DATA_PATH, prj_name), "media")
MEDIA_ROOT_PROTECTED = os.path.join(os.path.join(DATA_PATH, prj_name), "protected_media")
UPLOAD_PATH = os.path.join(MEDIA_ROOT, "upload")
UPLOAD_PATH_PROTECTED = os.path.join(MEDIA_ROOT, "protected_upload")

ADMIN_MEDIA_PREFIX = "/media/"

SECRET_KEY = "anawa"

ROOT_URLCONF = "pytigon.schserw.urls"

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "pytigon_lib.schdjangoext.django_settings.AppPackDirectoriesFinder",
    # other finders..
    "compressor.finders.CompressorFinder",
)

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
                "pytigon_lib.schdjangoext.python_style_template_loader.FSLoader",
                "django.template.loaders.app_directories.Loader",
            ],
            "builtins": ["pytigon.schserw.schsys.templatetags.defexfiltry"],
            "debug": DEBUG,
        },
    }
]

FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

if "EMBEDED_DJANGO_SERVER" in environ:
    MIDDLEWARE = [
        "django.middleware.common.CommonMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.locale.LocaleMiddleware",
        "pytigon.schserw.schmiddleware.csrf.DisableCSRF",
        "pytigon.schserw.schmiddleware.schjwt.JWTUserMiddleware",
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
        "pytigon.schserw.schmiddleware.schjwt.JWTUserMiddleware",
    ]

# if DEBUG:
#    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')


AUTHENTICATION_BACKENDS = (
    "graphql_jwt.backends.JSONWebTokenBackend",
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.messages",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.admin",
    "django.contrib.sites",
    "django.forms",
    "django.contrib.staticfiles",
    "django_select2",
    "mptt",
    "bootstrap4",
    "corsheaders",
    "pytigon.schserw.schsys",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "graphene_django",
    "django_filters",
    "compressor",
    "django_q",
    "log_viewer",
]

if PLATFORM_TYPE != "webserver":
    MIDDLEWARE.insert(
        0, "pytigon.schserw.schmiddleware.whitenoise2.WhiteNoiseMiddleware2"
    )
    INSTALLED_APPS.append("whitenoise.runserver_nostatic")

# if DEBUG:
#    INSTALLED_APPS.append("debug_toolbar")

if (
    not "PYTIGON_WITHOUT_CHANNELS" in os.environ
    and platform_name() != "Android"
    and platform_name() != "Emscripten"
):
    INSTALLED_APPS.append("channels")

DEFAULT_AUTO_FIELD  = 'django.db.models.AutoField'

CHANNELS_URL_TAB = []

HIDE_APPS = []

PRJS = []

if PRODUCTION_VERSION:
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
                "level": "INFO",
                "class": "logging.FileHandler",
                "filename": LOG_PATH + "/pytigon.log",
                #"maxBytes": 50000,
                #"backupCount": 2,
                "formatter": "standard",
            },
            "errorlogfile": {
                "level": "WARNING",
                "class": "logging.FileHandler",
                "filename": LOG_PATH + "/pytigon-err.log",
                #"maxBytes": 50000,
                #"backupCount": 2,
                "formatter": "standard",
            },
        },
        "loggers": {
            "django": {
                "handlers": ["logfile", "errorlogfile"],
                "level": "INFO",
                "propagate": True,
            },
            "daphne": {
                "handlers": ["logfile", "errorlogfile"],
                "level": "INFO",
                "propagate": True,
            },
            "httpclient": {
                "handlers": ["logfile", "errorlogfile"],
                "level": "INFO",
                "propagate": True,
            },
            "pytigon": {
                "handlers": ["logfile", "errorlogfile"],
                "level": "INFO",
                "propagate": True,
            },
            "pytigon_task": {
                "handlers": ["logfile", "errorlogfile"],
                "level": "INFO",
                "propagate": True,
            },
        },
    }

    if 'LOGS_TO_DOCKER' in environ and environ['LOGS_TO_DOCKER']:
        LOGGING["handlers"] = {
            "logfile": {
                "level": "INFO",
                "class": "logging.StreamHandler",
                "formatter": "standard",
            },
            "errorlogfile": {
                "level": "WARNING",
                "class": "logging.StreamHandler",
                "formatter": "standard",
            },
        }
    elif 'PYTIGON_TASK' in environ:
        LOGGING["handlers"]["logfile"]["filename"] = LOGGING["handlers"]["logfile"]["filename"].replace('.log',
                                                                                                        '-task.log')
        LOGGING["handlers"]["errorlogfile"]["filename"] = LOGGING["handlers"]["errorlogfile"]["filename"].replace(
            '.log', '_task.log')

LOG_VIEWER_FILES = ['pytigon.log', 'pytigon-err.log','pytigon-task.log','pytigon-err-task.log',]
LOG_VIEWER_FILES_DIR = LOG_PATH
LOG_VIEWER_PATTERNS = ['[',]

LOCALE_PATHS = [SERW_PATH + "/locale"]

# CSRF_USE_SESSIONS = True

ATOMIC_REQUESTS = True

INTERNAL_IPS = ("127.0.0.1", "127.0.0.2", "127.0.0.3", "localhost")

ALLOWED_HOSTS = ["*"]

PYTHON_INTERPRETER = sys.executable
PYTHON_CONSOLE = sys.executable

BOOTSTRAP4 = {"use_custom_controls": False}

BOOTSTRAP_ADMIN_SIDEBAR_MENU = True
BOOTSTRAP_BUTTON_SIZE_CLASS = ""
BOOTSTRAP_BUTTON_SIZE_CLASS = ""

# SEARCH_PATH = "/schwiki/%s/search/"

AUTO_RENDER_SELECT2_STATICS = False

ASGI_APPLICATION = "pytigon.schserw.routing.application"

if PLATFORM_TYPE == "webserver":
    if "CHANNELS_REDIS" in environ:
        CHANNELS_REDIS_SERVER, CHANNELS_REDIS_PORT = (
            environ["CHANNELS_REDIS"].split(":") + ["6379"]
        )[:2]
    else:
        CHANNELS_REDIS_SERVER = "127.0.0.1"
        CHANNELS_REDIS_PORT = "6379"

    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            # "ROUTING": "schserw.routing.channel_routing",
            "CONFIG": {
                "hosts": [(CHANNELS_REDIS_SERVER, int(CHANNELS_REDIS_PORT))]
            },
        }
    }
else:
    CHANNEL_LAYERS = {"default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}}

DEFAULT_FILE_STORAGE = "pytigon.ext_lib.django_storage.FSStorage"

if PLATFORM_TYPE == 'webserver':
    COMPRESS_ENABLED = True
else:
    COMPRESS_ENABLED = False
COMPRESS_STORAGE = "compressor.storage.GzipCompressorFileStorage"

STATIC_FS = None

def DEFAULT_FILE_STORAGE_FS():
    global STATIC_FS
    _m = MountFS()
    _m.mount("pytigon", OSFS(settings.ROOT_PATH))
    STATIC_FS = MultiFS()
    STATIC_FS.add_fs("static_main", OSFS(settings.STATIC_ROOT))
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

CORS_ORIGIN_WHITELIST = ("null",)

if platform_name() == "Android":
    CORS_ORIGIN_ALLOW_ALL = True

CACHE_URL = os.environ.setdefault("CACHE_URL", "")
if CACHE_URL:
    CACHES = {"default": django_cache_url.config()}
    SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
else:
    #CACHES = { "default": { 'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache' } }
    CACHES = {
        'default': {
            'BACKEND': 'diskcache.DjangoCache',
            'LOCATION': TEMP_PATH,
            'TIMEOUT': 300,
            'OPTIONS': {
                'size_limit': 2 ** 30   # 1 gigabyte
            },
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

GRAPHENE = {
    "SCHEMA": "pytigon.schserw.schsys.schema.schema",
    "MIDDLEWARE": ["graphql_jwt.middleware.JSONWebTokenMiddleware"],
}

GRAPHQL_JWT = {
    "JWT_VERIFY_EXPIRATION": False,
    #"JWT_EXPIRATION_DELTA": datetime.timedelta(minutes=5),
    #"JWT_REFRESH_EXPIRATION_DELTA": datetime.timedelta(days=7),
}

GRAPHENE_PUBLIC = False

try:
    import dj_email_url

    email_config = dj_email_url.config()
    vars().update(email_config)
except:
    pass

if "EMBEDED_DJANGO_SERVER" in environ:
    Q_CLUSTER = {
        'name': 'DjangORM',
        'workers': 1,
        'timeout': 360,
        'retry': 480,
        'queue_limit': 10,
        'bulk': 10,
        'orm': 'default'
    }
else:
    Q_CLUSTER = {
        'name': 'DjangORM',
        'workers': 2,
        'timeout': 360,
        'retry': 480,
        'queue_limit': 50,
        'bulk': 10,
        'orm': 'default'
    }

try:
    from pytigon.schserw import *
except:
    pass
