#!/usr/bin/env python
import os
import sys

from schlib import init_paths
init_paths()

base_path = __file__.replace("pytigon_android_service.py", "")
if base_path == "":
    base_path = "./"
else:
    os.chdir(base_path)

sys.path.insert(0,base_path)
sys.path.insert(0,os.path.join(base_path, "_android"))

from schserw import settings
from os import environ

#if 'PYTIGON_APP' in environ:
#    sys.path.insert(0,os.path.join(settings.APP_PACK_PATH, environ['PYTIGON_APP']))
#else:
#    sys.path.insert(0,os.path.join(settings.APP_PACK_PATH, '_schall'))

if 'PYTHON_SERVICE_ARGUMENT' in environ:
    print("python:Pytigon:arg:", environ['PYTHON_SERVICE_ARGUMENT'])
    sys.path.insert(0,os.path.join(settings.APP_PACK_PATH, environ['PYTHON_SERVICE_ARGUMENT']))
else:
    sys.path.insert(0,os.path.join(settings.APP_PACK_PATH, '_schall'))

    
#sys.path.insert(0,os.path.join(base_path, "python/lib/python%d.%d/site-packages" % (sys.version_info[0], sys.version_info[1]) ))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'settings_app')

from django.core.wsgi import get_wsgi_application
import django
import schserw.schsys.initdjango
django.setup()
schserw.schsys.initdjango.init_django()


application = get_wsgi_application()

if __name__ == '__main__': 
    import cherrypy

    cherrypy.tree.graft(application, "/")
    cherrypy.server.unsubscribe()

    server = cherrypy._cpserver.Server()
    server.socket_host = "0.0.0.0"
    server.socket_port = 8000
    server.thread_pool = 2
    server.subscribe()

    cherrypy.engine.start()
    cherrypy.engine.block()

#if __name__ == "__main__":
#    from schlib.schdjangoext.server import run_server
#    run_server('0.0.0.0', 8000, prod=False)
