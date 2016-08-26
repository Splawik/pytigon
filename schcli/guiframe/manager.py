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
    Top window
"""

from wx.lib.agw import aui
import wx

class SChAuiBaseManager(aui.framemanager.AuiManager):

    def Update(self):
        def _update():
            if self._frame:
                self.DoUpdate()
        wx.CallAfter(_update)


class SChAuiManager(SChAuiBaseManager):
    def __init__(self, *argi, **argv):
        aui.AuiManager.__init__(self, *argi, **argv)

    def AddPane(self, window, arg1=None, arg2=None):
        ret = aui.AuiManager.AddPane(self, window, arg1, arg2)
        if hasattr(window, 'SetPanel'):
            window.SetPanel(arg1)
        return ret

    def ActivatePane(self, window):
        #print "ActivatePane", window
        try:
            ret = aui.AuiManager.ActivatePane(self, window)
        except:
            ret = None
        return ret


