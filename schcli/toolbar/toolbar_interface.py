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

import wx


class BarNullInterface(object):

    class Page(object):

        class Panel(object):

            def __init__(self, page, title):
                self.page = page

            def append(
                self,
                id,
                title,
                bitmap=None,
                ):
                pass

        def __init__(self, bar, title):
            self.bar = bar

        def create_panel(self, title):
            return self.Panel(self, title)

    def __init__(self):
        pass

    def create_page(self, title):
        return self.Page(self, title)

    def bind(
        self,
        fun,
        id=wx.ID_ANY,
        e = None
        ):
        pass

    def un_bind(self, id, e=None):
        pass

    def realize_bar(self):
        pass

    def get_toolbars(self):
        return None

    def connect_object_to_panel(self, panel, object):
        pass


