#!/usr/bin/env python
import os
import sys

base_path = __file__.replace("manage.py", "")
if base_path == "":
    base_path = "./"
else:
    os.chdir(base_path)

base_path += "app_pack/_schall/"


sys.path.insert(0,base_path + "./")
sys.path.insert(0,base_path + "../../python/lib/python%d.%d/site-packages" % (sys.version_info[0], sys.version_info[1]))
sys.path.insert(0,base_path + "../..")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'settings_app')

#sys.path.insert(0, os.path.abspath(base_path + "../.."))

from schlib import init_paths
init_paths()

from schlib.schdjangoext.django_manage import *

if __name__ == "__main__":
    cmd(sys.argv, from_main=True)