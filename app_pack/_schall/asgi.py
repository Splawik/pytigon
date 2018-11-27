import os, sys

base_path = os.path.abspath(__file__.replace("asgi.py", ""))

if 'PYTIGON_ROOT_PATH' in os.environ:
    _rp = os.environ['PYTIGON_ROOT_PATH']
else:
    _rp = os.path.abspath(os.path.join(base_path, "../../"))

sys.path.insert(0,base_path)
sys.path.insert(0,_rp)

from schlib import init_paths
init_paths()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'settings_app')

import django
from channels.routing import get_default_application
django.setup()

application = get_default_application()
