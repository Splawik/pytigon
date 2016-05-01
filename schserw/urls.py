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

import platform


from django.conf.urls import url, include
from django.conf import settings
from django.contrib import admin

import os
import importlib

import traceback
from django.views.generic import TemplateView
from schlib.schdjangoext.django_init import AppConfigMod
from django.conf.urls.static import static

import schserw.schsys.views
import django.views.i18n
import django.conf.urls.i18n
import django_select2.urls

import schlib.schindent.indent_style

def get_py_to_js_compiler():
    return [settings.NODEJS, settings.RAPYD, "-p", "-b", "-m"]
    #return [settings.NODEJS, settings.RAPYD, "-p", "-b",]

schlib.schindent.indent_style.PY_TO_JS = get_py_to_js_compiler()

#import warnings
#warnings.simplefilter('error', DeprecationWarning)

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='schapp/index.html'), name='start'),
    url(r'schplugins/(?P<template_name>.*)', schserw.schsys.views.plugin_template),
    url(r'schsys/jsi18n/$', django.views.i18n.javascript_catalog, {'packages': ('django.conf', )}),
    url(r'schsys/i18n/', include(django.conf.urls.i18n)),
    url(r'admin/', include(admin.site.urls)),
    url(r'^site_media/(.*)$', django.views.static.serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^select2/', include(django_select2.urls)),
]

if settings.DEBUG:
    urlpatterns += static(str(settings.STATIC_URL), document_root=str(settings.STATICFILES_DIRS[0]))

for app in settings.INSTALLED_APPS:
        if isinstance(app, AppConfigMod):
            pos = app.name
        else:
            pos = app
            if pos.startswith('django') or pos.startswith('debug') or pos.startswith('registration') or pos.startswith('crispy') or pos.startswith('bootstrap_admin'):
                continue
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
            print(pos)
            traceback.print_exc()

#if settings.DEBUG:
#    for dir in settings.STATICFILES_DIRS:
#        for root, dirs, files in os.walk(dir+'_src'):
#            for file_name in files:
#                if file_name.lower().endswith('.py') or file_name.lower().endswith('.pjsx'):
#                    src = os.path.join(root, file_name)
#                    (base, ext) = os.path.splitext(file_name)
#                    dest_base_path = root.replace('_src','')
#                    dest = os.path.join(dest_base_path, base+".js")
#
#                    if not os.path.exists(dest_base_path):
#                        os.makedirs(dest_base_path)
#
#                    if os.path.exists(dest):
#                        if os.path.getmtime(dest) >= os.path.getmtime(src):
#                            continue
#                    with open(src, "rt") as f:
#                        code = f.read()
#                        #try:
#                        if True:
#                            if file_name.lower().endswith('.py'):
#                                codejs = schlib.schindent.indent_style.py_to_js(code, root)
#                            else:
#                                codejs = schlib.schindent.indent_style.pjsx_to_js(code, root)
#                            if codejs:
#                                with open(dest, "wt", encoding='utf-8') as f2:
#                                    f2.write(codejs)
#                        #except:
#                        #    print("compile error - file:", src)
