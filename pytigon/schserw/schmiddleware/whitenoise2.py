import os
from django.conf import settings
from whitenoise.middleware import WhiteNoiseMiddleware
from pytigon_lib.schdjangoext.django_init import AppConfigMod

class WhiteNoiseMiddleware2(WhiteNoiseMiddleware):
    def __init__(self, get_response=None, settings=settings):
        WhiteNoiseMiddleware.__init__(self, get_response, settings)
        if self.static_root:
            for app in settings.INSTALLED_APPS:
                if isinstance(app, AppConfigMod):
                    app_path = os.path.abspath(os.path.dirname(app.module.__file__))
                    prj_path = os.path.split(app_path)[0]
                    prj_name = os.path.split(prj_path)[-1]
                    static_path = os.path.join(prj_path, "static", prj_name)
                    self.add_files(static_path, prefix=self.static_prefix + prj_name + "/")
                    print(static_path, self.static_prefix + prj_name + "/")