#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import six
from urllib.parse import urlparse
from schlib.schdjangoext.django_init import get_app_config

_lp  = os.path.dirname(os.path.abspath(__file__))
_rp = _lp+"/../.."

sys.path.append(_lp)
sys.path.append(_rp)

from schserw.settings import *

from apps import APPS

try:
    from global_db_settings import setup_databases
except:
    setup_databases = None

APPSET_TITLE = "Pytigon web client"
APPSET_NAME = "_schremote"

THEMES = ['tablet_modern', 'tablet_modern', 'tablet_traditional']

LOCAL_ROOT_PATH = os.path.join(_lp, "..")
ROOT_PATH = _rp
sys.path.append(LOCAL_ROOT_PATH)

if not DEBUG:
    URL_ROOT_FOLDER='_schremote'

    STATIC_URL = '/'+URL_ROOT_FOLDER+'/static/'
    MEDIA_URL = '/'+URL_ROOT_FOLDER+'/site_media/'

MEDIA_ROOT =  os.path.join(_lp,  'media')

PACKS = []

for app in APPS:
    if '.' in app:
        pack = app.split('.')[0]
        if not pack in PACKS:
            PACKS.append(pack)
            sys.path.append(os.path.join(LOCAL_ROOT_PATH, pack))

    if not app in [ x if type(x)==str else x.label for x in INSTALLED_APPS]:
        INSTALLED_APPS.append(get_app_config(app))
        aa = app.split('.')
        TEMPLATES[0]['DIRS'].append(os.path.dirname(os.path.abspath(__file__))+"/../"+aa[0]+"/templates")
        if len(aa)==2:
            pp = os.path.dirname(os.path.abspath(__file__))+"/../"+aa[0]
            sys.path.append(pp)
            LOCALE_PATHS.append(os.path.dirname(os.path.abspath(__file__))+"/../"+aa[0]+"/locale")
        else:
            LOCALE_PATHS.append(os.path.dirname(os.path.abspath(__file__))+"/locale")

TEMPLATES[0]['DIRS'].insert(0, os.path.dirname(os.path.abspath(__file__))+"/templates")

p = os.path.expanduser("~")
if isinstance(p, six.text_type):
    _NAME = os.path.join(p, ".pytigon/%s/%s.db" % (APPSET_NAME, APPSET_NAME))
else:
    _NAME = os.path.join(p, ".pytigon/%s/%s.db" % (APPSET_NAME,APPSET_NAME)).decode("cp1250")

DATABASES = {
    'default':  {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': _NAME,
    },
}

if setup_databases:
    db_setup = setup_databases(APPSET_NAME)
    db_local = DATABASES['default']

    DATABASES = db_setup[0]
    DATABASES['local'] = db_local

    if db_setup[1]:
        AUTHENTICATION_BACKENDS = db_setup[1]
else:
    if "DATABASE_URL" in os.environ:
        db_url = os.environ["DATABASE_URL"]
        db_local = DATABASES['default']
        url = urlparse(db_url)
        scheme = url.scheme
        if scheme=='postgres':
            scheme='postgresql'
        database=url.path[1:]
        user=url.username
        password=url.password
        host=url.hostname
        port=url.port
        DATABASES = {
            'default':  {
                'ENGINE': 'django.db.backends.'+scheme,
                'NAME': database,
                'USER': user,
                'PASSWORD': password,
                'HOST': host,
                'PORT': port,
            },
        }
        DATABASES['local'] = db_local
try:
    from settings_app_local import *
except:
    pass