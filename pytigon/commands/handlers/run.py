"""Run Command Handler
Handles running Python scripts in Pytigon environment.
"""

import os
import sys

from .base import CommandHandler


class RunCommandHandler(CommandHandler):

    """Handler for running Python scripts.

    Handles commands like:
    - pytigon run_<app>.<script>
    - pytigon run_<app> <file.py>
    """

    def can_handle(self, argv: list[str]) -> bool:
        """Check if this handler can handle the given command.

        Args:
            argv: Command arguments

        Returns:
            True if command starts with 'run_', False otherwise

        """
        if len(argv) > 1:
            return argv[1].startswith("run_")
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
            # Parse command to extract app and script
            file_name = None
            x = argv[1].split("_", 1)

            if "." in x[1]:
                # Format: run_<app>.<script>
                x2 = x[1].split(".", 1)
                app = x2[0]
                script = x2[1]
                module_name = x[1]
            else:
                # Format: run_<app> <file.py>
                app = x[1]
                if len(argv) > 2:
                    file_name = argv[2]
                    # Make path absolute if relative
                    if not (file_name.startswith("/") or ":" in file_name[:2]):
                        file_name = os.path.join(
                            os.environ.get("START_PATH", os.getcwd()), file_name,
                        )
                    script = file_name.replace("\\", "/").split("/")[-1].split(".")[0]
                else:
                    module_name = x[1] + ".run"
                    script = "run"

            # Prepare project environment
            app, PRJ_PATH, paths = self._prepare_project(app)

            # Add project path to sys.path
            prj_path = os.path.join(PRJ_PATH, app)
            if prj_path not in sys.path:
                sys.path.append(prj_path)

            # Set Django settings module
            os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings_app")

            # Import and execute the script
            if file_name:
                # Import from file
                import importlib.util

                spec = importlib.util.spec_from_file_location(script, file_name)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
            else:
                # Import by module name
                import importlib

                module = importlib.import_module(script)

            # Call main function if it exists
            if hasattr(module, "main"):
                import django

                django.setup()
                return module.main(argv[2:])

            return 0

        except Exception as e:
            return self.handle_error(e, {"command": argv[1] if len(argv) > 1 else "run"})
