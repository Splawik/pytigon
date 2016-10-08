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
    from wx.adv import LayoutAlgorithm
except:
    from wx import LayoutAlgorithm
from schcli.guilib import schevent
from schlib.schtools import createparm
from schlib.schhttptools.schhtml_parser import ShtmlParser
from schcli.guiframe.htmlwin import SchHtmlWindow
from schcli.guilib.schevent import *

import six
#from wx.lib.pubsub import pub

class SchSashWindow(wx.Window):

    def __init__(
        self,
        parent,
        address_or_parser,
        parameters,
        pos=(0, 0),
        size=(0, 0),
        name='sash_panel',
        ):
        self.handleInfo = {}
        self.address_or_parser = address_or_parser
        #if self.address_or_parser.__class__.__name__ != 'ShtmlParser':
        #    print "SchSashWindow:", self.address_or_parser
        #else:
        #    print "SchSashWindow:", self.address_or_parser.address
        self.parameters = parameters
        self.WidgetCells = None
        self.default_button = None
        self.ParentTab = None

        self.ctrl_dict_old = {}
        self.ctrl_dict = {}
        self.href_pos = None
        self.href_list_back = []
        self.href_list_forward = []
        self.href_status = 0
        self.events_active = []
        self.last_size = None
        self._active = True

        wx.Window.__init__(
            self,
            parent,
            -1,
            pos,
            size,
            style= wx.WANTS_CHARS,
            name=name,
            )
        self.Init = False
        self.signals = {}
        self.statusText = ''
        self.exists = True
        self.vertical_position = None
        mp = self._read_html(address_or_parser, parameters)
        if not mp:
            print('ERROR READ HTML:', address_or_parser, parameters)
        address = mp.address
        header = mp.get_header()
        body = mp.get_body()
        #print('+++++++++++++++++++++++++++++++++++++++++++')
        #print(body[0].getvalue())
        #print('-------------------------------------------')
        footer = mp.get_footer()
        panel = mp.get_panel()
        config = mp.var
        self.title = mp.title
        winids = []
        self.address = address
        self.refr_obj_tab = []
        self.Header = None
        self.Panel = None
        self.Body = None
        self.Footer = None
        self.ActiveWin = None
        if header[0]:
            #topwin = wx.adv.SashLayoutWindow(self, -1, wx.DefaultPosition, (100,
            #        5), wx.SW_3D)
            topwin = wx.adv.SashLayoutWindow(self, -1, wx.DefaultPosition, (100,
                    5), wx.adv.SW_3D, style=wx.WANTS_CHARS)
            topwin.SetOrientation(wx.adv.LAYOUT_HORIZONTAL)
            topwin.SetAlignment(wx.adv.LAYOUT_TOP)
            topwin.SetSashVisible(wx.adv.SASH_BOTTOM, True)
            #self.Header = SchHtmlWindow(topwin, -1, size=(100, 100), style=0)
            self.Header = SchHtmlWindow(topwin, -1, 0)
            self.Header.set_htm_type('header')
            self.Header.TabWindow = self
            self.Header.show_page(header)
            dy = self.Header.calculate_best_size()[1]
            topwin.SetDefaultSize((1000, dy))
            self.topWindow = topwin
            winids.append(topwin.GetId())
        else:
            self.topWindow = None
        vscroll = True
        hscroll = True

        if 'no_vscrollbar' in config:
            vscroll = False
        if 'no_hscrollbar' in config:
            hscroll = False
        if 'vertical_position' in config:
            self.set_vertical_position(config['vertical_position'])

        #    self.Body = SchHtmlWindow(self, -1, style=0)
        #else:
        #    self.Body = SchHtmlWindow(self, -1, style=wx.ALWAYS_SHOW_SB)
        self.Body = SchHtmlWindow(self, -1, 0, hscroll, vscroll)
        self.Body.set_htm_type('body')
        self.Body.TabWindow = self


        attrs = mp.get_body_attrs()
        if 'width' in attrs and 'height' in attrs:
            w = attrs['width']
            h = attrs['height']
            #self.Body.calculate_best_size(int(w))
            self.Body.bestsize = (int(w)*4/3, int(h)*4/3)
        if 'no_background' in config:
            self.Body.no_background = True
        self.Body.show_page(body, parameters)
        self.Body.set_address_parm(address)
        if 'refresh' in mp.var:
            self.Body.refresh_time(int(mp.var['refresh']))
        if footer[0]:
            bottomwin = wx.adv.SashLayoutWindow(self, -1, wx.DefaultPosition,
                    (1000, 5), wx.adv.SW_3D)
            bottomwin.SetOrientation(wx.adv.LAYOUT_HORIZONTAL)
            bottomwin.SetAlignment(wx.adv.LAYOUT_BOTTOM)
            bottomwin.SetSashVisible(wx.adv.SASH_TOP, True)
            self.Footer = SchHtmlWindow(bottomwin, -1, 0)
            self.Footer.set_htm_type('footer')
            self.Footer.TabWindow = self
            self.Footer.show_page(footer)
            bottomwin.SetDefaultSize((1000, self.Footer.calculate_best_size()[1]))
            self.bottomWindow = bottomwin
            winids.append(bottomwin.GetId())
        else:
            self.bottomWindow = None
        if panel[0]:
            leftwin1 = wx.adv.SashLayoutWindow(self, -1, wx.DefaultPosition, (5,
                    100), wx.adv.SW_3D)
            leftwin1.SetOrientation(wx.adv.LAYOUT_VERTICAL)
            leftwin1.SetAlignment(wx.adv.LAYOUT_LEFT)
            leftwin1.SetSashVisible(wx.adv.SASH_RIGHT, True)
            self.Panel = SchHtmlWindow(leftwin1, -1, size=(5, 5), style=0)
            self.Panel.SetHtmType('panel')
            self.Panel.TabWindow = self
            self.Panel.show_page(panel)
            xy = self.Panel.calculate_best_size()
            leftwin1.SetDefaultSize(xy)
            self.leftWindow1 = leftwin1
            winids.append(leftwin1.GetId())
        else:
            self.leftWindow1 = None
        if winids:
            self.Bind(wx.adv.EVT_SASH_DRAGGED_RANGE, self.on_sash_drag,
                      id=min(winids), id2=max(winids))
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Controls = []
        self.LastControlWithFocus = None
        self.disable_setfocus = 0
        self.Bind(wx.EVT_NAVIGATION_KEY, self.on_navigate)
        self.Bind(schevent.EVT_REFRPARM, self.on_refr_parm)
        #LayoutAlgorithm().LayoutWindow(self, self.Body)
        #self.Body.draw_background()
        self.Body.Bind(wx.EVT_CHILD_FOCUS, self.on_child_focus)

        self.Bind(wx.EVT_SET_FOCUS, self.on_set_focus)

