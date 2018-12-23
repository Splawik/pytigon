#! /usr/bin/python3.7
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

from schlib.schtools.tools import get_executable
from schlib.schtools.platform_info import platform_name

def run(param=None):
    if param:
        argv=param
    else:
        argv=sys.argv

    base_path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(base_path)

    ext_lib_path = os.path.join(base_path, "ext_lib")
    if not ext_lib_path in sys.path:
        sys.path.append(ext_lib_path)

    os.environ['PYTIGON_ROOT_PATH'] = base_path
    if len(argv)>1 and argv[1].startswith('manage'):
        if '_' in argv[1]:
            from schserw.settings import ROOT_PATH, DATA_PATH, APP_PACK_PATH, \
                STATIC_APP_ROOT, MEDIA_ROOT, UPLOAD_PATH

            x = argv[1].split('_',1)
            app = x[1]

            if not os.path.exists(APP_PACK_PATH):
                from schlib.schtools.install_init import init
                init(app, ROOT_PATH, DATA_PATH, APP_PACK_PATH, STATIC_APP_ROOT, [MEDIA_ROOT, UPLOAD_PATH])

            path3 = os.path.join(APP_PACK_PATH, app)
            os.chdir(path3)
            subprocess.run([get_executable(), "manage.py"] + argv[2:])
            os.chdir(base_path)
        else:
            subprocess.run([get_executable(), "manage.py"] + argv[2:])
    elif len(argv) > 1 and argv[1].startswith('run_'):
        from schserw.settings import ROOT_PATH, DATA_PATH, APP_PACK_PATH, \
            STATIC_APP_ROOT, MEDIA_ROOT, UPLOAD_PATH
        x = argv[1].split('_', 1)
        if '/' in x[1]:
            x2 = x[1].split('/', 1)
            app = x2[0]
            script = x2[1]
        else:
            app = x[1]
            script = run.py

        path3 = os.path.join(APP_PACK_PATH, app)
        subprocess.run([get_executable(), ] + [os.path.join(path3, script),] + argv[2:])

    elif len(argv)>1 and argv[1].startswith('runserver'):
        if '_' in argv[1]:
            from schserw.settings import ROOT_PATH, DATA_PATH, APP_PACK_PATH, \
                STATIC_APP_ROOT, MEDIA_ROOT, UPLOAD_PATH
            x = argv[1].split('_', 1)
            app = x[1]

            if not os.path.exists(APP_PACK_PATH):
                from schlib.schtools.install_init import init
                init(app, ROOT_PATH, DATA_PATH, APP_PACK_PATH, STATIC_APP_ROOT, [MEDIA_ROOT, UPLOAD_PATH])

            path3 = os.path.join(APP_PACK_PATH, app)
            os.chdir(path3)
            options = []
            if not '-b' in argv[2:]:
                options = ['-b', '0.0.0.0:8000',]

            options.append('asgi:application')
            tmp = sys.argv
            sys.argv=['',] + argv[2:] + options

            if platform_name() == 'Android':
                from daphne.cli import CommandLineInterface
                CommandLineInterface.entrypoint()
            else:
                from hypercorn.__main__ import main
                main()

            sys.argv = tmp

            os.chdir(base_path)

    elif len(argv)>1 and ( argv[1].endswith('.py') or argv[1][-4:-1] == ".py" ):
        subprocess.run([get_executable(),] + argv[1:])
    else:
        from schcli.pytigon import main
        main()

if __name__ == '__main__':
    run(sys.argv)

