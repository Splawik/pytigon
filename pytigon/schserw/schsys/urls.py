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

# from django.conf.urls import url, include
from base64 import b64decode
from django.utils.translation import gettext_lazy as _

from django.urls import path
from django.contrib.auth import authenticate, login, logout

from django.views.generic import TemplateView
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from pytigon_lib.schdjangoext.tools import make_href

from pytigon_lib.schtools.tools import is_in_dicts, get_from_dicts

from . import views

DEFPARAM = (
    "color_body_0_2:303030,color_body_0_5:787878, color_body_0_7:A8A8A8,color_body_0_9:D8D8D8,\
color_body:F0F0F0,color_body_1_1:F1F1F1,color_body_1_3:F4F4F4,color_body_1_5:F7F7F7,color_body_1_8:FCFCFC,\
color_higlight:FFFFFF,color_shadow:A0A0A0,color_background_0_5:787878,color_background_0_8:C0C0C0,\
color_background_0_9:D8D8D8,color_background:F0F0F0,color_background_1_1:F1F1F1,\
color_background_1_2:F3F3F3,color_background_1_5:F7F7F7,color_info:FFFFF0"
)


@csrf_exempt
def sch_login(request, *argi, **argv):
    path = ""
    if is_in_dicts("next", (request.POST, request.GET)):
        path = get_from_dicts("next", (request.POST, request.GET))
        if path and path[-1] == "=":
            path = b64decode(path.encode("utf-8")).decode("utf-8")
    if not path:
        path = make_href("/")

    if is_in_dicts("username", (request.POST, request.GET)):
        username = get_from_dicts("username", (request.POST, request.GET))
        if is_in_dicts("password", (request.POST, request.GET)):
            password = get_from_dicts("password", (request.POST, request.GET))
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                parm = request.POST.get("client_param", "")
                if parm != "":
                    request.session["client_param"] = dict(
                        [pos.split(":") for pos in parm.split(",")]
                    )
                else:
                    request.session["client_param"] = dict(
                        [pos.split(":") for pos in DEFPARAM.split(",")]
                    )
                return HttpResponseRedirect(path)
            else:
                if "from_pytigon" in request.GET:
                    return HttpResponse("Error!")
                else:
                    title = _("Login error!")
                    txt = _("Incorrect login name or password")
                    return HttpResponse(
                        '<html><head><meta name="target" content="message" data-title="%s" data-text="%s" data-icon="error"/></head></html>'
                        % (title, txt)
                    )

    if "from_pytigon" in request.GET:
        return HttpResponse("Error!")
    else:
        return HttpResponseRedirect(request.get_full_path())


def sch_logout(request):
    logout(request)
    return HttpResponseRedirect(make_href("/"))


urlpatterns = [
    path("ok/", views.ok, name="ok"),
    #path("<int:id>/<str:title>/new_row_ok/", views.ret_ok, name="new_row_ok"),
    path("login/", TemplateView.as_view(template_name="schsys/app/login.html")),
    path("do_login/", sch_login),
    path("do_logout/", sch_logout),
    path("change_password/", views.change_password),
    path("change_profile_variant/<str:variant_name>/", views.change_profile_variant),
    # path('accounts/', include('allauth.urls')),
    path("message/<str:titleid>/(<str:messageid>/<int:id>/", views.message),
    path("datedialog/<str:action>/", views.datedialog),
    path("listdialog/<str:action>/", views.listdialog),
    path("treedialog/<str:app>/<str:tab>/<int:id>/<str:action>/", views.treedialog),
    path("tabdialog/<str:app>/<str:tab>/<int:id>/<str:action>/", views.tabdialog),
    path("table/<str:app>/<str:tab>/grid/", views.tbl),
    path("widget_web", TemplateView.as_view(template_name="schsys/widget_web.html")),
    path("plugins/<str:app>/<path:plugin_name>/", views.plugins),
    path("app_time_stamp/", views.app_time_stamp, {}),
    path("search/", views.search, {}),
]


gen = True
