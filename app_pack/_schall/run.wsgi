import os, sys

base_path = __file__.replace("run.wsgi", "")
if base_path == "":
    base_path = "./"
else:
    os.chdir(base_path)

sys.path.insert(0,base_path + "./")
sys.path.insert(0,base_path + "../../ext_lib")
sys.path.insert(0,base_path + "../..")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'settings_app')

from django.core.wsgi import get_wsgi_application
import django
import schserw.schsys.initdjango
django.setup()
schserw.schsys.initdjango.init_django()

application = get_wsgi_application()

if __name__ == '__main__': 
    import cherrypy
    from schlib.schtasks.cherrypy_task import subscribe,  get_process_manager

    cherrypy.tree.graft(application, "/")
    cherrypy.server.unsubscribe()

    server = cherrypy._cpserver.Server()
    server.socket_host = "0.0.0.0"
    server.socket_port = 8080
    server.thread_pool = 10
    server.subscribe()

    subscribe()
    get_process_manager()

    cherrypy.engine.start()
    cherrypy.engine.block()