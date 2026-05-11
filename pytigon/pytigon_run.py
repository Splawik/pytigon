"""Pytigon main runner and CLI command dispatcher.

Handles all pytigon CLI commands including project management,
web server startup, script execution, and tool integration.
"""

import sys
import os
import logging
import subprocess
import configparser

# ---------------------------------------------------------------------------
# Early initialization
# ---------------------------------------------------------------------------

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
_logger = logging.getLogger("pytigon_run")

# Add pytigon_lib to path if available
try:
    from pytigon_lib.schtools.tools import get_executable
except ImportError:
    # Fallback for development environments
    def get_executable():
        """Return the Python executable path."""
        return sys.executable

    _logger.debug("Using system Python executable as fallback")


# Set environment variables
os.environ["START_PATH"] = os.path.abspath(os.getcwd())
os.environ["XKB_CONFIG_ROOT"] = "/usr/share/X11/xkb"

# Set default secret key if not provided
if not ("SECRET_KEY" in os.environ or "PYTIGON_SECRET_KEY" in os.environ):
    os.environ["SECRET_KEY"] = "anawa"

# Handle --dev flag: use local project paths for development
if "--dev" in sys.argv or "ptig.py" in sys.argv:
    if "--dev" in sys.argv:
        sys.argv.remove("--dev")
    os.environ["PYTIGON_PRJ_PATH"] = os.path.join(os.environ["START_PATH"], "prj")
    os.environ["PYTIGON_DEBUG"] = "1"
    if not os.path.exists(os.environ["PYTIGON_PRJ_PATH"]):
        os.environ["PYTIGON_PRJ_PATH"] = os.environ["START_PATH"]

# Handle --script-mode flag
if "--script-mode" in sys.argv:
    sys.argv.remove("--script-mode")
    os.environ["SCRIPT_MODE"] = "1"


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------


def run(param=None):
    """Main entry point for Pytigon CLI.

    Uses the new command dispatcher architecture for better maintainability
    and security. Falls back to the legacy implementation if the dispatcher
    is not available.

    Args:
        param: Optional list of command-line arguments (overrides sys.argv).
    """
    try:
        from pytigon.commands import CommandDispatcher

        argv = param if param else sys.argv

        # Add ext_lib to path
        base_path = os.path.abspath(os.getcwd())
        ext_lib_path = os.path.join(base_path, "ext_lib")
        if ext_lib_path not in sys.path:
            sys.path.append(ext_lib_path)

        # Set root path
        os.environ["PYTIGON_ROOT_PATH"] = os.path.dirname(os.path.abspath(__file__))

        # Create dispatcher and dispatch command
        dispatcher = CommandDispatcher()
        return dispatcher.dispatch(argv)

    except Exception as e:
        _logger.error("Error in command dispatcher: %s", e)
        return 1


# ---------------------------------------------------------------------------
# Legacy implementation (kept for backward compatibility)
# ---------------------------------------------------------------------------


def _ensure_project_initialized(paths, app):
    """Ensure a project exists on disk, initializing it if necessary.

    Args:
        paths: Dictionary of main paths from get_main_paths().
        app: Application/project name.

    Returns:
        True if initialization was performed, False otherwise.
    """
    prj_path = paths["PRJ_PATH"]
    data_path = paths["DATA_PATH"]

    if not os.path.exists(prj_path) or not os.path.exists(data_path):
        from pytigon_lib.schtools.install_init import init

        init(
            app,
            paths["ROOT_PATH"],
            data_path,
            prj_path,
            paths["STATIC_PATH"],
            [paths["MEDIA_PATH"], paths["UPLOAD_PATH"]],
        )
        return True
    return False


def _schserw_init_prj_path(paths, app, param=None):
    """Initialize project paths for the schserw Django configuration.

    Args:
        paths: Dictionary of main paths from get_main_paths().
        app: Application name. If ".", derives the name from START_PATH.
        param: (unused) Reserved for future use.

    Returns:
        Tuple of (module_app_name, path_to_add_to_syspath) or None.
    """
    if app:
        prj_path = paths["PRJ_PATH"]
        from pytigon_lib import init_paths

        init_paths(app, os.path.join(prj_path, app))

        if app == ".":
            p1 = os.environ["START_PATH"]
            parts = p1.replace("\\", "/").rsplit("/", 1)
            mod_app = parts[-1]
            os.environ["PRJ_NAME"] = mod_app
            path2 = p1[: len(parts[0])]
            sys.path.append(path2)
            return (mod_app, path2)
        else:
            os.environ["PRJ_NAME"] = app
    return None


