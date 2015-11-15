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

#author: "Sławomir Chołaj (slawomir.cholaj@gmail.com)"
#copyright: "Copyright (C) ????/2012 Sławomir Chołaj"
#license: "LGPL 3.0"
#version: "0.1a"

import wx
from schcli.guictrl.schbasectrl import SchBaseCtrl


class COMPOSITE_PANEL(wx.Panel, SchBaseCtrl):
    def __init__(self, *args, **kwds):
        SchBaseCtrl.__init__(self, args, kwds)
        wx.Panel.__init__(self, *args, **kwds)

    #def __getattr__(self, attr_name):
    #    return getattr(self.GetParent(),attr_name)
