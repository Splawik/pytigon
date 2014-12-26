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
from .views import FileManagerForm
from schlib.schviews import form_with_perms
from django.views.generic import TemplateView

v = form_with_perms('schplace')
urlpatterns = patterns(
    '',
    (r'table/FileManager/list/(?P<param>.*)/$', v, dict(form_class=FileManagerForm, template_name='schcommander/filemanager.html')),
    (r'table/FileManager/grid/(?P<folder>.*)/(?P<value>[\w=]*)/$', 'schlib.schfs.vfstable.vfstable_view'),
    (r'table/FileManager/open/(?P<file>.*)/$', 'schlib.schfs.vfstable.vfsopen'),
    (r'table/FileManager/save/(?P<file>.*)/$', 'schlib.schfs.vfstable.vfssave' ),
    (r'table/FileManager/open_page/(?P<file>.*)/(?P<page>\d+)/$', 'schlib.schfs.vfstable.vfsopen_page'),
    (r'table/FileManager/copy/$', TemplateView.as_view(template_name='schcommander/copydialog.html') ),
    (r'table/FileManager/move/$', TemplateView.as_view(template_name='schcommander/movedialog.html') ),
    (r'table/FileManager/mkdir/$',TemplateView.as_view(template_name='schcommander/mkdir.html') ),
    (r'table/FileManager/rename/$',TemplateView.as_view(template_name='schcommander/rename.html')),
    )
