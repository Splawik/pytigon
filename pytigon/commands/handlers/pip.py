"""
Pip Command Handler
Handles pip package management in Pytigon environment.
"""

import os
import sys
from typing import List, Optional, Dict, Any

from .base import CommandHandler
from ..errors import CommandError


class PipCommandHandler(CommandHandler):
    """
    Handler for pip package management.

    Handles commands like:
    - pytigon pip_<app> [args]
    """

    def can_handle(self, argv: List[str]) -> bool:
        """
        Check if this handler can handle the given command.

        Args:
            argv: Command arguments

        Returns:
            True if command starts with 'pip_', False otherwise
        """
        if len(argv) > 1:
            return argv[1].startswith("pip_")
        return False

    def execute(self, argv: List[str], **kwargs) -> int:
        """
        Execute the pip command.

        Args:
            argv: Command arguments
            **kwargs: Additional keyword arguments

        Returns:
            Exit code
        """
        try:
            # Extract app name from command
            app = argv[1].split("_", 1)[1]

            # Get paths for the app
            paths = self.setup_paths(app)
            lib_path = os.path.join(paths.get("DATA_PATH", ""), app, "prjlib")

            # Initialize project paths if needed
            ret = self._init_prj_path(paths, app)
            if ret:
                argv[1] = ret[0]

            # Run pip command
            executable = self.get_executable()

            if "install" in argv:
                # Install to app-specific lib path
                command = (
                    [executable, "-m", "pip", "install"]
                    + argv[2:]
                    + ["--target", lib_path]
                )
            else:
                # Run other pip commands
                command = [executable, "-m", "pip"] + argv[2:]

            return self.run_subprocess(command)

        except Exception as e:
            return self.handle_error(
                e, {"command": argv[1] if len(argv) > 1 else "pip"}
            )
