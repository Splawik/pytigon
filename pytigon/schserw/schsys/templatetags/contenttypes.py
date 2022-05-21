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

""" python template filters
"""

from django import template
from django.contrib.contenttypes.models import ContentType

register = template.Library()


@register.filter(name="table_exists")
def table_exists(table_name):
    """Returns True if table exists else False"""
    ret = True
    try:
        obj = ContentType.objects.get(model=table_name.lower())
    except:
        ret = False
    return ret
