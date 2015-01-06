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

from django.conf.urls import patterns
from django.views.generic import TemplateView

urlpatterns = patterns(
    '',
    (r'datedialog/(?P<akcja>\w+)/$', 'schserw.schsys.views.datedialog'),
    (r'listdialog/(?P<akcja>\w+)/$', 'schserw.schsys.views.listdialog'),
    (r'treedialog/(?P<app>\w+)/(?P<tab>\w+)/(?P<id>[\d-]*)/(?P<akcja>\w+)/$','schserw.schsys.views.treedialog'),
    (r'tabdialog/(?P<app>\w+)/(?P<tab>\w+)/(?P<id>[\d-]*)/(?P<akcja>\w+)/$', 'schserw.schsys.views.tabdialog'),
    (r'table/(?P<app>\w+)/(?P<tab>\w+)/grid/$', 'schserw.schsys.views.tbl'),

    (r'db/field/open/(?P<file>.*)/$', 'schlib.schtools.dbtools.open_db_field'),
    (r'db/field/save/(?P<file>.*)/$', 'schlib.schtools.dbtools.save_db_field'),
    (r'widget_web$', TemplateView.as_view(template_name='schsys/widget_web.html') ),
    (r'plugins/(?P<app>\w+)/(?P<plugin_name>\w+)/$','schserw.schsys.views.plugins'),
    )

