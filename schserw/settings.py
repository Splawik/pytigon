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

#Pytigon - wxpython and django application framework

#author: "Slawomir Cholaj (slawomir.cholaj@gmail.com)"
#copyright: "Copyright (C) ????/2012 Slawomir Cholaj"
#license: "LGPL 3.0"
#version: "0.1a"

import os
import sys
from fs.mountfs import MountFS
from fs.osfs import OSFS
from django.conf import settings
from os import environ
from .main_paths import get_main_paths

APPSET_NAME = "_schall"
GEN_TIME = '0000.00.00 00:00:00'

if (sys.argv and ((sys.argv[0].endswith('manage.py') and 'runserver' in sys.argv) or '--debug' in sys.argv)) \
        or 'PYTIGON_DEBUG' in environ:
    DEBUG = True
    DB_DEBUG = True
    PRODUCTION_VERSION = False
else:
    DEBUG = False
    DB_DEBUG = False
    PRODUCTION_VERSION = True

if sys.argv and sys.argv[0].endswith('pytigon'):
    PRODUCTION_VERSION = False
    DEBUG = True

SHOW_LOGIN_WIN = True

paths = get_main_paths()

SERW_PATH = paths['SERW_PATH']
ROOT_PATH = paths['ROOT_PATH']
DATA_PATH = paths['DATA_PATH']
LOG_PATH = paths['LOG_PATH']
TEMP_PATH = paths['TEMP_PATH']
APP_PACK_PATH = paths['APP_PACK_PATH']

ADMINS = []
MANAGERS = ADMINS

TIME_ZONE = 'Europe/Warsaw'
LANGUAGE_CODE = 'pl'
USE_I18N = True
SITE_ID = 1
LANGUAGES = [['en', 'English'], ['pl', 'Polish']]
LOGIN_REDIRECT_URL = '/'
TEST_RUNNER = 'django.test.runner.DiscoverRunner'


BASE_URL = 'http://127.0.0.1:81'

URL_ROOT_FOLDER = ''
STATIC_URL = '/static/'
MEDIA_URL = '/site_media/'

APPEND_SLASH = False

STATICFILES_DIRS  = []
STATIC_ROOT = ROOT_PATH + '/static'

from schlib.schtools.platform_info import platform_name

#if platform_name()=='Android':
#    STATIC_ROOT = STATICFILES_DIRS[0]

if platform_name()=='Android' or 'PYTIGON_APP_IMAGE' in environ:
    STATIC_APP_ROOT = os.path.join(os.path.join(os.path.join(DATA_PATH, '..'), 'pytigon'), 'app_static')
else:
    #STATIC_APP_ROOT = STATICFILES_DIRS[0] + "/app"
    STATIC_APP_ROOT = STATIC_ROOT + "/app"

MEDIA_ROOT = os.path.join(os.path.join(DATA_PATH, APPSET_NAME), 'media')
UPLOAD_PATH = MEDIA_ROOT

ADMIN_MEDIA_PREFIX = '/media/'

SECRET_KEY = 'anawa'

ROOT_URLCONF = 'schserw.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            ROOT_PATH + '/templates',
            ROOT_PATH + '/schappdata/schplugins',
        ],
        'OPTIONS': {
            'context_processors': [
                'schserw.schsys.context_processors.sch_standard',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.request',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request'
            ],
            'loaders': [
                'schlib.schdjangoext.python_style_template_loader.Loader',
                'schlib.schdjangoext.python_style_template_loader.FSLoader',
                'django.template.loaders.app_directories.Loader',
            ],
            'builtins': ['schserw.schsys.templatetags.defexfiltry'],
            'debug': DEBUG,

        },
    },
]

FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

if 'EMBEDED_DJANGO_SERVER' in environ:
    MIDDLEWARE = [
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.locale.LocaleMiddleware',
        'schserw.schmiddleware.csrf.DisableCSRF',
    ]
else:
    MIDDLEWARE = [
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.locale.LocaleMiddleware',
        'django.contrib.auth.middleware.RemoteUserMiddleware',
    ]

MIDDLEWARE.insert(0, 'whitenoise.middleware.WhiteNoiseMiddleware')

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.messages',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.forms',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'django_select2',
    'bootstrap4',
    'corsheaders',
    'schserw.schsys',
]

if not 'PYTIGON_WITHOUT_CHANNELS' in os.environ  and platform_name()!='Android':
    INSTALLED_APPS.append('channels')

HIDE_APPS = []

