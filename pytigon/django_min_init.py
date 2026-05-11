"""Minimal Django initialization for pytigon.

Provides a lightweight Django setup routine that can be used in scripts
and embedded environments without loading the full Django configuration.
"""

import os
import sys

from pytigon_lib.schtools.main_paths import get_main_paths
from pytigon_lib import init_paths
from django import setup


def init(
    prj="schscripts",
    pytigon_standard=False,
    embeded_django=False,
    settings_callback=None,
):
    """Initialize Django with minimal settings for a pytigon project.

    Args:
        prj: Project name (default: "schscripts").
        pytigon_standard: If True, use full Django settings from the project.
            Otherwise, clear DATABASES, MIDDLEWARE, and INSTALLED_APPS.
        embeded_django: If True, initialize embedded Django HTTP client.
        settings_callback: Optional callback(settings) to customize Django
            settings before app population.
    """
    os.environ["DJANGO_SETTINGS_MODULE"] = f"{prj}.settings_app"

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
