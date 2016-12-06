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

import string
import wx

from schlib.schtools import schjson

from schcli.guictrl.basectrl import SchBaseCtrl

_ = wx.GetTranslation


class ListBoxNoFocus(wx.ListBox):

    def CanAcceptFocus(self):
        return False


class Select2Popup(wx.MiniFrame):
    def __init__(self, parent, id, title, pos, size, style, combo, href_id):
        from schcli.guiframe.page import SchPage
        self.combo = combo
        self.point = pos
        self.href_id = href_id

        wx.MiniFrame.__init__(self, parent, id, title, pos, size, wx.RESIZE_BORDER )


        self.edit_ctrl = wx.TextCtrl(self, size=(440,-1), style=wx.TE_PROCESS_ENTER|wx.TE_PROCESS_TAB)
        self.list_ctrl = ListBoxNoFocus(self, size=(440,200), style=wx.LB_SINGLE)

        self.edit_ctrl.Bind(wx.EVT_KEY_DOWN, self.on_key_down)
        self.edit_ctrl.Bind(wx.EVT_TEXT_ENTER, self.on_enter)
        self.list_ctrl.Bind(wx.EVT_LISTBOX_DCLICK, self.on_enter)

        self.Bind(wx.EVT_ACTIVATE, self.on_activate)
        self.Bind(wx.EVT_TEXT, self.OnText)

        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self.edit_ctrl)
        box.Add(self.list_ctrl, 1, wx.ALL | wx.GROW, 1)
        self.SetSizer(box)
        self.SetAutoLayout(True)
        self.Fit()

    def on_enter(self, event):
        id = self.list_ctrl.GetSelection()
        if id != wx.NOT_FOUND:
            self.Dismiss()
            item_id = self.list_ctrl.GetClientData(id)
            item_str = self.list_ctrl.GetString(id)
            self.combo.set_value(item_id, item_str)


    def on_activate(self, event):
        if not event.GetActive():
            self.Hide()
            self.combo.SetFocus()
        else:
            #LayoutAlgorithm().LayoutWindow(self.html, self.html.body)
            pass
        event.Skip()

    def on_key_down(self, event):
        print(event.KeyCode)
        if event.KeyCode == wx.WXK_ESCAPE:
            self.Dismiss()
        elif event.KeyCode == wx.WXK_DOWN:
            id = self.list_ctrl.GetSelection()
            if id != wx.NOT_FOUND:
                if id < self.list_ctrl.GetCount()-1:
                    self.list_ctrl.SetSelection(id+1)
        elif event.KeyCode == wx.WXK_UP:
            id = self.list_ctrl.GetSelection()
            if id != wx.NOT_FOUND:
                if id > 0:
                    self.list_ctrl.SetSelection(id-1)
        elif event.KeyCode == wx.WXK_TAB:
            return self.on_enter(event)
        else:
            event.Skip()

    def OnText(self, event):
        event.Skip()
        s = event.GetString()
        href = '/select2/fields/auto.json?term=%s&page=1&context=&field_id=%s' % (s, self.href_id)
        http = wx.GetApp().get_http(self.combo)
        http.get(self, href)
        #self.Http.get(self, str(self.href) + "test/", {"value": x})
                #self.Http.Get(self, str(self.href) + "test/", {"value": b32encode(value).encode('utf-8')})
        tab = schjson.loads(http.str())
        print(tab)
        http.clear_ptr()
        if not ('err' in tab and tab['err'] != 'nil'):
            self.list_ctrl.Clear()
            if len(tab['results'])>0:
                for pos in tab['results']:
                    self.list_ctrl.Append(pos['text'], pos['id'])
                self.list_ctrl.SetSelection(0)

    def SetXY(self, point):
        self.point = point

    def Popup(self):
        self.Show()
        self.Move(self.point)

    def Dismiss(self):
        self.Hide()
        self.combo.SetFocus()

    def clear(self):
        self.edit_ctrl.ChangeValue("")
        self.list_ctrl.Clear()

class SelectBase(wx.ComboCtrl,  SchBaseCtrl):

    def __init__(self, parent, **kwds):

        SchBaseCtrl.__init__(self, parent, kwds)

        if "style" in kwds:
            kwds['style'] |= wx.TE_PROCESS_ENTER
        else:
            kwds['style'] = wx.TE_PROCESS_ENTER

        if 'item_id' in self.param and self.param['item_id']!='None':
            self.item_id = int(self.param['item_id'])
            self.item_str = self.param['item_str']
        else:
            self.item_id = -1
            self.item_str = ""

        kwds['size'] = (445, -1)

        wx.ComboCtrl.__init__(self, parent, **kwds)

        if self.GetTextCtrl():
            self.GetTextCtrl().SetForegroundColour(wx.Colour(0, 0, 0))

        self.popup = None
        self.button1 = None
        self.button2 = None

        #self.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        self.Bind(wx.EVT_CHAR, self.OnChar)

        if self.item_str:
            self.SetValue(self.item_str)

        self.Bind(wx.EVT_KEY_DOWN, self.on_key_down_base)
        self.GetParent().get_parent_page().register_signal(self, "return_row")

    def return_row(self, **argv):
        self.set_value(argv["id"], argv['title'])

    def init(self, button1, button2):
        self.button1 = button1
        self.button2 = button2

    def on_key_down_base(self, event):
        if event.GetKeyCode() == wx.WXK_TAB:
            if event.ShiftDown():
                self.GetParent().GetParent().Navigate(self.GetParent(), True)
            else:
                self.GetParent().GetParent().Navigate(self.GetParent(), False)
        elif event.GetKeyCode() == wx.WXK_F2:
            self.button1.on_click(event)
        elif event.GetKeyCode() == wx.WXK_INSERT:
            self.button2.on_click(event)
        else:
            event.Skip()


    def set_value(self, item_id, item_str):
        self.item_id = item_id
        self.item_str = item_str
        self.SetValue(item_str)

    def GetValue(self):
        return self.item_id

    #def OnSetFocus(self, event):
    #    event.Skip()

    def OnChar(self, event):
        try:
            c = chr(event.GetUnicodeKey())
            if c in string.printable:
                self._on_button_click()
                self.popup.edit_ctrl.AppendText(c)
            else:
                event.Skip()
        except:
            event.Skip()

    def OnButtonClick(self):
        ret = self._on_button_click()
        self.popup.edit_ctrl.SetValue("")
        return ret

    def _on_button_click(self):
        if not self.popup:
            pos = self.GetScreenPosition()
            pos = (pos[0], pos[1] + self.GetSize()[1])
            if self.GetTextCtrl():
                #href_id = self.data['']
                #href_id = self.param['data'][0]['attrs']['data-select2-id']
                href_id = self.param['data'][0]['attrs']['data-field_id']
                self.popup = Select2Popup(self.GetTextCtrl(), -1, _("Select item"), pos=pos, size=(450, 400), style=wx.DEFAULT_DIALOG_STYLE,
                                combo=self, href_id=href_id)
            else:
                self.popup = Select2Popup(self, -1, _("Select item"), pos=pos, size=(450, 400), style=wx.DEFAULT_DIALOG_STYLE,
                                combo=self, href_id=href_id)

        self.popup.clear()

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

        self.popup.SetXY(pos)
        self.popup.Popup()


    def DoSetPopupControl(self, popup):
        pass

    def Dismiss(self):
        if self.popup:
            self.popup.Close()
            self.popup = None
        self.SetFocus()

