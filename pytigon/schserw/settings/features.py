import os

from pytigon_lib.schtools.main_paths import get_prj_name
from pytigon_lib.schtools.platform_info import platform_name

from .base import (
    ALLAUTH,
    BASE_PRJ_NAME,
    COMPRESS_ENABLED,
    DATA_PATH,
    DEBUG,
    ENV,
    GRAPHQL,
    MAILER,
    PLATFORM_TYPE,
    PRJ_PATH,
    PRJ_PATH_ALT,
    PRODUCTION_VERSION,
    PWA,
    PYTIGON_PATH,
    REST,
    RULES_ENABLED,
    SERW_PATH,
)

ROOT_URLCONF = "pytigon.schserw.urls"

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            PYTIGON_PATH + "/templates",
            PYTIGON_PATH + "/appdata/plugins",
            DATA_PATH + "/plugins",
        ],
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.request",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.request",
                "django.template.context_processors.csp",
                "pytigon.schserw.schsys.context_processors.sch_standard",
            ],
            "loaders": [
                "pytigon_lib.schdjangoext.python_style_template_loader.DBLoader",
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
                "pytigon_lib.schdjangoext.python_style_template_loader.FSLoader",
            ],
            "builtins": ["pytigon.schserw.schsys.templatetags.defexfiltry"],
            "debug": DEBUG and not PRODUCTION_VERSION,
        },
    }
]

if "site-packages" in PRJ_PATH and BASE_PRJ_NAME:
    TEMPLATES[0]["DIRS"].append(os.path.join(PRJ_PATH_ALT, BASE_PRJ_NAME, "templates"))

if DEBUG:
    TEMPLATES[0]["OPTIONS"]["loaders"].insert(
        0, "pytigon_lib.schdjangoext.python_style_template_loader.Loader"
    )

FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

if ENV("EMBEDED_DJANGO_SERVER"):
    MIDDLEWARE = [
        "django.middleware.common.CommonMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.locale.LocaleMiddleware",
        "pytigon.schserw.schmiddleware.csrf.DisableCSRF",
    ]
else:
    MIDDLEWARE = [
        "pytigon.schserw.schmiddleware.vary.VaryMiddleware",
        "corsheaders.middleware.CorsMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.locale.LocaleMiddleware",
        "django.contrib.auth.middleware.RemoteUserMiddleware",
        "django.middleware.csp.ContentSecurityPolicyMiddleware",
    ]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.messages",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.admin",
    "django.contrib.sites",
    "django.forms",
    "django_select2",
    "django_bootstrap5",
    "corsheaders",
    "widget_tweaks",
    "pytigon.schserw.schsys",
]

LOCALE_PATHS = [
    os.path.join(SERW_PATH, "locale"),
    os.path.join(PRJ_PATH, get_prj_name(), "locale"),
]

if DEBUG:
    INSTALLED_APPS.append("django_extensions")

if MAILER:
    INSTALLED_APPS.append("mailer")
    EMAIL_BACKEND = "mailer.backend.DbBackend"

if GRAPHQL:
    INSTALLED_APPS.append("graphene_django")
    INSTALLED_APPS.append("oauth2_provider")
    INSTALLED_APPS.append("pytigon.schserw.oauth2_ext")

