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


"""SchPage is a container for 4 SchForm classes: body, header, footer and panel. Only "body" object is obligatory.
"""


import wx
try:
    from wx.adv import LayoutAlgorithm
except:
    from wx import LayoutAlgorithm
from schcli.guilib import event
from schcli.guilib.signal import Signal
from schlib.schtools import createparm
from schlib.schhttptools.schhtml_parser import ShtmlParser
from schcli.guiframe.form import SchForm
from schcli.guilib.event import *


class SchPage(wx.Window, Signal):
    """SchPage class"""

    def __init__(self, parent, address_or_parser, parameters, pos=(0,0), size=wx.DefaultSize):
        """Contructor

        Args:
            parent - parent window
            address_or_parser: can be: address of http page (str type) or
            :class:'~schlib.schhttptools.schhtml_parser.ShtmlParser'
            parameters: dict
        """

        self._active = True
        self._ctrl_dict_old = {}
        self._ctrl_dict = {}
        self._last_size = None
        self._disable_setfocus = 0
        self._signal_handlers = []

        self.address_or_parser = address_or_parser
        self.parameters = parameters
        self.default_button = None
        self.parent_page = None
        self.last_control_with_focus = None
        self.vertical_position = None

        self.header = None
        self.panel = None
        self.body = None
        self.footer = None
        self.active_form = None
        self.active_ctrl = None

        Signal.__init__(self)
        wx.Window.__init__(self,parent,-1,pos,size,style= wx.WANTS_CHARS,name='SchPage')

        self.exists = True

        mp = self._read_html(address_or_parser, parameters)
        if not mp:
            print('ERROR READ HTML:', address_or_parser, parameters)

        self.address = mp.address
        header = mp.get_header()
        body = mp.get_body()
        footer = mp.get_footer()
        panel = mp.get_panel()
        config = mp.var

        vscroll = True
        hscroll = True

        if 'no_vscrollbar' in config:
            vscroll = False
        if 'no_hscrollbar' in config:
            hscroll = False
        if 'vertical_position' in config:
            self.set_vertical_position(config['vertical_position'])

        self.title = mp.title

        if 'disable_parent' in config:
            if config['disable_parent'] == '0':
                self.disable_parent = False
            else:
                self.disable_parent = True
        else:
            self.disable_parent = True

        winids = []

        if header[0]:
            topwin = wx.adv.SashLayoutWindow(self, -1, wx.DefaultPosition, (100, 5), wx.adv.SW_3D, style=wx.WANTS_CHARS)
            topwin.SetOrientation(wx.adv.LAYOUT_HORIZONTAL)
            topwin.SetAlignment(wx.adv.LAYOUT_TOP)
            topwin.SetSashVisible(wx.adv.SASH_BOTTOM, True)
            self.header = SchForm(topwin, page=self, form_type="header")
            self.header.show_form(header)
            dy = self.header.calculate_best_size()[1]
            topwin.SetDefaultSize((1000, dy))
            self._top_window = topwin
            winids.append(topwin.GetId())
        else:
            self._top_window = None

        if footer[0]:
            bottomwin = wx.adv.SashLayoutWindow(self, -1, wx.DefaultPosition, (1000, 5), wx.adv.SW_3D)
            bottomwin.SetOrientation(wx.adv.LAYOUT_HORIZONTAL)
            bottomwin.SetAlignment(wx.adv.LAYOUT_BOTTOM)
            bottomwin.SetSashVisible(wx.adv.SASH_TOP, True)
            self.footer = SchForm(bottomwin, page=self, form_type="footer")
            self.footer.show_form(footer)
            bottomwin.SetDefaultSize((1000, self.footer.calculate_best_size()[1]))
            self._bottom_window = bottomwin
            winids.append(bottomwin.GetId())
        else:
            self._bottom_window = None

        if panel[0]:
            leftwin = wx.adv.SashLayoutWindow(self, -1, wx.DefaultPosition, (5, 100), wx.adv.SW_3D)
            leftwin.SetOrientation(wx.adv.LAYOUT_VERTICAL)
            leftwin.SetAlignment(wx.adv.LAYOUT_LEFT)
            leftwin.SetSashVisible(wx.adv.SASH_RIGHT, True)
            self.panel = SchForm(leftwin, page=self, form_type="panel")
            self.panel.show_form(panel)
            xy = self.panel.calculate_best_size()
            leftwin.SetDefaultSize(xy)
            self._left_window = leftwin
            winids.append(leftwin.GetId())
        else:
            self._left_window = None

        self.body = SchForm(self, self, hscroll, vscroll)
        self.body.set_htm_type('body')
        attrs = mp.get_body_attrs()
        if 'width' in attrs and 'height' in attrs:
            w = attrs['width']
            h = attrs['height']
            self.body.bestsize = (int(w) * 4 / 3, int(h) * 4 / 3)
        self.body.show_form(body, parameters)
        self.body.set_address_parm(self.address)
        if 'refresh' in mp.var:
            self.body.refresh_time(int(mp.var['refresh']))

        if winids:
            self.Bind(wx.adv.EVT_SASH_DRAGGED_RANGE, self.on_sash_drag, id=min(winids), id2=max(winids))

        self.Bind(wx.EVT_SIZE, self.on_size)
        self.body.Bind(wx.EVT_CHILD_FOCUS, self.on_child_focus)
        self.Bind(wx.EVT_SET_FOCUS, self.on_set_focus)

    def reg_application_signal_handler(self, fun, signal):
        """register callback function for signal

        Args:
            fun - callback function
            signal - name of signal
        """
        for pos in self._signal_handlers:
            if pos[1] == signal:
                break
        dispatcher.connect(fun, signal, sender=dispatcher.Any )
        self._signal_handlers.append((fun, signal))

    def unreg_application_signal_handler(self, signal):
        """Unregister signal"
        """
        i = 0
        test = None
        for pos in  self._signal_handlers:
            if pos[1] == signal:
                test = pos
                break
            i+=1
        if test:
            dispatcher.disconnect(pos[0], pos[1], sender=dispatcher.Any)
            del self._signal_handlers[i]

    def _read_html(self, address_or_parser, parameters):
        """Run a http request and read result page

        Args:
            address_or_parser: can be: address of http page (str type) or
            :class:'~schlib.schhttptools.schhtml_parser.ShtmlParser'
            parameters: dict
        """
        mp, adr = wx.GetApp().read_html(self, address_or_parser, parameters)
        return mp

    def append_ctrl(self, obj):
        self._ctrl_dict[obj.get_unique_name()] = obj

    def restart_ctrl_lp(self):
        self._ctrl_dict_old = self._ctrl_dict
        self._ctrl_dict = {}

    def pop_ctrl(self, name):
        if name in self._ctrl_dict_old:
            ret = self._ctrl_dict_old[name]
            del self._ctrl_dict_old[name]
            return ret
        else:
            return None

    def test_ctrl(self, name):
        if name in self._ctrl_dict:
            return True
        else:
            return False

    def remove_old_ctrls(self):
        for name in self._ctrl_dict_old:
            win = self._ctrl_dict_old[name]
            win.Destroy()
            #if name in self.body.controls:
            #   del self.body.controls[name]
        self._ctrl_dict_old = {}

    def __getitem__(self, key):
        return self._ctrl_dict[key]

    def get_widgets(self):
        return self._ctrl_dict

    def init_frame(self):
        if self.header:
            self.header.init()
        if self.footer:
            self.footer.init()
        if self.panel:
            self.panel.init()

        self.body.init()

    def get_parent_page(self):
        """Return parent wxPage object"""
        return self.parent_page

    def set_default_button(self, button):
        """Set default button, when Enter key is pressed action connected to button is invoked"""
        self.default_button = button

    def on_key_down(self, event):
        if event.KeyCode == wx.WXK_RETURN and self.default_button:
            self.default_button.OnClick(event)
        else:
            event.Skip()

    def on_char_hook(self, event):
        if event.KeyCode == wx.WXK_ESCAPE:
            if hasattr(self.GetParent(), 'on_child_form_cancel'):
                self.GetParent().on_child_form_cancel()
            else:
                event.Skip()
        else:
            event.Skip()

    def get_title(self):
        """Return page title"""
        return self.title

    def set_adr_and_param(self, address_or_parser, param):
        """Modify web address and parameters

        Args:
            address_or_parser: can be: address of http page (str type) or
            :class:'~schlib.schhttptools.schhtml_parser.ShtmlParser'
            parameters: dict
        """
        self.address_or_parser = address_or_parser
        self.parameters = param

    def _refresh(self):
        if self.address_or_parser.__class__.__name__ == 'ShtmlParser':
            if self.address_or_parser.address:
                mp = self._read_html(self.address_or_parser.address,
                                     self.parameters)
            else:
                mp = self._read_html(self.address_or_parser, self.parameters)
        else:
            mp = self._read_html(self.address_or_parser, self.parameters)
        if not mp:
            return
        address = mp.address
        header = mp.get_header()
        body = mp.get_body()
        footer = mp.get_footer()
        panel = mp.get_panel()
        config = mp.var
        self.title = mp.title
        if self.header:
            if not self.header.show_form("""<html encoding="utf-8">""" + header + '</html>'):
                return False
        if self.body:
            if not self.body.show_form(body, self.parameters):
                return False
        if self.footer:
            if not self.footer.show_form("""<html encoding="utf-8">""" + footer + '</html>'):
                return False
        if self.panel:
            if not self.panel.show_form("""<html encoding="utf-8">""" + panel + '</html>'):
                return False
        if self.header:
            self.header.init()
        if self.footer:
            self.footer.init()
        if self.panel:
            self.panel.init()

        self.body.Refresh()
        self.body.init()
        return True

    def CanClose(self):
        if self.body:
            if not self.body.CanClose():
                return False
        if self.header:
            if not self.header.CanClose():
                return False
        if self.footer:
            if not self.footer.CanClose():
                return False
        if self.panel:
            if not self.panel.CanClose():
                return False

        if self.header: self.header._on_close()
        if self.body: self.body._on_close()
        if self.footer: self.footer._on_close()
        if self.panel: self.panel._on_close()

        for pos in self._signal_handlers:
            dispatcher.disconnect(pos[0], pos[1], sender=dispatcher.Any)

        return True

    def on_set_focus(self, evt):
        if self.body:
            self.body.SetFocus()

    def on_child_focus(self, evt):
        if not self._disable_setfocus:
            new_win = evt.GetWindow()
            parent = new_win.GetParent()
            while parent != None:
                if parent.__class__.__name__ == 'HtmlPanel':
                    parent.SelectTab()
                    break
                parent = parent.GetParent()
            while new_win != None:
                if new_win.GetParent() and new_win.GetParent().GetWindowStyleFlag() & wx.TAB_TRAVERSAL != 0:
                    break
                new_win = new_win.GetParent()
            if new_win != self.last_control_with_focus:
                if self.last_control_with_focus:
                    if hasattr(self.last_control_with_focus, 'KillFocus'):
                        self._disable_setfocus = True
                        getattr(self.last_control_with_focus, 'KillFocus')()
                        self._disable_setfocus = False
                self.last_control_with_focus = new_win
            evt.Skip()
        else:
            evt.Skip()

    def set_focus(self):
        if self.last_control_with_focus:
            self.last_control_with_focus.SetFocus()
        else:
            super().SetFocus()

    def on_sash_drag(self, event):
        if event.GetDragStatus() == wx.SASH_STATUS_OUT_OF_RANGE:
            return
        eobj = event.GetEventObject()
        if eobj is self._top_window:
            self._top_window.SetDefaultSize((1000, event.GetDragRect().height))
        elif eobj is self._left_window:
            self._left_window.SetDefaultSize((event.GetDragRect().width, 1000))
        elif eobj is self.bottom_window:
            self._bottom_window.SetDefaultSize((1000, event.GetDragRect().height))
        LayoutAlgorithm().LayoutWindow(self, self.body)
        self.body.Refresh()

    def on_size(self, event):
        LayoutAlgorithm().LayoutWindow(self, self.body)
        self.body.Refresh()
        if event:
            event.Skip()

    def get_last_control_with_focus(self):
        return self.last_control_with_focus

    def refresh_html(self, method=0):
        """Reload page from the server"""
        return self._refresh_html(method)

    def _refresh_html(self, method=0):
        ret = self._refresh()
        self.body.wxdc = None
        self.body.update_controls = True
        self.body.Refresh()
        if not ret:
            return False
        return True

    def has_parm(self, param):
        return self.item_exist(param)

    def get_parm(self, param):
        ctrl=self.get_item(param)
        if ctrl:
            return ctrl.GetValue()
        else:
            return None

    def get_item(self, ctrl_name):
        if self.body != None and hasattr(self.body, ctrl_name):
            return getattr(self.body, ctrl_name)
        if self.header != None and hasattr(self.header, ctrl_name):
            return getattr(self.header, ctrl_name)
        if self.panel != None and hasattr(self.panel, ctrl_name):
            return getattr(self.panel, ctrl_name)
        if self.footer != None and hasattr(self.footer, ctrl_name):
            return getattr(self.footer, ctrl_name)
        return None

    def item_exist(self, ctrl_name):
        """Test if a page have specified control

        Args:
            ctrl_name -  name of control element
        """
        if self.body and hasattr(self.body, ctrl_name):
            return True
        if self.header and hasattr(self.header, ctrl_name):
            return True
        if self.panel and hasattr(self.panel, ctrl_name):
            return True
        if self.footer and hasattr(self.footer, ctrl_name):
            return True
        return False

    def __getitem__(self, key):
        return self.get_item(key)

    def calculate_best_size(self):
        if self._last_size:
            dx = self._last_size.GetWidth()
            dy = self._last_size.GetHeight()
            self._last_size = None
            return (dx,dy)
        dx = 0
        dy = 0

        if self.header:
            (x, y) = self.header.calculate_best_size()
            dy = dy + y
        if self.body:
            (x, y) = self.body.calculate_best_size()
            dx = dx + x
            dy = dy + y
        if self.footer:
            (x, y) = self.footer.calculate_best_size()
            dy = dy + y
        if self.panel:
            (x, y) = self.panel.calculate_best_size()
            dx = dx + x
            if y > dy:
                dy = y
        return (dx, dy)

    def enable_forms(self, enable):
        """Enable or disable managed by this window forms

        Params:
            enable - if True enable forms, if False - disable forms
        """
        if enable==False:
            self._last_size = self.GetSize()
        if not (enable==False and not self.disable_parent):
            if self.header:
                self.header.Enable(enable)
            if self.body:
                self.body.Enable(enable)
            if self.footer:
                self.footer.Enable(enable)
            if self.panel:
                self.panel.Enable(enable)

    def change_notebook_page_title(self, new_title):
        """Change a title of notebook witch contain this SchPage object"""
        p = self.GetParent()
        tab = p.GetParent()
        sel = tab.GetPageIndex(p)
        tab.SetPageText(sel, new_title)

    def set_new_href(self, href):
        """Set new web address"""
        self.address_or_parser = href

    def activate_page(self):
        self._active = True
        self.body.SetFocus()

    def deactivate_page(self):
        self._active = False

    def is_active(self):
        return self._active

    def set_page(self, page_source):
        """Set content of body form asigned to this page

        Args:
            page_source: new text content
        """
        self.body.set_page(page_source)


    def set_vertical_position(self, position):
        """Position of child form

        position:
            "top"
            "bottom"
            None or "default" (defautl)
        """
        self.vertical_position = position

    def close(self):
        self.GetParent().on_child_form_cancel()
