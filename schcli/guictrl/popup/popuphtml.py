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

from base64 import b32encode
import wx
from schlib.schtools import schjson
try:
    from wx import ComboCtrl
except:
    from wx.combo import ComboCtrl
from wx.lib import masked


from wx.adv import LayoutAlgorithm

"""server interface
  test(value)
      return "uzupełnienie wartości kontrolki lub pusty ciąg znaków"
  dialog(value)
      return "strona html opisująca dialog"

  rekord: (key:rec), rec[0]: id
"""

class DataPopup(wx.ComboPopup):
    def __init__(self, size, combo, href):
        self.href = href
        self.combo = combo
        self.html = None
        self.size = size
        wx.ComboPopup.__init__(self)

    def Create(self, parent):
        self.html = self.combo.on_create(parent)
        parent.Bind(wx.EVT_KEY_DOWN, self.on_key_down)
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self.html, 1, wx.ALL|wx.GROW, 1)
        parent.SetSizer(box)
        parent.SetAutoLayout(True)
        parent.Fit()
        return True

    def GetControl(self):
        return self.html

    def GetStringValue(self):
        return self.combo.start_value

    def on_key_down(self, event):
        if event.KeyCode == wx.WXK_ESCAPE:
            self.Dismiss()
        else:
            event.Skip()

    def set_new_href(self, href):
        self.href = href
        if self.html:
            self.html.set_new_href(href)

    def OnPopup(self):
        self.combo.on_popoup()
        return wx.ComboPopup.OnPopup(self)

    def GetAdjustedSize(self, minWidth, prefHeight, maxHeight):
        width = self.size[0]
        height = self.size[1]
        return wx.ComboPopup.GetAdjustedSize(self, width, height, maxHeight)



