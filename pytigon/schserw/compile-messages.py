#!/usr/bin/env python

"""Compile .po translation files to .mo binary format.

This script walks through a locale directory and compiles all .po files
found into .mo files using the `msgfmt` command from gettext.

Search order for the locale directory:
    1. conf/locale (Django source tree layout)
    2. locale (project/app layout)
"""

import logging
import os
import shutil
import subprocess
import sys

_logger = logging.getLogger(__name__)


def find_msgfmt():
    """Find the msgfmt executable on the system.

    Returns:
        str: Path to the msgfmt executable, or None if not found.
    """
    # shutil.which searches PATH on the current platform, so this replaces the
    # previous hand-rolled probe plus a hard-coded list of GnuWin32/MSYS/Cygwin
    # install paths that only ever matched one developer's machine.
    for name in ("msgfmt", "msgfmt.exe"):
        found = shutil.which(name)
        if found:
            return found
    return None


def find_locale_dir():
    """Locate the locale directory to compile.

    Returns:
        str: Absolute path to the locale directory, or None if not found.
    """
    for candidate in (os.path.join("conf", "locale"), "locale"):
        if os.path.isdir(candidate):
            return os.path.abspath(candidate)
    return None


def compile_messages(base_dir=None, msgfmt_cmd=None):
    """Compile every .po file under a locale directory.

    Args:
        base_dir: Locale directory. Defaults to :func:`find_locale_dir`.
        msgfmt_cmd: Path to msgfmt. Defaults to :func:`find_msgfmt`.

    Returns:
        bool: True when all files compiled without error.
    """
    if base_dir is None:
        base_dir = find_locale_dir()
    if base_dir is None:
        _logger.error(
            "No locale directory found; run this from the Django source tree "
            "or from your project/app tree."
        )
        return False

    if msgfmt_cmd is None:
        msgfmt_cmd = find_msgfmt()
    if not msgfmt_cmd:
        _logger.error(
            "msgfmt not found. Install the gettext utilities "
            "(Linux: apt-get install gettext, macOS: brew install gettext, "
            "Windows: install MSYS2 or GnuWin32 and put it on PATH)."
        )
        return False

    errors_occurred = False
    for dirpath, _dirnames, filenames in os.walk(base_dir):
        for fname in filenames:
            if not fname.endswith(".po"):
                continue
            _logger.info("Processing %s in %s", fname, dirpath)
            pf = os.path.splitext(os.path.join(dirpath, fname))[0]
            try:
                result = subprocess.run(
                    [msgfmt_cmd, "-o", pf + ".mo", pf + ".po"],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                if result.returncode != 0:
                    _logger.error("Error processing %s:\n%s", fname, result.stderr)
                    errors_occurred = True
            except OSError as e:
                _logger.error("OS error processing %s: %s", fname, e)
                errors_occurred = True

    return not errors_occurred


def main(argv=None):
    """Entry point.

    Args:
        argv: Unused; present so the signature matches the other build scripts.

    Returns:
        int: Process exit code.
    """
    logging.basicConfig(format="%(message)s")
    return 0 if compile_messages() else 1


if __name__ == "__main__":
    sys.exit(main())
