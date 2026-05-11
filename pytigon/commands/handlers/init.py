"""
Init Command Handler
Handles project initialization.
"""

import os
import sys
from typing import List, Optional, Dict, Any

from .base import CommandHandler
from ..errors import CommandError


class InitCommandHandler(CommandHandler):
    """
    Handler for project initialization.

    Handles commands like:
    - pytigon init_<app>
    """

    def can_handle(self, argv: List[str]) -> bool:
        """
        Check if this handler can handle the given command.

        Args:
            argv: Command arguments

        Returns:
            True if command starts with 'init_', False otherwise
        """
        if len(argv) > 1:
            return argv[1].startswith("init_")
        return False

    def execute(self, argv: List[str], **kwargs) -> int:
        """
        Execute the init command.

        Args:
            argv: Command arguments
            **kwargs: Additional keyword arguments

        Returns:
            Exit code
        """
        try:
            # Extract app name from command
            x = argv[1].split("_", 1)
            if "." in x[1]:
                x2 = x[1].split(".", 1)
                app = x2[0]
            else:
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

            # Add project path to sys.path
            prj_path = os.path.join(PRJ_PATH, app)
            if prj_path not in sys.path:
                sys.path.append(prj_path)

            # Set Django settings module
            os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings_app")
            os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "1"

            # Setup Django
            import django

            django.setup()

            return 0

        except Exception as e:
            return self.handle_error(
                e, {"command": argv[1] if len(argv) > 1 else "init"}
            )
