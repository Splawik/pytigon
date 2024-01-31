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
import os
import configparser

from pytigon_lib.schtools.tools import get_executable
from os import environ

environ["START_PATH"] = os.path.abspath(os.getcwd())
environ["XKB_CONFIG_ROOT"] = "/usr/share/X11/xkb"

if not ("SECRET_KEY" in environ or "PYTIGON_SECRET_KEY" in environ):
    environ["SECRET_KEY"] = "anawa"

if "--dev" in sys.argv or "ptig.py" in sys.argv:
    if "--dev" in sys.argv:
        sys.argv.remove("--dev")
    environ["PYTIGON_PRJ_PATH"] = os.path.join(environ["START_PATH"], "prj")
    environ["PYTIGON_DEBUG"] = "1"
    if not os.path.exists(environ["PYTIGON_PRJ_PATH"]):
        environ["PYTIGON_PRJ_PATH"] = environ["START_PATH"]


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

    base_path = os.path.abspath(os.getcwd())
    # base_path = os.path.dirname(os.path.abspath(__file__))
    # os.chdir(base_path)

    ext_lib_path = os.path.join(base_path, "ext_lib")
    if not ext_lib_path in sys.path:
        sys.path.append(ext_lib_path)
    os.environ["PYTIGON_ROOT_PATH"] = os.path.dirname(os.path.abspath(__file__))

    if len(argv) > 1 and argv[1].startswith("manage"):
        if argv[1].startswith("manage_"):
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
        file_name = None
        x = argv[1].split("_", 1)
        if "." in x[1]:
            x2 = x[1].split(".", 1)
            app = x2[0]
            script = x2[1]
            module_name = x[1]
        else:
            app = x[1]
            if len(argv) > 2:
                file_name = argv[2]
                if not (file_name.startswith("/") or ":" in file_name[:2]):
                    file_name = os.path.join(environ["START_PATH"], file_name)
                script = file_name.replace("\\", "/").split("/")[-1].split(".")[0]
            else:
                module_name = x[1] + ".run"
                script = "run"

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

        prj_path = os.path.join(PRJ_PATH, app)
        if not prj_path in sys.path:
            sys.path.append(prj_path)
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings_app")

        if file_name:
            import importlib.util

            spec = importlib.util.spec_from_file_location(script, file_name)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        else:
            module = __import__(script)

        if hasattr(module, "main"):
            import django

            django.setup()
            getattr(module, "main")()

    elif len(argv) > 1 and argv[1].startswith("runserver_"):
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

        wsgi = False

        if "--noasgi" in argv:
            sys.argv.remove("--noasgi")
            wsgi = True

        options = []
        listen = None
        port = "8000"
        for item in argv[2:]:
            if item.startswith("--listen="):
                listen = item.split("=")[1]
                if ":" in listen:
                    address, port = listen.split(":")
                else:
                    address = listen
                    port = "8000"
                sys.argv.remove(item)
                break
        if listen:
            if wsgi:
                options = ["--listen", listen]
            else:
                if not ("-p" in sys.argv or "--port" in sys.argv):
                    options += ("-p", port)
                if not ("-b" in sys.argv or "--bind" in sys.argv):
                    options += [
                        "-b",
                        address,
                    ]
        else:
            address = "0.0.0.0"
            if wsgi:
                if not ("--port" in sys.argv or "--host" in sys.argv):
                    options += ["--listen", "0.0.0.0:8000"]
            else:
                if not ("-p" in sys.argv or "--port" in sys.argv):
                    options += ("-p", port)
                if not ("-b" in sys.argv or "--bind" in sys.argv):
                    options += [
                        "-b",
                        "0.0.0.0",
                    ]
        if wsgi:
            options.append("wsgi:application")
            wsgi = True
        else:
            options.append("asgi:application")

        tmp = sys.argv

        if "--with-gui" in argv:
            sys.argv.remove("--with-gui")
            sys.argv.append("--embededserver")
            sys.argv.append("--server_only")
            sys.argv.append("--listen=%s:%s" % (address, str(port)))
            params = ""
            if wsgi:
                params += "wsgi"
                sys.argv.append("--extra=%s" % params)
            sys.argv[1] = app
            from pytigon_gui.pytigon import main

            main()
        else:
            sys.argv = [""] + argv[2:] + options
            print("Web server: ", sys.argv[1:])
            if wsgi:
                from waitress.runner import run

                run()
            else:
                from daphne.cli import CommandLineInterface

                CommandLineInterface.entrypoint()

        sys.argv = tmp
        os.chdir(base_path)

    elif len(argv) > 1 and argv[1].startswith("python_"):
        from pytigon_lib.schtools.main_paths import get_main_paths

        app = argv[1].split("_", 1)[1]

        paths = get_main_paths(app)
        ret = schserw_init_prj_path(paths, app, param)
        if ret:
            argv[1] = ret[0]

        subprocess.run([get_executable()] + argv[2:])

    elif len(argv) > 1 and argv[1].startswith("pip_"):
        from pytigon_lib.schtools.main_paths import get_main_paths

        app = argv[1].split("_", 1)[1]

        paths = get_main_paths(app)
        lib_path = os.path.join(paths["DATA_PATH"], app, "prjlib")
        ret = schserw_init_prj_path(paths, app, param)
        if ret:
            argv[1] = ret[0]

        if "install" in argv:
            subprocess.run(
                [get_executable(), "-m", "pip", "install"]
                + argv[2:]
                + ["--target", lib_path]
            )
        else:
            subprocess.run([get_executable(), "-m", "pip"] + argv[2:])

    elif len(argv) > 1 and argv[1].startswith("init_"):
        x = argv[1].split("_", 1)
        if "." in x[1]:
            x2 = x[1].split(".", 1)
            app = x2[0]
        else:
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

        prj_path = os.path.join(PRJ_PATH, app)
        if not prj_path in sys.path:
            sys.path.append(prj_path)
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings_app")
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "1"
        import django

        django.setup()

    elif len(argv) > 1 and argv[1] == "python":
        from pytigon_lib.schtools.main_paths import get_main_paths

        paths = get_main_paths()
        ret = schserw_init_prj_path(paths, None, param)
        if ret:
            argv[1] = ret[0]

        subprocess.run([get_executable()] + argv[2:])
    elif len(argv) > 1 and argv[1] == "zig":
        from pytigon_lib.schtools.main_paths import get_main_paths

        paths = get_main_paths()
        ret = schserw_init_prj_path(paths, None, param)
        if ret:
            argv[1] = ret[0]

        subprocess.run([get_executable(), "-m", "ziglang"] + argv[2:])
    elif len(argv) > 1 and (
        argv[1].endswith(".py")
        or argv[1][-4:-1] == ".py"
        or argv[1] == "-m"
        or argv[1].startswith("$")
    ):
        from pytigon_lib.schtools.main_paths import get_main_paths

        paths = get_main_paths()
        ret = schserw_init_prj_path(paths, None, param)
        if ret:
            argv[1] = ret[0]
        if argv[1].startswith("$"):
            subprocess.run([get_executable(), "-m", argv[1][1:]] + argv[2:])
        else:
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

            if "--pywebview" in sys.argv:
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
                    webview.windows[0].events.loaded -= on_loaded

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

                window.events.loaded += on_loaded
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
