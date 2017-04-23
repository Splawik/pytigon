#!/usr/bin/env python
import os
import sys

base_path = __file__.replace("main.py", "")
if base_path == "":
    base_path = "./"
else:
    os.chdir(base_path)

from schserw import settings

sys.path.insert(0,os.path.join(settings.APP_PACK_PATH, '_schall'))
sys.path.insert(0,os.path.join(base_path, "python/lib/python%d.%d/site-packages" % (sys.version_info[0], sys.version_info[1]) ))
sys.path.insert(0,base_path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'settings_app')

from schlib import init_paths
init_paths()

from schlib.schdjangoext.django_manage import *

if __name__ == "__main__":
    argv = ['main.py', 'runserver',  '5000', '--noasgi',  '--noreload', '--nothreading']
    cmd(argv, from_main=True)
