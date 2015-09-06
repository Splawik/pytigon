#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import six
from schlib.schdjangoext.django_init import get_app_config

_lp  = os.path.dirname(os.path.abspath(__file__))
_rp = _lp+"/../.."

sys.path.append(_lp)
sys.path.append(_rp)

try:
    from schserw.settings_local import *
except:
    from schserw.settings import *

from apps import APPS

try:
    from global_db_settings import setup_databases
except:
    setup_databases = None

APPSET_TITLE = "Wiki"
APPSET_NAME = "_schwiki"

THEMES = ['auto', 'auto', 'auto']

LOCAL_SERW_PATH = _lp
LOCAL_ROOT_PATH = _lp+"/.."
ROOT_PATH = _rp

URL_POSTFIX = ''

if len(URL_POSTFIX) > 0:
    STATIC_URL = '/' + URL_POSTFIX + '/static/'
else:
    STATIC_URL = '/static/'

if len(URL_POSTFIX) > 0:
    MEDIA_URL = '/' + URL_POSTFIX + '/site_media/'
else:
    MEDIA_URL = '/site_media/'

sys.path.append(LOCAL_ROOT_PATH)

MEDIA_ROOT = ROOT_PATH + '/app_pack/' + APPSET_NAME +"/media"

for app in APPS:
    if not app in INSTALLED_APPS:
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
