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
from graphene_django.views import GraphQLView

from pytigon.schserw.schsys.schema import public_schema
from pytigon_lib.schdjangoext.django_init import AppConfigMod

from pytigon_lib.schdjangoext.tools import make_href

from .schsys import views

import logging

logger = logging.getLogger(__name__)

admin.site.enable_nav_sidebar = False

PytigonGraphQLViewPublic = GraphQLView

class PytigonGraphQLView(LoginRequiredMixin, GraphQLView):
    pass


_urlpatterns = []

if settings.URL_ROOT_FOLDER:
    urlpatterns = [
        path(settings.URL_ROOT_FOLDER + "/", include(_urlpatterns))
    ]
else:
    urlpatterns = _urlpatterns

_urlpatterns.extend(
    [
        path(
            "schsys/jsi18n/",
            django.views.i18n.JavaScriptCatalog,
            {"packages": ("django.conf",)},
        ),
        path("schsys/i18n/", include(django.conf.urls.i18n)),
        path("plugins/<path:template_name>", views.plugin_template),
        path("select2/", include(django_select2.urls)),
        path("favicon.ico", views.favicon),
        path(make_href("sw.js"), views.sw),
        path("graphql/", csrf_exempt(PytigonGraphQLView.as_view(graphiql=True))),
        path("graphql_public/", csrf_exempt(PytigonGraphQLViewPublic.as_view(graphiql=True, schema=public_schema))),
        path("admin/", admin.site.urls),
        path('accounts/', include('allauth.urls')),
        path("admin/log_viewer/", include("log_viewer.urls")),
    ]
)

if settings.PWA:
    _urlpatterns.extend(
        [
            path('', include('pwa.urls')),
            path('webpush/', include('webpush.urls')),
        ]
    )

if settings.DEBUG:
    _urlpatterns.append(
        re_path(
            "site_media/(.*)$",
            django.contrib.staticfiles.views.serve,
            {"document_root": settings.MEDIA_ROOT},
        )
    )
    _urlpatterns.append(
        re_path(
            "site_media_protected/(.*)$",
            django.contrib.staticfiles.views.serve,
            {"document_root": settings.MEDIA_ROOT_PROTECTED},
        )
    )
else:
    _urlpatterns.append(
        re_path(
            "site_media/(.*)$",
            django.contrib.staticfiles.views.serve,
            {"document_root": settings.MEDIA_ROOT},
        )
    )
    _urlpatterns.append(
        re_path("site_media_protected/(.*)$", views.site_media_protected)
    )

if hasattr(settings, "DEBUG_TOOLBAR") and settings.DEBUG_TOOLBAR:
    import debug_toolbar
    _urlpatterns.append(
        path('__debug__/', include(debug_toolbar.urls))
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
            or pos.startswith("bootstrap4")
        ):
            continue

    elementy = pos.split(".")
    module = __import__(pos)

    if pos == "pytigon":
        pass

    try:
        test = importlib.import_module(pos)
        if hasattr(test, "ModuleTitle"):
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
            if hasattr(item2.pattern, "_route") and item2.pattern._route.startswith('../'):
                print("A1")
                tmp.append(item2)
                item.url_patterns.remove(item2)

for item in tmp:
    item.pattern._route = item.pattern._route.replace('../','')
    _urlpatterns.append(item)

if len(settings.PRJS) > 0:
    for prj in settings.PRJS:
        if prj.startswith("_"):
            continue

        test = True
        for item in _urlpatterns:
            if item.pattern and hasattr(item.pattern, "_route") and item.pattern._route == prj + "/":
                test = False
                break
        if test:
            u = path(
                prj + "/",
                TemplateView.as_view(template_name="schapp/index.html"),
                {"start_page": True},
                name="start" + prj,
            )
            _urlpatterns.append(u)

    prjs = [(pos, app_description(pos)) for pos in settings.PRJS]

    u = path(
        "",
        TemplateView.as_view(template_name="schapp/index_all.html"),
        {"prjs": prjs},
        name="start",
    )
    _urlpatterns.append(u)
else:
    test = True
    for item in _urlpatterns:
        if item.pattern and hasattr(item.pattern, "_route") and item.pattern._route == "":
            if len(item.url_patterns)<2:
                test = False
                break
    if test:
        u = path("", TemplateView.as_view(template_name="schapp/index.html"), name="start")
        _urlpatterns.append(u)
