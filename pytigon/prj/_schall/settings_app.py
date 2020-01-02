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

from pytigon_lib import init_paths
init_paths()

from pytigon_lib.schdjangoext.django_init import get_app_config
from pytigon_lib.schtools.platform_info import platform_name

from pytigon.schserw.settings import *

from apps import APPS, PUBLIC, MAIN_PRJ

try:
    from global_db_settings import setup_databases
except:
    setup_databases = None

PRJ_TITLE = "Pytigon"
PRJ_NAME = "_schall"
MEDIA_ROOT = os.path.join(os.path.join(DATA_PATH, PRJ_NAME), 'media')
UPLOAD_PATH = os.path.join(MEDIA_ROOT, "upload")

THEMES = ['tablet_modern', 'tablet_modern', 'smartfon_standard']

LOCAL_ROOT_PATH = os.path.abspath(os.path.join(_lp, ".."))
ROOT_PATH = _rp
URL_ROOT_PREFIX = ""
if not LOCAL_ROOT_PATH in sys.path: sys.path.append(LOCAL_ROOT_PATH)

if PRODUCTION_VERSION and platform_name()!='Android' and not 'main.py' in sys.argv[0] and not 'pytigon' in sys.argv[0]\
        and not 'ptig' in sys.argv[0] and not 'pytigon_task.py' in sys.argv[0] and not MAIN_PRJ:
    URL_ROOT_FOLDER='_schall'
    URL_ROOT_PREFIX = URL_ROOT_FOLDER+"/"
    STATIC_URL = '/'+URL_ROOT_FOLDER+'/static/'
    MEDIA_URL = '/'+URL_ROOT_FOLDER+'/site_media/'


app_pack_folders = []
base_apps_path = PRJ_PATH
for ff in os.listdir(base_apps_path):
    if os.path.isdir( os.path.join(base_apps_path,ff)):
        if not ff.startswith('_'):
            app_pack_folders.append(ff)
for app_pack in app_pack_folders:
    base_apps_path2 = os.path.join(base_apps_path, app_pack)
    try:
        x = __import__(app_pack+".apps")
        if hasattr(x.apps, 'PUBLIC') and x.apps.PUBLIC:
            PRJS.append(app_pack)
            apps = x.apps.APPS
            for pos in apps:
                if '.' in pos:
                    name = pos
                else:
                    name = app_pack + '.' + pos
                if not name in APPS:
                    APPS.append(name)
    except:
        print("Error importing module: ", app_pack+".apps")

URL_ROOT_FOLDER=''
STATIC_URL = '/static/'
MEDIA_URL = '/site_media/'

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


from pytigon_lib.schtools.install_init import init
init(PRJ_NAME, ROOT_PATH, DATA_PATH, PRJ_PATH, STATIC_ROOT, [MEDIA_ROOT, UPLOAD_PATH])

START_PAGE = 'None'
SHOW_LOGIN_WIN = False
PACKS = []

for app in APPS:
    if '.' in app:
        pack = app.split('.')[0]
        if not pack in PACKS:
            PACKS.append(pack)
            p1 = os.path.join(LOCAL_ROOT_PATH, pack)
            if not p1 in sys.path: sys.path.append(p1)
            p2 = os.path.join(PRJ_PATH_ALT, pack)
            if not p2 in sys.path: sys.path.append(p2)

    if not app in [ x if type(x)==str else x.label for x in INSTALLED_APPS]:
        INSTALLED_APPS.append(get_app_config(app))
        aa = app.split('.')
        for root_path in [PRJ_PATH, PRJ_PATH_ALT]:
            base_path = os.path.join(root_path,  aa[0])
            if os.path.exists(base_path):
                TEMPLATES[0]['DIRS'].append(os.path.join(base_path, "templates"))
                if len(aa)==2:
                    if not base_path in sys.path: sys.path.append(base_path)
                    LOCALE_PATHS.append(os.path.join(base_path, "locale"))

TEMPLATES[0]['DIRS'].insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates"))
TEMPLATES[0]['DIRS'].insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "plugins"))
LOCALE_PATHS.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "locale"))

_NAME = os.path.join(DATA_PATH, "%s/%s.db" % (PRJ_NAME, PRJ_NAME))

DATABASES = {
    'default':  {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': _NAME,
    },
}

if setup_databases:
    db_setup = setup_databases(PRJ_NAME)
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

GEN_TIME = '2020.01.02 19:19:06'

