import os, sys

base_path = __file__.replace("wsgi.py", "")
if base_path == "":
    base_path = "./"
else:
    os.chdir(base_path)

base_path += "app_pack/_schall/"


sys.path.insert(0,base_path + "./")
sys.path.insert(0,base_path + "../../python/lib/python%d.%d/site-packages" % (sys.version_info[0], sys.version_info[1]))
sys.path.insert(0,base_path + "../..")

from schlib import init_paths
init_paths()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'settings_app')

from django.core.wsgi import get_wsgi_application
import django
import schserw.schsys.initdjango
django.setup()
schserw.schsys.initdjango.init_django()

application = get_wsgi_application()

if __name__ == '__main__': 
    from schlib.schdjangoext.server import run_server
    run_server('0.0.0.0', 8080)
