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


"""Module contains many additional db models.
"""

from django.db import models
from django import forms

from schlib.schtools.schjson import json_dumps, json_loads
from schlib.schdjangoext.fastform import form_from_str


class JSONModel(models.Model):
    class Meta:
        abstract = True

    jsondata = models.TextField('Json data', null=True, blank=True, editable=False, )

    def __getattribute__(self, name):
        if name.startswith('json_'):
            if not hasattr(self, '_data'):
                self._data = json_loads(self.jsondata)
            if name[5:] in self._data:
                return self._data[name[5:]]
            return None

        return super().__getattribute__(name)

    def get_json_data(self):
        if not hasattr(self, "_data"):
            if self.jsondata:
                self._data = json_loads(self.jsondata)
            else:
                self._data = {}
        return self._data

    def get_form(self, view, request, form_class, adding=False):
        data = self.get_json_data()
        if hasattr(self, "get_form_source"):
            txt = self.get_form_source()
            if txt:
                if data:
                    form_class2 = form_from_str(txt, init_data=data, base_form_class=form_class, prefix="json_")
                else:
                    form_class2 = form_from_str(txt, init_data={}, base_form_class=form_class, prefix="json_")
                return view.get_form(form_class2)
            else:
                return view.get_form(form_class)
        elif data:
            class form_class2(form_class):
                def __init__(self, *args, **kwargs):
                    nonlocal data
                    super().__init__(*args, **kwargs)
                    for key, value in data.items():
                        self.fields['json_%s' % key] = forms.CharField(label=key, initial=value)
            return view.get_form(form_class2)
        return view.get_form(form_class)

    def save(self, *args, **kwargs):
        if hasattr(self, '_data'):
            if 'json_update' in self._data:
                data = {}
                if self.jsondata:
                    d = json_loads(self.jsondata)
                    for key, value in d.items():
                        data[key] = value
                for key, value in self._data.items():
                    if key != 'json_update':
                        data[key] = value
                json_str = json_dumps(data)
            else:
                json_str = json_dumps(self._data)
            self.jsondata = json_str

        super().save(*args, **kwargs)

