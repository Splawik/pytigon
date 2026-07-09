"""Base Command Handler
Abstract base class for all command handlers.
"""

import os
import sys
from abc import ABC, abstractmethod
from typing import Any

from ..errors import ErrorHandler
from ..utils import PathResolver, SafeSubprocess


class CommandHandler(ABC):
    """Abstract base class for command handlers.

    All command handlers must implement the execute method.
    Provides common functionality for path resolution, subprocess execution,
    and error handling.
    """

    def __init__(self, config: dict[str, Any] | None = None):
        """Initialize CommandHandler.

        Args:
            config: Configuration dictionary for the handler

        """
        self.config = config or {}
        self.path_resolver = PathResolver()
        self.subprocess = SafeSubprocess()
        self.error_handler = ErrorHandler(debug=self.config.get("debug", False))

    @abstractmethod
    def execute(self, argv: list[str], **kwargs) -> int:
        """Execute the command.

        Args:
            argv: Command arguments
            **kwargs: Additional keyword arguments

        Returns:
            Exit code (0 for success, non-zero for failure)

        """

    @abstractmethod
    def can_handle(self, argv: list[str]) -> bool:
        """Check if this handler can handle the given command.

        Args:
            argv: Command arguments

        Returns:
            True if this handler can handle the command, False otherwise

        """

    def get_command_name(self, argv: list[str]) -> str | None:
        """Extract command name from arguments.

        Args:
            argv: Command arguments

        Returns:
            Command name or None if not found

        """
        if len(argv) > 1:
            return argv[1]
        return None

    def get_app_name(self, argv: list[str]) -> str | None:
        """Extract application name from command arguments.

        Args:
            argv: Command arguments

        Returns:
            Application name or None if not found

        """
        command = self.get_command_name(argv)
        if command and "_" in command:
            return command.split("_", 1)[1]
        return None

    def setup_paths(self, app: str | None = None) -> dict[str, str]:
        """Setup paths for the application.

        Args:
            app: Application name

        Returns:
            Dictionary of paths

        """
        try:
            from pytigon_lib.schtools.main_paths import get_main_paths

            return get_main_paths(app)
        except ImportError:
            # Fallback for development
            return {
                "ROOT_PATH": os.getcwd(),
                "PRJ_PATH": os.path.join(os.getcwd(), "prj"),
                "DATA_PATH": os.path.join(os.getcwd(), "data"),
                "STATIC_PATH": os.path.join(os.getcwd(), "static"),
                "MEDIA_PATH": os.path.join(os.getcwd(), "media"),
                "UPLOAD_PATH": os.path.join(os.getcwd(), "uploads"),
            }

    def _init_prj_path(self, paths: dict[str, str], app: str | None) -> tuple | None:
        """Initialize project path.

        Args:
            paths: Dictionary of paths
            app: Application name

        Returns:
            Tuple of (app_name, prj_path) or None

        """
        try:
            from pytigon_lib import init_paths

            prj_path = paths.get("PRJ_PATH", "")
            if app:
                init_paths(app, os.path.join(prj_path, app))
            else:
                init_paths(None, prj_path)

            if app == ".":
                p1 = os.getcwd()
                parts = p1.replace("\\", "/").rsplit("/", 1)
                mod_app = parts[-1]
                path2 = p1[: len(parts[0])]
                sys.path.append(path2)
                return (mod_app, path2)
            if app:
                os.environ["PRJ_NAME"] = app
        except ImportError:
            # pytigon_lib not available, skip initialization
            pass

        return None

    def init_project(self, app: str, paths: dict[str, str]) -> None:
        """Initialize project directories if they don't exist.

        Args:
            app: Application name
            paths: Dictionary of paths

        """
        PRJ_PATH = paths.get("PRJ_PATH", "")
        DATA_PATH = paths.get("DATA_PATH", "")

        if not os.path.exists(PRJ_PATH) or not os.path.exists(DATA_PATH):
            try:
                from pytigon_lib.schtools.install_init import init

                init(
                    app,
                    paths.get("ROOT_PATH", ""),
                    DATA_PATH,
                    PRJ_PATH,
                    paths.get("STATIC_PATH", ""),
                    [paths.get("MEDIA_PATH", ""), paths.get("UPLOAD_PATH", "")],
                )
            except ImportError:
                # Fallback: create directories manually
                os.makedirs(PRJ_PATH, exist_ok=True)
                os.makedirs(DATA_PATH, exist_ok=True)

    def get_executable(self) -> str:
        """Get the Python executable path.

        Returns:
            Path to Python executable

        """
        try:
            from pytigon_lib.schtools.tools import get_executable

            return get_executable()
        except ImportError:
            return sys.executable

    def run_subprocess(self, command: list[str], cwd: str | None = None) -> int:
        """Run a subprocess command safely.

        Args:
            command: Command to execute
            cwd: Working directory

        Returns:
            Exit code

        """
        return self.subprocess.run_simple(command, cwd=cwd)

    def handle_error(self, error: Exception, context: dict[str, Any] | None = None) -> int:
        """Handle an error using the error handler.

        Args:
            error: Exception to handle
            context: Additional context information

        Returns:
            Exit code

        """
        return self.error_handler.handle(error, context)
