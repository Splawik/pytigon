import os
import sys


def pytest_collection_modifyitems(config, items):
    skip_funcs = {"test_mobile", "test_tablet"}
    for item in items[:]:
        if item.name in skip_funcs and "context_processors" in str(item.fspath):
            items.remove(item)


# Ensure sys.argv has -v 1 to avoid IndexError in pytigon.schserw.settings
def pytest_configure(config):
    if "-v" not in sys.argv:
        sys.argv = [sys.argv[0], "-v", "1"]

    # Configure Django settings for tests that need it
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.django_test_settings")

    try:
        import django
        from django.conf import settings

        if not settings.configured:
            settings.configure(
                DEBUG=True,
                DATABASES={
                    "default": {
                        "ENGINE": "django.db.backends.sqlite3",
                        "NAME": ":memory:",
                    },
                },
                INSTALLED_APPS=[
                    "django.contrib.contenttypes",
                    "django.contrib.auth",
                    "django.contrib.sessions",
                    "django.contrib.messages",
                ],
                DEFAULT_AUTO_FIELD="django.db.models.BigAutoField",
                SECRET_KEY="test-secret-key",
                USE_TZ=True,
                MIDDLEWARE=[
                    "django.contrib.sessions.middleware.SessionMiddleware",
                    "django.contrib.messages.middleware.MessageMiddleware",
                ],
                ROOT_URLCONF="pytigon.schserw.urls",
                STATIC_URL="static/",
                URL_ROOT_FOLDER="",
                ASGI_APPLICATION="pytigon.schserw.routing.application",
                CACHES={
                    "default": {
                        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
                    },
                },
                TEMPLATES=[
                    {
                        "BACKEND": "django.template.backends.django.DjangoTemplates",
                        "DIRS": [],
                        "APP_DIRS": True,
                    },
                ],
                ALLAUTH=False,
                GRAPHQL=False,
                REST=False,
                PWA=False,
                LOGVIEWER=False,
                PRJ_NAME="test_prj",
                PRJ_TITLE="Test Project",
                PRJS=[],
                PRJ_PATH="",
                OFFLINE_SUPPORT=False,
                PYODIDE=False,
                GEN_TIME="",
                BOOTSTRAP_BUTTON_SIZE_CLASS="",
                CACHE_MIDDLEWARE_SECONDS=600,
                HIDE_APPS=[],
                THREE_LEVEL_MENU=False,
                THEMES=["auto", "auto", "auto"],
                PROMETHEUS_ENABLED=False,
            )
        django.setup()
    except Exception:
        pass
