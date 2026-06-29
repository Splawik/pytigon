#!/usr/bin/env python
"""Django management entry point for pytigon.

Configures the Python path and environment to allow running Django
management commands within the pytigon framework.
"""

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Determine and change to the project base directory
base_path = os.path.dirname(os.path.abspath(__file__))
if base_path:
    os.chdir(base_path)
else:
    base_path = "./"

from pytigon.schserw import settings

sys.path.insert(0, os.path.join(settings.PRJ_PATH, "_schall"))
sys.path.insert(
    0,
    os.path.join(
        base_path,
        f"python/lib/python{sys.version_info[0]}.{sys.version_info[1]}/site-packages",
    ),
)
sys.path.insert(0, base_path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

from pytigon_lib import init_paths

init_paths()

from pytigon_lib.schdjangoext.django_manage import cmd  # noqa: F401

if __name__ == "__main__":
    cmd(sys.argv, from_main=True)
