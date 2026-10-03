"""RunServer Command Handler
Handles running web servers (WSGI/ASGI).
"""

import logging
import os
import sys
import threading

from .base import CommandHandler

_logger = logging.getLogger(__name__)

_ADDRESS_DEFAULT = "0.0.0.0"
_PORT_DEFAULT = "8000"


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

            # Prepare project environment
            app, PRJ_PATH, paths = self._prepare_project(app)

            try:
                # Parse server options
                wsgi = "--noasgi" in argv
                if wsgi:
                    argv.remove("--noasgi")

                # Parse listen address and port
                listen = None
                port = _PORT_DEFAULT
                address = _ADDRESS_DEFAULT
                workers = None

                for item in argv[2:]:
                    if item.startswith("--listen="):
                        listen = item.partition("=")[2]
                        if ":" in listen:
                            # rpartition so bracketed IPv6 ("[::1]:8000") splits
                            # into address="[::1]" and port="8000".
                            address, _, port = listen.rpartition(":")
                        else:
                            address = listen
                            port = _PORT_DEFAULT
                        argv.remove(item)
                        break

                for item in argv[2:]:
                    if item.startswith("--workers="):
                        workers = int(item.split("=")[1])
                        argv.remove(item)
                        break

                # Build server options
                options = self._build_server_options(argv, wsgi, listen, address, port, workers)

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
        workers: int | None = None,
    ) -> dict:
        """Build server options based on arguments.

        Args:
            argv: Command arguments
            wsgi: Whether to use WSGI
            listen: Listen address (host:port)
            address: Bind address
            port: Bind port
            workers: Number of worker threads/processes

        Returns:
            Dict with keys: target, address, port, workers, cli_options

        """
        cli_options = []
        target_address = address
        target_port = port

        if listen:
            if wsgi:
                cli_options = ["--listen", listen]
            else:
                if "-p" not in argv and "--port" not in argv:
                    cli_options += ["-p", port]
                if "-b" not in argv and "--bind" not in argv:
                    cli_options += ["-b", address]
            # target_address/target_port already hold the parsed listen value
            # (see the --listen parsing above); no need to re-split here.
        elif wsgi:
            if "--port" not in argv and "--host" not in argv:
                cli_options += [
                    "--listen",
                    f"{_ADDRESS_DEFAULT}:{_PORT_DEFAULT}",
                ]
            target_address = _ADDRESS_DEFAULT
            target_port = _PORT_DEFAULT
        else:
            if "-p" not in argv and "--port" not in argv:
                cli_options += ["-p", port]
            if "-b" not in argv and "--bind" not in argv:
                cli_options += ["-b", _ADDRESS_DEFAULT]
            target_address = address
            target_port = port

        # Application entry point
        target = "wsgi:application" if wsgi else "asgi:application"
        cli_options.append(target)

        return {
            "target": target,
            "address": target_address,
            "port": target_port,
            "workers": workers,
            "cli_options": cli_options,
        }

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

            tmp = sys.argv
            try:
                sys.argv = [app] + gui_args
                main()
            finally:
                sys.argv = tmp
            return 0
        except ImportError as e:
            import traceback

            print("Error: pytigon_gui not available", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            return 1

    def _run_server(self, argv: list[str], options: dict, wsgi: bool) -> int:
        """Run server without GUI.

        Args:
            argv: Command arguments
            options: Server options dict with keys: target, address, port, workers, cli_options
            wsgi: Whether to use WSGI

        Returns:
            Exit code

        """
        tmp = sys.argv

        try:
            cli_options = options["cli_options"]
            sys.argv = [""] + argv[2:] + cli_options
            _logger.info("Web server: %s", sys.argv[1:])

            target = options["target"]
            address = options["address"]
            port = int(options["port"])
            workers = options.get("workers")

            try:
                from granian import Granian
                from granian.constants import Interfaces
            except ImportError:
                if wsgi:
                    _logger.info("granian not available, falling back to daphne for WSGI")
                else:
                    _logger.info("granian not available, falling back to daphne for ASGI")

                from daphne.cli import CommandLineInterface

                # entrypoint() calls sys.exit() itself; the return keeps the
                # function's int contract if that ever changes.
                CommandLineInterface.entrypoint()
                return 0
            else:
                import asyncio

                # Granian cancels worker tasks on shutdown; those
                # CancelledErrors are expected noise, so they are filtered out
                # of the global exception hooks. The patches are process-wide,
                # so they are restored as soon as serve() returns.
                orig_threading_excepthook = threading.excepthook
                orig_asyncio_exc_handler = (
                    asyncio.base_events.BaseEventLoop.default_exception_handler
                )

                def _filtered_threading_hook(args, _orig=orig_threading_excepthook):
                    if isinstance(args.exc_value, asyncio.CancelledError):
                        return
                    _orig(args)

                def _filtered_asyncio_handler(
                    loop, context, _orig=orig_asyncio_exc_handler
                ):
                    if isinstance(context.get("exception"), asyncio.CancelledError):
                        return
                    _orig(loop, context)

                threading.excepthook = _filtered_threading_hook
                asyncio.base_events.BaseEventLoop.default_exception_handler = (
                    _filtered_asyncio_handler
                )
                try:
                    interface = Interfaces.WSGI if wsgi else Interfaces.ASGI
                    kwargs = {
                        "target": target,
                        "address": address,
                        "port": port,
                        "interface": interface,
                    }
                    if workers is not None:
                        kwargs["workers"] = workers
                    # Any ImportError from inside serve() propagates: falling
                    # back to daphne here would silently mask a broken app.
                    Granian(**kwargs).serve()
                    return 0
                finally:
                    threading.excepthook = orig_threading_excepthook
                    asyncio.base_events.BaseEventLoop.default_exception_handler = (
                        orig_asyncio_exc_handler
                    )
        finally:
            sys.argv = tmp
