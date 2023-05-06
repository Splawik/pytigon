import sys
from django.conf import settings
from pytigon_lib.schtools.install_init import pip_install

sys.argv = sys.argv[:-1]
import os

os.chdir(os.path.expanduser("~"))

prjlib = os.path.join(settings.DATA_PATH, settings.PRJ_NAME, "prjlib")
notebook_path = os.path.join(prjlib, "notebook")

if not os.path.exists(notebook_path):
    pip_install("notebook jupytext --pre", prjlib)

try:
    from notebook.app import main

    sys.exit(main())
except ImportError:
    from notebook import notebookapp as app

    app.launch_new_instance()
