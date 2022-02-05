import os, sys

base_path = __file__.replace("asgi.py", "")
if base_path == "":
    base_path = "./"
else:
    os.chdir(base_path)

sys.path.insert(0, base_path + "./prj")
sys.path.insert(
    0,
    base_path
    + "python/lib/python%d.%d/site-packages"
    % (sys.version_info[0], sys.version_info[1]),
)
sys.path.insert(0, base_path)
sys.path.insert(0, base_path + "ext_lib")


sys_modules = {}
for key in sys.modules:
    sys_modules[key] = sys.modules[key]


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "_schall.settings_app")

import django
from channels.routing import get_default_application

django.setup()

application1 = get_default_application()

import sys

# tab = {}
# for pos in sys.modules:
#    print(pos)
#    if not ( pos.startswith('django') or pos.startswith('channels') or pos.startswith('sch') or pos.startswith('_sch') or pos.startswith('daphne') ):
#        tab[pos] = sys.modules[pos]
# sys.modules = tab


# import sys
# if 'init_modules' in globals():
# 	for m in [x for x in sys.modules.keys() if x not in init_modules]:
# del(sys.modules[m])
# else:
# 	init_modules = sys.modules.keys()


sys.modules = sys_modules


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "schportal.settings_app")

import django
from channels.routing import get_default_application

django.setup()

application2 = get_default_application()


class application:
    def __init__(self, scope):
        print("X1:", scope)
        self.app = application2(scope)

    async def __call__(self, receive, send):
        return await self.app(receive, send)
