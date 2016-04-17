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

class DataPopup(wx.MiniFrame):
    def __init__(self, parent, id, title, pos, size, style, combo, href):
        from schcli.guiframe.htmlsash import SchSashWindow
        self.href = href
        self.combo = combo
        self.point = pos
        self.size = size
        self.dismiss_block = False
        wx.Window.__init__(self, parent, id, title, pos, size) #, wx.RESIZE_BORDER )
        self.html = SchSashWindow(self, self.href + "dialog/|value", self.combo,  pos=(0, 0), size=size)
        self.html.Body.parent_combo = combo

        self.Bind(wx.EVT_KEY_DOWN, self.on_key_down)
        self.Bind(wx.EVT_ACTIVATE, self.on_activate)

        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self.html, 1, wx.ALL|wx.GROW, 1)
        self.SetSizer(box)
        self.SetAutoLayout(True)
        self.Fit()
        self.Move(self.point)


    def on_activate(self, event):
        if not event.GetActive():
            self.Hide()
            self.combo.SetFocus()
        else:
            LayoutAlgorithm().LayoutWindow(self.html, self.html.Body)
            self.html.Body.Refresh()
        event.Skip()

    def on_key_down(self, event):
        if event.KeyCode == wx.WXK_ESCAPE:
            self.Dismiss()
        else:
            event.Skip()

    def SetXY(self, point):
        self.point = point

    def Popup(self):
        self.Show()
        def _after():
            self.Move(self.point)
            self.SetSize(self.size)
            self.html.refresh_html()
            self.html.SetFocus()
        wx.CallAfter(_after)

    def Dismiss(self):
        if not self.dismiss_block:
            self.dismiss_block=True
            self.combo.set_focus()

    def _Dismiss(self):
        self.combo.set_focus()

    def set_new_href(self, href):
        self.href = href
        if self.html:
            self.html.set_new_href(href)


