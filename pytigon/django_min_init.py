import os
import sys

def init(
    prj="schscripts",
    pytigon_standard=False,
    embeded_django=False,
    settings_callback=None,
):
    os.environ["DJANGO_SETTINGS_MODULE"] = f"{prj}.settings_app"
    from pytigon_lib.schtools.main_paths import get_main_paths
    from pytigon_lib import init_paths
    from django import setup

    cfg = get_main_paths(prj)
    sys.path.append(cfg["PRJ_PATH"])
    init_paths(prj)

    from django.apps import apps
    from django.conf import settings

    if not pytigon_standard:
        settings.DATABASES = []
        settings.MIDDLEWARE = []
        settings.INSTALLED_APPS = []

    if settings_callback:
        settings_callback(settings)

    apps.populate(settings.INSTALLED_APPS)

    if embeded_django:
        from pytigon_lib.schhttptools.httpclient import init_embeded_django
        init_embeded_django()
