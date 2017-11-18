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

"""Module contain SchForm class.
"""

import gc
import sys
import types
import math

import wx
from wx.lib.scrolledpanel import ScrolledPanel
import wx.lib.agw.ribbon as RB

from schlib.schtools import createparm
from schlib.schparser.html_parsers import ShtmlParser
from schlib.schtools.tools import clean_href, is_null
from schlib.schhtml.wxdc import DcDc
from schlib.schhtml.htmlviewer import HtmlViewerParser

_ = wx.GetTranslation

_INIT_CSS_STR = None
_PRE_PRECESS_LIB = []


def install_pre_process_lib(fun):
    global _PRE_PRECESS_LIB
    _PRE_PRECESS_LIB.append(fun)


def _get_css():
    global _INIT_CSS_STR
    if _INIT_CSS_STR == None:
        with open(wx.GetApp().scr_path + '/schappdata/icss/form.icss', 'r') as f:
            _INIT_CSS_STR = f.read()
    return _INIT_CSS_STR


class SchForm(ScrolledPanel):
    """Html window"""

    @property
    def bestsize(self):
        return self._bestsize

    @bestsize.setter
    def bestsize(self, x):
        self._bestsize = x

    def __init__(self,  parent, page=None, hscroll=False,  vscroll=False, form_type='body'):
        """Constructor

        Args:
            parent - parent window
            page - parent SchPage object
            hscroll - enable horizontal scroll bar
            vscroll - enable vertical scroll  bar
            form_type - can be: body, header, footer, panel
        """
        self._bestsize = None
        self._scroll_xy = (0, 0)
        self._act_scroll_xy = (0, 0)
        self._enabled_controls = False
        self._last_size = (-1, -1)
        self._best_virtual_size = None
        self._block = False
        self._dc_buf = None
        self._dc_buf_x = 0
        self._dc_buf_y = 0
        self._lock = False

        self.no_vscrollbar = not vscroll
        self.no_hscrollbar = not hscroll
        self.address = None
        self.script = None
        self.parameters = None
        self.page_source = '<html></html>'
        self.script = None
        self.bestsize = None
        self.hover_obj = None
        self.cursor_type = 0
        self.wxdc = None
        self.after_init = False
        self.update_controls = False
        self.obj_action_dict = {}
        self.obj_id_dict = {}
        self.last_control_with_focus = None
        self.page = page
        self.form_type = form_type
        self.init_css_str = None
        self.evt_ind = -1
        self.closing = False
        self.acc_tabs = {}
        self.acc_tab = None
        self.last_clicked = None
        self.t1 = None

        ScrolledPanel.__init__(self, parent, -1, style=wx.WANTS_CHARS)
        try:
            self.SetBackgroundStyle(wx.BG_STYLE_ERASE)
        except:
            self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)


        self.SetupScrolling(hscroll, vscroll, rate_y=1)

        self.SetAcceleratorTable(wx.AcceleratorTable(wx.GetApp().GetTopWindow().aTable))

        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)
        self.Bind(wx.EVT_LEFT_UP, self.on_left_up)
        self.Bind(wx.EVT_RIGHT_UP, self.on_right_up)
        self.Bind(wx.EVT_MOTION, self.on_motion)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.on_erase_background)
        self.Bind(wx.EVT_SET_FOCUS, self.on_focus)

        self.EnableScrolling(False, False)


    def SetFocus(self):
        if self.last_control_with_focus:
            self.last_control_with_focus.SetFocus()
        else:
            wx.CallAfter(self.Navigate, None)


    def Navigate(self, ctrl, back = False):
        next = False
        children = [ child for child in self.GetChildren() if child.CanAcceptFocus() ]
        if back:
            widgets = reversed(children)
        else:
            widgets = children
        for w in widgets:
            if next or not ctrl:
                w.SetFocus()
                self.last_control_with_focus = w
                return
            if w==ctrl:
                next = True
        if children and len(children)>0:
            if back:
                children[-1].SetFocus()
                self.last_control_with_focus = children[-1]
            else:
                children[0].SetFocus()
                self.last_control_with_focus = children[0]

    def on_focus(self, event):
        if self.last_control_with_focus:
            self.last_control_with_focus.SetFocus()
        else:
            wx.CallAfter(self.Navigate, None)

    def bind_to_ctrl(self, ctrl, id, fun, fun2=None):
        """bind function callback to command event from ctrl

        Args:
            ctrl - widget
            id - command id
            fun - callback function command event
            fun2 - callback function for EVT_UPDATE_UI event

        """
        if fun2:
            ctrl.Bind(wx.EVT_UPDATE_UI, fun2, id=id)
        ctrl.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, fun, id=id)
        ctrl.Bind(RB.EVT_RIBBONTOOLBAR_CLICKED, fun, id=id)
        ctrl.Bind(wx.EVT_MENU, fun, id=id)

    def scroll_child_into_view(self, child):
        """scroll this window to position at which child window is visible"""
        if child.GetParent() == self:
            (sppu_x, sppu_y) = self.GetScrollPixelsPerUnit()
            (vs_x, vs_y) = self.GetViewStart()
            cr = child.GetRect()
            clntsz = self.GetClientSize()
            (new_vs_x, new_vs_y) = (-1, -1)
            if cr.y < 0 and sppu_y > 0:
                new_vs_y = vs_y + cr.y / sppu_y
            if cr.bottom > clntsz.height and sppu_y > 0:
                diff = math.ceil((1.0 * (cr.bottom - clntsz.height + 1)) / sppu_y)
                if cr.y - diff * sppu_y > 0:
                    new_vs_y = vs_y + diff
                else:
                    new_vs_y = vs_y + cr.y / sppu_y
            if new_vs_y != -1:
                self.Scroll(-1, new_vs_y)

    def set_css(self, css_str):
        """set css file for this form"""
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
        dc = wx.ClientDC(self)
        wxdc = DcDc(dc, calc_only=True, width=width, height=-1)
        p = HtmlViewerParser(dc=wxdc, calc_only=True,
                             init_css_str=self.get_css(), css_type=1)
        p.set_http_object(wx.GetApp().http)
        p.set_parent_window(self)
        if not self._lock:
            self._lock = True
            self.GetParent().restart_ctrl_lp()
            p.feed(self.page_source)
            self.GetParent().remove_old_ctrls()
            self._lock = False
        (dx, dy) = p.get_max_sizes()
        p.close()
        return (dx, dy)

    def calculate_best_size(self):
        psize = self.GetParent().GetParent().GetClientSize()
        if self.bestsize:
            (dx, dy) = self._calculate_size(self.bestsize[0])
        else:
            (dx, dy) = self._calculate_size((psize[0] * 3) / 4)
        self.bestsize = (dx, dy + 8)
        return self.bestsize

    def html_updatet(self, dc, size):
        """parse a html page after it was updated"""
        w = size.GetWidth()
        h = size.GetHeight()
        if w == 20 and h == 20:
            return
        if not self.wxdc:
            if self.no_vscrollbar:
                self.wxdc = DcDc(dc, calc_only=False, width=w - 1, height=-1)
            else:
                self.wxdc = DcDc(dc, calc_only=False, width=w - 1 - wx.SystemSettings.GetMetric(wx.SYS_VSCROLL_X),
                                 height=-1)
            p = HtmlViewerParser(dc=self.wxdc, calc_only=False,
                                 init_css_str=self.get_css(), css_type=1)
            p.set_http_object(wx.GetApp().http)
            p.set_parent_window(self)
            if not self._lock:
                self._lock = True
                self.GetParent().restart_ctrl_lp()
                p.feed(self.page_source)
                self.GetParent().remove_old_ctrls()
                self._lock = False
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


    def draw_background(self, refresh_all=False, size=None):
        """drawn a rendered html page as a background"""
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
            dc.Blit(x,y,rect.GetWidth(),rect.GetHeight(),self._dc_buf,x,y)
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
            dc.Blit(x,y,rect.GetWidth(),rect.GetHeight(),dc2,x,y)
            self._dc_buf = dc2
            self._dc_buf_x = x
            self._dc_buf_y = y
        self._block = False

    def on_erase_background(self, event):
        self.draw_background()

    def append_ctrl(self, ctrl):
        try:
            setattr(self, ctrl.unique_name, ctrl)
        except:
            pass
        self.GetParent().append_ctrl(ctrl)

    def enable_ctrls(self, ctrls):
        """set widgets which are enabled or disabled
        Widget enabled is updated when html page is refreshed

        Args:
            ctrls - list or tuple with widgets names
        """
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
        """enable od disable the form"""
        ret = super(SchForm, self).Enable(enable)
        if enable:
            wx.CallAfter(self.restore_scroll_pos)
        return ret

    def set_best_size(self, bestsize):
        """Set the best size for this form"""
        self.bestsize = bestsize

    #def on_opening_url(self, type, url):
    #    if hasattr(self, 'filter_url'):
    #        f = self.filter_url(type, url)
    #        if f != None:
    #            return f
    #    if url.startswith('/'):
    #        url2 = url
    #        base = wx.GetApp().base_address
    #        if base.startswith('http://127.0.0.2'):
    #            if url.startswith('/app_media'):
    #                if ':' in wx.GetApp().root_path:
    #                    url2 = wx.GetApp().root_path + '/app_pack' + url.replace('/app_media', '')
    #                    url2 = norm_path(url2)
    #                else:
    #                    url2 = 'file://' + wx.GetApp().root_path + '/app_pack' + url.replace('/app_media', '')
    #                    url2 = norm_path(url2)
    #        else:
    #            url2 = base + url
    #        return url2
    #    return True

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

    def refresh_time(self, number_of_sec):
        """When refresh time is set form automatically refresh his content every number_of_sec seconds"""
        self.t1 = wx.Timer(self)
        self.t1.Start(time * 1000)
        self.Bind(wx.EVT_TIMER, self.on_timer, self.t1)

    #def close_with_delay(self):
    #    wx.CallAfter(self.cancel, True)

    def on_timer(self, event):
        if self.page:
            if not self.page.exists:
                self.t1.Stop()
                return
        self.GetParent().refresh_html()

    def cancel(self):
        """Close this form without saving its content"""
        if self.page:
            self.page.exists = False
        if self.t1:
            self.t1.Stop()
        if self.page:
            self.page.GetParent().on_child_form_cancel()

    def ok(self):
        if self.page:
            self.page.exists = False
        if self.t1:
            self.t1.Stop()
        if self.page:
            self.page.GetParent().on_child_form_ok()

    def set_htm_type(self, form_type):
        self.form_type = form_type

    def get_gparent_page(self):
        """return grand parent SChPage object in hierarchy"""
        page = self.get_parent_page()
        if page:
            return page.get_parent_page()
        else:
            return None

    def get_parent_page(self):
        """return parent SChPage object in hierarchy"""
        return self.page

    def get_parent_form(self):
        """return parent SchFrame object in hierarchy"""
        gpage = self.get_gparent_page()
        if gpage:
            return gpage.active_form
        return None

    def on_right_up(self, evt):
        okno = self.new_main_page('^standard/editor/editor.html', self.get_parent_page().title + ' - '+_('page source'), None)
        def init_ctrl():
            okno.body.EDITOR.SetValue(self.page_source.tostream().getvalue())
            okno.body.EDITOR.GotoPos(0)
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
                for r in obj.rendered_rects:
                    rect = wx.Rect(r[0], r[1], r[2], r[3])
                    if rect.Contains(pos2):
                        self.href_clicked(self, obj.attrs)
                        evt.Skip()
                        return
        evt.Skip()

    def CanClose(self):
        """Test if form can be closed"""
        ret = True
        if hasattr(self, 'can_close'):
            ret = self.can_close()
        else:
            widgets = list(self.GetParent().get_widgets().values())
            for w in widgets:
                if hasattr(w, 'CanClose'):
                    if not w.CanClose():
                        ret = False
        return ret

    def _on_close(self):
        self.closing=True
        if hasattr(self, 'on_close'):
            self.on_close()
        gc.collect()

    def any_parent_command(self, command, *args, **kwds):
        """find first in hierarchy window which contains function with specyfied name and run this function

        Args:
            command: name of function to find
            args, kwds: parameters forwarded to function
        """
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

    def get_parm_obj(self):
        """Get parent object width method get_par"""
        parent = self
        while parent != None:
            if hasattr(parent, 'get_parm'):
                return parent
            parent = parent.GetParent()
        return None

    def refr(self, refr_always=False):
        #"""Refresh form"""
        #self.refr_obj(refr_always=True)
        #def refr_obj(self, refr_always=False):
        """Refresh html content"""

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
                if self.form_type == 'panel':
                    strona = mp.get_panel()
                elif self.form_type == 'header':
                    strona = mp.get_header()
                elif self.form_type == 'footer':
                    strona = mp.get_footer()
                else:
                    strona = mp.get_body()
                if self.show_form(strona, self.parameters):
                    self.init()

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
        """Set html page source"""
        self.page_source = page_source
        self.wxdc = None
        self.draw_background()

    def pre_process_page(self, page):
        global _PRE_PRECESS_LIB
        page2 = page
        for fun in _PRE_PRECESS_LIB:
            page2 = fun(self, page2)
        return page2

    def exec_code(self, script, parm=None):
        """run code attached to html page"""
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


    def show_form(self, page_and_script, parameters=None):
        """Show form

        Args:
            page_and_script: list or touple, 0: html page content, 1: script
            parameters: parameters forwarded to http server in request
        """
        if self.page and self.page.exists == False:
            return False

        self.page_source = self.pre_process_page(page_and_script[0])
        self.parameters = parameters
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

                for key in d:
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
        return True


    def init(self):
        """init form"""
        if not self.after_init:
            if hasattr(self, 'init_form'):
                wx.CallAfter(self.init_form)
            self.after_init = True
        else:
            if hasattr(self, 'reinit'):
                self.reinit()
            elif hasattr(self, 'init_form'):
                self.init_form()
        wx.CallAfter(self._build_acc_tab)


    def new_local_child_page(self,address,title='',parameters=None):
        return self.new_child_page('http://local.net/' + address, title, parameters)

    def new_plugin_child_page(self,path,address,title='',parameters=None):
        p = path.split('/')
        address2 = 'schappdata/schplugins/' + p[-3] + '/' + p[-2] + '/' + address
        return self.new_local_child_page(address2, title, parameters)

    def new_child_page(self,address_or_parser,title='',parameters=None):
        """Create a child page

        Args:
            address_or_parser: can be: address of http page (str type) or
            :class:'~schlib.schparser.html_parsers.ShtmlParser'
            title - new page title
            parameters: dict
        """
        self._scroll_xy = self.GetViewStart()
        self.get_parm_obj().active_form = self
        self.GetParent().active_form= self
        if hasattr(self.GetParent(), 'last_control_with_focus'):
            self.last_control_with_focus = self.GetParent().last_control_with_focus
        else:
            self.last_control_with_focus = None
        self.GetParent().disable_setfocus = True
        return self.any_parent_command('new_child_page', address_or_parser, title, parameters)

    def new_main_page(self,address_or_parser,title=None,parameters=None,panel='desktop'):
        return self.any_parent_command('new_main_page', address_or_parser, title,parameters, panel)

    def scroll_to_href(self, href):
        """scroll this window to position at which widget with a href attribute is visible"""
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

    def href_clicked(self,ctrl,attr_dict,upload=False,fields=False):
        """Handle action connected to widget with href attribute

        Args:
            ctrl - widget
            attr_dict - dict with attributes for http request
            upload - if true, this is action prepared to upload content to server
            fields - list of fields which values are sended to http server
        """
        self.last_clicked = ctrl

        if 'href' in attr_dict:
            href = attr_dict['href']
            if href and len(href)>0 and href[0]=='#':
                return self.scroll_to_href(href)
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
                    if type(f)==str:
                        href = clean_href(f)
                    else:
                        return f

            if href == None:
                if target == '_parent':
                    self.any_parent_command('on_child_form_cancel')
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
                okno = self.new_main_page('^standard/editor/editor.html', href, None)
                okno.body.EDITOR.SetValue(s)
                okno.body.EDITOR.GotoPos(0)
            else:
                if 'application' in http.ret_content_type:
                    wx.GetApp().GetTopWindow()._open_binary_data(http, href)
                    http.clear_ptr()
                    return

                s = http.str()
                http.clear_ptr()
                mp = ShtmlParser()
                mp.process(s, adr2)
                if 'target' in mp.var:
                    target = mp.var['target']
                http.clear_ptr()

                if href and hasattr(self, 'filter_http_result'):
                    f = self.filter_http_result(target, href, mp)
                    if f != None:
                        return f
                if target == '_self':
                    update_controls = self.update_controls
                    self.update_controls = True
                    self.show_form(mp.get_body(), self.get_parm_obj())
                    self.wxdc = None
                    self.draw_background()
                    self.Refresh()
                    self.init()
                    self.update_controls = update_controls
                    if 'href' in attr_dict:
                        href = attr_dict['href']
                    else:
                        href = None

                    if self.GetParent().address_or_parser.__class__.__name__ == 'ShtmlParser':
                        self.GetParent().address_or_parser.address = adr2
                    else:
                        self.GetParent().address_or_parser  = adr2

                    return
                if target in ('_blank', 'inline', 'popup_edit', 'popup_info', 'popup_delete', '_self',):
                    self.GetParent().active_ctrl = ctrl
                    win = self.new_child_page(mp, is_null(mp.title, title), parameters=self.get_parm_obj())
                    if win:
                        win.body.set_address_parm(str(adr2))
                    return
                if target == '_top':
                    self.new_main_page(mp, is_null(mp.title, title), parameters=self.get_parm_obj(), panel=None)
                    return

                if target.startswith('_top2'):
                    x = target[5:]
                    if x[0:1] == '_':
                        self.new_main_page(mp, is_null(mp.title, title), parameters=self.get_parm_obj(), panel=x[1:])
                    else:
                        self.new_main_page(mp, is_null(mp.title, title), parameters=self.get_parm_obj(), panel='desktop2')
                    return
                if target == '_parent':
                    self.any_parent_command('on_child_form_cancel')
                    return
                if target == '_refresh':
                    self.GetParent().refresh_html()
                    return
                if target == '_parent_refr':
                    self.any_parent_command('on_child_form_ok')
                    return
                if target == 'message':
                    dlg = wx.MessageDialog(self, s, is_null(mp.title, title), style=wx.OK)
                    dlg.ShowModal()
                    return

                if target == 'code':
                    script = mp.get_body()[1]
                    app = wx.GetApp()
                    main_window = app.GetTopWindow()
                    desktop = (main_window.desktop, )
                    mgr = main_window._mgr
                    menu_bar = main_window.get_menu_bar()
                    tool_bars = main_window.get_tool_bar()
                    exec (script.elem.text.replace('\r', ''))
                    return

    def signal_from_child(self, child_object, signal):
        pass

    def get_evt_ind(self):
        if self.evt_ind == -1:
            self.evt_ind = wx.ID_HIGHEST
        else:
            self.evt_ind += 1
        return self.evt_ind

    def set_acc_key_tab(self, win, tab):
        """Set accelerator table for window

        Args:
            win - window which handle accelerator keys
            tab - list or tuple of accelerator elements. Each emement has structure: (flag, keycode, callback fun)
        """
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
        obj._set_acc_key_tab(ret)

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
                def make_fun(tab, id_start):
                    def on_command(event):
                        id = event.GetId()
                        ind = id - id_start - 1
                        if ind >= 0 and ind < len(tab):
                            cmd = tab[ind][2]
                            cmd(event)
                        else:
                            event.Skip()
                    return on_command

                win.Bind(wx.EVT_MENU, make_fun(tab, id_start))
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
