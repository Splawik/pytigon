import os
import sys

base_path = __file__.replace("wsgi.py", "")
if base_path == "":
    base_path = "./"
else:
    os.chdir(base_path)

base_path += "prj/_schall/"


sys.path.insert(0,base_path + "./")
sys.path.insert(
    0,
    base_path
    + f"../../python/lib/python{sys.version_info[0]}.{sys.version_info[1]}/site-packages",
)
sys.path.insert(0,base_path + "../..")

# The imports below must stay after init_paths()/django.setup(): they rely on
# the project paths and settings being in place first.
# ruff: noqa: E402
from pytigon_lib import init_paths

init_paths()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'settings_app')

import django
from django.core.wsgi import get_wsgi_application

django.setup()

application = get_wsgi_application()

if __name__ == '__main__':
    from pytigon_lib.schdjangoext.server import run_server
    run_server('0.0.0.0', 8080)
