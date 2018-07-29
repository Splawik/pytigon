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
import tempfile

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

SHOW_LOGIN_WIN = True

SERW_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = SERW_PATH + '/..'

sys.path.append(SERW_PATH)
sys.path.append(ROOT_PATH)
sys.path.append(ROOT_PATH + '/ext_lib')
sys.path.append(ROOT_PATH + '/schappdata/schplugins')

from schlib.schtools.platform_info import platform_name

if platform_name()=='Android':
    p1 = p2 = None
    if 'SECONDARY_STORAGE' in environ:
        p1 = os.path.join(environ['SECONDARY_STORAGE'], "pytigon_data")
    if 'EXTERNAL_STORAGE' in environ:
        p2 = os.path.join(environ['EXTERNAL_STORAGE'], "pytigon_data")
    if p1:
        if os.path.exists(p2):
            DATA_PATH = p2
        else:
            DATA_PATH = p1
    else:
        DATA_PATH = p2
    LOG_PATH = DATA_PATH
else:
    if ROOT_PATH.startswith('/var/www'):
        DATA_PATH = os.path.join("/home/www-data/.pytigon")
        LOG_PATH = "/var/log"
    else:
        DATA_PATH = os.path.join(os.path.expanduser("~"), ".pytigon")
        LOG_PATH = DATA_PATH


TEMP_PATH = tempfile.gettempdir()

if platform_name()=='Android' or 'PYTIGON_APP_IMAGE' in environ:
    APP_PACK_PATH = os.path.join(os.path.join(os.path.join(DATA_PATH, '..'), 'pytigon'), 'app_pack')
else:
    APP_PACK_PATH = os.path.join(ROOT_PATH, 'app_pack')

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

STATICFILES_DIRS  = [ROOT_PATH + '/static', ]

if platform_name()=='Android':
    STATIC_ROOT = STATICFILES_DIRS[0]

MEDIA_ROOT = os.path.join(os.path.join(DATA_PATH, APPSET_NAME), 'media')
UPLOAD_PATH = os.path.join(os.path.join(DATA_PATH, APPSET_NAME), 'upload')

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

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.RemoteUserMiddleware',
    'schserw.schmiddleware.schpost.LoginToSession',
    #'schserw.schmiddleware.schpost.ViewPost',
    #'schserw.schmiddleware.schpost.ViewRequests',
    #'schserw.schmiddleware.schpost.BeautyHtml',
]

MIDDLEWARE.append('whitenoise.middleware.WhiteNoiseMiddleware')

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.messages',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.forms',
    'django.contrib.staticfiles',
    'django_select2',
    'bootstrap4',
    'corsheaders',
    'schserw.schsys',
]

if platform_name()!='Android':
    INSTALLED_APPS.append('channels')


HIDE_APPS = []

APP_PACKS = []

#LOGGING = {
#    'version': 1,
#    'handlers': {'console': {'level': 'DEBUG', 'class': 'logging.StreamHandler'}},
#    'loggers': {'django.db.backends': {'level': 'DEBUG', 'handers': ['console']}}
#}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'logging.NullHandler',
        },
        'logfile': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': LOG_PATH + "/pytigon.log",
            'maxBytes': 50000,
            'backupCount': 2,
            'formatter': 'standard',
        },
        'console':{
            'level':'INFO',
            'class':'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django': {
            'handlers':['console'],
            'propagate': True,
            'level':'WARN',
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'pytogion': {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
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

if PRODUCTION_VERSION and platform_name()!='Android':
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            #"ROUTING": "schserw.routing.channel_routing",
            "CONFIG": {
                "hosts": [("127.0.0.1", 6379)],
            },
        },
    }

DEFAULT_FILE_STORAGE = 'django_storage.FSStorage'

def DEFAULT_FILE_STORAGE_FS():
    _m = MountFS()
    _m.mount('pytigon', OSFS(settings.ROOT_PATH))
    _m.mount('static', OSFS(settings.STATICFILES_DIRS[0]))
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
    except:
        pass
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
