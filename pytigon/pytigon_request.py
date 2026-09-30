"""HTTP request helpers for pytigon's embedded Django client.

Provides initialization and simplified HTTP request functions that work
with pytigon's embedded Django HTTP client. Used by GUI and script modes
to communicate with the internal Django server.
"""

import logging
import os
import sys
from urllib.parse import urljoin

from pytigon_lib.schdjangoext.tools import make_href
from pytigon_lib.schhttptools import httpclient
from pytigon_lib.schtools.env import get_environ
from pytigon_lib.schtools.main_paths import get_main_paths

HTTP = None
_logger = logging.getLogger("pytigon_request")


def init(
    prj,
    username=None,
    password=None,
    user_agent="pytigon",
    create_auto_user=False,
    ptig_installer=None,
    path_alt=True,
):
    """Initialize the pytigon HTTP client for embedded Django communication.

    Args:
        prj: Project name.
        username: Optional login username.
        password: Optional login password.
        user_agent: User-Agent string for HTTP requests (default: "pytigon").
        create_auto_user: If True, create an 'auto' superuser.
        ptig_installer: Optional .ptig archive data. Can be bytes (binary data),
            a str file path, or a file-like object.
        path_alt: If True, extract ptig archive using alternative path logic.
    """
    global HTTP

    if ptig_installer:
        import io

        from pytigon_lib.schtools.install import Ptig

        if isinstance(ptig_installer, bytes):
            ptig_file = io.BytesIO(ptig_installer)
            ptig = Ptig(ptig_file)
        elif isinstance(ptig_installer, str):
            with open(ptig_installer, "rb") as ptig_file:
                ptig = Ptig(ptig_file)
        else:
            ptig = Ptig(ptig_installer)
        ptig.extract_ptig(path_alt)

    paths = get_main_paths(prj)
    prj_path = os.path.join(paths["PRJ_PATH"], prj)
    if prj_path not in sys.path:
        sys.path.append(prj_path)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings_app")

    httpclient.init_embeded_django()

    if create_auto_user:
        from django.contrib.auth import get_user_model
        from django.db import transaction

        env = get_environ()
        username = env("AUTOUSERNAME")
        password = env("AUTOPASSWORD")

        # get_user_model() respects a custom AUTH_USER_MODEL; importing
        # django.contrib.auth.models.User would break it.
        UserModel = get_user_model()
        lookup = {UserModel.USERNAME_FIELD: username}
        # get_or_create() is atomic and removes the get()-then-create() race
        # that could create two superusers (or raise IntegrityError) when two
        # embedded servers start concurrently.
        with transaction.atomic():
            user, created = UserModel._default_manager.get_or_create(**lookup)
            if created:
                user.set_password(password)
                user.is_staff = True
                user.is_superuser = True
                if hasattr(user, "email"):
                    user.email = "auto@pytigon.cloud"
                user.save()

    HTTP = httpclient.HttpClient("http://127.0.0.2")

    if username:
        parm = {"username": username, "password": password, "next": "/schsys/ok/"}
        HTTP.post(
            None,
            urljoin("http://127.0.0.2", make_href("/schsys/do_login/")),
            parm,
            credentials=(username, password),
            user_agent=user_agent,
        )


def request(url, params=None, user_agent="pytigon"):
    """Send an HTTP request via the embedded client.

    Args:
        url: Target URL path.
        params: Optional POST parameters. If None, a GET request is sent.
        user_agent: User-Agent string (default: "pytigon").

    Returns:
        The HTTP response object.

    Raises:
        RuntimeError: If init() has not been called before request().
    """
    if HTTP is None:
        raise RuntimeError("HTTP client not initialized. Call pytigon_request.init() first.")

    try:
        if params:
            return HTTP.post(None, url, params, user_agent=user_agent)
        else:
            return HTTP.get(None, url, user_agent=user_agent)
    except Exception as e:
        _logger.error("HTTP request failed for URL %s: %s", url, e)
        raise
