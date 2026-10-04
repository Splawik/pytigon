"""Shared pytest configuration for the pytigon test suite.

The Django bootstrap lives here rather than in a ``tests/plugins`` package: each
Pytigon repository ships a top-level ``plugins`` package, and importing them
through ``sys.path`` is ambiguous when more than one test tree is on the path.
"""

import os


def pytest_configure(config):
    """Initialise the ``_schtest`` project and set up Django once."""
    import django

    os.environ.setdefault("SECRET_KEY", "anawa")
    os.environ["SCRIPT_MODE"] = "1"
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings_app")

    from pytigon.django_min_init import init

    init(prj="_schtest", pytigon_standard=True)
    django.setup()


def pytest_sessionstart(session):
    """Allow the synthetic host names used by the test client.

    ``RequestFactory`` builds requests with the host ``testserver``. Views that
    build absolute URLs call ``request.get_host()``, which validates it against
    ``ALLOWED_HOSTS`` and otherwise raises ``DisallowedHost``.
    """
    from django.conf import settings

    if settings.ALLOWED_HOSTS != ["*"]:
        for host in ("testserver", "localhost"):
            if host not in settings.ALLOWED_HOSTS:
                settings.ALLOWED_HOSTS = [*settings.ALLOWED_HOSTS, host]
