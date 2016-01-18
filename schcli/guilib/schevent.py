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

ID_START = wx.NewId()

ID_NextTab = wx.NewId()
ID_PrevTab = wx.NewId()
ID_CloseTab = wx.NewId()
ID_NextPage = wx.NewId()
ID_PrevPage = wx.NewId()
ID_RefreshTab = wx.NewId()
ID_Exit = wx.NewId()
ID_Reset = wx.NewId()
ID_Undo = wx.NewId()
ID_Redo = wx.NewId()
ID_Cut = wx.NewId()
ID_Copy = wx.NewId()
ID_Paste = wx.NewId()
ID_SelAll = wx.NewId()
ID_Help = wx.NewId()
ID_GotoHeader = wx.NewId()
ID_GotoPanel = wx.NewId()
ID_GotoFooter = wx.NewId()
ID_GotoDesktop = wx.NewId()
ID_ShowHeader = wx.NewId()
ID_ShowPanel = wx.NewId()
ID_ShowFooter = wx.NewId()
ID_ShowDesktop = wx.NewId()
ID_ShowToolbar1 = wx.NewId()
ID_ShowToolbar2 = wx.NewId()
ID_ShowStatusBar = wx.NewId()
ID_RetValue = wx.NewId()

ID_ZOOM = wx.NewId()
ID_PAGE_SOURCE = wx.NewId()
ID_PAGE_BLOCK = wx.NewId()
ID_PAGE_VIEW = wx.NewId()
ID_HISTORY_SHOW = wx.NewId()
ID_CLEAR_HISTORY = wx.NewId()
ID_BOOKMARK_ADD = wx.NewId()
ID_SHOW_BOOKMARKS = wx.NewId()
ID_SHOW_DOWNLOAD = wx.NewId()
ID_DOWNLOAD_OPTIONS = wx.NewId()
ID_GENERAL_OPTIONS = wx.NewId()
ID_DOWNLOAD_OPTIONS = wx.NewId()
ID_FIND = wx.NewId()
ID_REPLACE = wx.NewId()
ID_PRINT = wx.NewId()
ID_PRINT_PREVIEW = wx.NewId()
ID_PRINT_SETTINGS = wx.NewId()
ID_WEB_BACK = wx.NewId()
ID_WEB_FORWARD = wx.NewId()
ID_WEB_STOP = wx.NewId()
ID_WEB_REFRESH = wx.NewId()
ID_WEB_ADDBOOKMARK = wx.NewId()
ID_WEB_NEW_WINDOW = wx.NewId()
ID_WEB_SOURCE = wx.NewId()
ID_WEB_UP = wx.NewId()
ID_WEB_DOWN = wx.NewId()
ID_WEB_EDIT = wx.NewId()
ID_TASKBAR_SHOW = wx.NewId()
ID_TASKBAR_HIDE = wx.NewId()
ID_TASKBAR_CLOSE = wx.NewId()
ID_TASKBAR_TOGGLE = wx.NewId()
ID_LOAD = wx.NewId()
ID_SAVE = wx.NewId()
ID_SAVE_AS = wx.NewId()

ID_SIGNAL = wx.NewId()

ID_END = wx.NewId()

#EVT_USER_FIRST=32000

userEVT_REFRPARM = wx.NewEventType()
EVT_REFRPARM = wx.PyEventBinder(userEVT_REFRPARM, 1)


#class RefrParmEvent(wx.PyCommandEvent):
#
#    def __init__(self, evt_type, id):
#        wx.PyCommandEvent.__init__(self, evt_type, id)

userEVT_SIGNAL = wx.NewEventType()
EVT_SIGNAL = wx.PyEventBinder(userEVT_SIGNAL, 1)


class SignalEvent(wx.PyCommandEvent):
    def __init__(self, id, name, param):
        wx.PyCommandEvent.__init__(self, userEVT_SIGNAL, id)
        self.name = name
        self.param = param
        self.ret = None

    def set_signale_name(self, name):
        self.name = name

    def get_signal_name(self):
        return self.name

    def set_signal_params(self, param):
        self.param = param

    def get_signal_param(self):
        return self.param

    def set_return_value(self, ret):
        self.ret = ret

    def get_return_value(self):
        return self.ret


class Signals():
    def __init__(self):
        self._capture_signals = {}
        self.Bind(EVT_SIGNAL, self.on_signal)


    def send_signal(self, signal, params):
        event = SignalEvent(self.GetId(), signa, params)
        self.GetEventHandler().ProcessEvent(event)
        event.get_return_value()


    def post_signal(self, signal, params):
        event = SignalEvent(self.GetId(), signa, params)
        return self.GetEventHandler().QueueEvent(event)


    def on_signal(self, event):
        name = event.get_signal_name()
        if name in self._capture_signals:
            fun = self._capture_signals[name]
            ret = fun(event.get_signal_param())
            event.set_return_value(ret)
        else:
            event.Skip()


    def handle_signal(self, signal_name, fun):
        self._capture_signals[signal_name] = fun