#        pub.subscribe(self.listener1, 'rootTopic')
#        tab = []
#        pub.sendMessage('rootTopic', arg1=123, arg2=tab)
#        print("TAB:", tab)

#    def listener1(self, arg1, arg2=None):
#        print('Function listener1 received:')
#        print('  arg1 =', arg1)
#        print('  arg2 =', arg2)
#        arg2.append(100)


    def init_binds(self):
        test_bind = True
        for pos in self.events_active:
            if pos[1] == ID_WEB_BACK:
                test_bind = False
                break

        #if test_bind:
        #    self.bind_to_active(self.on_back, ID_WEB_BACK)
        #    self.bind_to_active(self.on_check_can_go_back, ID_WEB_BACK, wx.EVT_UPDATE_UI)
        #    self.bind_to_active(self.on_forward, ID_WEB_FORWARD)
        #    self.bind_to_active(self.on_check_can_go_forward, ID_WEB_FORWARD, wx.EVT_UPDATE_UI)

    def bind_to_active(self, fun, id, e=None):
        self.events_active.append((fun, id, e))

    def reg_href(self, href, attr):
        if self.href_status in (0,2):
            for pos in self.href_list_back:
                if pos==self.href_pos:
                    del pos
            self.href_list_back.append(self.href_pos)
        if self.href_status == 0:
            self.href_list_forward = []
        self.href_pos = (href, attr)

    def on_check_can_go_back(self, event):
        test = len(self.href_list_back) > 0
        event.Enable(test)

    def on_check_can_go_forward(self, event):
        test = len(self.href_list_forward) > 0
        event.Enable(test)

    def on_back(self, event):
        self.back()

    def back(self):
        if len(self.href_list_back  )>0:
            self.href_list_forward.append(self.href_pos)
            href, attr = self.href_list_back[-1]
            self.href_status = 1
            if attr:
                self.Body.href_clicked(self.Body, attr)
            else:
                self.Body.href_clicked(self.Body, {'href': href, 'target': '_self'})
            self.href_status = 0
            del self.href_list_back[-1]

    def on_forward(self, event):
        self.forward()

    def forward(self):
        if len(self.href_list_forward)>0:
            href, attr = self.href_list_forward[-1]
            self.href_status = 2
            if attr:
                self.Body.href_clicked(self.Body, attr)
            else:
                self.Body.href_clicked(self.Body, {'href': href, 'target': '_self'})
            self.href_status = 0
            del self.href_list_forward[-1]


    def _read_html(self, address_or_parser, parameters):
        mp, adr = wx.GetApp().read_html(self, address_or_parser, parameters)
        if adr:
            self.href_pos=(adr,None)
        return mp

    def append_ctrl(self, obj):
        self.ctrl_dict[obj.get_unique_name()] = obj

    def restart_ctrl_lp(self):
        self.ctrl_dict_old = self.ctrl_dict
        self.ctrl_dict = {}

    def pop_ctrl(self, name):
        if name in self.ctrl_dict_old:
            ret = self.ctrl_dict_old[name]
            del self.ctrl_dict_old[name]
            return ret
        else:
            return None

    def test_ctrl(self, name):
        if name in self.ctrl_dict:
            return True
        else:
            return False

    def remove_old_ctrls(self):
        for name in self.ctrl_dict_old:
            win = self.ctrl_dict_old[name]
            win.Destroy()
            if name in self.Body.controls:
                del self.Body.controls[name]
        self.ctrl_dict_old = {}

    def bind_default_event(self, ctrl):
        # ctrl.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus) if not ctrl.GetWindowStyleFlag()
        # & wx.TE_PROCESS_ENTER: ctrl.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        pass

    def init_frame(self):
        if self.Header:
            self.Header.init_page()
        if self.Footer:
            self.Footer.init_page()
        if self.Panel:
            self.Panel.init_page()

        self.Body.init_page()

        self.init_binds()

    def get_parent_tab(self):
        return self.ParentTab

    def set_default_button(self, button):
        self.default_button = button

    def on_key_down(self, event):
        if event.KeyCode == wx.WXK_RETURN and self.default_button:
            self.default_button.OnClick(event)
        else:
            event.Skip()

    def on_char_hook(self, event):
        if event.KeyCode == wx.WXK_ESCAPE:
            if hasattr(self.GetParent(), 'cancel'):
                self.GetParent().cancel(True)
            else:
                event.Skip()
        else:
            event.Skip()

    def get_title(self):
        return self.title

    def set_adr_and_param(self, address_or_parser, param):
        self.address_or_parser = address_or_parser
        #if self.address_or_parser.__class__.__name__ != 'ShtmlParser':
        #    print "set_adr_and_param:", self.address_or_parser
        #else:
        #    print "set_adr_and_param:", self.address_or_parser.address
        
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

        #print('+++++++++++++++++++++++++++++++++++++++++++')
        #print(body[0].getvalue())
        #print('-------------------------------------------')

        footer = mp.get_footer()
        panel = mp.get_panel()
        config = mp.var
        self.title = mp.title
        if self.Header:
            if not self.Header.show_page("""<html encoding="utf-8">"""
                     + header + '</html>'):
                return False
        if self.Body:
            if not self.Body.show_page(body, self.parameters):
                return False
        if self.Footer:
            if not self.Footer.show_page("""<html encoding="utf-8">""" + footer
                                         + '</html>'):
                return False
        if self.Panel:
            if not self.Panel.show_page("""<html encoding="utf-8">""" + panel
                                        + '</html>'):
                return False
        if self.Header:
            self.Header.init_page()
        if self.Footer:
            self.Footer.init_page()
        if self.Panel:
            self.Panel.init_page()

        self.Body.Refresh()
        self.Body.init_page()
        return True

    def CanClose(self):
        if self.Header:
            if not self.Header.CanClose():
                return False
        if self.Body:
            if not self.Body.CanClose():
                return False
        if self.Footer:
            if not self.Footer.CanClose():
                return False
        if self.Panel:
            if not self.Panel.CanClose():
                return False

        self.deactivate_page()
        self.events_active = []

        if self.Header: self.Header._on_close()
        if self.Body: self.Body._on_close()
        if self.Footer: self.Footer._on_close()
        if self.Panel: self.Panel._on_close()

        return True

    def on_navigate(self, evt):
        forward = evt.GetDirection()
        test = False
        if len(self.Controls) > 0:
            for i in range(0, len(self.Controls)):
                if self.Controls[i] == self.LastControlWithFocus:
                    test = True
                    if forward:
                        if i < len(self.Controls) - 1:
                            self.Controls[i + 1].SetFocus()
                        else:
                            self.Controls[0].SetFocus()
                    else:
                        if i == 0:
                            self.Controls[-1].SetFocus()
                        else:
                            self.Controls[i - 1].SetFocus()
                    break
        if not test:
            pass

    def on_set_focus(self, evt):
        if self.Body:
            self.Body.SetFocus()

    def on_child_focus(self, evt):
        if not self.disable_setfocus:
            #print(evt, evt.GetId())
            #new_win = self.FindWindowById(evt.GetId())
            new_win = evt.GetWindow()
            parent = new_win.GetParent()
            #print("parent:", type(parent))
            while parent != None:
                if parent.__class__.__name__ == 'HtmlPanel':
                    parent.SelectTab()
                    break
                parent = parent.GetParent()
            while new_win != None:
                if new_win.GetParent()\
                     and new_win.GetParent().GetWindowStyleFlag()\
                     & wx.TAB_TRAVERSAL != 0:
                    break
                new_win = new_win.GetParent()
            if new_win != self.LastControlWithFocus:
                if self.LastControlWithFocus:
                    if hasattr(self.LastControlWithFocus, 'KillFocus'):
                        self.disable_setfocus = True
                        getattr(self.LastControlWithFocus, 'KillFocus')()
                        #new_win.SetFocus()
                        self.disable_setfocus = False
                self.LastControlWithFocus = new_win
            evt.Skip()
        else:
            evt.Skip()

    def set_focus(self):
        if self.LastControlWithFocus:
            self.LastControlWithFocus.SetFocus()
        else:
            super().SetFocus()


    def on_sash_drag(self, event):
        if event.GetDragStatus() == wx.SASH_STATUS_OUT_OF_RANGE:
            return
        eobj = event.GetEventObject()
        if eobj is self.topWindow:
            self.topWindow.SetDefaultSize((1000, event.GetDragRect().height))
        elif eobj is self.leftWindow1:
            self.leftWindow1.SetDefaultSize((event.GetDragRect().width, 1000))
        elif eobj is self.bottomWindow:
            self.bottomWindow.SetDefaultSize((1000, event.GetDragRect().height))
        LayoutAlgorithm().LayoutWindow(self, self.Body)
        self.Body.Refresh()

    def on_size(self, event):
        LayoutAlgorithm().LayoutWindow(self, self.Body)
        self.Body.Refresh()
        if event:
            event.Skip()

    def get_last_control_with_focus(self):
        return self.LastControlWithFocus

    def on_refr_parm(self, event):
        self.send_refr_obj()

    def register_refr_obj(self, obj):
        self.refr_obj_tab.append(obj)

    def send_refr_obj(self):
        for obj in self.refr_obj_tab:
            obj.refr_obj()

    def has_parm(self, parm):
        if self.Header != None and self.Header.item_exist(parm):
            return True
        if self.Panel != None and self.Panel.item_exist(parm):
            return True
        if self.Body != None and self.Body.item_exist(parm):
            return True
        if self.Footer != None and self.Footer.item_exist(parm):
            return True
        return False

    def get_parm(self, parm):
        if self.Header != None and self.Header.item_exist(parm):
            return self.Header.get_item(parm).GetValue()
        if self.Panel != None and self.Panel.item_exist(parm):
            return self.Panel.get_item(parm).GetValue()
        if self.Body != None and self.Body.item_exist(parm):
            return self.Body.get_item(parm).GetValue()
        if self.Footer != None and self.Footer.item_exist(parm):
            return self.Footer.get_item(parm).GetValue()
        return None

    def register_signal(self, obj, signal):
        if signal not in self.signals:
            self.signals[signal] = []
        if not obj in self.signals[signal]:
            self.signals[signal].append(obj)

    def unregister_signal(self, obj, signal):
        if obj in self.signals[signal]:
            id = self.signals[signal].index(obj)
            del self.signals[signal][id]

    def signal(self, signal):
        if signal in self.signals:
            for obj in self.signals[signal]:
                getattr(obj, signal)()

    def refresh_html(self, method=0):
        return self._refresh_html(method)

    def _refresh_html(self, method=0):
        ret = self._refresh()
        self.Body.wxdc = None
        self.Body.update_controls = True
        self.Body.Refresh()
        if not ret:
            return False
        return True

    def _show_cell_container(self, cells):
        child = cells.GetFirstChild()
        last = None
        while child != None:
            if child.__class__.__name__ == 'HtmlContainerCell':
                self._show_cell_container(child)
            else:
                if child.__class__.__name__ in ('HtmlWidgetCell',
                        'SchHtmlWidgetCell'):
                    next = child.GetNext()
                    if last:
                        last.SetNext(child.GetNext())
                    child.SetNext(None)
                    self.WidgetCells.append(child)
                    child = next
                    continue
            last = child
            child = child.GetNext()

    def get_item(self, key):
        if self.Header and self.Header.item_exist(key):
            return self.Header.get_item(key)
        if self.Body and self.Body.item_exist(key):
            return self.Body.get_item(key)
        if self.Footer and self.Footer.item_exist(key):
            return self.Footer.get_item(key)
        if self.Panel and self.Panel.item_exist(key):
            return self.Panel.get_item(key)
        return None

    def item_exist(self, key):
        if self.Header and self.Header.item_exist(key) or self.Body\
             and self.Body.item_exist(key) or self.Footer\
             and self.Footer.item_exist(key) or self.Panel\
             and self.Panel.item_exist(key):
            return True
        else:
            return False

    def __getitem__(self, key):
        ret = self.get_item(key)
        return ret

    def set_status_text(self, value):
        self.statusText = value
        if wx.GetApp().GetTopWindow().active_page == self:
            statusbar = wx.GetApp().GetTopWindow().GetStatusBar()
            if statusbar:
                statusbar.SetStatusText(self.statusText)

    def set_status_text2(self, value):
        statusbar = wx.GetApp().GetTopWindow().GetStatusBar()
        if statusbar:
            statusbar.SetStatusText(value, 1)

    def show_info(self):
        wx.GetApp().GetTopWindow().active_page = self
