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

from .htmltools import superstrip
import re

def comment_remover(text):
    def replacer(match):
        s = match.group(0)
        if s.startswith('/'):
            return ""
        else:
            return s
    pattern = re.compile(r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"', re.DOTALL | re.MULTILINE)
    return re.sub(pattern, replacer, text)

class CssPos(object):

    def __init__(self, line, attrs):
        key_main = line[-1]
        self.tag = superstrip(key_main)
        self.parents = {}
        if len(line) > 1:
            parent = CssPos(line[:-1], attrs)
            self.parents[parent.key()] = parent
            self.attrs = {}
        else:
            self.attrs = attrs

    def key(self):
        return self.tag

    def _extend_dict(self, dict_dest, dict_source):
        for pos in dict_source:
            dict_dest[pos] = dict_source[pos]

    def extend(self, line, attrs):
        if len(line) > 0:
            key_main = line[-1]
            if key_main in self.parents:
                self.parents[key_main].extend(line[:-1], attrs)
            else:
                parent = CssPos(line, attrs)
                self.parents[parent.key()] = parent
        else:
            for pos in attrs:
                self.attrs[pos] = attrs[pos]

    def _get_dict_from_parent(self, key, ret_attrs, obj):
        if key in self.parents:
            if obj.get_parent():
                attr = self.parents[key].get_dict(obj.get_parent())
                self._extend_dict(ret_attrs, attr)

    def get_dict(self, obj):
        ret_attrs = {}
        self._extend_dict(ret_attrs, self.attrs)
        if obj:
            self._get_dict_from_parent(obj.get_tag(), ret_attrs, obj)
            if obj.get_cls():
                self._get_dict_from_parent('.' + obj.get_cls(), ret_attrs, obj)
                self._get_dict_from_parent(obj.get_tag() + '.' + obj.get_cls(),
                        ret_attrs, obj)
            if obj.get_id():
                self._get_dict_from_parent('#' + obj.get_id(), ret_attrs, obj)
                self._get_dict_from_parent(obj.get_tag() + '.' + obj.get_id(),
                        ret_attrs, obj)
        return ret_attrs

    def test_print(self, indent):
        tab = indent * ' '
        print(tab, self.key(), ':')
        print(tab, 'attrs:')
        for key in self.attrs:
            print(tab, 4 * ' ', key, ':', self.attrs[key])
        print(tab, 'parents:')
        for key in self.parents:
            print(tab, 4 * ' ', 'key:')
            self.parents[key].Print(indent + 8)


class Css(object):

    def __init__(self):
        self.csspos_dict = {}
        self._act_dict = {}
        self._act_keys = []

    def _append_keys(self):
        if len(self._act_keys) > 0:
            for pos in self._act_keys:
                lastkey = pos[-1]
                if lastkey in self.csspos_dict:
                    self.csspos_dict[lastkey].extend(pos[:-1], self._act_dict)
                else:
                    y = CssPos(pos, self._act_dict)
                    self.csspos_dict[y.key()] = y
        self._act_keys = []
        self._act_dict = {}

    def parse_indent_str(self, s):
        for l in s.splitlines():
            if l == '':
                continue
            if l[0] == ' ':
                indent = True
            else:
                indent = False
            line = superstrip(l)
            y = line.split('//')
            if len(y) == 2:
                line = y[0]  # delete comments
            if line == '' or line == ' ':
                continue
            if indent:
                x = line.split(':')
                if len(x) == 2:
                    self._act_dict[x[0].strip()] = x[1].strip()
                if len(x) == 1:
                    self._act_dict[x[0].strip()] = '0'
            else:
                if len(self._act_keys) > 0:
                    self._append_keys()
                x = line.split(',')
                for pos in x:
                    self._act_keys.append(pos.strip().lower().split(' '))
                self._act_dict = {}
        if len(self._act_keys) > 0:
            self._append_keys()

    def _strip_list(self, l):
        ret = []
        for pos in l:
            ret.append(pos.strip())
        return ret

    def _hadle_section(self, section):
        x = section.split('{')
        ret = ''
        if len(x) == 2:
            xx = superstrip(x[0]).split(',')
            for pos in xx:
                self._act_keys.append(pos.strip().lower().split(' '))
                self._act_dict = {}
            y = x[1].split(';')
            for pos in y:
                z = self._strip_list(pos.split(':'))
                if z[0] != '' and z[0] != ' ':
                    if len(z) == 2:
                        self._act_dict[z[0].strip()] = z[1].strip()
                    if len(z) == 1:
                        self._act_dict[z[0].strip()] = '0'
            if len(self._act_keys) > 0:
                self._append_keys()

    def parse_str(self, s):
        s2 = comment_remover(s)
        x = superstrip(s2).split('}')
        for pos in x:
            self._hadle_section(pos)

    def test_print(self):
        tmp = CssPos([''], {})
        tmp.parents = self.csspos_dict
        tmp.test_print(0)

    def get_dict(self, obj):
        tmp = CssPos([''], {})
        tmp.parents = self.csspos_dict
        ret = tmp.get_dict(obj)
        return ret

