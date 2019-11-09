#!/usr/bin/env python3.7
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

# Pytigon - wxpython and django application framework

# author: "Slawomir Cholaj (slawomir.cholaj@gmail.com)"
# copyright: "Copyright (C) ????/2013 Slawomir Cholaj"
# license: "LGPL 3.0"
# version: "0.92"

import sys
import subprocess
import os

from pytigon_lib.schtools.tools import get_executable
from pytigon_lib.schtools.platform_info import platform_name
from os import environ

environ["START_PATH"] = os.path.abspath(os.getcwd())


def schserw_init_prj_path(app, param=None):
    if app:
        import pytigon.schserw.settings

        if app=='.':
            p1 = environ["START_PATH"]
            parts = p1.replace('\\', '/').split('/')
            mod_app = parts[-1]
            path2 = os.path.join(parts[0] if parts[0] else '/', *parts[1:-1])
            sys.path.append(path2)
            return (mod_app, path2)
        else:
            p1 = os.path.join(pytigon.schserw.settings.PRJ_PATH, app)
            sys.path.append(pytigon.schserw.settings.PRJ_PATH)
            if not os.path.exists(p1):
                p2 = os.path.join(pytigon.schserw.settings.PRJ_PATH_ALT, app)
                if os.path.exists(p2):
                    pytigon.schserw.settings.PRJ_PATH = (
                        pytigon.schserw.settings.PRJ_PATH_ALT
                    )

            if platform_name() != "Windows":
                os.environ["LD_LIBRARY_PATH"] = os.path.abspath(
                    os.path.join(pytigon.schserw.settings.DATA_PATH, "ext_prg", "tcc")
                )
        return None
    return None

def run(param=None):
    if param:
        argv = param
    else:
        argv = sys.argv

    base_path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(base_path)

    ext_lib_path = os.path.join(base_path, "ext_lib")
    if not ext_lib_path in sys.path:
        sys.path.append(ext_lib_path)
    os.environ["PYTIGON_ROOT_PATH"] = base_path
    if len(argv) > 1 and argv[1].startswith("manage"):
        if "_" in argv[1]:
            x = argv[1].split("_", 1)
            app = x[1]
            ret = schserw_init_prj_path(app, param)

            from pytigon.schserw.settings import (
                ROOT_PATH,
                DATA_PATH,
                PRJ_PATH,
                STATIC_APP_ROOT,
                MEDIA_ROOT,
                UPLOAD_PATH,
            )

            if ret:
                app=ret[0]
                PRJ_PATH=ret[1]

            if not os.path.exists(PRJ_PATH) or not os.path.exists(DATA_PATH):
                from pytigon_lib.schtools.install_init import init

                init(
                    app,
                    ROOT_PATH,
                    DATA_PATH,
                    PRJ_PATH,
                    STATIC_APP_ROOT,
                    [MEDIA_ROOT, UPLOAD_PATH],
                )

            path3 = os.path.join(PRJ_PATH, app)
            os.chdir(path3)
            subprocess.run([get_executable(), "manage.py"] + argv[2:])
            os.chdir(base_path)
        else:
            subprocess.run([get_executable(), "manage.py"] + argv[2:])
    elif len(argv) > 1 and argv[1].startswith("run_"):
        x = argv[1].split("_", 1)
        if "/" in x[1]:
            x2 = x[1].split("/", 1)
            app = x2[0]
            script = x2[1]
        else:
            app = x[1]
            script = "run.py"

        ret = schserw_init_prj_path(app, param)

        from pytigon.schserw.settings import (
            ROOT_PATH,
            DATA_PATH,
            PRJ_PATH,
            STATIC_APP_ROOT,
            MEDIA_ROOT,
            UPLOAD_PATH,
        )

        if ret:
            app = ret[0]
            PRJ_PATH = ret[1]

        path3 = os.path.join(PRJ_PATH, app)
        subprocess.run([get_executable()] + [os.path.join(path3, script)] + argv[2:])

    elif len(argv) > 1 and argv[1].startswith("runserver"):
        if "_" in argv[1]:
            x = argv[1].split("_", 1)
            app = x[1]

            ret = schserw_init_prj_path(app, param)

            from pytigon.schserw.settings import (
                ROOT_PATH,
                DATA_PATH,
                PRJ_PATH,
                STATIC_APP_ROOT,
                MEDIA_ROOT,
                UPLOAD_PATH,
            )

            if ret:
                app=ret[0]
                PRJ_PATH=ret[1]

            if not os.path.exists(PRJ_PATH) or not os.path.exists(DATA_PATH):
                from pytigon_lib.schtools.install_init import init

                init(
                    app,
                    ROOT_PATH,
                    DATA_PATH,
                    PRJ_PATH,
                    STATIC_APP_ROOT,
                    [MEDIA_ROOT, UPLOAD_PATH],
                )

            path3 = os.path.join(PRJ_PATH, app)
            os.chdir(path3)
            options = []
            if not "-b" in argv[2:]:
                options = ["-b", "0.0.0.0:8000"]

            options.append("asgi:application")
            tmp = sys.argv
            sys.argv = [""] + argv[2:] + options

            if platform_name() == "Android":
                from daphne.cli import CommandLineInterface

                CommandLineInterface.entrypoint()
            else:
                from hypercorn.__main__ import main

                main()

            sys.argv = tmp

            os.chdir(base_path)

    elif len(argv) > 1 and (argv[1].endswith(".py") or argv[1][-4:-1] == ".py"):
        app = argv[1]

        ret = schserw_init_prj_path(app, param)
        if ret:
            argv[1] = ret[0]

        subprocess.run([get_executable()] + argv[1:])
    else:
        help = False
        if len(argv) > 1 and argv[1] == "--help":
            help = True
        try:
            if help:
                print("First form:")
                print("===========")
            app = None
            for pos in argv[1:]:
                if not pos.startswith("-"):
                    app = pos
                    break

            ret = schserw_init_prj_path(app, param)

            if ret:
                app=ret[0]
                argv[1] = ret[0]
                PRJ_PATH=ret[1]

            from pytigon.schserw import settings as schserw_settings
            schserw_settings.PRJ_PATH = PRJ_PATH

            from pytigon_gui.pytigon import main
            main()

        except SystemExit:
            if help:
                print("Second form:")
                print("============")
                print(
                    "Manage pytigon application: pytigon manage_{{project_name}} options"
                )
                print(
                    "    to see all options run pytigon manage_{{project_name}} --help"
                )
                print("")
                print("Third option:")
                print("=============")
                print("Run web server: pytigon runserver_{{project_name}} options")
                print(
                    "    to see all options run pytigon runserver_{{project_name}} --help"
                )
                print("")
                print("The fourth option:")
                print("==================")
                print("Run python script: pytigon {{script_name}}.py")
                print("    run python script in pytigon enviroment")
                print("")
                print("The fifth option:")
                print("=================")
                print(
                    "Run python script in project directory: pytigon run_{{project_name}}/{{script_name}}.py"
                )
                print("    run python script in pytigon enviroment")
                print("")


if __name__ == "__main__":
    run(sys.argv)