if REST:
    INSTALLED_APPS.append("rest_framework")
    if "oauth2_provider" not in INSTALLED_APPS:
        INSTALLED_APPS.append("oauth2_provider")
        INSTALLED_APPS.append("pytigon.schserw.oauth2_ext")
    INSTALLED_APPS.append("drf_yasg")
    SWAGGER_USE_COMPAT_RENDERERS = False
    REST_FRAMEWORK = {
        "DEFAULT_AUTHENTICATION_CLASSES": [
            "oauth2_provider.contrib.rest_framework.OAuth2Authentication",
        ],
        "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    }

if GRAPHQL or REST:
    AUTHENTICATION_BACKENDS.append("graphql_jwt.backends.JSONWebTokenBackend")
    MIDDLEWARE.append("oauth2_provider.middleware.OAuth2TokenMiddleware")

    OAUTH2_PROVIDER = {
        "SCOPES": {
            "read": "Read scope",
            "write": "Write scope",
        },
        "PKCE_REQUIRED": False,
    }

    OAUTH2_PROVIDER_APPLICATION_MODEL = "oauth2_provider.Application"

if RULES_ENABLED:
    INSTALLED_APPS.append("rules")
    AUTHENTICATION_BACKENDS.append("rules.permissions.ObjectPermissionBackend")

if ALLAUTH:
    INSTALLED_APPS.append("allauth")
    INSTALLED_APPS.append("allauth.account")
    INSTALLED_APPS.append("allauth.socialaccount")
    AUTHENTICATION_BACKENDS.append("allauth.account.auth_backends.AuthenticationBackend")
    MIDDLEWARE.append("allauth.account.middleware.AccountMiddleware")

    import allauth

    LOCALE_PATHS.append(os.path.join(os.path.dirname(allauth.__file__), "locale"))

    CAN_RESET_PASSWORD = True
    CAN_CHANGE_PASSWORD = True
    CAN_REGISTER = True
else:
    INSTALLED_APPS.append("pytigon.schserw.nosocial")

    CAN_RESET_PASSWORD = False
    CAN_CHANGE_PASSWORD = True
    CAN_REGISTER = False

if COMPRESS_ENABLED:
    INSTALLED_APPS.append("compressor")
    STATICFILES_FINDERS.append("compressor.finders.CompressorFinder")
else:
    INSTALLED_APPS.append("_schserverless.schnocompress")

if PWA:
    INSTALLED_APPS.append("pwa_webpush")
    if DEBUG:
        pub_key = ENV("VAPID_PUBLIC_KEY", default="")
        prv_key = ENV("VAPID_PRIVATE_KEY", default="")
        v_email = ENV("VAPID_ADMIN_EMAIL", default="")
        if not pub_key or not prv_key:
            try:
                import base64

                from cryptography.hazmat.primitives.asymmetric import ec

                private_key = ec.generate_private_key(ec.SECP256R1())
                public_key = private_key.public_key()
                pub_numbers = public_key.public_numbers()
                prv_numbers = private_key.private_numbers()
                raw_pub = (
                    b"\x04"
                    + pub_numbers.x.to_bytes(32, "big")
                    + pub_numbers.y.to_bytes(32, "big")
                )
                pub_key = base64.urlsafe_b64encode(raw_pub).rstrip(b"=").decode()
                prv_key = base64.urlsafe_b64encode(
                    prv_numbers.private_value.to_bytes(32, "big")
                ).rstrip(b"=").decode()
            except ImportError:
                import warnings

                warnings.warn(
                    "PWA is enabled but VAPID_PUBLIC_KEY and VAPID_PRIVATE_KEY "
                    "are not set. Web Push will not work. Install cryptography "
                    "or set the environment variables."
                )
        WEBPUSH_SETTINGS = {
            "VAPID_PUBLIC_KEY": pub_key,
            "VAPID_PRIVATE_KEY": prv_key,
            "VAPID_ADMIN_EMAIL": v_email or "auto@pytigon.eu",
        }

if PLATFORM_TYPE != "webserver":
    MIDDLEWARE.insert(
        0,
        "whitenoise.middleware.WhiteNoiseMiddleware",
    )
    INSTALLED_APPS.append("whitenoise.runserver_nostatic")
    WHITENOISE_USE_FINDERS = True

INSTALLED_APPS.append("django.contrib.staticfiles")

if (
    not ENV("PYTIGON_WITHOUT_CHANNELS")
    and platform_name() != "Android"
    and platform_name() != "Emscripten"
):
    INSTALLED_APPS.append("channels")

if ENV("DJANGO_Q"):
    INSTALLED_APPS.append("django_q")

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

SKIP_APPS_PREFIXES = [
    "django",
    "debug",
    "registration",
    "bootstrap_admin",
    "channels",
    "django_bootstrap5",
]

CHANNELS_URL_TAB = []

HIDE_APPS = []

PRJS = []
