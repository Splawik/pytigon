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


import collections


class Html(object):
    def __init__(self, name, attr=None):
        self.name = name
        self.attr = attr
        self.value = None
        self.childs = []

    def setvalue(self, value):
        self.value = value

    def setattr(self, attr):
        self.attr = attr

    def append(self, elem, attr=None):
        if type(elem) == str:
            helem = Html(elem, attr)
        else:
            helem = elem
        self.childs.append(helem)
        return helem

    def dump(self):
        ret = '<' + self.name
        if self.attr:
            ret += ' ' + self.attr.replace("'", '"')
        ret = ret + '>'
        for elem in self.childs:
            ret += elem.dump()
        if self.value:
            if isinstance(self.value, collections.Callable):
                ret += self.value()
            else:
                ret += self.value
        ret += '</' + self.name + '>'
        return ret


def make_start_tag(tag, attrs):
    ret = '<' + tag
    for pos in attrs:
        if attrs[pos] != None:
            ret += ' ' + pos + '="' + attrs[pos] + '"'
        else:
            ret += ' ' + pos
    ret += '>'
    return ret
