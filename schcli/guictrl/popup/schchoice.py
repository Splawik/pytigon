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

try:
    from wx import ComboPopup, ComboCtrl
    wx.HtmlListBox = wx.ListBox
except:
    from wx.combo import ComboPopup, ComboCtrl

class HtmlComboPopup(wx.HtmlListBox, ComboPopup):

    def __init__(self):
        self.PostCreate(wx.PreHtmlListBox())
        ComboPopup.__init__(self)
        self.List = []
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)

    def on_key_down(self, evt):
        if evt.GetKeyCode() == wx.WXK_RETURN:
            self.curitem = self.GetSelection()
            self.value = self.curitem
            self.SetSelection(self.value)
            self.Dismiss()
            return
        evt.Skip()

    def on_get_item(self, n):
        return self.List[n]

    def clear(self):
        self.List = []

    def add_item(self, txt):
        self.List.append(txt)

    def on_motion(self, evt):
        item = self.HitTest(evt.GetPosition())
        if item >= 0:
            self.SetSelection(item)
            self.curitem = item

    def on_left_down(self, evt):
        self.value = self.curitem
        self.Dismiss()

    def init(self):
        self.value = -1
        self.curitem = -1

    def create(self, parent):
        wx.HtmlListBox.Create(self, parent, style=wx.LC_LIST | wx.LC_SINGLE_SEL
                               | wx.SIMPLE_BORDER, size=(500, 700))
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        return True

    def get_control(self):
        return self

    def set_string_value(self, val):
        if val in self.List:
            self.SetSelection(self.List.index(val))

    def get_string_value(self):
        if self.value >= 0:
            return self.List[self.value]
        return ''

    def on_popup(self):
        self.SetItemCount(len(self.List))
        ComboPopup.OnPopup(self)

    def on_dismiss(self):
        ComboPopup.OnDismiss(self)

    def paint_combo_control(self, dc, rect):
        ComboPopup.PaintComboControl(self, dc, rect)

    def on_combo_key_event(self, event):
        ComboPopup.OnComboKeyEvent(self, event)

    def on_combo_double_click(self):
        ComboPopup.OnComboDoubleClick(self)

    def get_adjusted_size(
        self,
        min_width,
        pref_height,
        max_height,
        ):
        return ComboPopup.GetAdjustedSize(self, min_width,
                pref_height, max_height)

    def lazy_create(self):
        return ComboPopup.LazyCreate(self)


class HtmlComboPopupControl(ComboCtrl):

    def __init__(self, *args, **kwds):
        ComboCtrl.__init__(self, *args, **kwds)
        self.popup = HtmlComboPopup()
        self.SetPopupControl(self.popup)
        self.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        self.RecValue = []
        self.ClearStr = ''
        self.StartValue = ''

    def on_set_focus(self, event):
        value = self.GetValue()
        self.FocusIn(value)
        event.Skip()

    def kill_focus(self):
        value = self.GetValue()
        self.FocusOut(value)

    def focus_in(self, value):
        if value != None:
            self.StartValue = value
        else:
            self.StartValue = ''

    def focus_out(self, value):
        pass

    def has_parm(self, parm):
        if parm == 'value':
            return True
        return False

    def get_parm(self, parm):
        if parm == 'value':
            return self.GetValue()
        return None

    def set_rec(
        self,
        value,
        value_rec,
        dismiss=True,
        ):
        self.StartValue = value
        self.SetValue(value)
        self.popup.SetStringValue(value)
        self.RecValue = value_rec
        if dismiss:
            self.popup.Dismiss()
        parent = self.GetParent()
        if hasattr(parent, 'OnPopupControlChangeValue'):
            parent.OnPopupControlChangeValue(self)

    def clear_rec(self):
        self.StartValue = ''
        self.popup.SetStringValue('')
        self.SetValue('')
        self.RecValue = []


