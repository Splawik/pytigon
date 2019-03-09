import sys
import os
from ext_lib.pygettext import main as gtext
import polib

ARGV = sys.argv

def make_messages(src_path, path, name, outpath=None):

    sys.argv = [None, '-a', '-d', name, '-p', path]

    for root, dirs, files in os.walk(src_path):
        for f in files:
            if f.endswith('.py'):
                p = os.path.join(root, f)
                sys.argv.append(p)
    gtext()

    wzr_filename = os.path.join(path, name+'.pot')
    for pos in os.scandir(path):
        if pos.is_dir():
            lang = pos.name
            ftmp = os.path.join(path, lang)
            if outpath:
                ftmp = os.path.join(ftmp, outpath)
            filename = os.path.join(ftmp, name + '.po')
            old_filename = filename.replace('.po', '.bak')
            mo_filename = filename.replace('.po', '.mo')
            try:
                os.remove(old_filename)
            except:
                pass
            try:
                os.rename(filename, old_filename)
            except:
                pass
            wzr = polib.pofile(wzr_filename)
            po = polib.pofile(old_filename)
            po.merge(wzr)
            po.save(filename)
            po.save_as_mofile(mo_filename)

if len(ARGV) < 2:
    make_messages('./schcli', './schcli/locale', 'pytigon')
else:
    for app_name in ARGV[1:]:
        path1 = os.path.join('./prj', app_name)
        path2 = os.path.join(path1, 'locale')
        make_messages(path1, path2, 'django', 'LC_MESSAGES')
