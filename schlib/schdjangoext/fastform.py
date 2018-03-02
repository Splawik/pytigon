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

"""
Form example in string format
Co to jest?
Nazwisko
Nazwisko2::*
imie//Imię!::*
Opis::_
Data::####.##.##
Wiek::0
Kwota!::9.99
Wybierz::[opcja1;opcja2
opcja3]
"""

from django import forms


def _scan_lines(input_str):
    l = input_str.replace('\r','').split('\n')
    ret = []
    append_to_last = False
    for pos in l:
        if append_to_last:
            ret[-1]=ret[-1]+";"+pos
            if ']' in pos:
                append_to_last=False
        else:
            ret.append(pos)
            if ':[' in pos and not ']' in pos:
                append_to_last = True
    return ret


def _get_name_and_title(s):
    required = False
    if s.endswith('!'):
        required = True
        s = s[:-1]

    if '//' in s:
        name, title = s.split('//', 1)
    else:
        title = s
        x = s.encode('ascii', 'replace').decode('utf-8').replace('?','_').lower()
        name = ""
        for z in x:
            if (z>='a' and z<='z') or (z>='0' and z<='9') or z=='_':
                name += z
        name = name[:16]
    return name, title, required


def _read_form_line(line):
    kwargs = {}
    field_type = None
    title=""
    name=""
    required=False
    frm=""
    if "::" in line:
        x = line.rsplit("::", 1)
        line2 = x[0].strip()
        frm = x[1].strip()
        if frm.startswith('0'):
            field_type=forms.IntegerField
            if len(frm)>1:
               kwargs = { 'min_value': 0, 'max_value': 10**len(frm) }
        elif frm.startswith('9'):
            field_type=forms.FloatField
            if len(frm)>1:
               kwargs = { 'min_value': 0, 'max_value': 10**len(frm) }
        elif frm.startswith('#'):
            field_type=forms.DateField
        elif frm.startswith('*'):
            field_type=forms.CharField
            if len(frm)>0:
               kwargs = { 'max_length': len(frm) }
        elif frm.startswith('_'):
            field_type=forms.CharField
            kwargs = { 'widget': forms.Textarea }
        elif frm.startswith('['):
            field_type=forms.ChoiceField
            choices = list([ (pos,pos,) for pos in frm[1:-1].split(';') if pos])
            kwargs = { 'choices': choices }
    else:
        if line.endswith('?'):
            field_type=forms.BooleanField
            line2 = line[:-1].strip()
        else:
            field_type=forms.CharField
            line2 = line
    name, title, required = _get_name_and_title(line2)
    return name, field_type, title, required, kwargs


def form_from_str(input_str, init_data = {}, base_form_class = forms.Form, prefix=""):
    if 'base_form' in input_str:
        make_form_str = "def make_form_class(base_form):\n" + "\n".join(
            ['    ' + pos for pos in input_str.split('\n')]) + "\n"
        exec(make_form_str)
        _Form = locals()['make_form_class'](base_form_class)
        return _Form
    else:
        class _Form(base_form_class):
            def __init__(self, *args, **kwargs):
                super(_Form, self).__init__(*args, **kwargs)

                tab = _scan_lines(input_str)
                for pos in tab:
                    if pos:
                        name, field_type, title, required, form_kwargs = _read_form_line(pos.strip())
                        if name in init_data:
                            self.fields[prefix+name] = field_type(label=title, required=required, initial=init_data[name], **form_kwargs)
                        else:
                            self.fields[prefix+name] = field_type(label=title, required=required, **form_kwargs)
        return _Form
