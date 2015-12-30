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
import platform

APPSET_NAME = "Pytigon"

if sys.argv and (sys.argv[0] == 'manage.py' or '--debug' in sys.argv):
    DEBUG = True
    DB_DEBUG = True
else:
    DEBUG = False
    DB_DEBUG = False

TEMPLATE_DEBUG = DEBUG

SHOW_LOGIN_WIN = True

SERW_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = SERW_PATH + '/..'

sys.path.append(SERW_PATH)
sys.path.append(ROOT_PATH)
sys.path.append(ROOT_PATH + '/ext_lib')
sys.path.append(ROOT_PATH + '/schappdata/schplugins')

ADMINS = []
MANAGERS = ADMINS

TIME_ZONE = 'Europe/Warsaw'
LANGUAGE_CODE = 'pl'
USE_I18N = True
SITE_ID = 1
LANGUAGES = (('pl', 'Polish'), ('en', 'English'))
LOGIN_REDIRECT_URL = '/'

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

BASE_URL = 'http://127.0.0.1:81'

URL_ROOT_FOLDER = ''
STATIC_URL = '/static/'
MEDIA_URL = '/site_media/'

if DEBUG:
    STATICFILES_DIRS  = [ROOT_PATH + '/static', ]
    #STATIC_ROOT = ROOT_PATH + '/static'
else:
    STATICFILES_DIRS  = [ROOT_PATH + '/static', ]
    #STATIC_ROOT = ROOT_PATH + '/static'

MEDIA_ROOT =  ROOT_PATH + '/app_pack'

UPLOAD_PATH = MEDIA_ROOT + '/upload/'

ADMIN_MEDIA_PREFIX = '/media/'

SECRET_KEY = 'anawa'

ROOT_URLCONF = 'schserw.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            ROOT_PATH + '/templates',
            ROOT_PATH + '/schappdata/schplugins',
            # insert your TEMPLATE_DIRS here
        ],
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:

                'schserw.schsys.context_processors.sch_standard',
                'schserw.schsys.context_processors.sch_html_widget',

                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.request',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.request'
            ],
            'loaders': [
                # insert your TEMPLATE_LOADERS here
                'schlib.schdjangoext.python_style_template_loader.Loader',
                'schlib.schdjangoext.python_style_template_loader.FSLoader',
                'django.template.loaders.app_directories.Loader',
            ]
        },
    },
]


MIDDLEWARE_CLASSES = (
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.RemoteUserMiddleware',
    'schserw.schmiddleware.schpost.LoginToSession',
    #'schserw.schmiddleware.schpost.ViewPost',
    #'schserw.schmiddleware.schpost.ViewRequests',
    #'schserw.schmiddleware.schpost.BeautyHtml',
    )

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.messages',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'bootstrap_admin',
    'django.contrib.admin',
    'schserw.schsys',
    'django.contrib.staticfiles',
    'crispy_forms',
    'django_select2',
    ]

HIDE_APPS = []

LOGGING = {
    'version': 1,
    'handlers': {'console': {'level': 'DEBUG', 'class': 'logging.StreamHandler'}},
    'loggers': {'django.db.backends': {'level': 'DEBUG', 'handers': ['console']}}
}

LOCALE_PATHS = [
    SERW_PATH + "/locale",
]


ATOMIC_REQUESTS = True

INTERNAL_IPS = ('127.0.0.1','127.0.0.2','127.0.0.3', 'localhost')

ALLOWED_HOSTS = ['*',]

PYTHON_INTERPRETER = 'python3'
PYTHON_CONSOLE = 'python3'

CRISPY_TEMPLATE_PACK = 'bootstrap3'

BOOTSTRAP_ADMIN_SIDEBAR_MENU = True

if platform.system() == "Linux":
    NODEJS = 'nodejs'
else:
    NODEJS  = ROOT_PATH + '/ext_prg/node.exe'

RAPYD = ROOT_PATH + '/ext_prg/rapydscript/bin/rapydscript'

AUTO_RENDER_SELECT2_STATICS = False

try:
    from schserw.settings_local import *
except:
    pass
