# -*- coding: utf-8 -*-
import os, sys

_lp = os.path.abspath(__file__.replace("wsgi.py", ""))

if 'PYTIGON_ROOT_PATH' in os.environ:
    _rp = os.environ['PYTIGON_ROOT_PATH']
else:
    _rp = os.path.abspath(os.path.join(_lp, "../../"))

sys.path.insert(0,_lp)
sys.path.insert(0,_rp)

from schlib import init_paths
init_paths()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'settings_app')

import django
from django.core.wsgi import get_wsgi_application
django.setup()

application = get_wsgi_application()
