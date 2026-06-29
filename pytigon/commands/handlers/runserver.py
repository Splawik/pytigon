"""RunServer Command Handler
Handles running web servers (WSGI/ASGI).
"""

import os
import sys

from .base import CommandHandler


class RunServerCommandHandler(CommandHandler):

    """Handler for running web servers.

    Handles commands like:
    - pytigon runserver_<app> [options]
    """

    def can_handle(self, argv: list[str]) -> bool:
        """Check if this handler can handle the given command.

        Args:
            argv: Command arguments

        Returns:
            True if command starts with 'runserver_', False otherwise

        """
        if len(argv) > 1:
            return argv[1].startswith("runserver_")
        return False

    def execute(self, argv: list[str], **kwargs) -> int:
        """Execute the runserver command.

        Args:
            argv: Command arguments
            **kwargs: Additional keyword arguments

        Returns:
            Exit code

        """
        try:
            # Save current working directory
            base_path = os.getcwd()

            # Extract app name from command
            x = argv[1].split("_", 1)
            app = x[1]

            # Get paths for the app
            paths = self.setup_paths(app)
            PRJ_PATH = paths.get("PRJ_PATH", "")
            DATA_PATH = paths.get("DATA_PATH", "")

            # Initialize project paths if needed
            ret = self._init_prj_path(paths, app)
            if ret:
                app = ret[0]
                PRJ_PATH = ret[1]

            # Initialize project if directories don't exist
            self.init_project(app, paths)

            # Change to project directory
            path3 = os.path.join(PRJ_PATH, app)
            os.chdir(path3)

            try:
                # Parse server options
                wsgi = "--noasgi" in argv
                if wsgi:
                    argv.remove("--noasgi")

                # Parse listen address and port
                listen = None
                port = "8000"
                address = "0.0.0.0"

                for item in argv[2:]:
                    if item.startswith("--listen="):
                        listen = item.split("=")[1]
                        if ":" in listen:
                            address, port = listen.split(":")
                        else:
                            address = listen
                            port = "8000"
                        argv.remove(item)
                        break

                # Build server options
                options = self._build_server_options(argv, wsgi, listen, address, port)

                # Check if running with GUI
                if "--with-gui" in argv:
                    return self._run_with_gui(argv, app, wsgi, address, port)
                return self._run_server(argv, options, wsgi)

            finally:
                # Restore original working directory
                os.chdir(base_path)

        except Exception as e:
            return self.handle_error(e, {"command": argv[1] if len(argv) > 1 else "runserver"})

    def _build_server_options(
        self,
        argv: list[str],
        wsgi: bool,
        listen: str | None,
        address: str,
        port: str,
    ) -> list[str]:
        """Build server options based on arguments.

        Args:
            argv: Command arguments
            wsgi: Whether to use WSGI
            listen: Listen address (host:port)
            address: Bind address
            port: Bind port

        Returns:
            List of server options

        """
        options = []

        if listen:
            if wsgi:
                options = ["--listen", listen]
            else:
                if "-p" not in argv and "--port" not in argv:
                    options += ["-p", port]
                if "-b" not in argv and "--bind" not in argv:
                    options += ["-b", address]
        elif wsgi:
            if "--port" not in argv and "--host" not in argv:
                options += ["--listen", "0.0.0.0:8000"]
        else:
            if "-p" not in argv and "--port" not in argv:
                options += ["-p", port]
            if "-b" not in argv and "--bind" not in argv:
                options += ["-b", "0.0.0.0"]

        # Add application entry point
        if wsgi:
            options.append("wsgi:application")
        else:
            options.append("asgi:application")

        return options

    def _run_with_gui(self, argv: list[str], app: str, wsgi: bool, address: str, port: str) -> int:
        """Run server with GUI.

        Args:
            argv: Command arguments
            app: Application name
            wsgi: Whether to use WSGI
            address: Bind address
            port: Bind port

        Returns:
            Exit code

        """
        # Remove --with-gui from argv
        argv.remove("--with-gui")

        # Build GUI arguments
        gui_args = ["--embededserver", "--server_only", f"--listen={address}:{port}"]
        if wsgi:
            gui_args.append("--extra=wsgi")

        # Set app name
        gui_args.insert(0, app)

        # Import and run GUI
        try:
            from pytigon_gui.pytigon import main

            sys.argv = [app] + gui_args
            main()
            return 0
        except ImportError:
            print("Error: pytigon_gui not available", file=sys.stderr)
            return 1

    def _run_server(self, argv: list[str], options: list[str], wsgi: bool) -> int:
        """Run server without GUI.

        Args:
            argv: Command arguments
            options: Server options
            wsgi: Whether to use WSGI

        Returns:
            Exit code

        """
        # Save original sys.argv
        tmp = sys.argv

        try:
            # Build server arguments
            sys.argv = [""] + argv[2:] + options
            print("Web server: ", sys.argv[1:])

            # Run appropriate server
            if wsgi:
                try:
                    from waitress.runner import run

                    run()
                    return 0
                except ImportError:
                    print("Error: waitress not available", file=sys.stderr)
                    return 1
            else:
                try:
                    from daphne.cli import CommandLineInterface

                    CommandLineInterface.entrypoint()
                    return 0
                except ImportError:
                    print("Error: daphne not available", file=sys.stderr)
                    return 1
        finally:
            # Restore original sys.argv
            sys.argv = tmp
