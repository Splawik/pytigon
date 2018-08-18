#! /usr/bin/python3.6
# -*- coding: utf-8 -*-
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation; either version 3, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY  ; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.

#Pytigon - wxpython and django application framework

#author: "Slawomir Cholaj (slawomir.cholaj@gmail.com)"
#copyright: "Copyright (C) ????/2013 Slawomir Cholaj"
#license: "LGPL 3.0"
#version: "0.1a"

import sys
import subprocess
import os

from schcli.pytigon import main
from schlib.schtools.tools import get_executable
from schlib.schtools.platform_info import platform_name
from os import environ

def run():
    base_path = __file__.replace("ptigrun.py", "")
    if base_path == "":
        base_path = os.getcwd()
    else:
        os.chdir(base_path)

    environ['PYTIGON_ROOT_PATH'] = base_path

    if len(sys.argv)>1 and sys.argv[1].startswith('manage'):
        if '_' in sys.argv[1]:
            x = sys.argv[1].split('_',1)
            app = x[1]

            if platform_name() == 'Android' or 'PYTIGON_APP_IMAGE' in os.environ:
                path2 = os.path.join(os.path.join(os.path.expanduser("~"), "pytigon"), 'app_pack')
            else:
                path2 = os.path.join(base_path, "app_pack")

            path3 = os.path.join(path2, app)
            os.chdir(path3)
            subprocess.run([get_executable(), "manage.py"] + sys.argv[2:])
            os.chdir(base_path)
        else:
            subprocess.run([get_executable(), "manage.py"] + sys.argv[2:])
    else:
        main(sys.argv[1:])

if __name__ == '__main__':
    run()

