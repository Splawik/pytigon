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
from schcli.guictrl.popup import popuphtml
import string
import datetime
from pdb import set_trace
from schlib.schtools import schjson

from  wx.grid import GridCellEditor


class PopupDataCellControl(popuphtml.DataPopupControl):

    def __init__(self,href,*args,**kwds):
        self.href = href
        self.defaultvalue = None
        popuphtml.DataPopupControl.__init__(self, *args, **kwds)


class PopupDataCellEditor(GridCellEditor):

    def __init__(self):
        GridCellEditor.__init__(self)
        self.address = None
        self.param = None

    def get_address(self):
        return self._address

    def set_address(self, address):
        if address != None and address[0] == '!':
            set_trace()
        self._address = address

    address = property(get_address, set_address)


    def Create(self,parent,id,evt_handler):
        self.Parent = parent
        self._tc = PopupDataCellControl(self.address, parent, id)
        self._tc.DismissObject = self
        self.SetControl(self._tc)
        self.evtHandler = evt_handler

        if evt_handler:
            self._tc.PushEventHandler(self.evtHandler)
            evt_handler.Bind(wx.EVT_KILL_FOCUS, self.on_kill_focus)

    def on_kill_focus(self, event):
        pass

    def SetSize(self, rect):
        self._tc.SetSize(rect.x, rect.y, rect.width+2, rect.height+2, wx.SIZE_ALLOW_MINUS_ONE)

    def Show(self, show, attr):
        GridCellEditor.Show(self, show, attr)

    def PaintBackground(self, rect, attr):
        pass

    def BeginEdit(self, row, col, grid):
        self.grid = grid
        self.start_value = None
        value = grid.GetTable().GetValue(row, col)

        if value.__class__ == datetime.date:
            self.start_value = value.isoformat()

        if type(value)==str:
            self.start_value = value
        else:
            self.start_value = str(value)

        self._tc.focus_in(self.start_value)
        if self.start_value:
            self._tc.set_rec(self.start_value, (self.start_value, ))
        self._tc.SetInsertionPointEnd()
        self._tc.GetTextCtrl().SetSelection(0, -1)
        self._tc.GetTextCtrl().SetFocus()

    def EndEdit(self, row, col, grid, old_value):
        self._tc.focus_out(self._tc.GetValue())
        changed = False
        value = self._tc.GetValue()
        if str(value) != str(self.start_value):
            changed = True
            grid.GetTable().SetValue(row, col, value)  # update the table
        grid.SetFocus()
        return changed

    def ApplyEdit(self, row, col, grid):
        val = self._tc.GetValue()
        grid.GetTable().SetValue(row, col, val)
        self.start_value = ''
        self._tc.SetValue('')

    def Reset(self):
        self._tc.SetValue(self.start_value)


    def IsAcceptedKey(self, evt):
        return (not (evt.ControlDown() or evt.AltDown()) and
                evt.GetKeyCode() != wx.WXK_SHIFT)

    def StartingKey(self, evt):
        key = evt.GetKeyCode()
        ch = None
        if key < 256 and key >= 0 and chr(key) in string.printable:
            ch = chr(key)
        if ch is not None:
            self._tc.start_value = ''
            self._tc.SetValue(ch)
            if self._tc.popup:
                self._tc.popup.set_string_value(ch)
            self._tc.rec_value = (ch, )
            if self._tc.popup:
                self._tc.popup.Dismiss()
            self._tc.SetInsertionPointEnd()
        else:
            evt.Skip()

    def StartingClick(self):
        print("START CLICK")
        pass

    def Clone(self):
        ret = PopupDataCellEditor()
        ret.SetParameters(self.param)
        return ret

    def set_parameters(self, params):
        self.param = params


class DatePopupDataCellEditor(PopupDataCellEditor):

    def __init__(self):
        PopupDataCellEditor.__init__(self)
        self.address = wx.GetApp().make_href('/schsys/datedialog/')

    def Create(
        self,
        parent,
        id,
        evt_handler,
        ):
        PopupDataCellEditor.Create(self, parent, id, evt_handler)
        self._tc.to_masked(autoformat='EUDATEYYYYMMDD.')

    def Clone(self):
        ret = DatePopupDataCellEditor()
        ret.address = self.address
        ret.SetParameters(self.param)
        return ret


class ListPopupCellEditor(PopupDataCellEditor):

    def __init__(self):
        PopupDataCellEditor.__init__(self)
        self.address = wx.GetApp().make_href('/schsys/listdialog/')

    def Create(self, parent, id, evt_handler):
        PopupDataCellEditor.Create(self, parent, id, evt_handler)
        self._tc.SetEventObject(self)

    def Clone(self):
        ret = ListPopupCellEditor()
        ret.address = self.address
        ret.SetParameters(self.param)
        return ret

    def BeginEdit(self, row, col, grid):
        typ = grid.GetTable().GetTypeName(row, col)
        id = typ.find(':')
        self.choices = schjson.loads(typ[id + 1:])
        PopupDataCellEditor.BeginEdit(self, row, col, grid)

    def OnButtonClick(self):
        if self._tc.simpleDialog:
            self._tc.popup.html.choices = self.choices
            self._tc.popup.html.refr()
        else:
            self._tc.page.body.choices = self.choices
            self._tc.page.body.refr()

    def set_rec(self, value, value_rec, dismiss=True):
        ret = ''
        if len(value) > 2 and value[1] == ':':
            return value
        else:
            for choice in self.choices:
                if choice[1].lower().startswith(value.lower()):
                    ret = choice[0] + ':' + choice[1]
            return ret


class GenericPopupCellEditor(PopupDataCellEditor):

    def __init__(self):
        PopupDataCellEditor.__init__(self)
        self.address = wx.GetApp().make_href('/schsys/datedialog/')

    def Clone(self):
        ret = GenericPopupCellEditor()
        ret.SetParameters(self.address)
        return ret

    def set_parameters(self, params):
        self.address = params


