import os, sys

base_path = __file__.replace("asgi.py", "")
if base_path == "":
    base_path = "./"
else:
    os.chdir(base_path)

sys.path.insert(0,base_path + "./")
sys.path.insert(0,base_path + "../../python/lib/python%d.%d/site-packages" % (sys.version_info[0], sys.version_info[1]))
sys.path.insert(0,base_path + "../..")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'settings_app')


from channels.asgi import get_channel_layer


from django.core.wsgi import get_wsgi_application
import django
import schserw.schsys.initdjango
django.setup()
schserw.schsys.initdjango.init_django()


channel_layer = get_channel_layer()
