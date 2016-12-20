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

import django.db.models.fields
#from mptt.models import TreeForeignKey
import mimetypes
from django.forms.widgets import TextInput, PasswordInput
from django.db import models
from django.forms.widgets import HiddenInput
#import schlib.schmodels.fields
django.db.models.fields.prep_for_like_query = lambda x: str(x).replace('\\', '\\\\')
from copy import deepcopy
from django.contrib.auth import get_permission_codename
from django.forms.forms import BaseForm
BaseForm._old_html_output = BaseForm._html_output


#models.TreeForeignKey = TreeForeignKey
#models.GTreeForeignKey = TreeForeignKey

models.TreeForeignKey = models.ForeignKey
models.GTreeForeignKey = models.ForeignKey
models.TreeModel = models.Model

def _html_output(
    self,
    normal_row,
    error_row,
    row_ender,
    help_text_html,
    errors_on_separate_row,
    ):
    normal_row2 = normal_row.replace('<th>', "<th align='left'><em>"
                                     ).replace('</th>', '</em></th>')
    return self._old_html_output(normal_row2, error_row, row_ender,
                                 help_text_html, errors_on_separate_row)


BaseForm._html_output = _html_output


def widget_attrs(self, widget):
    if self.max_length == None:
        max2 = 80
    else:
        if self.max_length > 80:
            max2 = 80
        else:
            max2 = self.max_length
    if self.max_length is not None and isinstance(widget, (TextInput, PasswordInput)):
        return {'max_length': str(self.max_length), 'size': str(max2)}


django.forms.fields.CharField.widget_attrs = widget_attrs

mimetypes.add_type('image/svg+xml', '.svg')


class FormProxy(object):

    def __init__(self, form):
        self.form = form

    def __getitem__(self, fields):
        tmp_fields = self.form.fields
        tabfields = fields.split('__')
        new_fields = deepcopy(self.form.fields)
        for (name, field) in list(new_fields.items()):
            if not name in tabfields:
                del new_fields[name]
        self.form.fields = new_fields
        ret = self.form.as_table()
        self.form.fields = tmp_fields
        return ret


def fields_as_table(self):
    return FormProxy(self)


django.forms.models.ModelForm.fields_as_table = fields_as_table


def widget_attrs2(self, widget):
    return {'class': 'jqcalendar', 'maxlength': '10', 'size': '10'}


#django.forms.fields.DateField.widget_attrs = widget_attrs2
from django.forms.widgets import Select


class SchSelect(Select):

    queryset = None

    def render(
        self,
        name,
        value,
        attrs=None,
        choices=(),
        ):
        if value:
            strvalue = str(self.queryset.get(id=value))
            ret = \
                '<CTRLPOPUPHTML WIDTH="200" href="/%s/table/%s/as_dict/" STRVALUE="%s:%s"></CTRLPOPUPHTML>'\
                 % (self.queryset.model._meta.app_label,
                    self.queryset.model._meta.object_name, value, strvalue)
        else:
            ret = \
                '<CTRLPOPUPHTML WIDTH="200" href="/%s/table/%s/as_dict/"></CTRLPOPUPHTML>'\
                 % (self.queryset.model._meta.app_label,
                    self.queryset.model._meta.object_name)
        return ret


old___init__ = django.forms.models.ModelChoiceField.__init__


def __init2__(
    self,
    queryset,
    empty_label='---------',
    cache_choices=False,
    required=True,
    widget=None,
    label=None,
    initial=None,
    help_text=None,
    to_field_name=None,
    *args,
    **kwargs
    ):
    ret = old___init__(
        self,
        queryset,
        empty_label,
        cache_choices,
        required,
        SchSelect,
        label,
        initial,
        help_text,
        to_field_name,
        args,
        kwargs,
        )
    self.widget.queryset = queryset
    return ret



#class HiddenForeignKey(models.ForeignKey):
#
#    def formfield(self, **kwargs):
#        field = models.ForeignKey.formfield(self, **kwargs)
#        field.widget = HiddenInput()
#        field.widget.choices = None
#        return field

#models.HiddenForeignKey = HiddenForeignKey


def _get_builtin_permissions_mod(opts):
    """Returns (codename, name) for all permissions in the given opts."""

    perms = []
    for action in ('add', 'change', 'delete', 'list'):
        perms.append((get_permission_codename(action, opts),
            'Can %s %s' % (action, opts.verbose_name_raw)))
    return perms


def init_django():
    return True


