"""Pytigon main runner and CLI command dispatcher.

Handles all pytigon CLI commands including project management,
web server startup, script execution, and tool integration.
"""

import logging
import os
import sys

# ---------------------------------------------------------------------------
# Early initialization
# ---------------------------------------------------------------------------

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
_logger = logging.getLogger("pytigon_run")

# Add pytigon_lib to path if available
try:
    from pytigon_lib.schtools.tools import get_executable
except ImportError:

    def get_executable():
        """Return the Python executable path."""
        return sys.executable

    _logger.debug("Using system Python executable as fallback")


# Set environment variables
os.environ["START_PATH"] = os.path.abspath(os.getcwd())
os.environ["XKB_CONFIG_ROOT"] = "/usr/share/X11/xkb"

# Set secret key if not provided (generates random key for dev)
if not ("SECRET_KEY" in os.environ or "PYTIGON_SECRET_KEY" in os.environ):
    import secrets

    os.environ["SECRET_KEY"] = secrets.token_hex(50)

# Handle --dev flag: use local project paths for development
if "--dev" in sys.argv or "ptig.py" in sys.argv:
    if "--dev" in sys.argv:
        sys.argv.remove("--dev")
    os.environ["PYTIGON_PRJ_PATH"] = os.path.join(os.environ["START_PATH"], "prj")
    os.environ["PYTIGON_DEBUG"] = "1"
    if not os.path.exists(os.environ["PYTIGON_PRJ_PATH"]):
        os.environ["PYTIGON_PRJ_PATH"] = os.environ["START_PATH"]

# Handle --script-mode flag
if "--script-mode" in sys.argv:
    sys.argv.remove("--script-mode")
    os.environ["SCRIPT_MODE"] = "1"


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
        from pytigon.commands import CommandDispatcher

        argv = param if param else sys.argv

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
