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

_ = wx.GetTranslation


class LoginDialog(wx.Dialog):
    """Helper class to create login dialog"""
    def __init__(self,parent,id,title,size=wx.DefaultSize,pos=wx.DefaultPosition,style=wx.DEFAULT_DIALOG_STYLE,
            use_metal=False, username=None):

        wx.Dialog.__init__(self, parent, id, title, pos, size, style)
        self.CenterOnParent()

        if 'wxMac' in wx.PlatformInfo and use_metal:
            self.SetExtraStyle(wx.DIALOG_EX_METAL)
        sizer = wx.GridBagSizer(5, 2)
        self.message = wx.StaticText(self, -1, '')
        font = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.message.SetFont(font)
        label1 = wx.StaticText(self, -1, _('User name:'))
        self.text1 = wx.TextCtrl(self, -1, '', size=(180, -1))
        if username:
            self.text1.SetValue(username)
        label2 = wx.StaticText(self, -1, _('Password:'))
        self.text2 = wx.TextCtrl(self, -1, '', size=(180, -1), style=wx.TE_PASSWORD)
        btnsizer = wx.StdDialogButtonSizer()
        btn = wx.Button(self, wx.ID_OK)
        btn.SetDefault()
        btnsizer.AddButton(btn)
        btn = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(btn)
        btnsizer.Realize()
        sizer.Add(self.message, (0, 0))
        sizer.Add(5,5,(1, 0))
        sizer.Add(label1, (1, 1))
        sizer.Add(self.text1, (1, 2))
        sizer.Add(label2, (2, 1))
        sizer.Add(self.text2, (2, 2))
        sizer.Add(btnsizer, (3, 2), (1, 1))
        sizer.Add(5,5,(4, 4))
        self.SetSizer(sizer)
        sizer.Fit(self)
        if username:
            self.text2.SetFocus()