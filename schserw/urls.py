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

#from django.conf.urls.defaults import *
from django.conf.urls import patterns, url, include
from django.http import HttpResponse
# import schserw.settings as settings
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static

import traceback
#import exceptions
#from django.contrib import databrowse
from django.views.generic import TemplateView
from django.contrib.auth.views import login
import re
from schlib.schdjangoext.django_init import AppConfigMod
from django.template.base import add_to_builtins

add_to_builtins('schserw.schsys.templatetags.defexfiltry')

#import django

#django.setup()
#admin.autodiscover()

#
# import logging l = logging.getLogger('django.db.backends')
# l.setLevel(logging.DEBUG) l.addHandler(logging.StreamHandler())


def ok(request):
    return HttpResponse("""<head><meta name="TARGET" content="_parent_refr" /><meta name="RETURN" content="RETURN_OK" /></head><body>OK</body>""")



# def BasePath(request): return HttpResponse("")

#defparm= "color_body_0_2:303030,color_body_0_5:787878, color_body_0_7:A8A8A8,color_body_0_9:D8D8D8,\
#color_body:F0F0F0,color_body_1_1:F1F1F1,color_body_1_3:F4F4F4,color_body_1_5:F7F7F7,color_body_1_8:FCFCFC,\
#color_higlight:FFFFFF,color_shadow:A0A0A0,color_background_0_5:787878,color_background_0_8:C0C0C0,\
#color_background_0_9:D8D8D8,color_background:F0F0F0,color_background_1_1:F1F1F1,\
#color_background_1_2:F3F3F3,color_background_1_5:F7F7F7,color_info:FFFFF0"


def sch_login(request, *argi, **argv):
    ret = login(request, *argi, **argv)
    return ret
#    parm = request.REQUEST.get('client_param', '')
 #   if parm != '':
#        request.session['client_param'] = parm
#    else:
#        request.session['client_param'] = defparm
        
#    return ret


urlpatterns = patterns(
    '',
    url(r'^$', TemplateView.as_view(template_name='schapp/index.html'), name='start'),
    (r'schplugins/(?P<template_name>.*)','schserw.schsys.views.plugin_template'),
    (r'schsys/r/', include('django.conf.urls.shortcut')),
    (r'schsys/jsi18n/$', 'django.views.i18n.javascript_catalog', {'packages': ('django.conf', )}),
    (r'schsys/i18n/', include('django.conf.urls.i18n')),
    (r'admin/', include(admin.site.urls)),
    (r'schsys/do_login/$', sch_login, { 'template_name': 'schapp/index.html'}),
    (r'schsys/do_logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    (r'schsys/message/(?P<titleid>.+)/(?P<messageid>.+)/(?P<id>\d+)/$','schserw.schsys.views.message'),
    #(r'^databrowse/(.*)', databrowse.site.root),
    (r'schsys/ok/$', 'schserw.urls.ok'),
    (r'^static/(.*)$', 'django.views.static.serve', {'document_root': settings.ROOT_PATH + '/static'}),
    (r'^site_media/(.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )

#urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#print(settings.MEDIA_URL, settings.MEDIA_ROOT)
# urlpatterns+=patterns('', (r'^site_media/(.*)$', 'django.views.static.serve',
# {'document_root': settings.ROOT_PATH+'/static/media' }))

#from django.apps.base import AppConfig

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
                    #urlpatterns += patterns('', (r'site_media/' + str(elementy[1]) + '/(.*)$', 'django.views.static.serve', {'document_root': settings.ROOT_PATH + '/app_sets/' + str(elementy[1])}))
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


#    urlpatterns = patterns('',
#        #'^', include(urlpatterns), # iff you wish to maintain the un-prefixed URL's too
#        url(r'^intranet/$', TemplateView.as_view(template_name='schapp/index.html'), name='start'),
#        ('^intranet/', include(urlpatterns)),
#    )
