# -*- coding: utf-8 -*-
import os
import sys
from urllib.parse import urlparse

_lp = os.path.dirname(os.path.abspath(__file__))

if 'PYTIGON_ROOT_PATH' in os.environ:
    _rp = os.environ['PYTIGON_ROOT_PATH']
else:
    _rp = os.path.abspath(os.path.join(_lp, "..", ".."))

if not _lp in sys.path: sys.path.insert(0,_lp)
if not _rp in sys.path: sys.path.insert(0,_rp)

from schlib import init_paths
init_paths()

from schlib.schdjangoext.django_init import get_app_config
from schlib.schtools.platform_info import platform_name

from schserw.settings import *

from apps import APPS, PUBLIC, MAIN_APP_PACK

try:
    from global_db_settings import setup_databases
except:
    setup_databases = None

APPSET_TITLE = "Setup application"
APPSET_NAME = "schsetup"
MEDIA_ROOT = os.path.join(os.path.join(DATA_PATH, APPSET_NAME), 'media')
UPLOAD_PATH = MEDIA_ROOT

THEMES = ['tablet_modern', 'tablet_modern', 'auto']

LOCAL_ROOT_PATH = os.path.abspath(os.path.join(_lp, ".."))
ROOT_PATH = _rp
URL_ROOT_PREFIX = ""
if not LOCAL_ROOT_PATH in sys.path: sys.path.append(LOCAL_ROOT_PATH)

if PRODUCTION_VERSION and platform_name()!='Android' and not 'main.py' in sys.argv[0] \
        and not 'pytigon' in sys.argv[0] and not 'pytigon_task.py' in sys.argv[0] and not MAIN_APP_PACK:
    URL_ROOT_FOLDER='schsetup'
    URL_ROOT_PREFIX = URL_ROOT_FOLDER+"/"
    STATIC_URL = '/'+URL_ROOT_FOLDER+'/static/'
    MEDIA_URL = '/'+URL_ROOT_FOLDER+'/site_media/'

from schlib.schtools.install_init import init
init(APPSET_NAME, ROOT_PATH, DATA_PATH, APP_PACK_PATH, STATIC_APP_ROOT, [MEDIA_ROOT, UPLOAD_PATH])

START_PAGE = 'None'
SHOW_LOGIN_WIN = True
PACKS = []

for app in APPS:
    if '.' in app:
        pack = app.split('.')[0]
        if not pack in PACKS:
            PACKS.append(pack)
            p1 = os.path.join(LOCAL_ROOT_PATH, pack)
            if not p1 in sys.path:  sys.path.append(p1)

    if not app in [ x if type(x)==str else x.label for x in INSTALLED_APPS]:
        INSTALLED_APPS.append(get_app_config(app))
        aa = app.split('.')
        TEMPLATES[0]['DIRS'].append(os.path.dirname(os.path.abspath(__file__))+"/../"+aa[0]+"/templates")
        if len(aa)==2:
            pp = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", aa[0]))
            if not pp in sys.path: sys.path.append(pp)
            LOCALE_PATHS.append(os.path.join(pp, "locale"))
        else:
            LOCALE_PATHS.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "locale"))

TEMPLATES[0]['DIRS'].insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates"))
INSTALLED_APPS.append('easy_thumbnails')
INSTALLED_APPS.append('filer')
INSTALLED_APPS.append('mptt')

INSTALLED_APPS.append('explorer')

THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    #'easy_thumbnails.processors.scale_and_crop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters',
)

FILER_DEBUG = True

EXPLORER_CONNECTIONS = { 'Default': 'default' } 
EXPLORER_DEFAULT_CONNECTION = 'default'
TEMPLATES[0]['DIRS'].insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "plugins"))

_NAME = os.path.join(DATA_PATH, "%s/%s.db" % (APPSET_NAME, APPSET_NAME))

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


CHANNELS_URL_TAB = [ 
 ("^"+URL_ROOT_PREFIX+r"schcommander/shell/socket.io/$", 'schcommander.consumers.ShellConsumer'),
]


try:
    from settings_app_local import *
except:
    pass

GEN_TIME = '2018.12.23 11:39:22'

