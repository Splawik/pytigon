import os, sys

home = os.path.dirname(__file__)
if not home:
    home=os.getcwd()

sys.path.append(home + "/../..")
sys.path.append(home)
sys.path.insert(0, home + '/../../ext_lib')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'settings_app')

from django.core.wsgi import get_wsgi_application

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
