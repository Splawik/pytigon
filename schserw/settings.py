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


APPSET_NAME = "Pytigon"

if sys.argv and (sys.argv[0] == 'manage.py' or '--debug' in sys.argv):
    DEBUG = True
    DB_DEBUG = True
else:
    DEBUG = True
    DB_DEBUG = True

TEMPLATE_DEBUG = DEBUG

SHOW_LOGIN_WIN = True

SERW_PATH = os.path.dirname(os.path.abspath(__file__))
LOCAL_SERW_PATH = SERW_PATH
ROOT_PATH = SERW_PATH + '/..'

sys.path.append(SERW_PATH)
sys.path.append(ROOT_PATH)
sys.path.append(ROOT_PATH + '/ext_lib')
sys.path.append(ROOT_PATH + '/schappdata/schplugins')

ADMINS = (('Slawomir Cholaj', 'slawomir.cholaj@gmail.com'), )
MANAGERS = ADMINS

AUTH_PROFILE_MODULE = 'schserw.schbase.Person'

TIME_ZONE = 'Europe/Warsaw'
LANGUAGE_CODE = 'pl'
USE_I18N = True
SITE_ID = 1
LANGUAGES = (('pl', 'Polish'), ('en', 'English'))
LOGIN_REDIRECT_URL = '/'

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

BASE_URL = 'http://127.0.0.1:81'
URL_POSTFIX = 'intranet'
_STATIC_ROOT = ROOT_PATH + '/static'
if len(URL_POSTFIX) > 0:
    _STATIC_URL = '/' + URL_POSTFIX + '/static/'
else:
    _STATIC_URL = '/static/'


MEDIA_ROOT = ROOT_PATH + '/app_sets'
if len(URL_POSTFIX) > 0:
    MEDIA_URL = '/' + URL_POSTFIX + '/site_media/'
else:
    MEDIA_URL = '/site_media/'
UPLOAD_PATH = '/home/publiczny/intranet/'
ADMIN_MEDIA_PREFIX = '/media/'

SECRET_KEY = 'anawa'

ROOT_URLCONF = 'schserw.urls'

TEMPLATE_LOADERS = (
                    'schlib.schdjangoext.python_style_template_loader.Loader',
                    'schlib.schdjangoext.python_style_template_loader.FSLoader',
                    #'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                    )

INTERNAL_IPS = ('127.0.0.1','127.0.0.2','127.0.0.3', 'localhost')

MIDDLEWARE_CLASSES = (
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'schserw.schmiddleware.schpost.LoginToSession',
    'django.contrib.auth.middleware.RemoteUserMiddleware',
    'schserw.schmiddleware.schpost.ViewPost',
    'schserw.schmiddleware.schpost.ViewRequests',
    #'schserw.schmiddleware.schpost.BeautyHtml',
    )

TEMPLATE_CONTEXT_PROCESSORS = [
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'schserw.schsys.context_processors.sch_standard',
    'schserw.schsys.context_processors.sch_html_widget',
    ]

TEMPLATE_DIRS = [ROOT_PATH + '/templates']

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.messages',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    #'registration',
    'django.contrib.admin',
    #'django.contrib.admin.apps.AdminConfig',
#    'django.contrib.databrowse',
    'mptt',
    'schserw.schsys',
#    'schserw.schwiki',
    'django.contrib.staticfiles',
    'crispy_forms',
    #'debug_toolbar',
    #'django_extensions',
    ]

HIDE_APPS = []

LOGGING = {'version': 1, 'handlers': {'console': {'level': 'DEBUG', 'class': 'logging.StreamHandler'}},
           'loggers': {'django.db.backends': {'level': 'DEBUG', 'handers': ['console']}}
}

LOCALE_PATHS = [
    SERW_PATH + "/locale",
]

STATICFILES_DIRS  = [ _STATIC_ROOT, ]

ATOMIC_REQUESTS = True

ALLOWED_HOSTS = ['127.0.0.1', '127.0.0.2', '127.0.0.3', 'localhost', 'localhost:8080']

#EMAIL_HOST = 'gmail.com'
#EMAIL_HOST_USER = 'slawomir.cholaj'
#EMAIL_HOST_PASSWORD = '----'
#DEFAULT_FROM_EMAIL = 'slawomir.cholaj@gmail.pl'
#SERVER_EMAIL = 'slawomir.cholaj@gmail.pl'
#EMAIL_USE_TLS = True

PYTHON_INTERPRETER = 'python'
PYTHON_CONSOLE = 'ipython --classic'


CRISPY_TEMPLATE_PACK = 'bootstrap3'
