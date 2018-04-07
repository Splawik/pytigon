#!/usr/bin/env python
import os
import sys

print("python:Pytigon:Z1")

from schlib import init_paths
init_paths()

print("python:Pytigon:Z2")

base_path = __file__.replace("pytigon_android_service.py", "")
if base_path == "":
    base_path = "./"
else:
    os.chdir(base_path)

print("python:Pytigon:Z3")

sys.path.insert(0,base_path)
sys.path.insert(0,os.path.join(base_path, "_android"))

print("python:Pytigon:Z4")

from schserw import settings
from os import environ

print("python:Pytigon:Z5")

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

print("python:Pytigon:Z6")

from django.core.wsgi import get_wsgi_application
import django
print("python:Pytigon:Z7")
import schserw.schsys.initdjango
print("python:Pytigon:Z8")
django.setup()
print("python:Pytigon:Z9")
schserw.schsys.initdjango.init_django()
print("python:Pytigon:Z10")


application = get_wsgi_application()

print("python:Pytigon:Z11")

if __name__ == '__main__': 
    import cherrypy
    print("python:Pytigon:Z12")
    cherrypy.config.update({
         'global': {
            'environment' : 'production'
          }
    })

    cherrypy.tree.graft(application, "/")
    cherrypy.server.unsubscribe()
    print("python:Pytigon:Z13")
    server = cherrypy._cpserver.Server()
    server.socket_host = "0.0.0.0"
    server.socket_port = 8000
    server.thread_pool = 4
    print("python:Pytigon:Z14")
    server.subscribe()
    print("python:Pytigon:Z15")
    cherrypy.engine.start()
    print("python:Pytigon:Z16")
    cherrypy.engine.block()
    print("python:Pytigon:Z17")