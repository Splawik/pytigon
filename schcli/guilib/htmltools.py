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
import platform
import schcli.guictrl.ctrl


class HtmlErrorDialog(wx.Dialog):

    def __init__(
        self,
        parent,
        id,
        title,
        text,
        size=wx.DefaultSize,
        pos=wx.DefaultPosition,
        style=wx.DEFAULT_DIALOG_STYLE,
        use_metal=False,
        ):

        try:
            pre = wx.PreDialog()
            pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
            pre.Create(
                parent,
                id,
                title,
                pos,
                size,
                style,
                )
            self.PostCreate(pre)
        except:
            wx.Dialog.__init__(self, parent, id, title, pos, size, style)

        if 'wxMac' in wx.PlatformInfo and use_metal:
            self.SetExtraStyle(wx.DIALOG_EX_METAL)
        sizer = wx.BoxSizer(wx.VERTICAL)


        if wx.Platform == '__WXMSW__':
            self.label = schcli.guictrl.ctrl.HTML2(self, size=(800, 600), name="webbrowser", backend="wxWebViewIE")
        else:
            self.label = schcli.guictrl.ctrl.HTML2(self, size=(800, 600), name="webbrowser")
        #self.label = schcli.guictrl.schctrl.HTML(self, size=(800,600), name="webbrowser", data=text)
        try:
            sizer.Add(self.label.wb, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        except:
            sizer.Add(self.label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        btnsizer = wx.StdDialogButtonSizer()
        btn = wx.Button(self, wx.ID_OK, 'Kontynuuj')
        btn.SetHelpText('The OK button completes the dialog')
        btn.SetDefault()
        btnsizer.AddButton(btn)
        btn = wx.Button(self, wx.ID_CANCEL, 'Przerwij program')
        btn.SetHelpText('The Cancel button cnacels the dialog. (Cool, huh?)')
        btnsizer.AddButton(btn)
        btnsizer.Realize()
        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.SetSizer(sizer)
        sizer.Fit(self)
        self.label.load_str(text)
        #self.t1 = wx.Timer(self)
        #self.t1.Start(25)
        #self.txt = text
        #self.Bind(wx.EVT_TIMER, self.on_timer, self.t1)


    def set_acc_key_tab(self, win, tab):
        pass

    #def on_timer(self, evt):
    #    if platform.system() == "Windows":
    #        wx.html2.WebView.New("messageloop")
    #    if self.txt:
    #        #print(self.txt)
    #        #self.label.load_url("www.onet.pl")
    #        self.label.load_str(self.txt)
    #        #self.label.SetValue(self.txt)
    #        self.txt = None

