"""
Python Command Handler
Handles running Python interpreter and Python scripts in Pytigon environment.
"""

import os
import sys
from typing import List, Optional, Dict, Any

from .base import CommandHandler
from ..errors import CommandError


class PythonCommandHandler(CommandHandler):
    """
    Handler for running Python interpreter and scripts.

    Handles commands like:
    - pytigon python_<app> [args]
    - pytigon python [args]
    - pytigon <script>.py [args]
    """

    def can_handle(self, argv: List[str]) -> bool:
        """
        Check if this handler can handle the given command.

        Args:
            argv: Command arguments

        Returns:
            True if command is 'python', starts with 'python_',
            or is a .py file (so ptig wig.py equals ptig python wig.py)
        """
        if len(argv) > 1:
            return (
                argv[1] == "python"
                or argv[1].startswith("python_")
                or argv[1].endswith(".py")
                or argv[1][-4:-1] == ".py"
                or (argv[1].startswith("-") and not argv[1].startswith("--"))
            )
        return False

    def execute(self, argv: List[str], **kwargs) -> int:
        """
        Execute the python command.

        Args:
            argv: Command arguments
            **kwargs: Additional keyword arguments

        Returns:
            Exit code
        """
        try:
            # Check if it's python_<app>
            if argv[1].startswith("python_"):
                return self._handle_python_app(argv)
            # Check if it's a .py file (ptig script.py = ptig python script.py)
            elif (
                argv[1].endswith(".py")
                or argv[1][-4:-1] == ".py"
                or (argv[1].startswith("-") and not argv[1].startswith("--"))
            ):
                return self._handle_script_file(argv)
            # Otherwise it's just 'python'
            else:
                return self._handle_python_simple(argv)

        except Exception as e:
            return self.handle_error(
                e, {"command": argv[1] if len(argv) > 1 else "python"}
            )

    def _handle_python_app(self, argv: List[str]) -> int:
        """
        Handle python_<app> command.

        Args:
            argv: Command arguments

        Returns:
            Exit code
        """
        # Extract app name from command
        app = argv[1].split("_", 1)[1]

        # Get paths for the app
        paths = self.setup_paths(app)

        # Initialize project paths if needed
        ret = self._init_prj_path(paths, app)
        if ret:
            argv[1] = ret[0]

        # Run Python interpreter
        executable = self.get_executable()
        command = [executable] + argv[2:]
        return self.run_subprocess(command)

    def _handle_python_simple(self, argv: List[str]) -> int:
        """
        Handle simple python command (without app specified).

        Args:
            argv: Command arguments

        Returns:
            Exit code
        """
        # Get paths for default app
        paths = self.setup_paths()

        # Initialize project paths if needed
        ret = self._init_prj_path(paths, None)
        if ret:
            argv[1] = ret[0]

        # Run Python interpreter
        executable = self.get_executable()
        command = [executable] + argv[2:]
        return self.run_subprocess(command)

    def _handle_script_file(self, argv: List[str]) -> int:
        """
        Handle .py script file execution (ptig script.py = ptig python script.py).

        Args:
            argv: Command arguments (argv[1] is the .py file)

        Returns:
            Exit code
        """
        # Get paths for default app

        paths = self.setup_paths()

        # Initialize project paths if needed
        ret = self._init_prj_path(paths, None)
        if ret:
            argv[1] = ret[0]

        # Run Python script (include argv[1] which is the .py file)
        executable = self.get_executable()
        command = [executable] + argv[1:]
        return self.run_subprocess(command)
