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

import gc
try:
    from wx.adv import SashLayoutWindow
except:
    from wx import SashLayoutWindow

#from schcli.guilib.schevent import EVT_USER_FIRST
from schlib.schtools import createparm
import sys
#from urlparse import urlparse
from schlib.schhttptools.schhtml_parser import ShtmlParser
import types
from schlib.schindent.indent_tools import norm_html
from schlib.schhttptools import schhtml_parser
#from tempfile import NamedTemporaryFile
from schlib.schtools.schpath import norm_path, clean_href
from schlib.schtools.encode import encode_utf
import math
from wx.lib.scrolledpanel import ScrolledPanel
from schlib.schhtml.wxdc import DcDc
from schlib.schhtml.htmlviewer import HtmlViewerParser
from schlib.schtools.data import is_null
from schcli.guilib.schevent import *

import wx.lib.agw.ribbon as RB


import six

# from guilib.schevent import * typeEVT_SHOW1 = wx.NewEventType() EVT_SHOW1 =
# wx.PyEventBinder(typeEVT_SHOW1, 1)

_pre_process_lib = []


def install_pre_process_lib(fun):
    global _pre_process_lib
    _pre_process_lib.append(fun)


init_css_str = None
lp = 0


def _get_css():
    global init_css_str
    if init_css_str == None:
        f = open(wx.GetApp().scr_path + '/schappdata/icss/form.icss', 'r')
        init_css_str = f.read()
        f.close()
    return init_css_str


class SchHtmlWindow(ScrolledPanel):
    """Html window"""

    @property
    def bestsize(self):
        return self._bestsize

    @bestsize.setter
    def bestsize(self, x):
        self._bestsize = x

    def __init__(self,  parent, id, style, hscroll=False,  vscroll=False):
        self._bestsize = None
        self.no_vscrollbar = not vscroll
        self.no_hscrollbar = not hscroll
        #if 'style' in kwds:
        #    if not kwds['style'] & wx.ALWAYS_SHOW_SB:
        #        self.no_vscrollbar = True
        #    kwds['style    '] = wx.TAB_TRAVERSAL | wx.WANTS_CHARS \
        #                    | wx.NO_FULL_REPAINT_ON_RESIZE
        #kwds['style'] = wx.VSCROLL
        #self.no_vscrollbar = True

        #style |= wx.TAB_TRAVERSAL

        ScrolledPanel.__init__(self, parent, id, style=wx.WANTS_CHARS)
        try:
            self.SetBackgroundStyle(wx.BG_STYLE_ERASE)
        except:
            self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)

        self.address = None
        self.EffectiveUrl = ""
        self.ActiveCtrl = None
        self.BaseUrl = None
        self.no_background = False
        self.script = None
        self.clientObj = None
        self.controls = {}
        self.Parametry = None
        self.page_source = '<html></html>'
        self.script = None
        self.bestsize = None
        self.hover_obj = None
        self.cursor_type = 0
        self._scroll_xy = (0, 0)
        self._act_scroll_xy = (0, 0)
        self._enabled_controls = False
        self.wxdc = None
        self.after_init = False
        self.update_controls = False
        self._last_size = (-1, -1)
        self._best_virtual_size = None
        self.obj_action_dict = {}
        self.obj_id_dict = {}
        self._block = False
        self._dc_buf = None
        self._dc_buf_x = 0
        self._dc_buf_y = 0
        self.LastControlWithFocus = None
        self.TabWindow = None
        self.html_type = 'body'
        self.init_css_str = None
        self.evt_ind = -1
        self.closing = False
        self.acc_tabs = {}
        self.acc_tab = None
        self.last_clicked = None

        self.SetupScrolling(hscroll, vscroll, rate_y=1)
        self.register_signal(self, 'Refr')

        self.SetAcceleratorTable(wx.AcceleratorTable(wx.GetApp().GetTopWindow().aTable))

        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)
        self.Bind(wx.EVT_LEFT_UP, self.on_left_up)
        self.Bind(wx.EVT_RIGHT_UP, self.on_right_up)
        self.Bind(wx.EVT_MOTION, self.on_motion)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.on_erase_background)
        self.Bind(wx.EVT_SET_FOCUS, self.on_focus)

        #self.Bind(wx.EVT_MENU, self.on_back, id=ID_WEB_BACK)
        #self.Bind(wx.EVT_UPDATE_UI, self.on_check_can_go_back)
        #self.GetApp().GetTopWindow().toolbar_interface.bind()

        #self.t0 = wx.Timer(self)
        #self.t0.Start(1000)
        self.t1 = None
        self.EnableScrolling(False, False)
        #wx.GetApp().GetTopWindow().toolbar_interface.bind(self.on_back, ID_WEB_BACK)
        #wx.GetApp().GetTopWindow().toolbar_interface.bind(self.on_check_can_go_back, ID_WEB_BACK, wx.EVT_UPDATE_UI)
        #wx.GetApp().GetTopWindow().toolbar_interface.bind(self.on_check_can_go_back, -1, wx.EVT_UPDATE_UI)

        #self.bind_to_active(self.on_back, ID_WEB_BACK)
        #self.bind_to_active(self.on_check_can_go_back, ID_WEB_BACK, wx.EVT_UPDATE_UI)
        #self.bind_to_active(self.on_forward, ID_WEB_FORWARD)
        #self.bind_to_active(self.on_check_can_go_forward, ID_WEB_FORWARD, wx.EVT_UPDATE_UI)
        self.GetParent().register_signal(self, "refresh_controls")
        self.GetParent().register_signal(self, "child_canceled")


    def refresh_controls(self):
        if hasattr(self, "refresh_after_ok"):
            self.refresh_after_ok()

    def child_canceled(self):
        #self.GetParent().disable_setfocus = False
        #if hasattr(self.GetParent(), 'LastControlWithFocus'):
        #    self.GetParent().LastControlWithFocus.SetFocus()
        #    print("FOCUS:", self.GetParent().LastControlWithFocus)
        if hasattr(self, "child_closed"):
            self.child_closed()

    def ret_ok(self, id, title):
        #self.GetParent().disable_setfocus = False
        #print("ret_ok:", id, title)
        #parent_panel = self.get_parent_panel()
        if parent_panel and parent_panel.last_clicked and hasattr(parent_panel.last_clicked,"ret_ok"):
            parent_panel.last_clicked.ret_ok(id, title)
        self.any_parent_command('on_ok', None)

    def navigate(self, ctrl, back = False):
        next = False
        children = [ child for child in self.GetChildren() if child.AcceptsFocus() ]
        if back:
            widgets = reversed(children)
        else:
            widgets = children
        for w in widgets:
            if next or not ctrl:
                w.SetFocus()
                self.LastControlWithFocus = w
                return
            if w==ctrl:
                next = True
        if children and len(children)>0:
            if back:
                children[-1].SetFocus()
                self.LastControlWithFocus = children[-1]
            else:
                children[0].SetFocus()
                self.LastControlWithFocus = children[0]

    def on_focus(self, event):
        print("on_focus?????", self.LastControlWithFocus)
        if self.LastControlWithFocus:
            self.LastControlWithFocus.SetFocus()
        else:
            self.navigate(None)

    #def SetFocus(self):
    #    self.on_focus(None)


    def bind_to_ctrl(self, ctrl, id, fun, fun2=None):
        if fun2:
            ctrl.Bind(wx.EVT_UPDATE_UI, fun2, id=id)
        ctrl.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, fun, id=id)
        ctrl.Bind(RB.EVT_RIBBONTOOLBAR_CLICKED, fun, id=id)
        ctrl.Bind(wx.EVT_MENU, fun, id=id)

    def bind_to_active(self, fun, id, e=None):
        self.get_parent().bind_to_active(fun, id, e)

