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

from django.conf.urls import url, include

from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView

from django.views.generic import TemplateView
import django.contrib.auth.views
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from pytigon_lib.schdjangoext.tools import make_href

from pytigon_lib.schtools.tools import is_in_dicts, get_from_dicts

from . import views

DEFPARAM = "color_body_0_2:303030,color_body_0_5:787878, color_body_0_7:A8A8A8,color_body_0_9:D8D8D8,\
color_body:F0F0F0,color_body_1_1:F1F1F1,color_body_1_3:F4F4F4,color_body_1_5:F7F7F7,color_body_1_8:FCFCFC,\
color_higlight:FFFFFF,color_shadow:A0A0A0,color_background_0_5:787878,color_background_0_8:C0C0C0,\
color_background_0_9:D8D8D8,color_background:F0F0F0,color_background_1_1:F1F1F1,\
color_background_1_2:F3F3F3,color_background_1_5:F7F7F7,color_info:FFFFF0"

@csrf_exempt
def sch_login(request, *argi, **argv):
    path = ""
    path_after_error = ""
    if is_in_dicts('next', (request.POST, request.GET)):
        path = get_from_dicts('next', (request.POST, request.GET))
    if not path:
        path = settings.URL_ROOT_FOLDER + "/"
    if is_in_dicts('next_after_error', (request.POST, request.GET)):
        path_after_error = get_from_dicts('next_after_error', (request.POST, request.GET))
    if not path_after_error:
        path_after_error = path

    if is_in_dicts('username', (request.POST, request.GET) ):
        username = get_from_dicts('username', (request.POST, request.GET) )
        if is_in_dicts('password', (request.POST, request.GET)):
            password = get_from_dicts('password', (request.POST, request.GET))
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if username == 'auto':
                    request.session['autologin'] = True
                parm = request.POST.get('client_param', '')
                if parm != '':
                    request.session['client_param'] = dict([pos.split(':') for pos in parm.split(',')])
                else:
                    request.session['client_param'] = dict([pos.split(':') for pos in DEFPARAM.split(',')])
                return HttpResponseRedirect(path)

    if 'from_pytigon' in request.GET:
        return HttpResponse("Error!")
    else:
        return HttpResponseRedirect(path_after_error)



urlpatterns = [
    url(r'^ok/$', views.ok, name='ok'),
    url(r'^(?P<id>.+)/(?P<title>.+)/ret_ok/$', views.ret_ok, name='ret_ok'),

    url(r'^login/$', TemplateView.as_view(template_name='schapp/login.html')),

    url(r'^do_login/$', sch_login), #, { 'template_name': 'schapp/index.html'}),
    url(r'^do_logout/$', django.contrib.auth.views.LogoutView.as_view(next_page = make_href("/") ) ),
    url(r'^change_password/$', views.change_password),

    url(r'^accounts/', include('allauth.urls')),

    url(r'^message/(?P<titleid>.+)/(?P<messageid>.+)/(?P<id>\d+)/$', views.message),

    url(r'^datedialog/(?P<action>\w+)/$', views.datedialog),
    url(r'^listdialog/(?P<action>\w+)/$', views.listdialog),
    url(r'^treedialog/(?P<app>\w+)/(?P<tab>\w+)/(?P<id>[\d-]*)/(?P<action>\w+)/$',
        views.treedialog),
    url(r'^tabdialog/(?P<app>\w+)/(?P<tab>\w+)/(?P<id>[\d-]*)/(?P<action>\w+)/$', views.tabdialog),
    url(r'^table/(?P<app>\w+)/(?P<tab>\w+)/grid/$', views.tbl),

    url(r'^widget_web$', TemplateView.as_view(template_name='schsys/widget_web.html') ),
    url(r'^plugins/(?P<app>\w+)/(?P<plugin_name>[\w_]+)/$', views.plugins),

    url('app_time_stamp/$', views.app_time_stamp, {}),
    url('search/$', views.search, {}),
]


gen = True