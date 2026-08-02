"""Pytigon main runner and CLI command dispatcher.

Handles all pytigon CLI commands including project management,
web server startup, script execution, and tool integration.
"""

import logging
import os
import sys

_logger = logging.getLogger("pytigon_run")


def _configure_logging() -> None:
    """Configure root logging for the CLI process.

    Deliberately called from ``run`` (the process entry point) rather than at
    import time, so that importing this module — for example from an application
    that embeds Pytigon, from the GUI, or from tests — does not take over the
    embedding process's logging configuration.
    """
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def _setup_process_environment(argv: list[str]) -> list[str]:
    """Apply CLI/environment setup previously done at import time.

    Sets the working-directory and secret-key environment variables, and strips
    the ``--dev`` / ``--script-mode`` convenience flags from ``argv`` so the
    dispatcher only sees real commands.

    Args:
        argv: The raw command-line arguments.

    Returns:
        The cleaned argument list (flags removed).
    """
    os.environ["START_PATH"] = os.path.abspath(os.getcwd())
    os.environ["XKB_CONFIG_ROOT"] = "/usr/share/X11/xkb"

    if not ("SECRET_KEY" in os.environ or "PYTIGON_SECRET_KEY" in os.environ):
        import secrets

        os.environ["SECRET_KEY"] = secrets.token_hex(50)

    argv = list(argv)

    if "--dev" in argv or "ptig.py" in argv:
        if "--dev" in argv:
            argv.remove("--dev")
        os.environ["PYTIGON_PRJ_PATH"] = os.path.join(os.environ["START_PATH"], "prj")
        os.environ["PYTIGON_DEBUG"] = "1"
        if not os.path.exists(os.environ["PYTIGON_PRJ_PATH"]):
            os.environ["PYTIGON_PRJ_PATH"] = os.environ["START_PATH"]

    if "--script-mode" in argv:
        argv.remove("--script-mode")
        os.environ["SCRIPT_MODE"] = "1"

    return argv


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------


def run(param=None):
    """Main entry point for Pytigon CLI.

    Uses the command dispatcher architecture for maintainability and security.

    Args:
        param: Optional list of command-line arguments (overrides sys.argv).
    """
    try:
        _configure_logging()

        from pytigon.commands import CommandDispatcher

        argv = param if param is not None else sys.argv
        argv = _setup_process_environment(argv)

        base_path = os.path.abspath(os.getcwd())
        ext_lib_path = os.path.join(base_path, "ext_lib")
        if ext_lib_path not in sys.path:
            sys.path.append(ext_lib_path)

        os.environ["PYTIGON_ROOT_PATH"] = os.path.dirname(os.path.abspath(__file__))

        dispatcher = CommandDispatcher()
        return dispatcher.dispatch(argv)

    except Exception as e:
        _logger.error("Error in command dispatcher: %s", e)
        return 1


if __name__ == "__main__":
    run(sys.argv)