APP_PACKS = []

if PRODUCTION_VERSION:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'standard': {
                'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
                'datefmt' : "%Y-%m-%d %H:%M:%S"
            },
        },
        'handlers': {
            'logfile': {
                'level': 'INFO',
                'class':'logging.handlers.RotatingFileHandler',
                'filename': LOG_PATH + "/pytigon.log",
                'maxBytes': 50000,
                'backupCount': 2,
                'formatter': 'standard',
            },
            'errorlogfile': {
                'level': 'WARNING',
                'class':'logging.handlers.RotatingFileHandler',
                'filename': LOG_PATH + "/pytigon_err.log",
                'maxBytes': 50000,
                'backupCount': 2,
                'formatter': 'standard',
            },
        },
        'loggers': {
            'django': {
                'handlers':['logfile', 'errorlogfile'],
                'level':'INFO',
                'propagate': True,
            },
            'daphne': {
                'handlers': ['logfile', 'errorlogfile'],
                'level': 'INFO',
                'propagate': True,
            },
            'httpclient': {
                  'handlers': ['logfile', 'errorlogfile'],
                  'level': 'INFO',
                  'propagate': True,
              },
            'pytigon': {
                'handlers': ['logfile', 'errorlogfile'],
                'level': 'INFO',
                'propagate': True,
            },
            'pytigon_task': {
                'handlers': ['logfile', 'errorlogfile'],
                'level': 'INFO',
                'propagate': True,
            },
        }
    }

LOCALE_PATHS = [
    SERW_PATH + "/locale",
]

#CSRF_USE_SESSIONS = True

ATOMIC_REQUESTS = True

INTERNAL_IPS = ('127.0.0.1','127.0.0.2','127.0.0.3', 'localhost')

ALLOWED_HOSTS = ['*',]

PYTHON_INTERPRETER = sys.executable
PYTHON_CONSOLE = sys.executable

BOOTSTRAP_ADMIN_SIDEBAR_MENU = True
BOOTSTRAP_BUTTON_SIZE_CLASS = ""

#SEARCH_PATH = "/schwiki/%s/search/"

AUTO_RENDER_SELECT2_STATICS = False

ASGI_APPLICATION = "schserw.routing.application"

#if  PRODUCTION_VERSION and platform_name()!='Android':
#    CHANNEL_LAYERS = {
#        "default": {
#            "BACKEND": "channels_redis.core.RedisChannelLayer",
#            #"ROUTING": "schserw.routing.channel_routing",
#            "CONFIG": {
#                "hosts": [("127.0.0.1", 6379)],
#            },
#        },
#    }

DEFAULT_FILE_STORAGE = 'django_storage.FSStorage'

def DEFAULT_FILE_STORAGE_FS():
    _m = MountFS()
    _m.mount('pytigon', OSFS(settings.ROOT_PATH))
    _m.mount('static', OSFS(settings.STATIC_ROOT))
    _m.mount('app', OSFS(settings.LOCAL_ROOT_PATH))
    _m.mount('data', OSFS(settings.DATA_PATH))
    try:
        _m.mount('temp', OSFS(settings.TEMP_PATH))
    except:
        pass
    try:
        _m.mount('media', OSFS(settings.MEDIA_ROOT))
    except:
        pass
    try:
        _m.mount('upload', OSFS(settings.UPLOAD_PATH))
        _m.mount('filer_public', OSFS(os.path.join(settings.UPLOAD_PATH,"filer_public")))
        _m.mount('filer_private', OSFS(os.path.join(settings.UPLOAD_PATH,"filer_private")))
        _m.mount('filer_public_thumbnails', OSFS(os.path.join(settings.UPLOAD_PATH,"filer_public_thumbnails")))
        _m.mount('filer_private_thumbnails', OSFS(os.path.join(settings.UPLOAD_PATH,"filer_private_thumbnails")))
    except:
        pass

    if sys.argv and sys.argv[0].endswith('pytigon'):
        if platform_name() == 'Windows':
            _m.mount('osfs', OSFS("c:\\"))
        else:
            _m.mount('osfs', OSFS("/"))
    return _m

DATA_UPLOAD_MAX_MEMORY_SIZE = 26214400
OFFLINE_SUPPORT = False

CORS_ORIGIN_WHITELIST = (
    'null',
)

if platform_name()=='Android':
   CORS_ORIGIN_ALLOW_ALL = True

try:
    from schserw.settings_local import *
except:
    pass
