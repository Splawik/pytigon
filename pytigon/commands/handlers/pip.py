"""Pip Command Handler
Handles running pip in prj environment.
"""

import os

from .base import CommandHandler
import pytigon_lib


class PipCommandHandler(CommandHandler):
    """Handler for running pip in prj environment.

    Handles commands like:
    - pytigon pip_<app> args
    """

    def can_handle(self, argv: list[str]) -> bool:
        """Check if this handler can handle the given command.

        Args:
            argv: Command arguments

        Returns:
            True if command starts with 'pip_', False otherwise

        """
        if len(argv) > 1:
            return argv[1].startswith("pip_")
        return False

    def execute(self, argv: list[str], **kwargs) -> int:
        """Execute the run command.

        Args:
            argv: Command arguments
            **kwargs: Additional keyword arguments

        Returns:
            Exit code

        """
        try:
            if len(argv) < 3:
                return self.handle_error(
                    ValueError("Missing pip subcommand. Usage: ptig pip_<app> <command> [args]"),
                    {"command": argv[1] if len(argv) > 1 else "pip"},
                )

            # Parse command to extract app and script
            x = argv[1].split("_", 1)
            app = x[1]
            if app:
                pytigon_lib.init_paths(app)

            executable = self.get_executable()

            command = [
                executable,
                "-m",
                "pip",
                argv[2],
            ]

            if argv[2] == "install":
                command.append("--user")

            command += argv[3:]

            print(os.environ["PYTHONUSERBASE"])
            ret = self.run_subprocess(command)
            return ret

        except Exception as e:
            return self.handle_error(e, {"command": argv[1] if len(argv) > 1 else "pip"})