#        web = None
#        if 'browser' in self.handleInfo:
#            web = self.handleInfo['browser']
#            if web and web.href:
#                wx.GetApp().GetTopWindow().toolbar_interface.get_toolbars()['browser'
#                        ]['address'].SetValue(web.href)
        self.set_status_text(self.statusText)

    def del_info(self):
        self.set_status_text('')
        wx.GetApp().GetTopWindow().active_page = None
#        self.handleInfo['browser'] = None

    def refr_info(self, key):
        pass
#        if key == 'browser':
#            web = None
#            if 'browser' in self.handleInfo:
#                web = self.handleInfo['browser']
#            if wx.GetApp().GetTopWindow().active_page == self:
#                if web:
#                    wx.GetApp().GetTopWindow().toolbar_interface.get_toolbars()['browser'
#                            ]['address'].SetValue(web.href)
#                else:
#                    wx.GetApp().GetTopWindow().toolbar_interface.get_toolbars()['browser'
#                            ]['address'].SetValue('')
#                wx.GetApp().GetTopWindow().toolbar_interface.get_toolbars()['browser'
#                        ]['bar'].Refr(web)

    def set_handle_info(self, key, value):
        self.handleInfo[key] = value

    def calculate_best_size(self):
        if self.last_size:
            dx = self.last_size.GetWidth()
            dy = self.last_size.GetHeight()
            self.last_size = None
            return (dx,dy)
        dx = 0
        dy = 0
        if self.Header:
            (x, y) = self.Header.calculate_best_size()
            dy = dy + y
        if self.Body:
            (x, y) = self.Body.calculate_best_size()
            dx = dx + x
            dy = dy + y
        if self.Footer:
            (x, y) = self.Footer.calculate_best_size()
            dy = dy + y
        if self.Panel:
            (x, y) = self.Panel.calculate_best_size()
            dx = dx + x
            if y > dy:
                dy = y
        return (dx, dy)

    def enable_panels(self, enable):
        if enable==False:
            self.last_size = self.GetSize()
        if self.Header:
            self.Header.Enable(enable)
        if self.Body:
            self.Body.Enable(enable)
        if self.Footer:
            self.Footer.Enable(enable)
        if self.Panel:
            self.Panel.Enable(enable)

    def change_notebook_page_title(self, new_title):
        p = self.GetParent()
        tab = p.GetParent()
        sel = tab.GetPageIndex(p)
        tab.SetPageText(sel, new_title)

    def set_new_href(self, href):
        self.address_or_parser = href        
        #if self.address_or_parser.__class__.__name__ != 'ShtmlParser':
        #    print "set_new_href:", self.address_or_parser
        #else:
        #    print "set_new_href:", self.address_or_parser.address


    def activate_page(self):
        self._active = True
        for pos in self.events_active:
            if pos[2]:
                wx.GetApp().GetTopWindow().toolbar_interface.bind(pos[0], pos[1], pos[2])
            else:
                wx.GetApp().GetTopWindow().toolbar_interface.bind(pos[0], pos[1])
        #self.show_info()
        self.Body.SetFocus()

    def deactivate_page(self):
        self._active = False
        for pos in self.events_active:
            if pos[2]:
                wx.GetApp().GetTopWindow().toolbar_interface.un_bind(pos[1], pos[2])
            else:
                wx.GetApp().GetTopWindow().toolbar_interface.un_bind(pos[1])
        self.del_info()

    def is_active(self):
        return self._active

    def set_page(self, page_source):
        self.Body.set_page(page_source)


    def set_vertical_position(self, position):
        """
        position:
            "top"
            "bottom"
            None or "default" (defautl)
        """
        self.vertical_position = position
