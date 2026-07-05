#!/usr/bin/env python
"""Extract translatable strings from Python/HTML/JS files into .po files.

This script uses xgettext from GNU gettext to scan project files for
translatable strings and generates or updates .po files for the specified
languages.
"""

import getopt
import os
import re
import subprocess
import sys
import tempfile

from django.conf import settings

settings.configure(use_i18n=True)
from django.utils.translation import templatize

pythonize_re = re.compile(r"\n\s*//")

# Domain constants
DOMAIN_DJANGO = "django"
DOMAIN_DJANGOJS = "djangojs"


def find_xgettext():
    """Find the xgettext executable on the system.

    Returns:
        str: Path to xgettext executable, or None if not found.
    """
    for name in ("xgettext", "xgettext.exe"):
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
    candidates = [
        r"C:\Programy\GnuWin32\bin\xgettext.exe",
        r"C:\Program Files\GnuWin32\bin\xgettext.exe",
        r"C:\Program Files (x86)\GnuWin32\bin\xgettext.exe",
        r"C:\msys64\usr\bin\xgettext.exe",
        r"C:\cygwin\bin\xgettext.exe",
    ]
    for candidate in candidates:
        if os.path.isfile(candidate):
            return candidate

    return None


def find_msguniq():
    """Find the msguniq executable on the system.

    Returns:
        str: Path to msguniq executable, or None if not found.
    """
    for name in ("msguniq", "msguniq.exe"):
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
    return None


def find_msgmerge():
    """Find the msgmerge executable on the system.

    Returns:
        str: Path to msgmerge executable, or None if not found.
    """
    for name in ("msgmerge", "msgmerge.exe"):
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
    return None


def run_xgettext(filepath, domain, potfile_exists, xgettext_cmd):
    """Run xgettext on a single file and return the output.

    Args:
        filepath: Path to the file to process.
        domain: Translation domain (django or djangojs).
        potfile_exists: Whether a .pot file already exists.
        xgettext_cmd: Path to xgettext executable.

    Returns:
        bytes: Output from xgettext, or empty bytes on failure.
    """
    lang = "Perl" if domain == DOMAIN_DJANGOJS else "Python"
    omit_header = "--omit-header" if potfile_exists else ""

    cmd = [
        xgettext_cmd,
        "-d",
        domain,
        "-L",
        lang,
        "--keyword=gettext_noop",
        "--keyword=gettext_lazy",
        "--keyword=ngettext_lazy",
        "-o",
        "-",
        filepath,
    ]
    if omit_header:
        cmd.insert(1, omit_header)

    try:
        result = subprocess.run(cmd, capture_output=True)
        if result.stderr:
            sys.stderr.write(
                "Errors while running xgettext on {}:\n{}\n".format(
                    os.path.basename(filepath),
                    result.stderr.decode("utf-8", errors="replace"),
                )
            )
        return result.stdout
    except OSError as e:
        sys.stderr.write(
            f"OS error running xgettext on {os.path.basename(filepath)}: {e}\n"
        )
        return b""


