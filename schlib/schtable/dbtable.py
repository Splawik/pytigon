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


import django.apps.registry

from schlib.schtable import table
from schlib.schtools import schjson


__COLMAP__ = {
    'AutoField': 'string',
    'SOIntCol': 'long',
    'CharField': 'string',
    'TextField': 'string',
    'BooleanField': 'bool',
    'SOFloatCol': 'double',
    'SOKeyCol': 'long',
    'SOForeignKey': 'x',
    'SOEnumCol': 'string',
    'SODateTimeCol': 'date',
    'DateField': 'date',
    'SODecimalCol': 'double',
    'SOCurrencyCol': 'double',
    'SOBLOBCol': 'string',
    'SOPickleCol': 'string',
    'SOStringLikeCol': 'string',
    }

__COLINIT__ = {
    'AutoField': None,
    'SOIntCol': '0',
    'CharField': '',
    'TextField': '',
    'BooleanField': True,
    'SOFloatCol': 0.0,
    'SOKeyCol': None,
    'HiddenForeignKey': None,
    'ForeignKey': None,
    'SOEnumCol': '',
    'SODateTimeCol': '2000-01-01',
    'DateField': '2000-01-01',
    'SODecimalCol': 0.0,
    'SOCurrencyCol': 0.0,
    'SOBLOBCol': '',
    'SOPickleCol': '',
    'SOStringLikeCol': '',
    }

__COLSIZE__ = {
    'AutoField': 9,
    'SOIntCol': 9,
    'CharField': 0,
    'TextField': 0,
    'BooleanField': 1,
    'SOFloatCol': 12,
    'SOKeyCol': 25,
    'ForeignKey': 25,
    'HiddenForeignKey': 25,
    'SOEnumCol': 25,
    'SODateTimeCol': 18,
    'SODateCol': 10,
    'SODecimalCol': 12,
    'SOCurrencyCol': 12,
    'SOBLOBCol': 9,
    'SOPickleCol': 10,
    'SOStringLikeCol': 0,
    'DateField': 10,
    }


