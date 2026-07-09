import os
import sys

pytest_plugins = [
    "plugins.pytigon_plugin",
]


def pytest_configure(config):
    import django
    from django.conf import settings

    django.setup()
