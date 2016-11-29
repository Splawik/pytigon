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
from schlib.schhtml.htmlviewer import tdata_from_html
try:
    from urllib.parse import unquote
except:
    from urllib import unquote


class SchBaseCtrl(object):

    def __init__(self, args, kwds):
        self.unique_name = None
        self.init_base(args, kwds)
        self.accept_focus = True
        self.acc_tab = False

    def CanAcceptFocus(self):
        if self.IsShown() and self.IsEnabled():
            return self.accept_focus
        else:
            return False

    def CanAcceptFocusFromKeyboard(self):
        return self.CanAcceptFocus()

    def init_base(self, args, kwds):
        self.parent = args[0]
        self.ldatabuf = None

        self.tag = None
        if 'param' in kwds:
            if 'tag' in kwds['param']:
                self.tag = kwds['param']['tag']

        if 'href' in kwds:
            self.href = kwds['href']
            if self.href == None:
                self.href = ''
            del kwds['href']
        else:
            self.href = None
        if 'label' in kwds:
            self.label = kwds['label']
            del kwds['label']
        else:
            self.label = None
        if 'id' in kwds:
            self.nr_id = kwds['id']
            del kwds['id']
        else:
            self.nr_id = None
        if 'target' in kwds:
            self.target = kwds['target']
            del kwds['target']
        else:
            self.target = '_blank'
        if 'value' in kwds:
            self.value = kwds['value']
            del kwds['value']
        else:
            self.value = None
        if 'valuetype' in kwds:
            self.valuetype = kwds['valuetype']
            del kwds['valuetype']
        else:
            self.valuetype = 'data'
        if 'defaultvalue' in kwds:
            self.defaultvalue = kwds['defaultvalue']
            del kwds['defaultvalue']
        else:
            self.defaultvalue = None
        if 'length' in kwds:
            self.length = kwds['length']
            del kwds['length']
        else:
            self.length = 0
        if 'maxlength' in kwds:
            self.maxlength = kwds['maxlength']
            del kwds['maxlength']
        else:
            self.maxlength = 0
        if 'readonly' in kwds:
            self.readonly = kwds['readonly']
            del kwds['readonly']
        else:
            self.readonly = False
        if 'hidden' in kwds:
            self.hidden = True
            del kwds['hidden']
        else:
            self.hidden = False
        if 'src' in kwds:
            self.src = kwds['src']
            del kwds['src']
        else:
            self.src = None
        if 'onload' in kwds:
            self.onload = kwds['onload']
            del kwds['onload']
        else:
            self.onload = None
        if 'tdata' in kwds:
            self.tdatabuf = None
            self.tdata = kwds['tdata']
            del kwds['tdata']
        else:
            self.tdata = None
            self.tdatabuf = None
        if 'ldata' in kwds:
            self.ldata = kwds['ldata']
            del kwds['ldata']
        else:
            self.ldata = None
        if 'data' in kwds:
            self.data = unquote(kwds['data'])
            del kwds['data']
        else:
            self.data = None
        if 'param' in kwds:
            self.param = kwds['param']
            del kwds['param']
        else:
            self.param = None
        if 'style' in kwds:
            self.style = kwds['style']
            del kwds['style']
        else:
            self.style=None
            #kwds['style'] = eval(str(style))

        print(self.tag)
        ctrl_process = wx.GetApp().ctrl_process
        if self.tag in ctrl_process:
            for fun in ctrl_process[self.tag]:
                fun(self)

    def set_unique_name(self, name):
        self.unique_name = name

    def get_unique_name(self):
        return self.unique_name

    def set_acc_key_tab(self, tab):
        return self.GetParent().set_acc_key_tab(self, tab)

    def after_create(self):
        self.Bind(wx.EVT_KEY_DOWN, self.on_key_down_base)
        if self.onload:
            d = {'wx': wx, 'self': self}
            exec(self.onload, d)

        if hasattr(self, "__ext_init__"):
            self.__ext_init__()

    def on_key_down_base(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            wx.CallAfter(self.GetParent().close_with_delay)
        elif event.GetKeyCode() == wx.WXK_TAB:
            if event.ShiftDown():
                self.GetParent().Navigate(self, True)
            else:
                self.GetParent().Navigate(self, False)
        else:
            event.Skip()

    def is_ctrl_block(self):
        return self.GetParent().is_ctrl_block(self)

    def load_data_from_server(self, path):
        http = wx.GetApp().get_http(self.parent)
        http.get(self, str(path))
        s = http.ptr()
        http.clear_ptr()
        return s

    def load_string_from_server(self, path):
        http = wx.GetApp().get_http(self.parent)
        http.get(self, str(path))
        s = http.str()
        http.clear_ptr()
        return s

    def refresh_tdata(self, html_src=None):
        if not self.tdata:
            if self.src:
                if html_src:
                    tables = html_src
                else:
                    tables = self.load_data_from_server(self.src).decode('utf-8')

                self.tdatabuf = tdata_from_html(tables, wx.GetApp().http)

    def get_tdata(self):
        if self.tdata:
            return self.tdata
        if self.tdatabuf:
            return self.tdatabuf
        if self.src:
            self.refresh_tdata()
        return self.tdatabuf

    def refresh_ldata(self):
        if not self.ldata:
            if self.src:
                lista = self.LoadDataFromServer(self.src)
                mp = list_parser.TreeParser()
                mp.feed(lista)
                mp.close()
                self.ldatabuf = mp.TreeParent[0][1]

    def get_ldata(self):
        if self.ldata:
            return self.ldata
        if self.ldatabuf:
            return self.ldatabuf
        if self.src:
            self.refreshLDATA()
        return self.ldatabuf

    def get_parent_form(self):
        parent = self.GetParent()
        while(parent!=None):
            if type(parent).__name__ == 'SchForm':
                return parent
            parent = parent.GetParent()
        return None
