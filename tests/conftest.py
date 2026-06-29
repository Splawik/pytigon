import os
import sys


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
            )
        django.setup()
    except Exception:
        pass
