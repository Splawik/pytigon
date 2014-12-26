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
import os

if not wx.Platform == '__WXMSW__':


    def init_plugin(
        app,
        mainframe,
        desktop,
        mgr,
        menubar,
        toolbar,
        accel,
        ):
        from .poppler_viewer import PDFWindow
        from schcli.guictrl.schctrl import SchBaseCtrl
        import schcli.guictrl.schctrl


        class Pdfviewer(PDFWindow, SchBaseCtrl):

            def __init__(self, *args, **kwds):
                SchBaseCtrl.__init__(self, args, kwds)
# self.obj = SChBaseCtrl(self, args, kwds)
#
# wx.Panel.__init__(self, parent, -1) print "x1:", args print "x2:", kwds del
# kwds['name']
                #if 'name' in kwds:
                #    del kwds['name']
                PDFWindow.__init__(self, *args)#, **kwds)

# print "PDFWindow"
#
# hsizer = wx.BoxSizer( wx.HORIZONTAL ) vsizer = wx.BoxSizer( wx.VERTICAL )
# self.buttonpanel = pdfButtonPanel(self, wx.NewId(), wx.DefaultPosition,
# wx.DefaultSize, 0) vsizer.Add(self.buttonpanel, 0,
# wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT|wx.TOP, 5) self.viewer =
# pdfViewer( self, wx.NewId(), wx.DefaultPosition, wx.DefaultSize,
# wx.HSCROLL|wx.VSCROLL|wx.SUNKEN_BORDER) vsizer.Add(self.viewer, 1,
# wx.GROW|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5) hsizer.Add(vsizer, 1,
# wx.GROW|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5) self.SetSizer(hsizer)
# self.SetAutoLayout(True)
#
# self.buttonpanel.viewer = self.viewer self.viewer.buttonpanel =
# self.buttonpanel self.temp_file_name = None

            def load_file(self, file, delete_on_exit=False):
                wx.BeginBusyCursor()
                self.LoadDocument(file)
# self.viewer.LoadFile(file)
                wx.EndBusyCursor()
                if delete_on_exit:
                    self.temp_file_name = file

            def CanClose(self):
                if self.temp_file_name:
                    os.remove(self.temp_file_name)
                return True


        schcli.guictrl.schctrl.PDFVIEWER = Pdfviewer


else:


    def init_plugin(
        app,
        mainframe,
        desktop,
        mgr,
        menubar,
        toolbar,
        accel,
        ):
        pass


