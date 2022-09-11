#!/usr/bin/env python
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
from multiprocessing import Process
import os
import configparser

from pytigon_lib.schtools.tools import get_executable
from pytigon_lib.schtools.platform_info import platform_name
from os import environ

environ["START_PATH"] = os.path.abspath(os.getcwd())
environ["XKB_CONFIG_ROOT"] = "/usr/share/X11/xkb"


def schserw_init_prj_path(paths, app, param=None):
    if app:
        prj_path = paths["PRJ_PATH"]
        from pytigon_lib import init_paths

        init_paths(app, os.path.join(prj_path, app))

        if app == ".":
            p1 = environ["START_PATH"]
            parts = p1.replace("\\", "/").rsplit("/", 1)
            mod_app = parts[-1]
            environ["PRJ_NAME"] = mod_app
            path2 = p1[0 : len(parts[0])]
            sys.path.append(path2)
            return (mod_app, path2)
        else:
            environ["PRJ_NAME"] = app
    return None


def get_app_conf(path):
    config_file = os.path.join(path, "install.ini")
    if os.path.exists(config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
        return config
    else:
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
            from pytigon_lib.schtools.main_paths import get_main_paths

            paths = get_main_paths(app)
            PRJ_PATH = paths["PRJ_PATH"]
            DATA_PATH = paths["DATA_PATH"]
            ret = schserw_init_prj_path(paths, app, param)
            if ret:
                app = ret[0]
                PRJ_PATH = ret[1]

            if not os.path.exists(PRJ_PATH) or not os.path.exists(DATA_PATH):
                from pytigon_lib.schtools.install_init import init

                init(
                    app,
                    paths["ROOT_PATH"],
                    DATA_PATH,
                    PRJ_PATH,
                    paths["STATIC_PATH"],
                    [paths["MEDIA_PATH"], paths["UPLOAD_PATH"]],
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

        from pytigon_lib.schtools.main_paths import get_main_paths

        paths = get_main_paths(app)

        PRJ_PATH = paths["PRJ_PATH"]

        ret = schserw_init_prj_path(paths, app, param)

        if ret:
            app = ret[0]
            PRJ_PATH = ret[1]

        path3 = os.path.join(PRJ_PATH, app)
        subprocess.run([get_executable()] + [os.path.join(path3, script)] + argv[2:])

    elif len(argv) > 1 and argv[1].startswith("runserver"):
        if "_" in argv[1]:
            x = argv[1].split("_", 1)
            app = x[1]

            from pytigon_lib.schtools.main_paths import get_main_paths

            paths = get_main_paths(app)
            PRJ_PATH = paths["PRJ_PATH"]
            DATA_PATH = paths["DATA_PATH"]

            ret = schserw_init_prj_path(paths, app, param)

            if ret:
                app = ret[0]
                PRJ_PATH = ret[1]

            if not os.path.exists(PRJ_PATH) or not os.path.exists(DATA_PATH):
                from pytigon_lib.schtools.install_init import init

                init(
                    app,
                    paths["ROOT_PATH"],
                    DATA_PATH,
                    PRJ_PATH,
                    paths["STATIC_PATH"],
                    [paths["MEDIA_PATH"], paths["UPLOAD_PATH"]],
                )

            path3 = os.path.join(PRJ_PATH, app)
            os.chdir(path3)
            options = []
            if not "-b" in argv[2:]:
                address = "0.0.0.0"
                options = ["-b", "0.0.0.0"]
            else:
                id = argv[2:].index("-b")
                if id >= 0:
                    address = argv[2:][id + 1]
            options.append("asgi:application")
            tmp = sys.argv
            sys.argv = [""] + argv[2:] + options

            if platform_name() == "Android":
                from daphne.cli import CommandLineInterface

                CommandLineInterface.entrypoint()
            else:
                try:
                    from hypercorn.__main__ import main
                except:
                    from daphne.cli import CommandLineInterface

                    CommandLineInterface.entrypoint()
                    return

                if "--with-gui" in argv:
                    sys.argv.remove("--with-gui")

                    # from pytigon.schserw import settings as schserw_settings
                    # if ret:
                    #    argv[1] = ret[0]
                    #    schserw_settings.PRJ_PATH = ret[1]

                    p = Process(target=main, args=(sys.argv[1:],))
                    p.start()

                    from pytigon_lib.schbrowser.schcef import run

                    conf = get_app_conf(os.path.join(PRJ_PATH, argv[1]))
                    if conf:
                        title = conf["DEFAULT"]["PRJ_TITLE"]
                        run(
                            "http://"
                            + address.replace("0.0.0.0", "127.0.0.1")
                            + "/"
                            + app
                            + "/",
                            app,
                            title,
                        )
                    else:
                        run(
                            "http://"
                            + address.replace("0.0.0.0", "127.0.0.1")
                            + "/"
                            + app
                            + "/",
                            app,
                            "Pytigon application",
                        )

                    p.kill()
                else:
                    main()
            sys.argv = tmp
            os.chdir(base_path)

    elif len(argv) > 1 and (
        argv[1].endswith(".py") or argv[1][-4:-1] == ".py" or argv[1] == "-m"
    ):
        app = argv[1]

        from pytigon_lib.schtools.main_paths import get_main_paths

        paths = get_main_paths(app)
        ret = schserw_init_prj_path(paths, app, param)
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

            from pytigon_lib.schtools.main_paths import get_main_paths

            paths = get_main_paths(app)

            ret = schserw_init_prj_path(paths, app, param)

            # from pytigon.schserw import settings as schserw_settings
            # if ret:
            #    argv[1] = ret[0]
            #    schserw_settings.PRJ_PATH = ret[1]

            if "-b" in sys.argv or "--embeded-browser" in sys.argv:
                import webview
                from pytigon.pytigon_request import init, request

                conf = get_app_conf(os.path.join(paths["PRJ_PATH"], argv[1]))
                index_path = os.path.join(
                    paths["STATIC_PATH"], "pywebview", "index.html"
                )
                try:
                    with open(index_path, "rt") as f:
                        index_str = f.read()
                except:
                    index_str = " "

                def _request(url, params=None):
                    if params:
                        params2 = params
                    else:
                        params2 = None
                    ret = request(url, params2, user_agent="webviewembeded")
                    return ret

                class Api:
                    def get(self, url, params=None):
                        ret = _request(url, params)
                        return ret.str()

                api = Api()
                if conf:
                    window = webview.create_window(
                        conf["DEFAULT"]["PRJ_TITLE"],
                        # url = "http://127.0.0.5/",
                        html=index_str,
                        js_api=api,
                        min_size=(1024, 768),
                        # background_color='#0FF',
                    )
                else:
                    window = webview.create_window(
                        "Pytigon application",
                        # url = "http://127.0.0.5/",
                        html=index_str,
                        js_api=api,
                        min_size=(1024, 768),
                        # background_color = '#0FF',
                    )

                def on_loaded():
                    webview.windows[0].loaded -= on_loaded

                    # from pytigon_lib.schbrowser.schcef import run
                    # if conf:
                    #    try:
                    #        title = conf['DEFAULT']['PRJ_TITLE']
                    #    except:
                    #        title = "Pytigon"
                    #    run("http://127.0.0.2", app, title)
                    # else:
                    #    run("http://127.0.0.2", app, "Pytigon application")

                    def _init():
                        init(app, "auto", "anawa", user_agent="webviewembeded")

                    ret = _init()
                    start_request = _request("/")
                    start_content = start_request.str()
                    webview.windows[0].load_html(start_content, "http://127.0.0.5/")

                window.loaded += on_loaded
                webview.start(debug=True)
            else:
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
