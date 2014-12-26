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
from schlib.schviews import generic_table_start

from django.contrib.auth.models import User, Group
#from django.views.generic.simple import redirect_to
from django.shortcuts import redirect

urlpatterns = patterns('', 
                       #(r'search/(?P<typ>.+)/', 'schbase.views.autocomplete_search'),
                       (r'table/ProxyUser/(?P<id>\d+)/edit/password/',
                        redirect, {'url': '/admin/auth/user/%(id)s/password/'}), 
                       (r'search/(?P<typ>.+)/', 'schbase.views.autocomplete_search'))
gen = generic_table_start(urlpatterns, 'schbase')
gen.standard('Parameter', 'Parameters')
gen.standard('Autocomplete', 'Dictionaries')
gen.standard('ProxyUser', 'Users')
gen.standard('ProxyGroup', 'User groups')
