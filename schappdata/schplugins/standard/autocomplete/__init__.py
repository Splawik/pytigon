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
from schlib.schtools import schjson
from autocomplete import TextCtrlAutoComplete
from schcli.guictrl.ctrl import SchBaseCtrl
import schcli.guictrl.ctrl

#import urllib.request, urllib.parse, urllib.error


class DbDict(object):

    def __init__(self, href):
        self.href = href
        self.tab = ['']

    def filter(self, parent, f):
        http = wx.GetApp().get_http(parent)
        http.get(self, str(self.href), {'query': f.encode('utf-8')})
        s = http.str()
        try:
            self.tab = schjson.loads(s)
        except:
            self.tab = []
        self.tab2 = []
        for pos in self.tab:
# self.tab2.append((pos['label'], pos['value']))
            self.tab2.append((pos['value'], ))
        self.tab = self.tab2
        http.clear_ptr()

    def __iter__(self):
        for x in self.tab:
            yield x

    def __getitem__(self, id):
        if id < len(self.tab):
            return self.tab[id]
        else:
            return None

    def __len__(self):
        return len(self.tab)

    def __contains__(self, x):
        if x in self.tab:
            return True
        else:
            return False


class Autocomplete(TextCtrlAutoComplete, SchBaseCtrl):

    def __init__(self, parent, **kwds):
        SchBaseCtrl.__init__(self, parent, kwds)
        self.dynamic_choices = DbDict(self.src)
        if 'style' in kwds:
            style = kwds['style']
            style = style | wx.TE_MULTILINE | wx.TE_PROCESS_ENTER
            kwds['style'] = style
        else:
            kwds['style'] = wx.TE_MULTILINE | wx.TE_PROCESS_ENTER

# if kwds.has_key("size"): size = kwds["size"] print "size:", size kwds["size"]
# = wx.Size(size[0],30) else: kwds["size"] = wx.Size(-1, 30)

        kwds['choices'] = self.dynamic_choices
        TextCtrlAutoComplete.__init__(self, parent, colNames=('label', 'value'), **kwds)
        self.SetEntryCallback(self.set_dynamic_choices)
        self.SetMatchFunction(self.match)
        if 'data' in self.param:
            self.SetValue(self.param['data'].encode('utf-8'))

# self.SetSelectCallback(self.select_callback)
#
# def onListItemSelected (self, event): print "onListItemSelected" return
# TextCtrlAutoComplete.onListItemSelected(self, event)
#
# def select_callback(self, value): self.SetValue(value)

    def SetValue(self, value):
        if value.__class__ == str:
            return TextCtrlAutoComplete.SetValue(self, value.decode('utf-8'))
        else:
            return TextCtrlAutoComplete.SetValue(self, value)

    def on_key_down(self, event):
        kc = event.GetKeyCode()
# sel = self.dropdownlistbox.GetFirstSelected() if kc == wx.WXK_DOWN : if sel <
# (self.dropdownlistbox.GetItemCount () - 1) : self.dropdownlistbox.Select(
# sel+1 ) self._listItemVisible() self._showDropDown ()
# self._setValueFromSelected2() elif kc == wx.WXK_UP : if sel > 0 :
# self.dropdownlistbox.Select( sel - 1 ) self._listItemVisible()
# self._showDropDown () self._setValueFromSelected2()
        if kc in (wx.WXK_LEFT, wx.WXK_RIGHT):
            event.Skip()
        else:
            super(Autocomplete, self).onKeyDown(event)

    def match(self, text, choice):
        """Demonstrate \"smart\" matching feature, by ignoring http:// and www. when \
doing
        matches.

"""

        t = text.lower()
        c = choice.lower()
        if c.startswith(t):
            return True
        if c.startswith(r'http://'):
            c = c[7:]
        if c.startswith(t):
            return True
        if c.startswith('www.'):
            c = c[4:]
        return c.startswith(t)

    def set_dynamic_choices(self):
        ctrl = self
        text = ctrl.GetValue().lower()
        self.dynamic_choices.filter(self.GetParent(), text)
        if len(self.dynamic_choices) > 1:
            ctrl.SetMultipleChoices(self.dynamic_choices)
        else:
            if len(self.dynamic_choices) > 0:
                ctrl.SetChoices(self.dynamic_choices[0])

    def _set_value_from_selected(self):
        x = TextCtrlAutoComplete._setValueFromSelected(self)
        return x

    def _set_value_from_selected2(self):
        sel = self.dropdownlistbox.GetFirstSelected()
        if sel > -1:
            if self._colFetch != -1:
                col = self._colFetch
            else:
                col = self._colSearch
            itemtext = self.dropdownlistbox.GetItem(sel, col).GetText()
            self.SetValue(itemtext)


def init_plugin(
    app,
    mainframe,
    desktop,
    mgr,
    menubar,
    toolbar,
    accel,
    ):
    schcli.guictrl.ctrl.AUTOCOMPLETE = Autocomplete