def _get_app_conf(path):
    """Read install.ini configuration from a project path.

    Args:
        path: Directory containing install.ini.

    Returns:
        ConfigParser instance or None if not found.
    """
    config_file = os.path.join(path, "install.ini")
    if os.path.exists(config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
        return config
    return None


def _setup_project_and_paths(paths, app):
    """Common setup: ensure project exists and add project paths to sys.path.

    Args:
        paths: Dictionary of main paths from get_main_paths().
        app: Application/project name.

    Returns:
        Tuple of (app_name, prj_path) after resolving via _schserw_init_prj_path.
    """
    prj_path = paths["PRJ_PATH"]
    data_path = paths["DATA_PATH"]

    ret = _schserw_init_prj_path(paths, app)
    if ret:
        app = ret[0]
        prj_path = ret[1]

    _ensure_project_initialized(paths, app)

    prj_full_path = os.path.join(prj_path, app)
    if prj_full_path not in sys.path:
        sys.path.append(prj_full_path)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings_app")

    return app, prj_path


def _print_help():
    """Print detailed usage help for pytigon CLI commands."""
    print("First form:")
    print("===========")
    print("")
    print("Second form:")
    print("============")
    print("Manage pytigon application: pytigon manage_{{project_name}} options")
    print("    to see all options run pytigon manage_{{project_name}} --help")
    print("")
    print("Third option:")
    print("=============")
    print("Run web server: pytigon runserver_{{project_name}} options")
    print("    to see all options run pytigon runserver_{{project_name}} --help")
    print("")
    print("The fourth option:")
    print("==================")
    print("Run python script: pytigon {{script_name}}.py")
    print("    run python script in pytigon environment")
    print("")
    print("The fifth option:")
    print("=================")
    print(
        "Run python script in project directory: "
        "pytigon run_{{project_name}}/{{script_name}}.py"
    )
    print("    run python script in pytigon environment")
    print("")


def _run_legacy(param=None):
    """Legacy implementation for backward compatibility.

    This is the original implementation, kept as fallback if the new
    command dispatcher architecture is not available.

    Args:
        param: Optional list of command-line arguments (overrides sys.argv).
    """
    argv = param if param else sys.argv

    base_path = os.path.abspath(os.getcwd())
    ext_lib_path = os.path.join(base_path, "ext_lib")
    if ext_lib_path not in sys.path:
        sys.path.append(ext_lib_path)
    os.environ["PYTIGON_ROOT_PATH"] = os.path.dirname(os.path.abspath(__file__))

    # ---- Command: manage_<app> -------------------------------------------
    if len(argv) > 1 and argv[1].startswith("manage"):
        if argv[1].startswith("manage_"):
            # manage_<app> [options...]
            x = argv[1].split("_", 1)
            app = x[1]
            from pytigon_lib.schtools.main_paths import get_main_paths

            paths = get_main_paths(app)
            app, prj_path = _setup_project_and_paths(paths, app)

            path3 = os.path.join(prj_path, app)
            os.chdir(path3)
            subprocess.run([get_executable(), "manage.py"] + argv[2:])
            os.chdir(base_path)
        else:
            # manage [options...]
            subprocess.run([get_executable(), "manage.py"] + argv[2:])

    # ---- Command: run_<app>[.<script>] -----------------------------------
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
                    file_name = os.path.join(os.environ["START_PATH"], file_name)
                script = file_name.replace("\\", "/").split("/")[-1].split(".")[0]
            else:
                module_name = x[1] + ".run"
                script = "run"

        from pytigon_lib.schtools.main_paths import get_main_paths

        paths = get_main_paths(app)
        app, prj_path = _setup_project_and_paths(paths, app)

        prj_full_path = os.path.join(prj_path, app)
        if prj_full_path not in sys.path:
            sys.path.append(prj_full_path)
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
            return getattr(module, "main")(argv[2:])

    # ---- Command: runserver_<app> ----------------------------------------
    elif len(argv) > 1 and argv[1].startswith("runserver_"):
        x = argv[1].split("_", 1)
        app = x[1]

        from pytigon_lib.schtools.main_paths import get_main_paths

        paths = get_main_paths(app)
        app, prj_path = _setup_project_and_paths(paths, app)

        path3 = os.path.join(prj_path, app)
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
                if "-p" not in sys.argv and "--port" not in sys.argv:
                    options += ("-p", port)
                if "-b" not in sys.argv and "--bind" not in sys.argv:
                    options += ["-b", address]
        else:
            address = "0.0.0.0"
            if wsgi:
                if "--port" not in sys.argv and "--host" not in sys.argv:
                    options += ["--listen", "0.0.0.0:8000"]
            else:
                if "-p" not in sys.argv and "--port" not in sys.argv:
                    options += ("-p", port)
                if "-b" not in sys.argv and "--bind" not in sys.argv:
                    options += ["-b", "0.0.0.0"]
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
            sys.argv.append(f"--listen={address}:{port}")
            params = ""
            if wsgi:
                params += "wsgi"
                sys.argv.append(f"--extra={params}")
            sys.argv[1] = app
            from pytigon_gui.pytigon import main

            main()
        else:
            sys.argv = [""] + argv[2:] + options
            _logger.info("Web server: %s", sys.argv[1:])
            if wsgi:
                from waitress.runner import run

                run()
            else:
                from daphne.cli import CommandLineInterface

                CommandLineInterface.entrypoint()

        sys.argv = tmp
        os.chdir(base_path)

    # ---- Command: python_<app> -------------------------------------------
    elif len(argv) > 1 and argv[1].startswith("python_"):
        from pytigon_lib.schtools.main_paths import get_main_paths

        app = argv[1].split("_", 1)[1]

        paths = get_main_paths(app)
        ret = _schserw_init_prj_path(paths, app, param)
        if ret:
            argv[1] = ret[0]

        subprocess.run([get_executable()] + argv[2:])

    # ---- Command: pip_<app> ----------------------------------------------
    elif len(argv) > 1 and argv[1].startswith("pip_"):
        from pytigon_lib.schtools.main_paths import get_main_paths

        app = argv[1].split("_", 1)[1]

        paths = get_main_paths(app)
        lib_path = os.path.join(paths["DATA_PATH"], app, "prjlib")
        ret = _schserw_init_prj_path(paths, app, param)
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

    # ---- Command: init_<app> ---------------------------------------------
    elif len(argv) > 1 and argv[1].startswith("init_"):
        x = argv[1].split("_", 1)
        if "." in x[1]:
            x2 = x[1].split(".", 1)
            app = x2[0]
        else:
            app = x[1]

        from pytigon_lib.schtools.main_paths import get_main_paths

        paths = get_main_paths(app)
        app, prj_path = _setup_project_and_paths(paths, app)

        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "1"
        import django

        django.setup()

    # ---- Command: python -------------------------------------------------
    elif len(argv) > 1 and argv[1] == "python":
        from pytigon_lib.schtools.main_paths import get_main_paths

        paths = get_main_paths()
        ret = _schserw_init_prj_path(paths, None, param)
        if ret:
            argv[1] = ret[0]

        subprocess.run([get_executable()] + argv[2:])

    # ---- Command: zig ----------------------------------------------------
    elif len(argv) > 1 and argv[1] == "zig":
        from pytigon_lib.schtools.main_paths import get_main_paths

        paths = get_main_paths()
        ret = _schserw_init_prj_path(paths, None, param)
        if ret:
            argv[1] = ret[0]

        subprocess.run([get_executable(), "-m", "ziglang"] + argv[2:])

    # ---- Command: nim / nimble / -y -------------------------------------
    elif len(argv) > 1 and argv[1] in ("nim", "nimble", "-y"):
        from pytigon_lib.schtools.main_paths import get_main_paths
        from pytigon_lib.schtools.nim_integration import get_nim_path

        paths = get_main_paths()
        ret = _schserw_init_prj_path(paths, None, param)
        if ret:
            argv[1] = ret[0]
        nim_path = get_nim_path(paths["DATA_PATH"])
        if nim_path:
            nim_path = os.path.join(nim_path, "bin")
            if os.name == "nt":
                os.environ["PATH"] = os.environ["PATH"] + ";" + nim_path
            else:
                os.environ["PATH"] = os.environ["PATH"] + ":" + nim_path
            exe_name = argv[1] + ".exe" if os.name == "nt" else argv[1]
            subprocess.run([os.path.join(nim_path, exe_name)] + argv[2:])

    # ---- Command: @<program> ---------------------------------------------
    elif len(argv) > 1 and argv[1].startswith("@"):
        from pytigon_lib.schtools.main_paths import get_main_paths

        paths = get_main_paths()
        ret = _schserw_init_prj_path(paths, None, param)
        if ret:
            argv[1] = ret[0]
        prg_path = os.path.join(paths["DATA_PATH"], "prg")
        exe_name = argv[1][1:] + ".exe" if os.name == "nt" else argv[1][1:]
        subprocess.run([os.path.join(prg_path, exe_name)] + argv[2:])

    # ---- Command: *.py or -m or $* / ** patterns -------------------------
    elif len(argv) > 1 and (
        argv[1].endswith(".py")
        or argv[1][-4:-1] == ".py"
        or argv[1] == "-m"
        or argv[1][:1] in ("$", "*")
    ):
        from pytigon_lib.schtools.main_paths import get_main_paths

        paths = get_main_paths()
        ret = _schserw_init_prj_path(paths, None, param)
        if ret:
            argv[1] = ret[0]
        if argv[1][:1] in ("$", "*"):
            subprocess.run([get_executable(), "-m", argv[1][1:]] + argv[2:])
        else:
            subprocess.run([get_executable()] + argv[1:])

    # ---- No matching command: show help or launch GUI --------------------
    else:
        help_flag = len(argv) > 1 and argv[1] == "--help"
        try:
            if help_flag:
                _print_help()
            app = None
            for pos in argv[1:]:
                if not pos.startswith("-"):
                    app = pos
                    break

            from pytigon_lib.schtools.main_paths import get_main_paths

            paths = get_main_paths(app)

            ret = _schserw_init_prj_path(paths, app, param)

            if "--pywebview" in sys.argv:
                import webview
                from pytigon.pytigon_request import init, request

                conf = _get_app_conf(os.path.join(paths["PRJ_PATH"], argv[1]))
                index_path = os.path.join(
                    paths["STATIC_PATH"], "pywebview", "index.html"
                )
                try:
                    with open(index_path, "rt") as f:
                        index_str = f.read()
                except (FileNotFoundError, PermissionError, IOError) as e:
                    _logger.debug(
                        "Failed to load index.html from %s: %s", index_path, e
                    )
                    index_str = " "

                def _request(url, params=None):
                    return request(
                        url, params if params else None, user_agent="webviewembeded"
                    )

                class Api:
                    def get(self, url, params=None):
                        return _request(url, params).str()

                api = Api()
                if conf:
                    window = webview.create_window(
                        conf["DEFAULT"]["PRJ_TITLE"],
                        html=index_str,
                        js_api=api,
                        min_size=(1024, 768),
                    )
                else:
                    window = webview.create_window(
                        "Pytigon application",
                        html=index_str,
                        js_api=api,
                        min_size=(1024, 768),
                    )

                def on_loaded():
                    webview.windows[0].events.loaded -= on_loaded

                    def _init():
                        init(app, "auto", "anawa", user_agent="webviewembeded")

                    _init()
                    start_request = _request("/")
                    start_content = start_request.str()
                    webview.windows[0].load_html(start_content, "http://127.0.0.5/")

                window.events.loaded += on_loaded
                webview.start(debug=True)
            else:
                from pytigon_gui.pytigon import main

                main()

        except SystemExit:
            if help_flag:
                print("Second form:")
                print("============")
                print(
                    "Manage pytigon application: "
                    "pytigon manage_{{project_name}} options"
                )
                print(
                    "    to see all options run pytigon manage_{{project_name}} --help"
                )
                print("")
                print("Third option:")
                print("=============")
                print("Run web server: pytigon runserver_{{project_name}} options")
                print(
                    "    to see all options run "
                    "pytigon runserver_{{project_name}} --help"
                )
                print("")
                print("The fourth option:")
                print("==================")
                print("Run python script: pytigon {{script_name}}.py")
                print("    run python script in pytigon environment")
                print("")
                print("The fifth option:")
                print("=================")
                print(
                    "Run python script in project directory: "
                    "pytigon run_{{project_name}}/{{script_name}}.py"
                )
                print("    run python script in pytigon environment")
                print("")


if __name__ == "__main__":
    run(sys.argv)
