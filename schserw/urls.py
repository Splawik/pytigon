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
import traceback
import os
from os import environ

from django.conf.urls import url, include
from django.conf import settings
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.urls import path #include

import django.views.i18n
import django.conf.urls.i18n
import django_select2.urls


from schlib.schdjangoext.django_init import AppConfigMod

import schserw.schsys.views
from schlib.schdjangoext.tools import make_href
from schlib.schtools.platform_info import platform_name

urlpatterns = [
    url('schsys/jsi18n/$', django.views.i18n.JavaScriptCatalog, {'packages': ('django.conf', )}),
    url('schsys/i18n/', include(django.conf.urls.i18n)),
    url('admin/', admin.site.urls),
    url('schplugins/(?P<template_name>.*)', schserw.schsys.views.plugin_template),
    url('site_media/(.*)$', django.views.static.serve, {'document_root': settings.MEDIA_ROOT}),
    url('select2/', include(django_select2.urls)),
    url('favicon.ico', schserw.schsys.views.favicon),
    url( make_href('sw.js'), schserw.schsys.views.sw),
]

def app_description(app_pack):
    file_name = os.path.join(os.path.join(settings.APP_PACK_PATH, app_pack), 'settings_app.py')
    try:
        with open(file_name, "rt") as f:
            txt = f.read()
            for pos in txt.split('\n'):
                if pos.startswith('APPSET_TITLE'):
                    return pos.split('=')[1].split('\"')[1]
        return app_pack
    except:
        return app_pack

if len(settings.APP_PACKS) > 0:
    for app_pack in settings.APP_PACKS:
        if app_pack.startswith('_'):
            continue
        #u = url(r'^'+app_pack+'/$', TemplateView.as_view(template_name='schapp/index.html'),
        #        {'app_pack': app_pack, 'start_page': True }, name='start'+app_pack )
        u = url(r'^'+app_pack+'/$', TemplateView.as_view(template_name='schapp/index.html'),
                {'start_page': True }, name='start'+app_pack )
        urlpatterns.append(u)

    app_packs = [ (pos, app_description(pos)) for pos in settings.APP_PACKS ]

    u=url(r'^$', TemplateView.as_view(template_name='schapp/index_all.html'),
          {'app_packs': app_packs }, name='start')

    urlpatterns.append(u)
else:
    u=url(r'^$', TemplateView.as_view(template_name='schapp/index.html'),  {'app_pack': None }, name='start')
    urlpatterns.append(u)

if settings.DEBUG or platform_name()=='Android' or 'PYTIGON_APP_IMAGE' in environ or not settings.PRODUCTION_VERSION:
    if 'PYTIGON_APP_IMAGE' in environ:
        urlpatterns += static(str(settings.STATIC_URL+"app/"), document_root=str(settings.STATIC_APP_ROOT))
    urlpatterns += static(str(settings.STATIC_URL), document_root=str(settings.STATICFILES_DIRS[0]))

SHOW_ERROR = False

for app in settings.INSTALLED_APPS:
    if isinstance(app, AppConfigMod):
        pos = app.name
    else:
        pos = app
        if pos.startswith('django') or pos.startswith('debug') or pos.startswith('registration') \
        or pos.startswith('bootstrap_admin') or pos.startswith('channels')\
        or pos.startswith('bootstrap4'):
            continue
        if pos == 'schserw.schsys':
            SHOW_ERROR = True
    elementy = pos.split('.')
    module = __import__(pos)

    if pos == 'pytigon':
        pass

    try:
            module_name = '%s.urls' % str(pos)
            m = importlib.import_module(module_name)
            if len(elementy) > 1:
                urlpatterns.append(url(r'%s/' % str(elementy[1]), include(m)))
            else:
                urlpatterns.append(url(r'%s/' % str(elementy[0]), include(m)))
    except:
        if SHOW_ERROR:
            print(pos)
            traceback.print_exc()

#urlpatterns = _urlpatterns

if settings.URL_ROOT_FOLDER:
    urlpatterns = [
        path(settings.URL_ROOT_FOLDER+"/", include(urlpatterns)),
    ]
