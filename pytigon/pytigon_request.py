import os
import sys

from pytigon_lib.schtools.main_paths import get_main_paths
from pytigon_lib.schhttptools import httpclient

HTTP = None


def init(prj, username, password, user_agent="pytigon"):
    global HTTP

    paths = get_main_paths(prj)
    prj_path = os.path.join(paths["PRJ_PATH"], prj)
    if not prj_path in sys.path:
        sys.path.append(prj_path)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings_app")
    httpclient.init_embeded_django()
    HTTP = httpclient.HttpClient("http://127.0.0.2")

    if username:
        parm = {"username": username, "password": password, "next": "/schsys/ok/"}
        response = HTTP.post(
            None,
            "/schsys/do_login/",
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
