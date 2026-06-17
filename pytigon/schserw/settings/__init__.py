#import warnings
#warnings.filterwarnings("error")

from .base import *
from .features import *
from .infra import *


def finish(settings):
    global LOGIN_REDIRECT_URL, URL_ROOT_FOLDER
    if settings["URL_ROOT_FOLDER"] and len(settings["URL_ROOT_FOLDER"]) > 0:
        settings["LOGIN_REDIRECT_URL"] = "/" + settings["URL_ROOT_FOLDER"] + "/"

    if ENV("PROMETHEUS_ENABLED"):
        MIDDLEWARE.insert(0, "django_prometheus.middleware.PrometheusBeforeMiddleware")
        MIDDLEWARE.append("django_prometheus.middleware.PrometheusAfterMiddleware")
        if "default" in DATABASES:
            engine = DATABASES["default"]["ENGINE"]
            if engine in (
                "django.db.backends.sqlite3",
                "django.db.backends.postgresql",
                "django.db.backends.mysql",
            ):
                DATABASES["default"]["ENGINE"] = engine.replace(
                    "django.db.backends", "django_prometheus.db.backends"
                )
        if "default" in CACHES:
            backend = CACHES["default"]["BACKEND"]
            if backend in (
                "django.core.cache.backends.memcached.PyMemcacheCache",
                "django.core.cache.backends.memcached.PyLibMCCache",
                "django.core.cache.backends.redis.RedisCache",
                "django.core.cache.backends.filebased.FileBasedCache",
            ):
                CACHES["default"]["BACKEND"] = backend.replace(
                    "django.core.cache.backends",
                    "django_prometheus.cache.backends",
                )
