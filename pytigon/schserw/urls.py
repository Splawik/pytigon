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

#Pytigon - wxpython and django application framework

#author: "Slawomir Cholaj (slawomir.cholaj@gmail.com)"
#copyright: "Copyright (C) ????/2012 Slawomir Cholaj"
#license: "LGPL 3.0"
#version: "0.1a"

import importlib
import os

from django.conf.urls import url, include
from django.conf import settings
from django.views.generic import TemplateView
#from django.urls import path #include

import django.views.i18n
import django.conf.urls.i18n
import django_select2.urls
import django.contrib.staticfiles
from django.contrib.staticfiles import views
#import django.contrib.staticfiles.views.serve

from django.urls import path
from django.contrib.auth.mixins import LoginRequiredMixin
from graphene_django.views import GraphQLView

from pytigon_lib.schdjangoext.django_init import AppConfigMod

from pytigon_lib.schdjangoext.tools import make_href

from .schsys import views

import logging
logger = logging.getLogger(__name__)


if hasattr(settings, "GRAPHENE_PUBLIC"):
    PytigonGraphQLView = GraphQLView
else:
    class PytigonGraphQLView(LoginRequiredMixin, GraphQLView):
        pass

_urlpatterns = []

if settings.URL_ROOT_FOLDER:
    urlpatterns = [
        #path(settings.URL_ROOT_FOLDER+"/", include(urlpatterns)),
        url(settings.URL_ROOT_FOLDER + "/", include(_urlpatterns)),
    ]
else:
    urlpatterns = _urlpatterns

_urlpatterns.extend([
    url('schsys/jsi18n/$', django.views.i18n.JavaScriptCatalog, {'packages': ('django.conf', )}),
    url('schsys/i18n/', include(django.conf.urls.i18n)),
    url('plugins/(?P<template_name>.*)', views.plugin_template),
    #url('site_media/(.*)$', django.views.static.serve, {'document_root': settings.MEDIA_ROOT}),
    url('site_media/(.*)$', django.contrib.staticfiles.views.serve, {'document_root': settings.MEDIA_ROOT}),
    url('select2/', include(django_select2.urls)),
    url('favicon.ico', views.favicon),
    url(make_href('sw.js'), views.sw),
    path('graphql', PytigonGraphQLView.as_view(graphiql=True)),
])

def app_description(prj):
    file_name = os.path.join(os.path.join(settings.PRJ_PATH, prj), 'settings_app.py')
    try:
        with open(file_name, "rt") as f:
            txt = f.read()
            for pos in txt.split('\n'):
                if pos.startswith('PRJ_TITLE'):
                    return pos.split('=')[1].split('\"')[1]
        return prj
    except:
        return prj

if len(settings.PRJS) > 0:
    for prj in settings.PRJS:
        if prj.startswith('_'):
            continue
        #u = url(r'^'+prj+'/$', TemplateView.as_view(template_name='schapp/index.html'),
        #        {'prj': prj, 'start_page': True }, name='start'+prj )
        u = url(r'^'+prj+'/$', TemplateView.as_view(template_name='schapp/index.html'),
                {'start_page': True }, name='start'+prj )
        _urlpatterns.append(u)

    prjs = [ (pos, app_description(pos)) for pos in settings.PRJS ]

    u=url(r'^$', TemplateView.as_view(template_name='schapp/index_all.html'),
          {'prjs': prjs }, name='start')

    _urlpatterns.append(u)
else:
    #u=url(r'^$', TemplateView.as_view(template_name='schapp/index.html'),  {'prj': None }, name='start')
    u = url(r'^$', TemplateView.as_view(template_name='schapp/index.html'), name='start')
    _urlpatterns.append(u)

#if settings.DEBUG or platform_name()=='Android' or 'PYTIGON_APP_IMAGE' in environ or not settings.PRODUCTION_VERSION:
#    if 'PYTIGON_APP_IMAGE' in environ:
#        _urlpatterns += static(str(settings.STATIC_URL+"app/"), document_root=str(settings.STATIC_APP_ROOT))
#    _urlpatterns += static(str(settings.STATIC_URL), document_root=str(settings.STATIC_URL))

#SHOW_ERROR = False

for app in settings.INSTALLED_APPS:
    if isinstance(app, AppConfigMod):
        pos = app.name
    else:
        pos = app
        if pos.startswith('django') or pos.startswith('debug') or pos.startswith('registration') \
        or pos.startswith('bootstrap_admin') or pos.startswith('channels')\
        or pos.startswith('bootstrap4'):
            continue
        #if pos == 'schserw.schsys':
        #    SHOW_ERROR = True
    elementy = pos.split('.')
    module = __import__(pos)

    if pos == 'pytigon':
        pass

    try:
        test =  importlib.import_module(pos)
        if hasattr(test, "ModuleTitle"):
            module_name = '%s.urls' % str(pos)
            m = importlib.import_module(module_name)
            if hasattr(m, 'gen'):
                _urlpatterns.append(url(r'^%s/' % str(elementy[-1]), include(m)))
    except ModuleNotFoundError as e:
        x = pos.split('.')[0]
        y = e.name.split('.')[0]
        if x != y:
            logger.exception(f"URLs error: {pos}")
    except:
        logger.exception(f"URLs error: {pos}")
