"""
Tool Command Handler
Handles external tool commands (nim, zig, @tools).
"""

import os
import sys
from typing import List, Optional, Dict, Any
import importlib.util

from .base import CommandHandler
from ..errors import CommandError


class ToolCommandHandler(CommandHandler):
    """
    Handler for external tool commands.

    Handles commands like:
    - pytigon nim [args]
    - pytigon nimble [args]
    - pytigon @<tool> [args]
    """

    def can_handle(self, argv: List[str]) -> bool:
        """
        Check if this handler can handle the given command.

        Args:
            argv: Command arguments

        Returns:
            True if command is a tool command, False otherwise
        """
        if len(argv) > 1:
            return argv[1] in ("nim", "nimble", "-y") or argv[1].startswith("@")
        return False

    def execute(self, argv: List[str], **kwargs) -> int:
        """
        Execute the tool command.

        Args:
            argv: Command arguments
            **kwargs: Additional keyword arguments

        Returns:
            Exit code
        """
        try:
            # Get paths for default app
            paths = self.setup_paths()

            # Initialize project paths if needed
            ret = self._init_prj_path(paths, None)
            if ret:
                argv[1] = ret[0]

            # Handle different tool types
            if argv[1] in ("nim", "nimble", "-y"):
                return self._handle_nim(argv, paths)
            elif argv[1].startswith("@"):
                return self._handle_at_tool(argv, paths)
            else:
                raise CommandError(f"Unknown tool command: {argv[1]}", code=30)

        except Exception as e:
            return self.handle_error(e, {"command": argv[1] if len(argv) > 1 else "tool"})

    def _handle_nim(self, argv: List[str], paths: Dict[str, str]) -> int:
        """
        Handle nim/nimble commands.

        Args:
            argv: Command arguments
            paths: Dictionary of paths

        Returns:
            Exit code
        """
        try:
            from pytigon_lib.schtools.nim_integration import get_nim_path

            nim_path = get_nim_path(paths.get("DATA_PATH", ""))
            if nim_path:
                nim_path = os.path.join(nim_path, "bin")
                if os.name == "nt":
                    os.environ["PATH"] = os.environ["PATH"] + ";" + nim_path
                else:
                    os.environ["PATH"] = os.environ["PATH"] + ":" + nim_path

                # Build command
                exe_name = argv[1] + ".exe" if os.name == "nt" else argv[1]
                command = [os.path.join(nim_path, exe_name)] + argv[2:]

                return self.run_subprocess(command)
            else:
                print("Error: Nim not found", file=sys.stderr)
                return 1
        except ImportError:
            print("Error: Nim integration not available", file=sys.stderr)
            return 1

    def _handle_at_tool(self, argv: List[str], paths: Dict[str, str]) -> int:
        """
        Handle @tool commands.

        Args:
            argv: Command arguments
            paths: Dictionary of paths

        Returns:
            Exit code
        """

        if argv[1] == "@zig":
            argv[1] = "@ziglang"

        if importlib.util.find_spec(argv[1][1:]) is not None:
            # Run Python interpreter
            executable = self.get_executable()
            command = [executable, "-m", argv[1][1:]] + argv[2:]
            return self.run_subprocess(command)
        else:
            # Build tool path
            prg_path = os.path.join(paths.get("DATA_PATH", ""), "prg")
            tool_name = argv[1][1:]  # Remove @ prefix

            # Build command
            exe_name = tool_name + ".exe" if os.name == "nt" else tool_name

            command = [os.path.join(prg_path, exe_name)] + argv[2:]
            return self.run_subprocess(command)
