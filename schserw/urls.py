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

from django.conf.urls import patterns, url, include
from django.http import HttpResponse
from django.conf import settings
from django.contrib import admin

import os

import traceback
from django.views.generic import TemplateView
from django.contrib.auth.views import login
from schlib.schdjangoext.django_init import AppConfigMod
from django.template.base import add_to_builtins

#from schlib.schjs.compile import py_to_js, psjx_to_js
from schlib.schindent.indent_style import py_to_js, pjsx_to_js


add_to_builtins('schserw.schsys.templatetags.defexfiltry')


def ok(request):
    return HttpResponse("""<head><meta name="TARGET" content="_parent_refr" /><meta name="RETURN" content="RETURN_OK" /></head><body>OK</body>""")


def sch_login(request, *argi, **argv):
    ret = login(request, *argi, **argv)
    return ret


urlpatterns = patterns(
    '',
    url(r'^$', TemplateView.as_view(template_name='schapp/index.html'), name='start'),
    (r'schplugins/(?P<template_name>.*)','schserw.schsys.views.plugin_template'),
    #(r'schsys/r/', include('django.conf.urls.shortcut')),
    (r'schsys/jsi18n/$', 'django.views.i18n.javascript_catalog', {'packages': ('django.conf', )}),
    (r'schsys/i18n/', include('django.conf.urls.i18n')),
    (r'admin/', include(admin.site.urls)),
    (r'schsys/do_login/$', sch_login, { 'template_name': 'schapp/index.html'}),
    (r'schsys/do_logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    (r'schsys/message/(?P<titleid>.+)/(?P<messageid>.+)/(?P<id>\d+)/$','schserw.schsys.views.message'),
    (r'schsys/ok/$', 'schserw.urls.ok'),
    (r'^static/(.*)$', 'django.views.static.serve', {'document_root': settings.ROOT_PATH + '/static'}),
    (r'^site_media/(.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )


for app in settings.INSTALLED_APPS:

        if isinstance(app, AppConfigMod):
            pos = app.name
        else:
            pos = app
            if pos.startswith('django') or pos.startswith('mptt') or pos.startswith('debug') or pos.startswith('registration') or pos.startswith('crispy'):
                continue

        elementy = pos.split('.')
        module = __import__(pos)

        if pos == 'pytigon':
            pass

        try:
        #if True:
            #if not pos.startswith('django') and not pos.startswith('mptt') and not pos.startswith('debug'):
                module_name = '%s.urls' % str(pos)
                __import__('%s.urls' % str(pos))
                if len(elementy) > 1:
                    urlpatterns += patterns('', (r'%s/' % str(elementy[1]),
                                            include('%s.urls' % str(pos))))
                    #urlpatterns += patterns('', (r'site_media/' + str(elementy[1]) + '/(.*)$', 'django.views.static.serve', {'document_root': settings.ROOT_PATH + '/app_pack/' + str(elementy[1])}))
                else:
                    urlpatterns += patterns('', (r'%s/' % str(elementy[0]),
                                            include('%s.urls' % str(pos))))
                    #urlpatterns += patterns('', (r'site_media/' + str(elementy[0]) + '/(.*)$', 'django.views.static.serve', {'document_root': settings.LOCAL_SERW_PATH + '/media/' + str(elementy[0])}))
        #except exceptions.ImportError:
        #else:
        except:
            #if settings.DEBUG:
                #exceptions.ImportError
            print(pos)
            traceback.print_exc()

            #else:
            #    pass


if settings.DEBUG:
    for dir in settings.STATICFILES_DIRS:
        for root, dirs, files in os.walk(dir+'_src'):
            for file_name in files:
                if file_name.lower().endswith('.py') or file_name.lower().endswith('.pjsx'):
                    src = os.path.join(root, file_name)
                    (base, ext) = os.path.splitext(file_name)
                    dest_base_path = root.replace('_src','')
                    dest = os.path.join(dest_base_path, base+".js")

                    if not os.path.exists(dest_base_path):
                        os.makedirs(dest_base_path)

                    if os.path.exists(dest):
                        if os.path.getmtime(dest) >= os.path.getmtime(src):
                            continue

                    with open(src, "rt") as f:
                        code = f.read()

                        if file_name.lower().endswith('.py'):
                            codejs = py_to_js(code, root)
                        else:
                            codejs = pjsx_to_js(code, root)

                        with open(dest, "wt") as f2:
                            f2.write(codejs)
