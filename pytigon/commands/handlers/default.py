"""Default Command Handler
Handles default case (GUI mode or help).
"""

import os
import sys
from typing import Any

from .base import CommandHandler


class DefaultCommandHandler(CommandHandler):

    """Handler for default case (GUI mode or help).

    Handles commands like:
    - pytigon <app> [options]
    - pytigon --help
    """

    def can_handle(self, argv: list[str]) -> bool:
        """Check if this handler can handle the given command.

        Args:
            argv: Command arguments

        Returns:
            True (this is the default handler)

        """
        return True

    def execute(self, argv: list[str], **kwargs) -> int:
        """Execute the default command.

        Args:
            argv: Command arguments
            **kwargs: Additional keyword arguments

        Returns:
            Exit code

        """
        try:
            # Check if help is requested
            help_requested = len(argv) > 1 and argv[1] == "--help"

            if help_requested:
                return self._show_help()

            # Find app name in arguments
            app = None
            for pos in argv[1:]:
                if not pos.startswith("-"):
                    app = pos
                    break

            # Get paths for the app
            paths = self.setup_paths(app)

            # Initialize project paths if needed
            ret = self._init_prj_path(paths, app)

            # Check if running with pywebview
            if "--pywebview" in sys.argv:
                return self._run_pywebview(argv, paths, app)
            return self._run_gui(argv, paths, app)

        except Exception as e:
            return self.handle_error(e, {"command": "default"})

    def _show_help(self) -> int:
        """Show help information.

        Returns:
            Exit code (0 for success)

        """
        print("First form:")
        print("===========")
        print("Manage pytigon application: pytigon manage_{{project_name}} options")
        print("    to see all options run pytigon manage_{{project_name}} --help")
        print("")
        print("Second form:")
        print("============")
        print("Run web server: pytigon runserver_{{project_name}} options")
        print("    to see all options run pytigon runserver_{{project_name}} --help")
        print("")
        print("Third option:")
        print("=============")
        print("Run python script: pytigon {{script_name}}.py")
        print("    run python script in pytigon environment")
        print("")
        print("The fourth option:")
        print("==================")
        print(
            "Run python script in project directory: pytigon run_{{project_name}}/{{script_name}}.py",
        )
        print("    run python script in pytigon environment")
        print("")
        return 0

    def _run_pywebview(self, argv: list[str], paths: dict[str, str], app: str | None) -> int:
        """Run with pywebview.

        Args:
            argv: Command arguments
            paths: Dictionary of paths
            app: Application name

        Returns:
            Exit code

        """
        try:
            import webview

            from pytigon.pytigon_request import init, request

            # Get app configuration
            conf = self._get_app_conf(os.path.join(paths.get("PRJ_PATH", ""), argv[1]))

            # Load index.html
            index_path = os.path.join(paths.get("STATIC_PATH", ""), "pywebview", "index.html")
            try:
                with open(index_path) as f:
                    index_str = f.read()
            except (OSError, FileNotFoundError, PermissionError) as e:
                import logging

                logging.debug(f"Failed to load index.html from {index_path}: {e}")
                index_str = " "

            # Define request function
            def _request(url, params=None):
                params2 = params if params else None
                ret = request(url, params2, user_agent="webviewembeded")
                return ret

            # Define API class
            class Api:
                def get(self, url, params=None):
                    ret = _request(url, params)
                    return ret.str()

            # Create window
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

            # Define on_loaded callback
            def on_loaded():
                webview.windows[0].events.loaded -= on_loaded

                def _init():
                    init(app, "auto", "anawa", user_agent="webviewembeded")

                ret = _init()
                start_request = _request("/")
                start_content = start_request.str()
                webview.windows[0].load_html(start_content, "http://127.0.0.5/")

            window.events.loaded += on_loaded
            webview.start(debug=True)

            return 0

        except ImportError:
            print("Error: pywebview not available", file=sys.stderr)
            return 1

    def _run_gui(self, argv: list[str], paths: dict[str, str], app: str | None) -> int:
        """Run GUI mode.

        Args:
            argv: Command arguments
            paths: Dictionary of paths
            app: Application name

        Returns:
            Exit code

        """
        try:
            from pytigon_gui.pytigon import main

            main()
            return 0
        except ImportError:
            print("Error: pytigon_gui not available", file=sys.stderr)
            return 1

    def _get_app_conf(self, path: str) -> dict[str, Any] | None:
        """Get application configuration.

        Args:
            path: Path to application directory

        Returns:
            Configuration dictionary or None

        """
        import configparser

        config_file = os.path.join(path, "install.ini")
        if os.path.exists(config_file):
            config = configparser.ConfigParser()
            config.read(config_file)
            return config
        return None
