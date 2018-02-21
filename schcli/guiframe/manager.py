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

    def __init__(self, *argi, **argv):
        aui.framemanager.AuiManager.__init__(self, *argi, **argv)
        self.Bind(wx.EVT_WINDOW_CREATE, self.DoUpdateEvt)

    #def Update(self):
    #    if '__WXGTK__' in wx.PlatformInfo:
    #        def _fun():
    #            self.DoUpdate()
    #            if self._frame:
    #                self._frame.Refresh()
    #        wx.CallAfter(_fun)
    #    else:
    #        super().Update()


    #def OnRender(self, event):
    #    if self._frame and self._frame.GetHandle():
    #        super().OnRender(event)
    #    else:
    #        event.Skip()

    def OnLeftDown(self, event):
        part = self.HitTest(*event.GetPosition())
        if not part.type in [0,1]:
            super().OnLeftDown(event)



class SChAuiManager(SChAuiBaseManager):
    def __init__(self, *argi, **argv):
        aui.AuiManager.__init__(self, *argi, **argv)

    def AddPane(self, window, arg1, *argi, **argv):
        ret = aui.AuiManager.AddPane(self, window, arg1, *argi, **argv)
        if hasattr(window, 'SetPanel'):
            window.SetPanel(arg1)
        return ret

    def ActivatePane(self, window):
        try:
            ret = aui.AuiManager.ActivatePane(self, window)
        except:
            ret = None
        return ret
