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

import traceback
import sys
import os

from django.conf import settings

def import_model(app, tab):
    """import model module for specified application and return module instance."""
    try:
        m = '%s.models' % str(app)
        module = None
        models = None
        for tmp in sys.modules:
            if m in tmp:
                module = sys.modules[tmp]
                models = module
                break
        if not module:
            module = __import__('%s.models' % str(app))
        if module:
            if not models:
                models = getattr(module, 'models')
            model = getattr(models, tab)
            return model
        return None
    except:
        traceback.print_exc()

def gettempdir():
    return settings.TEMP_PATH

def make_href(href):
    if settings.URL_ROOT_FOLDER and href.startswith('/'):
        return "/" + settings.URL_ROOT_FOLDER + href
    else:
        return href