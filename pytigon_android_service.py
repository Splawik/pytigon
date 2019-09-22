#!/usr/bin/env python
import os
import sys

base_path = os.path.dirname(os.path.abspath(__file__))
if not base_path in sys.path:
    sys.path.insert(0, base_path)

from pytigon_lib import init_paths
init_paths()

from pytigon.schserw import settings

PRJ_NAME = "_schall"
PORT = '8000'

if 'PYTHON_SERVICE_ARGUMENT' in os.environ:
    PRJ_NAME = os.environ['PYTHON_SERVICE_ARGUMENT']
    app_path = os.path.join(settings.PRJ_PATH, PRJ_NAME)
    if not app_path in sys.path:
        sys.path.insert(0,app_path)


if __name__ == '__main__':
    from pytigon.pytigon_run import run
    cmd = ['android', 'runserver_' + PRJ_NAME, '-b', '0.0.0.0', '-p', PORT]
    run(cmd)