class DbTable(table.Table):

    def __init__(self, app, tab):
        self.auto_cols = []
        self.foreign_key_parm = dict()
        self.app = app
        self.tab = tab

        self.tab_conw = {
            'long': self.conw_long,
            'string': self.conw_none,
            'double': self.conw_float,
            'bool': self.conw_bool,
            'choice': self.conw_none,
            'x': self.conw_x,
            }

        self.model_class = django.apps.registry.apps.get_model(app, tab)
        self.col_length = self._get_col_length()
        self.col_names = self._get_col_names()
        self.col_types = self._get_col_types()
        self.default_rec = self._get_default_rec()
        self.query = None

    def conw_long(self, l):
        if l:
            return int(l)
        else:
            return None

    def conw_none(self, n):
        return n

    def conw_float(self, f):
        if f:
            return float(f)
        else:
            return None

    def conw_bool(self, b):
        if b:
            return bool(b)
        else:
            return None

    def conw_x(self, x):
        if x == None or len(x) == 0:
            ret = x.GetStringRepr()
        else:
            ret = 0
        return ret

    def _get_col_names(self):
        n = []
        for col in self.model_class._meta.fields:
            if col.verbose_name:
                n.append(col.verbose_name)
            else:
                n.append(col.name)
        return n

    def _get_default_rec(self):
        n = []
        global __COLINIT__
        for col in self.model_class._meta.fields:
            n.append(__COLINIT__[col.__class__.__name__])
        return n

    def _get_col_types(self):
        n = []
        global __COLMAP__
        for col in self.model_class._meta.fields:
            if type(col).__name__ in ('ForeignKey', 'HiddenForeignKey'):
                pos = 'x:/%s/table/%s/%s/dict/' % (self.app, self.tab, col.name)
                if col.name[:-2] in self.foreign_key_parm:
                    pos = pos + '|' + self.foreign_key_parm
                n.append(pos)
            else:
                if col.choices:
                    n.append('y:' + schjson.dumps(col.choices))
                else:
                    n.append(__COLMAP__[col.__class__.__name__])
        return n

    def _get_col_length(self):
        global __COLMAP__
        global __COLSIZE__
        ret = []
        for col in self.model_class._meta.fields:
            size = __COLSIZE__[col.__class__.__name__]
            if size == 0:
                if col.choices:
                    max = 0
                    for choice in col.choices:
                        if len(choice[1]) > max:
                            max = len(choice[1])
                    size = max
                else:
                    size = col.max_length
            if size == None or size == 0:
                size = 25
            ret.append(size)
        return ret[1:]

    def _set_sort(self, objects, sort):
        sortobj = objects
        items = sort.split(',')
        for item in items:
            znak = False
            if item[0] == '-':
                item = item[1:]
                znak = True
            for col in self.model_class._meta.fields:
                if col.verbose_name:
                    colname0 = col.verbose_name
                else:
                    colname0 = col.name
                colname1 = col.name
                if item == colname0:
                    if znak:
                        colname1 = '-' + colname1
                    sortobj = sortobj.order_by(colname1)
        return sortobj

    def page(self,nr,sort=None,value=None):
        if value and value != '':
            if hasattr(self.model_class, 'simple_query'):
                data = self.model_class.simple_query(value)
            else:
                data = self.model_class.objects.all()
        else:
            data = self.model_class.objects.all()
        if sort:
            data = self._set_sort(data, sort)
        tab = []
        data = data[nr * 256:(nr + 1) * 256]
        for rec in data:
            row = []
            for field in self.model_class._meta.fields:
                value = field.value_from_object(rec)
                if field.choices:
                    if value in dict(field.choices):
                        value = str(value) + ':' + dict(field.choices)[value]
                    else:
                        value = ''
                else:
                    if type(field).__name__ in ('ForeignKey', 'HiddenForeignKey'):
                        value2 = getattr(rec, field.name)
                        if value2:
                            value2 = str(value2.id) + ':' + str(value2)
                        if value == None:
                            value = '0'
                        if value2 == None:
                            value2 = ''
                        value = str(value2)
                row.append(value)
            tab.append(row)
        return tab


    def rec_as_str(self, nr):
        obj = self.model_class.objects.get(id=nr)
        return str(obj)

    def count(self, v):
        return self.model_class.objects.count()

    def insert_rec(self, rec):
        i = 1
        obj = self.model_class()
        for field in self.model_class._meta.fields[1:]:
            if field.choices:
                field.save_form_data(obj, rec[i].split(':')[0])
            else:
                if type(field).__name__ in ('ForeignKey', 'HiddenForeignKey'):
                    if rec[i] == '' or rec[i] == None:
                        field.save_form_data(obj, None)
                    else:
                        field.save_form_data(obj, field.rel.to.objects.get(id=int(rec[i].split(':')[0])))
                else:
                    field.save_form_data(obj, rec[i])
            i = i + 1
        obj.save()
        return None

    def update_rec(self, rec):
        i = 1
        obj = self.model_class.objects.get(id=rec[0])
        for field in self.model_class._meta.fields[1:]:
            if field.choices:
                field.save_form_data(obj, rec[i].split(':')[0])
            else:
                if type(field).__name__ in ('ForeignKey', 'HiddenForeignKey'):
                    if rec[i] == '':
                        field.save_form_data(obj, None)
                    else:
                        field.save_form_data(obj,
                                field.rel.to.objects.get(id=int(rec[i].split(':')[0])))
                else:
                    field.save_form_data(obj, rec[i])
            i = i + 1
        obj.save()

    def delete_rec(self, nr):
        obj = self.model_class.objects.get(id=nr)
        obj.delete()

    def auto(self,col_name,col_names,rec):
        pass