def make_messages():
    """Main entry point: scan files, extract strings, and update .po files."""
    # Determine locale directory
    localedir = None
    if os.path.isdir(os.path.join("conf", "locale")):
        localedir = os.path.abspath(os.path.join("conf", "locale"))
    elif os.path.isdir("locale"):
        localedir = os.path.abspath("locale")
    else:
        print(
            "This script should be run from the Django source tree or "
            "your project or app tree."
        )
        print(
            "If you did indeed run it from the checkout or your project or application,"
        )
        print(
            "maybe you are just missing the conf/locale (in the django tree) "
            "or locale (for project"
        )
        print("and application) directory?")
        print(
            "make-messages.py doesn't create it automatically, you have to "
            "create it by hand if"
        )
        print("you want to enable i18n for your project or application.")
        sys.exit(1)

    # Parse command-line options
    (opts, args) = getopt.getopt(sys.argv[1:], "l:d:va")
    lang = None
    domain = DOMAIN_DJANGO
    verbose = False
    all_languages = False

    for o, v in opts:
        if o == "-l":
            lang = v
        elif o == "-d":
            domain = v
        elif o == "-v":
            verbose = True
        elif o == "-a":
            all_languages = True

    if domain not in (DOMAIN_DJANGO, DOMAIN_DJANGOJS):
        print(
            "Currently make-messages.py only supports domains 'django' and 'djangojs'"
        )
        sys.exit(1)

    if lang is None and not all_languages:
        print("Usage: make-messages.py -l <language>")
        print("   or: make-messages.py -a")
        sys.exit(1)

    # Find required tools
    xgettext_cmd = find_xgettext()
    if not xgettext_cmd:
        print("Error: xgettext not found. Please install gettext utilities.")
        sys.exit(1)

    msguniq_cmd = find_msguniq()
    msgmerge_cmd = find_msgmerge()

    # Build language list
    languages = []
    if lang is not None:
        languages.append(lang)
    elif all_languages:
        languages = [el for el in os.listdir(localedir) if not el.startswith(".")]

    with tempfile.TemporaryDirectory() as tmpdir:
        for lang in languages:
            print(f"Processing language: {lang}")
            basedir = os.path.join(localedir, lang, "LC_MESSAGES")
            if not os.path.isdir(basedir):
                os.makedirs(basedir)

            pofile = os.path.join(basedir, f"{domain}.po")
            potfile = os.path.join(basedir, f"{domain}.pot")

            # Remove old pot file
            if os.path.exists(potfile):
                os.unlink(potfile)

            potfile_exists = False

            for dirpath, _dirnames, filenames in os.walk("."):
                for file in filenames:
                    if domain == DOMAIN_DJANGOJS and file.endswith(".js"):
                        if verbose:
                            sys.stdout.write(
                                f"Processing file {file} in {dirpath}\n"
                            )
                        src_path = os.path.join(dirpath, file)
                        with open(src_path, "rb") as fh:
                            src = fh.read()

                        src = pythonize_re.sub(b"\n#", src)

                        # Create temporary Python version
                        tmp_py_path = os.path.join(
                            tmpdir, file.replace("/", "_") + ".py"
                        )
                        with open(tmp_py_path, "wb") as fh:
                            fh.write(src)

                        msgs = run_xgettext(
                            tmp_py_path, domain, potfile_exists, xgettext_cmd
                        )

                        # Fix path references in output
                        old_ref = ("#: " + tmp_py_path).encode("utf-8")
                        new_ref = ("#: " + os.path.join(dirpath, file)[2:]).encode(
                            "utf-8"
                        )
                        msgs = msgs.replace(old_ref, new_ref)

                        if msgs:
                            with open(potfile, "ab") as fh:
                                fh.write(msgs)
                            potfile_exists = True

                    elif domain == DOMAIN_DJANGO and (
                        file.endswith(".py") or file.endswith(".html")
                    ):
                        thefile = file
                        tmp_py_path = os.path.join(dirpath, file)

                        if file.endswith(".html"):
                            src_path = os.path.join(dirpath, file)
                            with open(src_path, "rb") as fh:
                                src = fh.read()

                            tmp_py_path = os.path.join(
                                tmpdir, file.replace("/", "_") + ".py"
                            )
                            with open(tmp_py_path, "wb") as fh:
                                fh.write(templatize(src))

                            thefile = tmp_py_path

                        if verbose:
                            sys.stdout.write(
                                f"Processing file {file} in {dirpath}\n"
                            )

                        msgs = run_xgettext(
                            thefile, domain, potfile_exists, xgettext_cmd
                        )

                        # Fix path references if using temp file
                        if file.endswith(".html"):
                            old_ref = ("#: " + thefile).encode("utf-8")
                            new_ref = ("#: " + os.path.join(dirpath, file)[2:]).encode(
                                "utf-8"
                            )
                            msgs = msgs.replace(old_ref, new_ref)

                        if msgs:
                            with open(potfile, "ab") as fh:
                                fh.write(msgs)
                            potfile_exists = True

            # Run msguniq on the pot file
            if os.path.exists(potfile) and msguniq_cmd:
                try:
                    with open(potfile, "rb") as fh:
                        pot_data = fh.read()

                    result = subprocess.run(
                        [msguniq_cmd, potfile],
                        capture_output=True,
                    )
                    if result.stderr:
                        sys.stderr.write(
                            "Errors while running msguniq:\n{}\n".format(result.stderr.decode("utf-8", errors="replace"))
                        )

                    msgs = result.stdout

                    with open(potfile, "wb") as fh:
                        fh.write(msgs)
                except OSError as e:
                    sys.stderr.write(f"OS error running msguniq: {e}\n")

                # Merge with existing po file
                if os.path.exists(pofile) and msgmerge_cmd:
                    try:
                        result = subprocess.run(
                            [msgmerge_cmd, "-q", pofile, potfile],
                            capture_output=True,
                        )
                        if result.stderr:
                            sys.stderr.write(
                                "Errors while running msgmerge:\n{}\n".format(result.stderr.decode("utf-8", errors="replace"))
                            )

                        if result.stdout:
                            with open(pofile, "wb") as fh:
                                fh.write(result.stdout)
                    except OSError as e:
                        sys.stderr.write(f"OS error running msgmerge: {e}\n")
                elif os.path.exists(potfile):
                    # No existing po file, copy pot content
                    with open(potfile, "rb") as fh:
                        pot_content = fh.read()
                    with open(pofile, "wb") as fh:
                        fh.write(pot_content)

                # Clean up pot file
                if os.path.exists(potfile):
                    os.unlink(potfile)


if __name__ == "__main__":
    make_messages()
