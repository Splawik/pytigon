import os
from django.conf import settings
from whitenoise.middleware import WhiteNoiseMiddleware
from pytigon_lib.schdjangoext.django_init import AppConfigMod
from django.core.files.storage import default_storage
from fs.osfs import OSFS
from django.http import HttpResponseNotFound


class WhiteNoiseMiddleware2(WhiteNoiseMiddleware):
    def __init__(self, get_response=None, settings=settings):
        """
        Initialize the WhiteNoiseMiddleware2 instance.

        :param get_response: The callable producing the response for the current
            request.
        :param settings: The Django settings module to use when initializing the
            middleware.
        :type settings: django.conf.Settings
        """
        WhiteNoiseMiddleware.__init__(self, get_response, settings)
        if self.static_root:
            maps = {}
            for app in settings.INSTALLED_APPS:
                if isinstance(app, AppConfigMod):
                    app_path = os.path.abspath(os.path.dirname(app.module.__file__))
                    prj_path = os.path.split(app_path)[0]
                    prj_name = os.path.split(prj_path)[-1]
                    static_path = os.path.join(prj_path, "static", prj_name)
                    if prj_name not in maps:
                        maps[prj_name] = [
                            static_path,
                            self.static_prefix + prj_name + "/",
                        ]
            fs = None
            if default_storage.fs:
                for pos in default_storage.fs.mounts:
                    if pos[0] == "/static/":
                        fs = pos[1]
                        break
            for key in maps:
                pos = maps[key]
                self.add_files(pos[0], prefix=pos[1])
                if fs:
                    if os.path.exists((pos[0])):
                        fs.add_fs(key, OSFS(pos[0]))

    def __call__(self, request):
        """
        Process the request and return the response.

        If the request path contains "/static", WhiteNoise will attempt to
        serve the static file from the configured static root directory.
        Otherwise, the request will be passed to the next middleware in the
        chain.

        If the request ends with ".map", WhiteNoise will return a 404 response
        because source maps are not served by WhiteNoise.

        :param request: The request object.
        :type request: django.http.HttpRequest
        :return: The response object.
        :rtype: django.http.HttpResponse
        """
        response = None
        if "/static" in request.path:
            response = self.process_request(request)
        if response is None:
            if not request.path.endswith(".map"):
                response = self.get_response(request)
            else:
                response = HttpResponseNotFound(
                    "File: " + request.path + " does'nt exists"
                )
        return response
