"""URL configuration for the Pytigon server application.

Defines all URL patterns including:
- Static media serving
- GraphQL and REST API endpoints
- OAuth2 provider URLs
- Dynamic app URL loading from INSTALLED_APPS
- Project-specific start pages
"""

import importlib
import logging
import os
import posixpath

import django.contrib.staticfiles
import django.views.i18n
import django_select2.urls
from django.conf import settings
from django.http import FileResponse, Http404
from django.urls import include, path, re_path
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.vary import vary_on_headers
from django.views.generic import TemplateView

if settings.GRAPHQL:
    from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import admin

from pytigon_lib.schdjangoext.django_init import AppConfigMod
from pytigon_lib.schdjangoext.tools import make_href

from .schsys import views

logger = logging.getLogger(__name__)

if settings.GRAPHQL:
    from graphene_django.views import GraphQLView

    from pytigon.schserw.schsys.schema import public_schema, schema
    from pytigon_lib.schdjangoext.oauth_for_graphql import OAuth2ProtectedGraph

    PytigonGraphQLViewPublic = GraphQLView

    class PytigonGraphQLView(LoginRequiredMixin, GraphQLView):
        """GraphQL view requiring authentication."""

        pass


if "django.contrib.admin" in settings.INSTALLED_APPS:
    admin.site.enable_nav_sidebar = False

_urlpatterns = []

if settings.URL_ROOT_FOLDER:
    urlpatterns = [path(settings.URL_ROOT_FOLDER + "/", include(_urlpatterns))]
else:
    urlpatterns = _urlpatterns

_urlpatterns.extend(
    [
        path(
            "schsys/jsi18n.js",
            cache_page(60 * 60 * 24 * 30)(
                django.views.i18n.JavaScriptCatalog.as_view(
                    packages=[
                        "pytigon.schserw.schsys",
                    ]
                )
            ),
            name="javascript-catalog",
        ),
        path(
            "schsys/i18n/setlang/",
            django.views.i18n.set_language,
            name="set_language",
        ),
        path("plugins/<path:template_name>", views.plugin_template),
        path("select2/", include(django_select2.urls)),
        path("favicon.ico", views.favicon),
        path(make_href("sw.js"), views.sw),
    ]
)

if "django.contrib.admin" in settings.INSTALLED_APPS:
    _urlpatterns.append(path("admin/", admin.site.urls))


if settings.LOGVIEWER:
    _urlpatterns.append(path("admin/log_viewer/", include("log_viewer.urls")))

if settings.ALLAUTH:
    _urlpatterns.append(path("accounts/", include("allauth.urls")))

if settings.GRAPHQL:
    _urlpatterns.extend(
        [
            path(
                "graphql/",
                                csrf_exempt(
                    OAuth2ProtectedGraph.as_view(
                        graphiql=settings.DEBUG, schema=schema
                    )
                ),
            ),
            path(
                "graphql_public/",
                csrf_exempt(
                    PytigonGraphQLViewPublic.as_view(
                        graphiql=settings.DEBUG, schema=public_schema
                    )
                ),
            ),
        ]
    )

if settings.REST:
    from drf_yasg import openapi
    from drf_yasg.views import get_schema_view
    from rest_framework import permissions, status
    from rest_framework.decorators import api_view
    from rest_framework.response import Response

    schema_view = get_schema_view(
        openapi.Info(
            title="Rest API",
            default_version="v1",
            description="Rest API for Pytigon application",
            contact=openapi.Contact(email="admin@pytigon.eu"),
        ),
        public=True,
        permission_classes=(permissions.AllowAny,),
    )

    _urlpatterns.extend(
        [
            path("api-auth/", include("rest_framework.urls")),
            path(
                "api/",
                schema_view.with_ui("swagger", cache_timeout=0),
                name="schema-swagger-ui",
            ),
        ]
    )

    @api_view(["GET"])
    def rest_hello(request):
        """Health-check endpoint for the REST API."""
        if request.method == "GET":
            return Response({"message": f"Hello {request.user}, {request.auth}"})
        return Response(status=status.HTTP_404_NOT_FOUND)

    _urlpatterns.append(path("rest_hello", rest_hello))

    # Load REST API URLs from installed apps
    for app in settings.INSTALLED_APPS:
        if isinstance(app, AppConfigMod):
            pos = app.name
        else:
            pos = app
            if (
                pos.startswith("django")
                or pos.startswith("debug")
                or pos.startswith("registration")
                or pos.startswith("bootstrap_admin")
                or pos.startswith("channels")
                or pos.startswith("django_bootstrap5")
            ):
                continue
        module_name = f"{str(pos)}.rest_api"
        try:
            m = importlib.import_module(module_name)
            if hasattr(m, "urlpatterns"):
                _urlpatterns.extend(
                    [
                        path(
                            f"api/{pos}/",
                            include(f"{pos}.rest_api"),
                            name=f"api_{pos}",
                        ),
                    ]
                )
        except ModuleNotFoundError:
            pass


if settings.GRAPHQL or settings.REST:
    from oauth2_ext.views import ApplicationScopesTokenView

    _urlpatterns.extend(
        [
            path(
                "o/",
                include("oauth2_provider.urls", namespace="oauth2_provider"),
            ),
            path("o/token/", ApplicationScopesTokenView.as_view(), name="token"),
        ]
    )

if settings.PWA:
    _urlpatterns.extend(
        [
            path(r"", include("pwa_webpush.urls")),
        ]
    )


