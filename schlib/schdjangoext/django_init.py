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
#copyright: "Copyright (C) ????/2013 Slawomir Cholaj"
#license: "LGPL 3.0"
#version: "0.1a"


from importlib import import_module

from django.apps.config import AppConfig, MODELS_MODULE_NAME
from django.utils.module_loading import module_has_submodule


class AppConfigMod(AppConfig):
    def __init__(self, *argi, **argv):
        super().__init__(*argi, **argv)

    def import_models(self, all_models):
        self.models = all_models
        if module_has_submodule(self.module, MODELS_MODULE_NAME):
            models_module_name = '%s.%s' % (self.name, MODELS_MODULE_NAME)
            try:
                self.models_module = import_module(models_module_name)
            except:
                self.models_module = None


def get_app_config(app_name):
    if '.' in app_name:
        return AppConfigMod.create(app_name.split('.')[1])
    else:
        return AppConfigMod.create(app_name)

def get_app_name(app):
    if isinstance(app, AppConfig):
        return app.name
    else:
        return app