class DataPopupControl(ComboCtrl):

    def __init__(self, *args, **kwds):
        if "style" in kwds:
            kwds['style'] |= wx.TE_PROCESS_ENTER
        else:
            kwds['style'] = wx.TE_PROCESS_ENTER

        ComboCtrl.__init__(self, *args, **kwds)

        self.win = None

        href = self.href.split(';')
        if len(href)>1:
            self.href = href[0]
            self.href2 = href[1]
        else:
            self.href2=None

        self.Http = wx.GetApp().get_http(self)
        self.Http.get(self, str(self.href) + "size/")

        self.size = schjson.loads(self.Http.str())
        self.Http.clear_ptr()

        self.RecValue = []
        if self.defaultvalue:
            self.ClearStr = self.defaultvalue
        else:
            self.ClearStr = ""
        self.StartValue = ""

        self.DismissObject = None
        self.EventObject = None

        pos = self.GetScreenPosition()
        pos = (pos[0], pos[1] + self.GetSize()[1])

        self.sash = None
        self.popup = None
        self.defSize = False

        self.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)

        self.simpleDialog = True
        #self.simpleDialog = False
        if self.GetTextCtrl():
            self.GetTextCtrl().SetForegroundColour(wx.Colour(0, 0, 0))

    def to_masked(self, **kwds):
        self.win = ComboCtrl.GetTextCtrl(self)
        self.win.__class__ = masked.TextCtrl
        self.win._PostInit(setupEventHandling = True, name = 'maskedTextCtrl', value = '')
        self.win.SetCtrlParameters(**kwds)

    def GetTextCtrl(self):
        if self.win:
            return self.win
        return ComboCtrl.GetTextCtrl(self)

    def SetFocus(self):
        if self.GetTextCtrl():
            self.GetTextCtrl().SetFocus()
        else:
            self.SetFocus()

    def any_parent_command(self, command, *args, **kwds):
        '''Uruchomienie komendy okna nadrzędnego np: any_parent_command("RegisterRefrObj",self)'''

        parent = self
        while parent != None:
            if hasattr(parent, command):
                return getattr(parent, command)(*args, **kwds)
            parent = parent.GetParent()
        return None

    def OnSetFocus(self, event):
        value = ComboCtrl.GetValue(self)
        self.FocusIn(value)
        event.Skip()

    def KillFocus(self):
        value = ComboCtrl.GetValue(self)
        if self.readonly:
            self.FocusOut(value)

    def AlternateButtonClick(self):
        if self.EventObject:
            if hasattr(self.EventObject, "OnBeforeButtonClick"):
                self.EventObject.OnBeforeButtonClick()

        if self.simpleDialog:
            self.RunExtDialog()
        else:
            self.RunSimpleDialog()

        if self.EventObject:
            if hasattr(self.EventObject, "OnButtonClick"):
                self.EventObject.OnButtonClick()

    def OnButtonClick(self):
        if self.EventObject:
            if hasattr(self.EventObject, "OnBeforeButtonClick"):
                self.EventObject.OnBeforeButtonClick()

        if self.simpleDialog:
            self.RunSimpleDialog()
        else:
            self.RunExtDialog()

        if self.EventObject:
            if hasattr(self.EventObject, "OnButtonClick"):
                self.EventObject.OnButtonClick()


    def RunSimpleDialog(self):
        if not self.popup:
            pos = self.GetScreenPosition()
            pos = (pos[0], pos[1] + self.GetSize()[1])
            if self.GetTextCtrl():
                self.popup = DataPopup(self.GetTextCtrl(), -1, "Wybierz pozycję", pos=pos, size=self.size, style=wx.DEFAULT_DIALOG_STYLE,
                                combo=self, href=self.href)
            else:
                self.popup = DataPopup(self, -1, "Wybierz pozycję", pos=pos, size=self.size, style=wx.DEFAULT_DIALOG_STYLE,
                                combo=self, href=self.href)
            self.popup.Show()
            print(pos)

        pos = self.GetScreenPosition()
        pos = (pos[0], pos[1] + self.GetSize()[1])
        pos = [pos[0], pos[1]]

        screen_dx = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_X)
        screen_dy = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_Y)

        try:
            popup_size = self.popup.GetSize()
        except:
            popup_size = self.popup.GetSizeTuple()

        if pos[0] + popup_size[0] > screen_dx:
            pos[0] = screen_dx - popup_size[0]
        if pos[1] + popup_size[1] > screen_dy:
            pos[1] = pos[1]-self.GetSize().GetHeight()-popup_size[1]

        self.defSize = True
        self.popup.SetXY(pos)
        self.popup.Popup()

    def RunExtDialog(self):
        self.GetTextCtrl().SetFocus()

        parm = dict()
        parm["value"] = self.get_parm("value")

        if self.href2:
            href = self.href2
        else:
            href = self.href

        self.sash = self.GetParent().NewChildPage(str(href + "dialog/|value"), "Wybierz pozycję", parm)
        self.sash.Body.old_any_parent_command = self.sash.Body.any_parent_command
        self.sash.Body.any_parent_command = self.any_parent_command
        self.sash.Body.parent_combo = self

    def GetLastControlWithFocus(self):
        return self

    def FocusIn(self, value):
        pass

    def FocusOut(self, value):
        if str(value) != self.StartValue:
            if not str(value) == "":
                self.Http = wx.GetApp().get_http(self)
                x = b32encode(value.encode('utf-8'))
                self.Http.post(self, str(self.href) + "test/", {"value": x})
                #self.Http.Get(self, str(self.href) + "test/", {"value": b32encode(value).encode('utf-8')})
                tab = schjson.loads(self.Http.str())
                ret = tab[0]

                self.Http.clear_ptr()
                if ret != 1:
                    if ret == 2:
                        self.forceFocus = False
                        self.OnButtonClick()
                    else:
                        self.ClearRec()
                else:
                    self.SetRec(tab[1], tab[2], False)

    def has_parm(self, parm):
        return True if parm=='value' else False

    def get_parm(self, parm):
        return b32encode(ComboCtrl.GetValue(self).encode('utf-8')) if parm=='value' else None

    def SetRec(self, value, value_rec, dismiss=False):
        value2 = value
        if self.EventObject:
            if hasattr(self.EventObject, "SetRec"):
                value2 = self.EventObject.SetRec(value, value_rec, dismiss)

        self.StartValue = value2
        self.SetValue(value2)
        self.RecValue = value_rec

        if dismiss:
            self.Dismiss()

        parent = self.GetParent()
        if hasattr(parent, "OnPopupControlChangeValue"):
            parent.OnPopupControlChangeValue(self)


    def get_rec(self):
        return self.RecValue

    def ClearRec(self):
        self.StartValue = ""
        self.SetValue(self.ClearStr)
        self.RecValue = []

    def DoSetPopupControl(self, popup):
        pass

    def Dismiss(self):
        if self.sash:
            self.sash.Body.old_any_parent_command("on_cancel", None)
            self.sash = None
        else:
            if self.popup:
                self.popup.Close()
                self.popup = None
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

        href3 += "dialog/|value"

        if self.popup:
            self.popup.set_new_href(href3)