def _serve_media(request, path, document_root):
    """Serve media files from document_root.

    Replacement for django.views.static.serve (removed in Django 5.0).

    Args:
        request: The HTTP request.
        path: Relative path within document_root.
        document_root: Base directory containing media files.

    Returns:
        FileResponse with the requested file.

    Raises:
        Http404: If path is invalid, a directory, or the file does not exist.
    """
    path = posixpath.normpath(path).lstrip("/")
    root = os.path.realpath(document_root) if os.path.exists(document_root) else os.path.normpath(document_root)
    fullpath = os.path.normpath(os.path.join(root, path))
    if not fullpath.startswith(root):
        raise Http404("Path traversal detected")
    if os.path.isdir(fullpath):
        raise Http404("Directory indexes are not allowed here.")
    if not os.path.exists(fullpath):
        raise Http404(f'"{path}" does not exist')
    return FileResponse(open(fullpath, "rb"), as_attachment=False)


_urlpatterns.append(
    re_path(
        r"^site_media/(?P<path>.*)$",
        _serve_media,
        {"document_root": settings.MEDIA_ROOT},
    )
)
_urlpatterns.append(re_path(r"site_media_protected/(.*)$", views.site_media_protected))

if settings.DEBUG:
    _urlpatterns.append(
        re_path(
            r"^media_protected/(?P<path>.*)$",
            _serve_media,
            {"document_root": settings.MEDIA_ROOT_PROTECTED},
        )
    )


def app_description(prj):
    """Read the project title from the project's settings_app.py file.

    Args:
        prj: Project name.

    Returns:
        str: Project title if found, otherwise the project name itself.
    """
    file_name = os.path.join(os.path.join(settings.PRJ_PATH, prj), "settings_app.py")
    try:
        with open(file_name) as f:
            txt = f.read()
            for pos in txt.split("\n"):
                if pos.startswith("PRJ_TITLE"):
                    return pos.split("=")[1].split('"')[1]
        return prj
    except (IndexError, OSError):
        return prj


# Load URL patterns from installed apps
for app in settings.INSTALLED_APPS:
    if isinstance(app, AppConfigMod):
        pos = app.name
    else:
        pos = app
        if (
            pos.startswith("django")
            or pos.startswith("debug")
            or pos.startswith("registration")
            or pos.startswith("bootstrap_admin")
            or pos.startswith("channels")
            or pos.startswith("django_bootstrap5")
        ):
            continue

    elementy = pos.split(".")

    if pos == "pytigon":
        pass

    try:
        test = importlib.import_module(pos)
        if hasattr(test, "ModuleName"):
            module_name = f"{str(pos)}.urls"
            m = importlib.import_module(module_name)
            if hasattr(m, "gen"):
                _urlpatterns.append(path(f"{str(elementy[-1])}/", include(m)))
            if hasattr(m, "process_main_urls"):
                ret = m.process_main_urls(_urlpatterns)
                if ret:
                    _urlpatterns = ret
    except ModuleNotFoundError as e:
        x = pos.split(".")[0]
        y = e.name.split(".")[0] if e.name else ""
        if x != y:
            logger.error("URLs module not found: %s", pos, exc_info=True)
    except Exception:
        logger.error("URLs error for app: %s", pos, exc_info=True)

# Extract URL patterns starting with "../" for later re-insertion
tmp = []
for item in _urlpatterns:
    if hasattr(item, "url_patterns"):
        for item2 in item.url_patterns:
            if hasattr(item2.pattern, "_route") and item2.pattern._route.startswith(
                "../"
            ):
                tmp.append(item2)
                item.url_patterns.remove(item2)

# Add start pages for each project in PRJS
if len(settings.PRJS) > 0:
    for prj in settings.PRJS:
        if prj.startswith("_"):
            continue

        test = True
        for item in _urlpatterns:
            if (
                item.pattern
                and hasattr(item.pattern, "_route")
                and item.pattern._route == prj + "/"
            ):
                test = False
                break
        if test:
            u = path(
                prj + "/",
                cache_page(settings.CACHE_MIDDLEWARE_SECONDS)(
                    vary_on_headers("User-Agent", "Cookie")(views.start)
                ),
                {"start_page": True},
                name="start" + prj,
            )
            _urlpatterns.append(u)

    prjs = [(pos, app_description(pos)) for pos in settings.PRJS]
    u = path(
        "",
        cache_page(settings.CACHE_MIDDLEWARE_SECONDS)(
            vary_on_headers("User-Agent", "Cookie")(
                TemplateView.as_view(template_name="schsys/app/index_all.html")
            )
        ),
        {"prjs": prjs},
        name="start",
    )
    _urlpatterns.append(u)
else:
    test = True
    for item in _urlpatterns:
        if (
            item.pattern
            and hasattr(item.pattern, "_route")
            and item.pattern._route == ""
        ):
            if len(item.url_patterns) < 2:
                test = False
                break
    if test:
        u = path(
            "",
            cache_page(settings.CACHE_MIDDLEWARE_SECONDS)(
                vary_on_headers("User-Agent", "Cookie")(views.start)
            ),
            name="start",
        )
        _urlpatterns.append(u)

# Re-insert patterns that started with ".."
for item in tmp:
    if item.pattern._route == "../":
        for item2 in _urlpatterns:
            if hasattr(item2.pattern, "_route") and item2.pattern._route == "":
                _urlpatterns.remove(item2)
                break
    item.pattern._route = item.pattern._route.replace("../", "")
    _urlpatterns.append(item)

if settings.PROMETHEUS_ENABLED:
    _urlpatterns.extend(
        [
            path(r"", include("django_prometheus.urls")),
        ]
    )
