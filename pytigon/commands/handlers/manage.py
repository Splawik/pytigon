"""
Manage Command Handler
Handles Django management commands.
"""

import os
import sys
from typing import List, Optional, Dict, Any

from .base import CommandHandler
from ..errors import CommandError


class ManageCommandHandler(CommandHandler):
    """
    Handler for Django management commands.

    Handles commands like:
    - pytigon manage_<app> <command>
    - pytigon manage <command>
    """

    def can_handle(self, argv: List[str]) -> bool:
        """
        Check if this handler can handle the given command.

        Args:
            argv: Command arguments

        Returns:
            True if command starts with 'manage', False otherwise
        """
        if len(argv) > 1:
            return argv[1].startswith("manage")
        return False

    def execute(self, argv: List[str], **kwargs) -> int:
        """
        Execute the manage command.

        Args:
            argv: Command arguments
            **kwargs: Additional keyword arguments

        Returns:
            Exit code
        """
        try:
            # Save current working directory
            base_path = os.getcwd()

            # Check if it's manage_<app> or just manage
            if argv[1].startswith("manage_"):
                return self._handle_manage_app(argv, base_path)
            else:
                return self._handle_manage_simple(argv, base_path)

        except Exception as e:
            return self.handle_error(
                e, {"command": argv[1] if len(argv) > 1 else "manage"}
            )

    def _handle_manage_app(self, argv: List[str], base_path: str) -> int:
        """
        Handle manage_<app> command.

        Args:
            argv: Command arguments
            base_path: Original working directory

        Returns:
            Exit code
        """
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
            # Run Django manage.py
            executable = self.get_executable()
            command = [executable, "manage.py"] + argv[2:]
            return self.run_subprocess(command)
        finally:
            # Restore original working directory
            os.chdir(base_path)

    def _handle_manage_simple(self, argv: List[str], base_path: str) -> int:
        """
        Handle simple manage command (without app specified).

        Args:
            argv: Command arguments
            base_path: Original working directory

        Returns:
            Exit code
        """
        # Run Django manage.py in current directory
        executable = self.get_executable()
        command = [executable, "manage.py"] + argv[2:]
        return self.run_subprocess(command)
