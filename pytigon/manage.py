#!/usr/bin/env python
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

base_path = __file__.replace("manage.py", "")
if base_path == "":
    base_path = "./"
else:
    os.chdir(base_path)

from pytigon.schserw import settings

sys.path.insert(0, os.path.join(settings.PRJ_PATH, "_schall"))
sys.path.insert(
    0,
    os.path.join(
        base_path,
        "python/lib/python%d.%d/site-packages"
        % (sys.version_info[0], sys.version_info[1]),
    ),
)
sys.path.insert(0, base_path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

from pytigon_lib import init_paths

init_paths()

from pytigon_lib.schdjangoext.django_manage import *

if __name__ == "__main__":
    cmd(sys.argv, from_main=True)
