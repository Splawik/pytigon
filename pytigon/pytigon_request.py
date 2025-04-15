import os
import sys

from pytigon_lib.schtools.main_paths import get_main_paths
from pytigon_lib.schhttptools import httpclient
from django.conf import settings

HTTP = None


def init(
    prj, username=None, password=None, user_agent="pytigon", create_auto_user=False
):
    global HTTP

    paths = get_main_paths(prj)
    prj_path = os.path.join(paths["PRJ_PATH"], prj)
    if prj_path not in sys.path:
        sys.path.append(prj_path)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings_app")
    httpclient.init_embeded_django()

    if create_auto_user:
        from django.contrib.auth.models import User

        User.objects.create_superuser("auto", "auto@pytigon.cloud", "anawa")

    HTTP = httpclient.HttpClient("http://127.0.0.2")

    if username:
        parm = {"username": username, "password": password, "next": "/schsys/ok/"}
        HTTP.post(
            None,
            "http://127.0.0.2/"
            + (settings.URL_ROOT_PREFIX if settings.URL_ROOT_FOLDER else "")
            + "schsys/do_login/",
            parm,
            credentials=(username, password),
            user_agent=user_agent,
        )


def request(url, params=None, user_agent="pytigon"):
    if params:
        response = HTTP.post(None, url, params, user_agent=user_agent)
    else:
        response = HTTP.get(None, url, user_agent=user_agent)
    return response
