"""
Pip Command Handler
Handles running pip in prj environment.
"""

import os

from .base import CommandHandler


class PipCommandHandler(CommandHandler):
    """
    Handler for running Python scripts.

    Handles commands like:
    - pytigon pip_<app> args
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
        Execute the run command.

        Args:
            argv: Command arguments
            **kwargs: Additional keyword arguments

        Returns:
            Exit code
        """
        try:
            # Parse command to extract app and script
            x = argv[1].split("_", 1)
            app = x[1]

            # Get paths for the app
            paths = self.setup_paths(app)
            data_path = paths.get("DATA_PATH", "")
            prjlib = os.path.join(data_path, app, "prjlib")

            executable = self.get_executable()

            command = [
                executable,
                "-m",
                "pip",
                argv[2],
            ]

            if argv[2] == "install":
                command.append("--disable-pip-version-check")
                command.append(f"--target={prjlib}")

            command += argv[3:]

            if "PYTHONPATH" in os.environ:
                python_path = os.environ["PYTHONPATH"]
            else:
                python_path = None
            os.environ["PYTHONPATH"] = prjlib
            ret = self.run_subprocess(command)
            if python_path:
                os.environ["PYTHONPATH"] = python_path
            return ret

        except Exception as e:
            return self.handle_error(e, {"command": argv[1] if len(argv) > 1 else "pip"})
