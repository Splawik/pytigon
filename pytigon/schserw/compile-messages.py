#!/usr/bin/env python

"""Compile .po translation files to .mo binary format.

This script walks through a locale directory and compiles all .po files
found into .mo files using the `msgfmt` command from gettext.

Search order for the locale directory:
    1. conf/locale (Django source tree layout)
    2. locale (project/app layout)
"""

import os
import subprocess
import sys


def find_msgfmt():
    """Find the msgfmt executable on the system.

    Returns:
        str: Path to msgfmt executable, or None if not found.
    """
    # Common names for msgfmt
    for name in ("msgfmt", "msgfmt.exe"):
        try:
            result = subprocess.run(
                [name, "--version"],
                capture_output=True,
                timeout=5,
            )
            if result.returncode == 0:
                return name
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue

    # Try common Windows paths
    windows_candidates = [
        r"C:\Programy\GnuWin32\bin\msgfmt.exe",
        r"C:\Program Files\GnuWin32\bin\msgfmt.exe",
        r"C:\Program Files (x86)\GnuWin32\bin\msgfmt.exe",
        r"C:\msys64\usr\bin\msgfmt.exe",
        r"C:\cygwin\bin\msgfmt.exe",
    ]
    for candidate in windows_candidates:
        if os.path.isfile(candidate):
            return candidate

    return None


def compile_messages():
    """Main entry point: find locale directory and compile all .po files."""
    basedir = None
    if os.path.isdir(os.path.join("conf", "locale")):
        basedir = os.path.abspath(os.path.join("conf", "locale"))
    elif os.path.isdir("locale"):
        basedir = os.path.abspath("locale")
    else:
        print(
            "This script should be run from the Django source tree or "
            "your project or app tree."
        )
        sys.exit(1)

    msgfmt_cmd = find_msgfmt()
    if not msgfmt_cmd:
        print(
            "Error: msgfmt not found. Please install gettext utilities:\n"
            "  - Linux: apt-get install gettext / yum install gettext\n"
            "  - macOS: brew install gettext\n"
            "  - Windows: install GnuWin32 or MSYS2"
        )
        sys.exit(1)

    errors_occurred = False
    for dirpath, _dirnames, filenames in os.walk(basedir):
        for fname in filenames:
            if fname.endswith(".po"):
                sys.stderr.write("Processing file %s in %s\n" % (fname, dirpath))
                pf = os.path.splitext(os.path.join(dirpath, fname))[0]
                try:
                    result = subprocess.run(
                        [msgfmt_cmd, "-o", pf + ".mo", pf + ".po"],
                        capture_output=True,
                        text=True,
                    )
                    if result.returncode != 0:
                        sys.stderr.write(
                            "Error processing %s:\n%s\n" % (fname, result.stderr)
                        )
                        errors_occurred = True
                except OSError as e:
                    sys.stderr.write("OS error processing %s: %s\n" % (fname, e))
                    errors_occurred = True

    if errors_occurred:
        sys.exit(1)


if __name__ == "__main__":
    compile_messages()
