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

from schcli.guilib.events import *
from schcli.toolbar.standardtoolbarbuttons import StandardButtons
from schcli.guiframe.page import SchPage

_ = wx.GetTranslation


class BaseHtmlPanel():
    def __init__(self, page, real_panel):
        self.page = page
        self.real_panel = real_panel
        self.html_page = None
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.real_panel.SetSizer(self.sizer)

    def get_width(self):
        return 0

    def get_height(self):
        return 0

    def get_window(self):
        return self.real_panel

    def set_page(self, html_page):
        if self.html_page:
            self.sizer.Replace(self.html_page, html_page)
            self.html_page.Destroy()
        else:
            self.sizer.Add(html_page, 0, wx.LEFT | wx.TOP | wx.EXPAND | wx.RIGHT, 2)

        self.html_page = html_page

        self.sizer.Fit(self.real_panel)


class ToolbarButton():

    TYPE_SIMPLE = 0
    TYPE_DROPDOWN = 1
    TYPE_HYBRID = 2
    TYPE_TOOGLE = 3
    TYPE_PANEL = 4
    TYPE_SEPARATOR = 5

    def __init__(self, parent_panel, id, title, bitmap = None, bitmap_disabled = None, kind=TYPE_SIMPLE):
        self.parent_panel = parent_panel
        self.id = id
        self.title = title
        self.bitmap = bitmap
        if bitmap_disabled is None and bitmap is not None:
            self.bitmap_disabled = wx.NullBitmap
        else:
            self.bitmap_disabled = bitmap_disabled
        self.kind = kind


class ToolbarPanel(object):

    TYPE_PANEL_BUTTONBAR = 0
    TYPE_PANEL_TOOLBAR = 1
    TYPE_PANEL_PANELBAR = 2

    def __init__(self, parent_page, title, kind=TYPE_PANEL_BUTTONBAR):
        self.parent_page = parent_page
        self.title = title
        self.kind = kind
        self.buttons = []

    def _transform_bitmaps_parm(self, bitmaps):
        b = [None, None]
        if len(bitmaps)>0:
            b[0] = bitmaps[0]
        if len(bitmaps)>1:
            b[1] = bitmaps[1]
        return b

    def create_button(self, id, title, bitmap=None, bitmap_disabled=None, kind=ToolbarButton.TYPE_SIMPLE):
        return ToolbarButton(self, id, title, bitmap, bitmap_disabled, kind)

    def append(self, id, title, bitmap=None, bitmap_disabled=None, kind=ToolbarButton.TYPE_SIMPLE):
        button = self.create_button(id, title, bitmap, bitmap_disabled, kind)
        self.buttons.append(button)
        return button

    def add_simple_tool(self, id, title, bitmaps):
        b = self._transform_bitmaps_parm(bitmaps)
        return self.append(id, title, b[0], b[1], kind = ToolbarButton.TYPE_SIMPLE)

    def add_dropdown_tool(self, id, title, bitmaps):
        b = self._transform_bitmaps_parm(bitmaps)
        return self.append(id, title, b[0], b[1], kind = ToolbarButton.TYPE_DROPDOWN)

    def add_hybrid_tool(self, id, title, bitmaps):
        b = self._transform_bitmaps_parm(bitmaps)
        return self.append(id, title, b[0], b[1], kind = ToolbarButton.TYPE_HYBRID)

    def add_toogle_tool(self, id, title, bitmaps):
        b = self._transform_bitmaps_parm(bitmaps)
        return self.append(id, title, b[0], b[1], kind = ToolbarButton.TYPE_TOOGLE)

    def add_separator(self):
        pass


class ToolbarPage(object):
    TYPE_PAGE_NORMAL = 0

    def __init__(self, parent_bar, title, kind=TYPE_PAGE_NORMAL):
        self.parent_bar = parent_bar
        self.title = title
        self.kind = kind
        self.panels = []

    def create_panel(self, title, kind):
        return self.ToolbarPanel(self, title, kind=ToolbarPanel.TYPE_PANEL_BUTTONBAR)

    def create_html_panel(self, title):
        return None

    def append(self, title, kind=ToolbarPanel.TYPE_PANEL_BUTTONBAR):
        p = self.create_panel(title, kind)
        self.panels.append(p)
        return p


class ToolbarBar(object):
    def __init__(self, parent, gui_style):
        self.parent = parent
        self.main_page = None
        self.gui_style = gui_style

        self.toolbars = {}
        self.pages = []
        self.user_panels = {}

        self.standard_buttons = StandardButtons(self, gui_style)
        self.standard_buttons.create_file_panel(self.main_page)
        self.standard_buttons.create_edit_panel(self.main_page)
        self.standard_buttons.create_operations_panel(self.main_page)
        self.standard_buttons.create_browse_panel(self.main_page)
        self.standard_buttons.create_address_panel(self.main_page)

    def create_page(self, title, kind=ToolbarPage.TYPE_PAGE_NORMAL):
        return self.ToolbarPage(self, title, kind)

    def remove_page(self, title):
        for page in self.pages:
            if page.title == title:
                self.pages.remove(page)
                break
        for key, panel in self.user_panels.items():
            if panel.page.title == title:
                del self.user_panels[key]
                return

    def append(self, title, kind=ToolbarPage.TYPE_PAGE_NORMAL):
        for page in self.pages:
            if page.title == title and page.kind == kind:
                return page
        p = self.create_page(title, kind)
        if not self.main_page:
            self.main_page = p
        self.pages.append(p)
        return p

    def create(self):
        pass

    def close(self):
        pass

    def create_panel_in_main_page(self, title, kind):
        if not self.main_page:
            self.append(_("main"))
        return self.main_page.create_panel(title, kind)

    def bind(self, fun, id=wx.ID_ANY, e=None):
        if e:
            self.parent.Bind(e, fun, id=id)
        else:
            self.parent.Bind(wx.EVT_MENU, fun, id=id)

    def un_bind(self, id=wx.ID_ANY, e=None):
        if e:
            self.parent.Unbind(e, id=id)
        else:
            self.parent.Unbind(wx.EVT_MENU, id=id)

    def create_html_win(self, toolbar_page, address_or_parser, parameters):
        if not toolbar_page:
            u_name = 'main'
            page_name = _('main')
            panel_name = 'main'
        else:
            u_name = toolbar_page
            names = toolbar_page.split('__')
            if len(names) > 1:
                page_name = names[0].replace('_', ' ')
                panel_name = names[1].replace('_', ' ')
            else:
                page_name = toolbar_page.replace('_', ' ')
                panel_name = page_name

        if u_name in self.user_panels:
            panel = self.user_panels[u_name]
        else:
            if page_name in self.pages:
                page = self.pages[page]
            else:
                page = self.append(page_name)
            panel = page.create_html_panel(panel_name)

        if panel:
            dx = panel.get_width() + 3
            dy = panel.get_height() + 5

            page2 = SchPage(panel.get_window(), address_or_parser, parameters, size=wx.Size(dx, dy), pos=wx.Point(2, 2))
            best = page2.body.calculate_best_size()
            page2.SetSize(wx.Size(best[0], best[1]))
            panel.set_page(page2)
            self.user_panels[u_name] = panel
            page2.body.toolbar_interface = self
            page2.body.toolbar_interface_page = page
            return page2

        return None

    def new_child_page(self,address_or_parser,title='',param=None):
        return wx.GetApp().GetTopWindow().new_main_page(address_or_parser, title,param)
