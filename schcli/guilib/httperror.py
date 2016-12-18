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
import sys

import schcli.guictrl.ctrl

_ = wx.GetTranslation

class HttpErrorDialog(wx.Dialog):

    def __init__(self,parent,title,text,size=wx.DefaultSize,pos=wx.DefaultPosition,style=wx.DEFAULT_DIALOG_STYLE,
            use_metal=False):
        try:
            pre = wx.PreDialog()
            pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
            pre.Create(parent,wx.ID_ANY,title,pos,size,style)
            self.PostCreate(pre)
        except:
            wx.Dialog.__init__(self, parent, wx.ID_ANY, title, pos, size, style)

        if 'wxMac' in wx.PlatformInfo and use_metal:
            self.SetExtraStyle(wx.DIALOG_EX_METAL)
        sizer = wx.BoxSizer(wx.VERTICAL)


        if wx.Platform == '__WXMSW__':
            self.label = schcli.guictrl.ctrl.HTML2(self, size=(800, 600), name="webbrowser", backend="wxWebViewIE")
        else:
            self.label = schcli.guictrl.ctrl.HTML2(self, size=(800, 600), name="webbrowser")

        try:
            sizer.Add(self.label.wb, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        except:
            sizer.Add(self.label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)

        btnsizer = wx.StdDialogButtonSizer()
        btn = wx.Button(self, wx.ID_OK, _('Continue'))
        btn.SetDefault()
        btnsizer.AddButton(btn)
        btn = wx.Button(self, wx.ID_CANCEL, _('Break'))
        btn.SetHelpText(_('The Break button breaks the application'))
        btnsizer.AddButton(btn)
        btnsizer.Realize()
        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.SetSizer(sizer)
        sizer.Fit(self)
        self.label.load_str(text)


def http_error(parent, content):
    """Show form with error content returned by http server

    Args:
        parent - parent window
        content - html page returned by http server
    """
    lock = wx.GetApp().lock
    if not lock:
        wx.GetApp().lock = True

        if parent and hasattr(parent,'Invalidate'):
            parent.Invalidate()

        if type(content)==str:
            c = content
        else:
            c = content.decode('utf-8')
        dlg = HttpErrorDialog(wx.GetApp().GetTopWindow(), _("Error message"), c, size=(800,600))
        dlg.CenterOnScreen()
        try:
            val = dlg.ShowModal()
        except:
            print("ERROR")
        wx.GetApp().lock = False

        if val == wx.ID_CANCEL:
            sys.exit()
