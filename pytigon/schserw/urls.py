#!/usr/bin/python
# -*- coding: utf-8 -*-
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation; either version 3, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.

# Pytigon - wxpython and django application framework

# author: "Slawomir Cholaj (slawomir.cholaj@gmail.com)"
# copyright: "Copyright (C) ????/2012 Slawomir Cholaj"
# license: "LGPL 3.0"
# version: "0.1a"

import importlib
import os

from django.urls import include, path, re_path
from django.conf import settings
from django.views.generic import TemplateView

import django.views.i18n
import django.conf.urls.i18n
import django_select2.urls
import django.contrib.staticfiles
from django.contrib.staticfiles import views
from django.views.decorators.csrf import csrf_exempt

from django.urls import path
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import admin

from pytigon_lib.schdjangoext.django_init import AppConfigMod

from pytigon_lib.schdjangoext.tools import make_href

from .schsys import views

import logging

logger = logging.getLogger(__name__)

if settings.GRAPHQL:
    from graphene_django.views import GraphQLView
    from pytigon_lib.schdjangoext.oauth_for_graphql import OAuth2ProtectedGraph
    from pytigon.schserw.schsys.schema import schema, public_schema

    PytigonGraphQLViewPublic = GraphQLView

    class PytigonGraphQLView(LoginRequiredMixin, GraphQLView):
        pass


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
            django.views.i18n.JavaScriptCatalog.as_view(
                packages=[
                    "pytigon.schserw.schsys",
                ]
            ),
            name="javascript-catalog",
        ),
        path("schsys/i18n/", include(django.conf.urls.i18n)),
        path("plugins/<path:template_name>", views.plugin_template),
        path("select2/", include(django_select2.urls)),
        path("favicon.ico", views.favicon),
        path(make_href("sw.js"), views.sw),
        path("admin/", admin.site.urls),
    ]
)

if settings.LOGVIEWER:
    _urlpatterns.append(path("admin/log_viewer/", include("log_viewer.urls")))

if settings.ALLAUTH:
    _urlpatterns.append(path("accounts/", include("allauth.urls")))

if settings.GRAPHQL:
    _urlpatterns.extend(
        [
            path(
                "graphql/",
                csrf_exempt(OAuth2ProtectedGraph.as_view(graphiql=True, schema=schema)),
            ),
            path(
                "graphql_public/",
                csrf_exempt(
                    PytigonGraphQLViewPublic.as_view(
                        graphiql=True, schema=public_schema
                    )
                ),
            ),
        ]
    )

if settings.REST:
    from drf_yasg import openapi
    from drf_yasg.views import get_schema_view
    from rest_framework import permissions
    from rest_framework.decorators import api_view
    from rest_framework.response import Response
    from rest_framework import status

    schema_view = get_schema_view(
        openapi.Info(
            title="Rest api",
            default_version="v1",
            description="Rest api for pytigon application",
            contact=openapi.Contact(email="admi@epytigon.eu"),
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

    @api_view(
        [
            "GET",
        ]
    )
    def rest_hello(request):
        if request.method == "GET":
            print(dir(request))
            return Response({"message": "Hello %s, %s" % (request.user, request.auth)})
        return Response(status=status.HTTP_404_NOT_FOUND)

    _urlpatterns.append(path("rest_hello", rest_hello))

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
        module_name = "%s.rest_api" % str(pos)
        try:
            m = importlib.import_module(module_name)
            if hasattr(m, "urlpatterns"):
                _urlpatterns.extend(
                    [
                        path(
                            "api/%s/" % pos,
                            include("%s.rest_api" % pos),
                            name="api_%s" % pos,
                        ),
                    ]
                )
        except ModuleNotFoundError:
            pass


if settings.GRAPHQL or settings.REST:
    from oauth2_ext.views import ApplicationScopesTokenView

    _urlpatterns.extend(
        [
            path("o/", include("oauth2_provider.urls", namespace="oauth2_provider")),
            path("o/token/", ApplicationScopesTokenView.as_view(), name="token"),
        ]
    )

if settings.PWA:
    _urlpatterns.extend(
        [
            path(r"", include("pwa_webpush.urls")),
        ]
    )

_urlpatterns.append(
    re_path(
        r"^site_media/(?P<path>.*)$",
        django.views.static.serve,
        {"document_root": settings.MEDIA_ROOT},
    )
)
_urlpatterns.append(re_path(r"site_media_protected/(.*)$", views.site_media_protected))

if settings.DEBUG:
    _urlpatterns.append(
        re_path(
            r"^media_protected/(?P<path>.*)$",
            django.views.static.serve,
            {"document_root": settings.MEDIA_ROOT_PROTECTED},
        )
    )


def app_description(prj):
    file_name = os.path.join(os.path.join(settings.PRJ_PATH, prj), "settings_app.py")
    try:
        with open(file_name, "rt") as f:
            txt = f.read()
            for pos in txt.split("\n"):
                if pos.startswith("PRJ_TITLE"):
                    return pos.split("=")[1].split('"')[1]
        return prj
    except:
        return prj


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
    module = __import__(pos)

    if pos == "pytigon":
        pass

    try:
        test = importlib.import_module(pos)
        if hasattr(test, "ModuleName"):
            module_name = "%s.urls" % str(pos)
            m = importlib.import_module(module_name)
            if hasattr(m, "gen"):
                _urlpatterns.append(path("%s/" % str(elementy[-1]), include(m)))
    except ModuleNotFoundError as e:
        x = pos.split(".")[0]
        y = e.name.split(".")[0]
        if x != y:
            logger.exception(f"URLs error: {pos}")
    except:
        logger.exception(f"URLs error: {pos}")

tmp = []
for item in _urlpatterns:
    if hasattr(item, "url_patterns"):
        for item2 in item.url_patterns:
            if hasattr(item2.pattern, "_route") and item2.pattern._route.startswith(
                "../"
            ):
                tmp.append(item2)
                item.url_patterns.remove(item2)

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
                TemplateView.as_view(template_name="schsys/app/index.html"),
                {"start_page": True},
                name="start" + prj,
            )
            _urlpatterns.append(u)

    prjs = [(pos, app_description(pos)) for pos in settings.PRJS]

    u = path(
        "",
        TemplateView.as_view(template_name="schsys/app/index_all.html"),
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
            TemplateView.as_view(template_name="schsys/app/index.html"),
            name="start",
        )
        _urlpatterns.append(u)

for item in tmp:
    if item.pattern._route == "../":
        for item2 in _urlpatterns:
            if hasattr(item2.pattern, "_route") and item2.pattern._route == "":
                _urlpatterns.remove(item2)
                break
    item.pattern._route = item.pattern._route.replace("../", "")
    _urlpatterns.append(item)
