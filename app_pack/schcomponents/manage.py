#!/usr/bin/env python
import os
import sys
from os import environ

base_path = __file__.replace("manage.py", "")
if base_path == "":
    base_path = "./"
else:
    os.chdir(base_path)

if 'PYTIGON_ROOT_PATH' in environ:
    sys.path.insert(0, environ['PYTIGON_ROOT_PATH'])
else:
    sys.path.insert(0, os.path.abspath(base_path + "../.."))

sys.path.insert(0, base_path)

from schlib import init_paths
init_paths()

from schlib.schdjangoext.django_manage import *

if __name__ == "__main__":
    cmd(sys.argv, from_main=True)