#    def on_check_can_go_back(self, event):
#        if not self.closing:
#            test = len(self.get_parent().href_list) > 1
#            event.Enable(test)
#        else:
#            event.Skip()

#    def on_check_can_go_back(self, event):
#        if not self.closing:
#            test = len(self.get_parent().href_list_forward) > 1
#            event.Enable(test)
#        else:
#            event.Skip()

    def print(self, *argi, **argv):
        if '/edit/' in self.EffectiveUrl:
            return print(*argi, **argv)

    def signal_from_child(self, child, signal):
        pass

    def scroll_child_into_view(self, child):
        if child.GetParent() == self:
            (sppu_x, sppu_y) = self.GetScrollPixelsPerUnit()
            (vs_x, vs_y) = self.GetViewStart()
            cr = child.GetRect()
            clntsz = self.GetClientSize()
            (new_vs_x, new_vs_y) = (-1, -1)
            if cr.y < 0 and sppu_y > 0:
                new_vs_y = vs_y + cr.y / sppu_y
            if cr.bottom > clntsz.height and sppu_y > 0:
                diff = math.ceil((1.0 * (cr.bottom - clntsz.height + 1))
                                 / sppu_y)
                if cr.y - diff * sppu_y > 0:
                    new_vs_y = vs_y + diff
                else:
                    new_vs_y = vs_y + cr.y / sppu_y
            if new_vs_y != -1:
                self.Scroll(-1, new_vs_y)

    def get_parent(self):
        win = ScrolledPanel.GetParent(self)
        if win.__class__ == SashLayoutWindow:
            return win.GetParent()
        else:
            return win

    def set_css(self, css_str):
        self.init_css_str = css_str

    def get_css(self):
        if self.init_css_str:
            return self.init_css_str
        else:
            return _get_css()

    def GetBestVirtualSize(self):
        if self._best_virtual_size:
            return self._best_virtual_size
        else:
            try:
                (dx, dy) = self.GetSize()
            except:
                return (0,0)
            #dx -= wx.SystemSettings.GetMetric(wx.SYS_VSCROLL_X) + 1
            #dy -= wx.SystemSettings.GetMetric(wx.SYS_HSCROLL_Y) + 1
            return (dx, dy)

    def _calculate_size(self, width):

        psize = self.GetParent().GetParent().GetSize()
        dc = wx.ClientDC(self)
        wxdc = DcDc(dc, calc_only=True, width=width, height=-1)
        self.get_parent().restart_ctrl_lp()
        p = HtmlViewerParser(dc=wxdc, calc_only=True,
                             init_css_str=self.get_css(), css_type=1)
        p.set_http_object(wx.GetApp().HTTP)
        p.set_parent_window(self)
        p.feed(self.page_source)
        (dx, dy) = p.get_max_sizes()
        p.close()
        self.remove_old_ctrls()
        return (dx, dy)

    def remove_old_ctrls(self):
        self.get_parent().remove_old_ctrls()
        #self.controls = {}

    def calculate_best_size(self):
        if '/edit/' in self.EffectiveUrl:
            pass
        #if not self.bestsize:
        if True:
            psize = self.GetParent().GetParent().GetClientSize()
            if self.bestsize:
                (dx, dy) = self._calculate_size(self.bestsize[0])
            else:
                (dx, dy) = self._calculate_size((psize[0] * 3) / 4)
            #print "calculate_best_size2: ", dx, dy+8
            self.bestsize = (dx, dy + 8)
            #self.bestsize = (dx, dy)
            return self.bestsize
        #else:
        #    self.print("calculate_best:", self.bestsize)
        #    return self.bestsize

    def html_updatet(self, dc, size):
        w = size.GetWidth()
        h = size.GetHeight()
        if w == 20 and h == 20:
            print("20x20")
            return
        if not self.wxdc:
            if self.no_vscrollbar:
                self.wxdc = DcDc(dc, calc_only=False, width=w - 1, height=-1)
            else:
                self.wxdc = DcDc(dc, calc_only=False, width=w - 1 - wx.SystemSettings.GetMetric(wx.SYS_HSCROLL_Y),
                                 height=-1)
            self.get_parent().restart_ctrl_lp()
            p = HtmlViewerParser(dc=self.wxdc, calc_only=False,
                                 init_css_str=self.get_css(), css_type=1)
            p.set_http_object(wx.GetApp().HTTP)
            p.set_parent_window(self)
            p.feed(self.page_source)
            self.remove_old_ctrls()
            self.obj_action_dict = p.obj_action_dict
            self.obj_id_dict = p.obj_id_dict
            if not self.no_vscrollbar:
                (w2, h2) = p.get_max_sizes()
                #h2+=8
                #h2-=wx.SystemSettings.GetMetric(wx.SYS_VSCROLL_X)
                hscroll = True if w2 > w + 3 else False
                vscroll = True if h2 > h + 3 else False
                if self.no_hscrollbar:
                    hscroll = False
                if ( vscroll or hscroll ) and w > 0 and h > 0 and w2 > 0 and h2 > 0:
                    if vscroll:
                        w2 = w2 + wx.SystemSettings.GetMetric(wx.SYS_VSCROLL_X)
                    if hscroll:
                        h2 = h2 + wx.SystemSettings.GetMetric(wx.SYS_HSCROLL_Y)
                    self._best_virtual_size = (w2, h2)
                    self.EnableScrolling(hscroll, vscroll)
                self.SetVirtualSize((w2, h2))
            else:
                self.EnableScrolling(False, False)
                self.SetVirtualSize((w, h))
            p.close()
            self.update_controls = False


    def on_erase_background(self, event):
        #rect = self.GetRect()
        #if not rect[2]==1 and not rect[3]==1:
        #   print(rect)
        self.draw_background()
        #event.Skip()


    def draw_background(self, refresh_all=False, size=None):
        if self._block:
            return
        self._block = True
        if not self.wxdc:
            self.Scroll(0, 0)
        (xv, yv) = self.GetViewStart()
        (dx, dy) = self.GetScrollPixelsPerUnit()
        (x, y) = (xv * dx, yv * dy)
        self._act_scroll_xy = (x, y)
        dc = wx.ClientDC(self)
        if self.wxdc and self._dc_buf and self._dc_buf_x == x and self._dc_buf_y \
                == y:
            dc.SetDeviceOrigin(-1 * x, -1 * y)
            rect = self.GetRect()
            dc.Blit(
                x,
                y,
                rect.GetWidth(),
                rect.GetHeight(),
                self._dc_buf,
                x,
                y,
            )
        else:
            rect = self.GetRect()
            if rect.GetWidth() < 1 or rect.GetHeight() < 1:
                rect = wx.Rect(0, 0, 1, 1) #width=1, height=1)
            dc.SetDeviceOrigin(-1 * x, -1 * y)
            bitmap = wx.Bitmap(rect.GetWidth(), rect.GetHeight())
            dc2 = wx.MemoryDC(bitmap)
            dc2.SetBackground(wx.Brush(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DFACE)))
            dc2.Clear()
            dc2.SetDeviceOrigin(-1 * x, -1 * y)
            if not self.wxdc:
                if size:
                    self.html_updatet(dc2, size)
                else:
                    self.html_updatet(dc2, rect)
            else:
                self.wxdc.dc = dc2
                self.wxdc.play()


            dc.Blit(
                x,
                y,
                rect.GetWidth(),
                rect.GetHeight(),
                dc2,
                x,
                y,
            )
            self._dc_buf = dc2
            self._dc_buf_x = x
            self._dc_buf_y = y
        self._block = False

    def append_ctrl(self, ctrl):
        name = ctrl.GetName()
        while name in self.controls:
            name += '$'
        self.controls[name] = ctrl
        if not '$' in name:
            try:
                setattr(self, name, ctrl)
            except:
                pass
        self.GetParent().append_ctrl(ctrl)

    def enable_ctrls(self, ctrls):
        self._enabled_controls = ctrls

    def is_ctrl_block(self, ctrl):
        if self._enabled_controls:
            if ctrl in self._enabled_controls:
                return False
            else:
                return True
        else:
            return True

    def restore_scroll_pos(self):
        wx.ScrolledWindow.Scroll(self, self._scroll_xy[0], self._scroll_xy[1])

    def enable(self, enable=True):
        ret = super(SchHtmlWindow, self).Enable(enable)
        if enable:
            wx.CallAfter(self.restore_scroll_pos)
        return ret

    def set_best_size(self, bestsize):
        self.bestsize = bestsize
        if '/edit/' in self.EffectiveUrl:
            pass


        #print "set_best_size:", self.bestsize

    def on_opening_url(self, type, url):
        if hasattr(self, 'filter_url'):
            f = self.filter_url(type, url)
            if f != None:
                return f
        if url.startswith('/'):
            url2 = url
            base = wx.GetApp().base_address
            if base.startswith('http://127.0.0.2'):
                if url.startswith('/app_media'):
                    if ':' in wx.GetApp().root_path:
                        url2 = wx.GetApp().root_path + '/app_pack' \
                               + url.replace('/app_media', '')
                        url2 = norm_path(url2)
                    else:
                        url2 = 'file://' + wx.GetApp().root_path + '/app_pack' \
                               + url.replace('/app_media', '')
                        url2 = norm_path(url2)
            else:
                url2 = base + url
            return url2
        return True

    def on_left_down(self, evt):
        parent = self.GetParent()
        while parent != None:
            if parent.__class__.__name__ == 'HtmlPanel':
                parent.SelectTab()
                break
            parent = parent.GetParent()
        evt.Skip()

    def on_link_clicked(self, evt):
        href = evt.GetHref()
        target = evt.GetTarget()
        if target == '':
            target = '_blank'
        if not (href.startswith('http://') or href.startswith('/')):
            href = self.address.split('?')[0] + href
        wx.CallAfter(self.href_clicked, self, {'href': href, 'target': target})
        return

    def refresh_time(self, time):
        self.t1 = wx.Timer(self)
        self.t1.Start(time * 1000)
        self.Bind(wx.EVT_TIMER, self.on_timer, self.t1)

    #def on_can_back(self, event):
    #    print("on_can_back")
    #    event.Enable(False)

    #def on_back(self, event):
    #    self.back()

    #def back(self):
    #    href_list = self.get_parent().href_list
    #    if len(href_list)>1:
    #        del href_list[-1]
    #        href, attr = href_list[-1]
    #        if attr:
    #            self.href_clicked(self, attr)
    #        else:
    #            self.href_clicked(self, {'href': href, 'target': '_self'})
    #        del href_list[-1]



    def close_with_delay(self):
        self.cancel(True)

    #def on_timer0(self, event):
    #    pos0 = wx.GetMousePosition()
    #    pos1 = self.GetScreenPosition()
    #    x = pos0.x - pos1.x
    #    y = pos0.y - pos1.y
    #    self.redraw_html_elems((x, y))

    def on_timer(self, event):
        if self.TabWindow:
            if not self.TabWindow.exists:
                self.t1.Stop()
                return
        self.GetParent().refresh_html()

    def cancel(self, cancel):
        if self.TabWindow:
            self.TabWindow.exists = False
        if self.t1:
            self.t1.Stop()
        if self.TabWindow:
            self.TabWindow.GetParent().cancel(True)

    def set_htm_type(self, html_type):
        self.html_type = html_type

    def get_parent_panel(self):
        if self.get_tab():
            parent_tab = self.get_tab().get_parent_tab()
            if parent_tab:
                return parent_tab.ActiveWin
        return None

    def get_tab(self):
        return self.TabWindow

    def on_right_up(self, evt):
        okno = self.new_main_page('^standard/editor/editor.html',
                                  self.get_tab().title + ' - page source', None)
        #okno.Body['EDITOR'].SetValue(norm_html(self.page_source))
        def init_ctrl():
            okno.Body['EDITOR'].SetValue(self.page_source.tostream().getvalue())
            okno.Body['EDITOR'].GotoPos(0)
        wx.CallAfter(init_ctrl)

    def _get_obj_for_redraw(self, pos, type=0):
        if 'href' in self.obj_action_dict:
            for obj in self.obj_action_dict['href']:
                if type == 1 or obj.can_hover():
                    for r in obj.rendered_rects:
                        rect = wx.Rect(r[0], r[1], r[2], r[3])
                        if rect.Contains(pos):
                            return obj
        if type == 1:
            return None
        if 'class' in self.obj_action_dict:
            for obj in self.obj_action_dict['class']:
                if obj.can_hover():
                    for r in obj.rendered_rects:
                        rect = wx.Rect(r[0], r[1], r[2], r[3])
                        if rect.Contains(pos):
                            return obj
        for id in self.obj_id_dict:
            obj = self.obj_id_dict[id]
            for r in obj.rendered_rects:
                if obj.can_hover():
                    rect = wx.Rect(r[0], r[1], r[2], r[3])
                    if rect.Contains(pos):
                        return obj
        return None

    def on_motion(self, evt):
        pos = evt.GetPosition()
        pos2 = (pos[0]+self._act_scroll_xy[0], pos[1]+self._act_scroll_xy[1])
        self.redraw_html_elems(pos2)
        evt.Skip()

    def redraw_html_elems(self, pos):
        obj = self._get_obj_for_redraw(pos)
        if obj or self.hover_obj:
            dc = wx.ClientDC(self)
            self.wxdc.dc = dc
            if self.hover_obj:
                if obj != self.hover_obj:
                    self.hover_obj.gparent.set_hover(False)
                    self.hover_obj.gparent.refresh()
            if obj:
                if obj != self.hover_obj and obj.can_hover():
                    print("redraw")
                    obj.gparent.set_hover(True)
                    obj.gparent.refresh()
        self.hover_obj = obj
        if self._get_obj_for_redraw(pos, type=1):
            cursor_type = 1
        else:
            cursor_type = 0
        if cursor_type != self.cursor_type:
            if cursor_type == 0:
                self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))
            elif cursor_type == 1:
                self.SetCursor(wx.Cursor(wx.CURSOR_HAND))
            else:
                self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))
            self.cursor_type = cursor_type

    def on_left_up(self, evt):
        pos = evt.GetPosition()
        pos2 = (pos[0]+self._act_scroll_xy[0], pos[1]+self._act_scroll_xy[1])
        if 'href' in self.obj_action_dict:
            for obj in self.obj_action_dict['href']:
                #print("href:", obj, obj.rendered_rects)
                for r in obj.rendered_rects:
                    rect = wx.Rect(r[0], r[1], r[2], r[3])
                    if rect.Contains(pos2):
                        self.href_clicked(self, obj.attrs)
                        evt.Skip()
                        return
        evt.Skip()

    def register_signal(self, obj, signal):
        if hasattr(self.GetParent(), 'register_signal'):
            self.GetParent().register_signal(obj, signal)

    def CanClose(self):
        ret = True
        if hasattr(self, 'can_close'):
            ret = self.can_close()
        else:
            widgets = list(self.get_widgets().values())
            for w in widgets:
                if hasattr(w, 'CanClose'):
                    if not w.CanClose():
                        ret = False
        return ret

    def _on_close(self):
        self.closing=True
        if hasattr(self, 'on_close'):
            self.on_close()
        self.GetParent().unregister_signal(self, "refresh_controls")
        self.GetParent().unregister_signal(self, "child_canceled")
        gc.collect()

    def any_parent_command(
            self,
            command,
            *args,
            **kwds
    ):
        parent = self.GetParent()
        while parent != None:
            if hasattr(parent, command):
                return getattr(parent, command)(*args, **kwds)
            parent = parent.GetParent()
        print("METHOD NOT FOUND!: ", command)
        return None

    def set_address_parm(self, address):
        """page address for refr_obj in format http://adres?zmienna1|zmienna2,zmienna"""

        if address:
            elementy = address.split('|')
            if elementy[0][-1] == '/':
                address2 = address
            else:
                address2 = elementy[0] + '/'
                if len(elementy) > 1:
                    address2 = address2 + '|' + elementy[1]
            self.address = address2
            self.EffectiveUrl = address2

    def get_parm_obj(self):
        """Get parent object width method get_par"""

        parent = self
        while parent != None:
            if hasattr(parent, 'get_parm'):
                return parent
            parent = parent.GetParent()
        return None

    def refr(self):
        self.refr_obj(refr_always=True)

    def refr_obj(self, refr_always=False):
        """Refresh html contentod - related to set_address_par"""

        if refr_always or self.GetParent().IsShown():
            if self.address:
                parm = createparm.create_parm(self.address, self.get_parm_obj())
                http = wx.GetApp().get_http(self)
                if parm:
                    (err, url) = http.get(self, str(parm[0] + parm[1]
                                                    + parm[2]))
                else:
                    (err, url) = http.get(self, self.address)
                if err == 404:
                    return

                mp = ShtmlParser()
                mp.process(http.str(), 'local')
                http.clear_ptr()
                if self.html_type == 'panel':
                    strona = mp.get_panel()
                elif self.html_type == 'header':
                    strona = mp.get_header()
                elif self.html_type == 'footer':
                    strona = mp.get_footer()
                else:
                    strona = mp.get_body()
                if self.show_page(strona, self.Parametry):
                    self.init_page()


    def on_size(self, event):
        if event.GetSize() == (0, 0) or event.GetSize() == (20, 20):
            self._last_size = event.GetSize()
            event.Skip()
            return
        if self._last_size != event.GetSize():
            self._last_size = event.GetSize()
            self.wxdc = None
            self.draw_background(True, event.GetSize())
            event.Skip()

    def set_page(self, page_source):
        self.page_source = page_source
        self.wxdc = None
        self.draw_background()

    def __getitem__(self, key):
        if key in self.controls:
            return self.controls[key]
        try:
            ret = super(SchHtmlWindow, self).__getitem__(self, key)
            return ret
        except:
            print("key error:", key)
            return None

            #return ScrolledPanel.__getitem__(self, key)

    def get_item(self, key):
        if key.startswith('PARENT_'):
            parentpanel = self.get_parent_panel()
            if parentpanel:
                return getattr(parentpanel, key[7:])
            else:
                return None
        else:
            return self.get_widgets()[key]

    def item_exist(self, key):
        if key in self.get_widgets() or key.startswith('PARENT_'):
            return True
        else:
            return False

    def get_widgets(self):
        return self.controls

    def pre_process_page(self, page):
        global _pre_process_lib
        page2 = page
        for fun in _pre_process_lib:
            page2 = fun(self, page2)
        return page2

    def exec_code(self, script, parm=None):
        if not parm:
            d = {'wx': wx, 'self': self}
        else:
            d = parm
            d['self'] = self
        try:
            exec (script, d)
        except:
            print('### ERROR IN SCRIPT ###################################')
            print(script)
            print('#######################################################')
            import traceback

            print(sys.exc_info()[0])
            print(traceback.print_exc())
            print('#######################################################')


    def show_page(self, page_and_script, parametry=None):
        if self.TabWindow and self.TabWindow.exists == False:
            return False
        self.page_source = self.pre_process_page(page_and_script[0])
        if self.page_source == '$$$':
            self.t2 = wx.CallLater(10000, self.close_with_delay)
            return False
        self.Parametry = parametry
        if not self.script:
            self.script = str(page_and_script[1])
            if self.script and len(self.script) > 1:
                app = wx.GetApp()
                main_window = app.GetTopWindow()
                desktop = (main_window.desktop, )
                mgr = main_window._mgr
                menu_bar = main_window.get_menu_bar()
                script_tmp = self.script.replace('\r', '').split('\n')
                script = ''
                tab = -1
                for line in script_tmp:
                    if tab == -1:
                        if line.strip() != '':
                            tab = len(line) - len(line.lstrip())
                    if tab >= 0:
                        script = script + line[tab:] + '\n'
                d = {'wx': wx}
                self.exec_code(script, d)
                #try:
                ##    exec (script, d)
                #except:
                #    print('### ERROR IN SCRIPT ###################################')
                #    print(script)
                #    print('#######################################################')
                #    import traceback
                #
                #    print(sys.exc_info()[0])
                #    print(traceback.print_exc())
                #    print('#######################################################')

                for key in d:
                    self.clientObj = d
                    if not key.startswith('__'):
                        if hasattr(d[key], '__call__'):
                            fun = d[key]
                            try:
                                method = types.MethodType(d[key], self, self.__class__)
                            except:
                                method = types.MethodType(d[key], self)
                            if hasattr(self, key):
                                setattr(self, "base_"+key, getattr(self, key))
                            setattr(self, key, method)
                        else:
                            setattr(self, key, d[key])
            else:
                self.clientObj = None

        widgets = self.get_widgets()
        for key in widgets:
            try:
                if key == 'Parent':
                    setattr(self, 'FormParent', widgets[key])
                else:
                    setattr(self, key, widgets[key])
            except:
                print('setattr error:', key, widgets[key].__class__.__name__)
        return True

    def go(self, address):
        return html.HtmlWindow.load_page('http://' + address)

    def init_page(self):
        if not self.after_init:
            if hasattr(self, 'init_form'):
                wx.CallAfter(self.init_form)
                #self.init_form()
            self.after_init = True
        else:
            if hasattr(self, 'reinit'):
                self.reinit()
            elif hasattr(self, 'init_form'):
                self.init_form()
        wx.CallAfter(self._build_acc_tab)


    def new_local_child_page(
            self,
            address,
            title='',
            parametry=None,
    ):
        return self.new_child_page('http://local.net/' + address, title,
                                   parametry)

    def new_plugin_child_page(
            self,
            path,
            address,
            title='',
            parametry=None,
    ):
        p = path.split('/')
        address2 = 'schappdata/schplugins/' + p[-3] + '/' + p[-2] + '/' + address
        return self.new_local_child_page(address2, title, parametry)

    def new_child_page(
            self,
            address_or_parser,
            title='',
            param=None,
    ):
        self._scroll_xy = self.GetViewStart()
        self.get_parm_obj().ActiveWin = self
        self.GetParent().ActiveWin = self
        if hasattr(self.GetParent(), 'LastControlWithFocus'):
            self.LastControlWithFocus = self.GetParent().LastControlWithFocus
        else:
            self.LastControlWithFocus = None
        self.GetParent().disable_setfocus = True
        return self.any_parent_command('new_child_page', address_or_parser, title,
                                       param)

    def new_main_page(
            self,
            address_or_parser,
            title=None,
            param=None,
            panel='desktop',
    ):
        return self.any_parent_command('new_main_page', address_or_parser, title,
                                       param, panel)

    def ok(self):
        pass

    def anuluj(self):
        pass

    #def zapisz(self):
    #    pass

    #def AcceptsFocus(self):
    #    return True

    #def AcceptsFocusFromKeyboard(self):
    #    return self.AcceptsFocus()


    def goto_href(self, href):
        ref = href[1:]
        if ref in self.obj_id_dict:
            obj = self.obj_id_dict[ref]
            rects = obj.rendered_rects
            if len(rects)>0:
                rect = rects[0]
                x=rect[0]
                y=rect[1]
                if self.GetScrollPixelsPerUnit()[0]>0:
                    dx = x/self.GetScrollPixelsPerUnit()[0]
                else:
                    dx = -1
                if self.GetScrollPixelsPerUnit()[1]>0:
                    dy = y/self.GetScrollPixelsPerUnit()[1]
                else:
                    dy = -1
                self.Scroll(dx, dy)

    def href_clicked(
            self,
            ctrl,
            attr_dict,
            upload=False,
            fields=False,
            params=None,
    ):
        self.last_clicked = ctrl

        if 'href' in attr_dict:
            href = attr_dict['href']
            if href and len(href)>0 and href[0]=='#':
                return self.goto_href(href)
            if href:
                href = clean_href(href)
            if 'target' in attr_dict:
                target = attr_dict['target']
            else:
                target = '_blank'
            if 'title' in attr_dict:
                title = attr_dict['title']
            else:
                title = None

            if href and hasattr(self, 'filter_url'):
                f = self.filter_url(target, href)
                if f != None:
                    if isinstance(f, six.string_types):
                    #if f.__class__ in (str, unicode):
                        href = clean_href(f)
                    else:
                        return f

            if href == None:
                if target == '_parent':
                    self.any_parent_command('on_cancel', None)
                    return
                if target == '_refresh':
                    self.any_parent_command('send_refr_obj')
                if target == '_refresh_data':
                    self.any_parent_command('_refresh')
                return
            if href[:7] == 'http://' or href[:7] == 'file://':
                adr = href
            else:
                if href:
                    if href[0] == '.':
                        elm1 = self.get_parm_obj().address.split('?')[0]
                        if not elm1[-1] == '/':
                            id = elm1.rfind('/')
                            if id >= 0:
                                elm1 = elm1[:id + 1]
                            else:
                                elm1 = ''
                        adr = elm1 + href
                    else:
                        adr = href
                else:
                    adr = self.get_parm_obj().address

            if '/pdf/view' in adr:
                wx.GetApp().GetTopWindow().show_pdf(adr)
                return

            if '/odf/view' in adr:
                wx.GetApp().GetTopWindow().show_odf(adr)
                return

            parm = createparm.create_parm(adr, self.get_parm_obj(), no_encode=True)
            if parm:
                adr = parm[0]

            if fields:
                (typ, fields2) = fields.split(':')
                adr = adr + '|' + fields2
            if target == '_refresh_data':
                self.any_parent_command('set_adr_and_param', adr, self.get_parm_obj())
                self.any_parent_command('refresh_html')
                return
            parm = createparm.create_parm(adr, self.get_parm_obj(), no_encode=True)
            post = None
            if parm:
                if typ in ('POST', 'post'):
                    adr = parm[0]
                    post = parm[2]
                else:
                    adr = parm[0] + parm[1] + parm[2]
                    post = None

            http = wx.GetApp().get_http(ctrl)

            if upload:
                (err, adr2) = http.post(self, adr, post, upload=True)
            else:
                if post:
                    (err, adr2) = http.post(self, adr, post)
                else:
                    (err, adr2) = http.get(self, adr)

            if 'text/plain' in http.ret_content_type:
                s = http.str()
                http.clear_ptr()
                if title:
                    edit_name = title
                else:
                    edit_name = href
                okno = self.new_main_page('^standard/editor/editor.html', href,
                                          None)
                okno.Body['EDITOR'].SetValue(s)
                okno.Body['EDITOR'].GotoPos(0)
            else:
                if 'application' in http.ret_content_type:
                    wx.GetApp().GetTopWindow().open_binary_data(http, href)
                    http.clear_ptr()
                    return

                s = http.str()
                http.clear_ptr()
                mp = schhtml_parser.ShtmlParser()
                mp.process(s, encode_utf(adr2))
                if 'target' in mp.var:
                    target = mp.var['target']
                http.clear_ptr()

                if href and hasattr(self, 'filter_http_result'):
                    f = self.filter_http_result(target, href, mp)
                    if f != None:
                        return f
                if target == '_self':
                    #self.GetParent().refresh_html()
                    #return
                    update_controls = self.update_controls
                    self.update_controls = True
                    self.show_page(mp.get_body(), self.get_parm_obj())

                        #pass

                    self.wxdc = None
                    self.draw_background()
                    self.Refresh()
                    self.init_page()
                    self.update_controls = update_controls
                    if 'href' in attr_dict:
                        href = attr_dict['href']
                    else:
                        href = None
                    #self.get_parent().href_list.append((href, attr_dict))
                    self.get_parent().reg_href(href, attr_dict)

                    if self.GetParent().address_or_parser.__class__.__name__ == 'ShtmlParser':
                        self.GetParent().address_or_parser.address = adr2
                    else:
                        self.GetParent().address_or_parser  = adr2

                    return
                if target == '_blank':
                    self.GetParent().ActiveCtrl = ctrl
                    win = self.new_child_page(mp, is_null(mp.title, title),
                                              param=self.get_parm_obj())
                    if win:
                        win.Body.set_address_parm(str(adr2))
                    return
                if target == '_top':
                    self.new_main_page(mp, is_null(mp.title, title),
                                       param=self.get_parm_obj(), panel=None)
                    return

                if target.startswith('_top2'):
                    x = target[5:]
                    if x[0:1] == '_':
                        self.new_main_page(mp, is_null(mp.title, title),
                                           param=self.get_parm_obj(), panel=x[1:])
                    else:
                        self.new_main_page(mp, is_null(mp.title, title),
                                           param=self.get_parm_obj(), panel='Desktop2')
                    return
                if target == '_parent':
                    self.any_parent_command('on_cancel', None)
                    return
                if target == '_refresh':
                    self.GetParent().refresh_html()
                    return
                if target == '_parent_refr':
                    self.any_parent_command('on_ok', None)
                    return
                if target == 'message':
                    dlg = wx.MessageDialog(self, s, is_null(mp.title, title),
                                           style=wx.OK)
                    dlg.ShowModal()
                    return

                if target == 'code':
                    script = mp.get_body()[1]
                    app = wx.GetApp()
                    main_window = app.GetTopWindow()
                    desktop = (main_window.desktop, )
                    mgr = main_window._mgr
                    menu_bar = main_window.get_menu_bar()
                    tool_bars = main_window.toolbar_interface.get_toolbars()
                    exec (script.replace('\r', ''))
                    return

    def get_evt_ind(self):
        if self.evt_ind == -1:
            self.evt_ind = wx.ID_HIGHEST
        else:
            self.evt_ind += 1
        return self.evt_ind

    def set_acc_key_tab(self, win, tab):
        if win in self.acc_tabs:
            self.acc_tabs[win].append(tab)
        else:
            self.acc_tabs[win] = [tab,]

    def _build_acc_tab(self, to_win=None):
        ret = []
        if to_win:
            obj=to_win
        else:
            obj=self
        for win in self.acc_tabs.keys():
            tab = []
            for pos in self.acc_tabs[win]:
                tab += pos
            ret.append((win,tab))
            #obj._set_acc_key_tab(win, tab)
        obj._set_acc_key_tab(ret)


    #def _set_acc_key_tab(self, win, tab):
    def _set_acc_key_tab(self, tabs):
        tab2 = []

        for tab_pos in tabs:
            win = tab_pos[0]
            tab = tab_pos[1]

            id_start = self.get_evt_ind()
            for pos in tab:
                tab2.append((pos[0], pos[1], self.get_evt_ind()))

            if wx.Platform == '__WXMSW__':
                win.SetAcceleratorTable(wx.AcceleratorTable(tab2))
                tab2 = []
                def on_command(event):
                    id = event.GetId()
                    ind = id - id_start - 1
                    print("on_command:", id, ind)
                    if ind >= 0 and ind < len(tab):
                        cmd = tab[ind][2]
                        cmd(event)
                    else:
                        event.Skip()

                win.Bind(wx.EVT_MENU, on_command)
            else:
                if not self.acc_tab:
                    self.acc_tab = []
                for pos in tab:
                    self.acc_tab.append(list(pos)+[win,])

                if not win.acc_tab:
                    win.Bind(wx.EVT_KEY_DOWN, self.on_acc_key_down)
                    win.acc_tab = True


        if wx.Platform != '__WXMSW__':
            self.SetAcceleratorTable(wx.AcceleratorTable(tab2))




    def on_acc_key_down(self, event):
        if event.KeyCode == 307:
            return
        print(event)
        for a in self.acc_tab:
            if event.KeyCode == a[1]:
                if ( not event.AltDown() ) and (a[0] & wx.ACCEL_ALT ):
                    continue
                if ( not event.ControlDown()) and (a[0] & wx.ACCEL_CTRL):
                    continue
                if ( not event.ShiftDown()) and (a[0] & wx.ACCEL_SHIFT):
                    continue

                if event.AltDown() and not (a[0] & wx.ACCEL_ALT ):
                    continue
                if event.ControlDown() and not (a[0] & wx.ACCEL_CTRL):
                    continue
                if event.ShiftDown() and not (a[0] & wx.ACCEL_SHIFT):
                    continue
                p = wx.Window.FindFocus()
                while p:
                    if p==a[3]:
                        a[2](event)
                        return
                    p = p.GetParent()
                return
        event.Skip()
