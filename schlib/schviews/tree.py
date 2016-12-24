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


class MakeTreeFromObject(object):
    def __init__(self, model, callback, field_name=None):
        self.model = model
        self.callback = callback
        self.field_name = field_name

    def _tree_from_object_childs(self, parent):
        ret = ''
        l = self.model.objects.filter(parent=parent)
        for o in l:
            if self.callback(0, o):
                ret += '<li>'
                ret += "<span class='folder'>" + self.callback(1, o) + '</span>'
                ret += '<ul>'
                tab_action = self.callback(2, o)
                for pos in tab_action:
                    ret += '<li>'
                    link = pos[0]
                    name = pos[1]
                    ret += "<span class='file'><a href='" + link + "'>" + name\
                         + '</a></span>'
                    ret += '</li>'
                ret += self._tree_from_object_childs(o)
                ret += '</ul>'
                ret += '</li>'
        return ret.replace('<ul></ul>', '')

    def _tree_from_object(self):
        ret = ''
        l = self.model.objects.filter(parent=None)
        for o in l:
            if self.callback(0, o):
                ret += '<li>'
                ret += "<span class='folder'>" + self.callback(1, o) + '</span>'
                ret += '<ul>'
                tab_action = self.callback(2, o)
                for pos in tab_action:
                    ret += '<li>'
                    link = pos[0]
                    name = pos[1]
                    ret += "<span class='file'><a href='" + link + "'>" + name\
                         + '</a></span>'
                    ret += '</li>'
                ret += self._tree_from_object_childs(o)
                ret += '</ul>'
                ret += '</li>'
        return ret

    def _gen(self, head_ctrl, end_head_ctrl):
        try:
            if self.field_name:
                ret = head_ctrl
                ret += '<li>'
                ret += "<span class='folder'>" + self.field_name + '</span>'
                ret += '<ul>'
                ret += self._tree_from_object()
                ret += '</ul>'
                ret += '</li>'
                ret += end_head_ctrl
            else:
                ret = head_ctrl
                ret += self._tree_from_object()
                ret += end_head_ctrl
        except:
            import sys
            import traceback
            print(sys.exc_info()[0])
            print(sys.exc_info())
            traceback.print_exc()
        return ret

    def gen_html(self):
        return self._gen("<ul id='browser' class='filetree'>", '</ul>')

    def gen_shtml(self):
        return self._gen('', '')
