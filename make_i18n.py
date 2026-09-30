import os
import sys

import polib

# Imported as a package module: a bare "ext_lib.pygettext" only resolved when
# this script happened to be run from inside the pytigon package directory.
from pytigon.ext_lib.pygettext import main as gtext

ARGV = sys.argv


def make_messages(src_path, path, name, outpath=None):

    sys.argv = [None, "-a", "-d", name, "-p", path]

    for root, _dirs, files in os.walk(src_path):
        for f in files:
            if f.endswith(".py"):
                p = os.path.join(root, f)
                sys.argv.append(p)
    gtext()

    wzr_filename = os.path.join(path, name + ".pot")
    for pos in os.scandir(path):
        if pos.is_dir():
            lang = pos.name
            ftmp = os.path.join(path, lang)
            if outpath:
                ftmp = os.path.join(ftmp, outpath)
            filename = os.path.join(ftmp, name + ".po")
            old_filename = filename.replace(".po", ".bak")
            mo_filename = filename.replace(".po", ".mo")
            try:
                os.remove(old_filename)
            except FileNotFoundError:
                pass
            try:
                os.rename(filename, old_filename)
            except (FileNotFoundError, OSError):
                pass
            wzr = polib.pofile(wzr_filename)
            po = polib.pofile(old_filename)
            po.merge(wzr)
            po.save(filename)
            po.save_as_mofile(mo_filename)


if len(ARGV) < 2:
    make_messages("./pytigon_gui", "./pytigon_gui/locale", "pytigon")
else:
    for app_name in ARGV[1:]:
        path1 = os.path.join("./prj", app_name)
        path2 = os.path.join(path1, "locale")
        make_messages(path1, path2, "django", "LC_MESSAGES")