class DataPopupControl(ComboCtrl):

    def __init__(self, *args, **kwds):
        if "style" in kwds:
            kwds['style'] |= wx.TE_PROCESS_ENTER
        else:
            kwds['style'] = wx.TE_PROCESS_ENTER

        if 'dialog_with_value' in kwds:
            self.dialog_with_value = kwds['dialog_with_value']
            del kwds['dialog_with_value']
        else:
            self.dialog_with_value = True
        ComboCtrl.__init__(self, *args, **kwds)

        self.win = None
        self.html = None
        self.rec_value = []
        self.event_object = None
        self.sash = None
        self.popup = None
        self.start_value = ""

        if self.defaultvalue:
            self.clear_str = self.defaultvalue
        else:
            self.clear_str = ""

        href = self.href.split(';')
        if len(href)>1:
            self.href = href[0]
            self.href2 = href[1]
        else:
            self.href2=None

        self.http = wx.GetApp().get_http(self)
        self.http.get(self, str(self.href) + "size/")
        self.size = schjson.loads(self.http.str())
        self.http.clear_ptr()

        #self.Bind(wx.EVT_SET_FOCUS, self.on_setfocus)

        self.simpleDialog = True
        if self.GetTextCtrl():
            self.GetTextCtrl().SetForegroundColour(wx.Colour(0, 0, 0))

        self.UseAltPopupWindow(enable=True)

        popoup = self._create_popoup()
        self.SetPopupControl(popoup)


    def _create_popoup(self):
        if not self.popup:
            self.popup = DataPopup(size=self.size, combo=self, href=self.href)
        return self.popup

    def to_masked(self, **kwds):
        self.win = ComboCtrl.GetTextCtrl(self)
        self.win.__class__ = masked.TextCtrl
        self.win._PostInit(setupEventHandling = True, name = 'maskedTextCtrl', value = '')
        self.win.SetCtrlParameters(**kwds)

    def GetTextCtrl(self):
        if self.win:
            return self.win
        return ComboCtrl.GetTextCtrl(self)

    def _SetFocus(self):
        if self.GetTextCtrl():
            self.GetTextCtrl().SetFocus()
        else:
            self.SetFocus()

    def KillFocus(self):
        value = ComboCtrl.GetValue(self)
        #if self.readonly:
        #    self.focus_out(value)

    def any_parent_command(self, command, *args, **kwds):
        parent = self
        while parent != None:
            if hasattr(parent, command):
                return getattr(parent, command)(*args, **kwds)
            parent = parent.GetParent()
        return None

    def on_setfocus(self, event):
        value = ComboCtrl.GetValue(self)
        self.focus_in(value)
        event.Skip()

    def alternate_button_click(self):
        if self.event_object:
            if hasattr(self.event_object, "on_before_button_click"):
                self.event_object.on_before_button_click()

        self.run_ext_dialog()

        if self.event_object:
            if hasattr(self.event_object, "OnButtonClick"):
                self.event_object.OnButtonClick()

    def run_ext_dialog(self):
        self.GetTextCtrl().SetFocus()

        parm = dict()
        parm["value"] = self.get_parm("value")

        if self.href2:
            href = self.href2
        else:
            href = self.href

        _href = href + "dialog/|value" if self.dialog_with_value else href + "dialog/"
        self.sash = self.GetParent().NewChildPage(str(_href), "Select", parm)
        self.sash.Body.old_any_parent_command = self.sash.Body.any_parent_command
        self.sash.Body.any_parent_command = self.any_parent_command
        self.sash.Body.parent_combo = self

    def get_last_control_with_focus(self):
        return self

    def focus_in(self, value):
        pass

    def focus_out(self, value):
        if str(value) != self.start_value:
            if not str(value) == "":
                self.http = wx.GetApp().get_http(self)
                x = b32encode(value.encode('utf-8'))
                self.http.post(self, str(self.href) + "test/", {"value": x})
                tab = schjson.loads(self.http.str())
                ret = tab[0]

                self.http.clear_ptr()
                if ret != 1:
                    if ret == 2:
                        self.forceFocus = False
                        self.OnButtonClick()
                    else:
                        self.clear_rec()
                else:
                    self.set_rec(tab[1], tab[2], False)

    def has_parm(self, parm):
        return True if parm=='value' else False

    def get_parm(self, parm):
        return b32encode(ComboCtrl.GetValue(self).encode('utf-8')) if parm=='value' else None

    def set_rec(self, value, value_rec, dismiss=False):
        value2 = value
        if self.event_object:
            if hasattr(self.event_object, "set_rec"):
                value2 = self.event_object.set_rec(value, value_rec, dismiss)

        self.start_value = value2
        self.SetValue(value2)
        self.rec_value = value_rec

        if dismiss:
            self.Dismiss()

        parent = self.GetParent()
        if hasattr(parent, "on_popup_control_change_value"):
            parent.on_popup_control_change_value(self)

    def get_rec(self):
        return self.rec_value

    def clear_rec(self):
        self.start_value = ""
        self.SetValue(self.clear_str)
        self.rec_value = []

    def on_create(self, parent):
        from schcli.guiframe.htmlsash import SchSashWindow
        href = self.href + "dialog/|value" if self.dialog_with_value else self.href + "dialog/"
        self.html = SchSashWindow(parent, href, self, size=self.size)
        self.html.Body.parent_combo = self
        return self.html

    def on_popoup(self):
        if self.html:
            wx.BeginBusyCursor()
            self.html.Body.Hide()
            def _after():
                self.html.refresh_html()
                self.html.SetFocus()
                #print("X1")
                self.html.on_size(None)
                #self.html.Body.on_erase_background(None)
                #self.html.Body.init_page()
                #self.html.Body.draw_background()
                self.html.Body.init_page()
                #wx.CallAfter(self.html.Body.refr, self.start_value)
                #print("X2")
                self.html.Body.refr(self.start_value)
                #print("X3")
                self.html.Body.Show()
                wx.EndBusyCursor()
            wx.CallAfter(_after)

    def Dismiss(self):
        if self.sash:
            self.sash.Body.old_any_parent_command("on_cancel", None)
            self.sash = None
        else:
            super().Dismiss()
        self.SetFocus()


    def set_new_href(self, href):
        self.href = href

        href3 = self.href.split(';')
        if len(href3)>1:
            self.href = href3[0]
            self.href2 = href3[1]
        else:
            self.href2=None

        if self.href2:
            href3 = self.href2
        else:
            href3 = self.href

        if self.dialog_with_value:
            href3 += "dialog/|value"
        else:
            href3 += "dialog/"

        if self.popup:
            self.popup.set_new_href(href3)
