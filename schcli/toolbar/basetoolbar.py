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

"""
Module contains base classes for toolbars and menu:
Class hierary:
ToolbarBar
    ToolbarPage
        ToolbarPanel
            ToolbarButton
            ToolbarButton
            ...
        ToolbarPanel
        ....
        BaseHtmlPanel
    ....

One ToolbarBar can contains many ToolbarPage objects, one ToolbarPage can contains many ToolbarPanel objects etc.

There are real toolbars and menus, which are base on those abstract classes:
- MenuToolbarBar
- GenericToolbarBar
- StandardToolbarBar
- ModernToolbarBar
- TreeToolbarBar
"""

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
    """Toolbar button"""

    TYPE_SIMPLE = 0
    TYPE_DROPDOWN = 1
    TYPE_HYBRID = 2
    TYPE_TOOGLE = 3
    TYPE_PANEL = 4
    TYPE_SEPARATOR = 5

    def __init__(self, parent_panel, id, title, bitmap = None, bitmap_disabled = None, kind=TYPE_SIMPLE):
        """Constructor, creating a new toolbar button

        Args:
            parent_panel - parent ToolbarPanel object
            id - An integer by which the tool may be identified
            title - button title
            bitmap - button bitmap
            bitmap_disabled - button bitmap used when button is disabled
            kind - type of button, may be:
                TYPE_SIMPLE = 0
                TYPE_DROPDOWN = 1
                TYPE_HYBRID = 2
                TYPE_TOOGLE = 3
                TYPE_PANEL = 4
                TYPE_SEPARATOR = 5
        """
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
    """Toolbar panel"""

    TYPE_PANEL_BUTTONBAR = 0
    TYPE_PANEL_TOOLBAR = 1
    TYPE_PANEL_PANELBAR = 2

    def __init__(self, parent_page, title, kind=TYPE_PANEL_BUTTONBAR):
        """Constructor, creating a new toolbar panel

        Args:
            parent_page - parent ToolbarPage object
            title - panel title
            kind - type of panel, may be:
                TYPE_PANEL_BUTTONBAR = 0
                TYPE_PANEL_TOOLBAR = 1
                TYPE_PANEL_PANELBAR = 2
        """
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
        """Function return new ToolbarButton, shoud be derived. In derived class shoud return ToolbarButton
        derived object.

        Args: see ToolbarButton contructor
        """
        return ToolbarButton(self, id, title, bitmap, bitmap_disabled, kind)

    def append(self, id, title, bitmap=None, bitmap_disabled=None, kind=ToolbarButton.TYPE_SIMPLE):
        """Append button to panel.

        Args: see ToolbarButton contructor
        """
        button = self.create_button(id, title, bitmap, bitmap_disabled, kind)
        self.buttons.append(button)
        return button

    def add_simple_tool(self, id, title, bitmaps):
        """Append simple tool to toolbar.

        Args:
            id - an integer by which the tool may be identified
            title - button title
            bitmaps - list of bitmaps, can contains 0, 1 or 2 bitmaps
                first bitmap is used for tool in normal state, second for disabled tool.
        """
        b = self._transform_bitmaps_parm(bitmaps)
        return self.append(id, title, b[0], b[1], kind = ToolbarButton.TYPE_SIMPLE)

    def add_dropdown_tool(self, id, title, bitmaps):
        """Append simple tool to toolbar.

        Args:
            id - an integer by which the tool may be identified
            title - button title
            bitmaps - list of bitmaps, can contains 0, 1 or 2 bitmaps
                first bitmap is used for tool in normal state, second for disabled tool.
        """
        b = self._transform_bitmaps_parm(bitmaps)
        return self.append(id, title, b[0], b[1], kind = ToolbarButton.TYPE_DROPDOWN)

    def add_hybrid_tool(self, id, title, bitmaps):
        """Append hybrid tool to toolbar.

        Args:
            id - an integer by which the tool may be identified
            title - button title
            bitmaps - list of bitmaps, can contains 0, 1 or 2 bitmaps
                first bitmap is used for tool in normal state, second for disabled tool.
        """
        b = self._transform_bitmaps_parm(bitmaps)
        return self.append(id, title, b[0], b[1], kind = ToolbarButton.TYPE_HYBRID)

    def add_toogle_tool(self, id, title, bitmaps):
        """Append toogle tool to toolbar.

        Args:
            id - an integer by which the tool may be identified
            title - button title
            bitmaps - list of bitmaps, can contains 0, 1 or 2 bitmaps
                first bitmap is used for tool in normal state, second for disabled tool.
        """
        b = self._transform_bitmaps_parm(bitmaps)
        return self.append(id, title, b[0], b[1], kind = ToolbarButton.TYPE_TOOGLE)

    def add_separator(self):
        """Append separator to toolbar."""
        pass


class ToolbarPage(object):
    """Toolbar page"""

    TYPE_PAGE_NORMAL = 0

    def __init__(self, parent_bar, title, kind=TYPE_PAGE_NORMAL):
        """Constructor, creating a new ToolbarPage page.

        Args:
            parent_bar - parent ToolbarBar object
            title - page title
            kind - type of page, may be:
                TYPE_PAGE_NORMAL = 0
        """
        self.parent_bar = parent_bar
        self.name = title
        self.title = _(title)
        self.kind = kind
        self.panels = []

    def create_panel(self, title, kind):
        """Function return new ToolbarPanel, shoud be derived. In derived class shoud return ToolbarPanel
        derived object.

        Args: see ToolbarPanel contructor
        """
        return self.ToolbarPanel(self, title, kind=ToolbarPanel.TYPE_PANEL_BUTTONBAR)

    def create_html_panel(self, title):
        """Function shoud be overwriten in derived class.
        In derived class shoud return BaseHtmlPanel derived object.

        Args: see BaseHtmlPanel contructor
        """
        return None

    def append(self, title, kind=ToolbarPanel.TYPE_PANEL_BUTTONBAR):
        """Append new ToolbarPanel to page.

        Args:
            title - panel title
            kind - see ToolbarPanel constructor

        """
        p = self.create_panel(title, kind)
        self.panels.append(p)
        return p


class ToolbarBar(object):
    """Toolbar bar"""

    def __init__(self, parent, gui_style):
        """Constructor, ToolbarBar is base class for all menus and toolbars connected to top frame window.

        Args:
            parent - parent window - top wx.Frame derived object
            gui_style - string description of gui interface. Base on this string standard toolbar elements are created.
        """
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
        """Function return new ToolbarPage, shoud be derived. In derived class shoud return ToolbarPage
        derived object.

        Args: see ToolbarPage contructor
        """
        return self.ToolbarPage(self, title, kind)

    def remove_page(self, title):
        """Remove page witch specified title from toolbar

        Args:
            title: title of removed page
        """
        for page in self.pages:
            if page.title == title:
                self.pages.remove(page)
                break
        for key, panel in self.user_panels.items():
            if panel.page.title == title:
                del self.user_panels[key]
                return

    def append(self, title, kind=ToolbarPage.TYPE_PAGE_NORMAL):
        """Append page to toolbar.

        Args: see ToolbarPage constructor
        """
        for page in self.pages:
            if page.name == title and page.kind == kind:
                return page
        p = self.create_page(title, kind)
        if not self.main_page:
            self.main_page = p
        self.pages.append(p)
        return p

    def create(self):
        """Create toolbar"""
        pass

    def close(self):
        """Close toolbar"""
        pass

    def create_panel_in_main_page(self, title, kind):
        """Create panel in a main page

        Args:
            title - new panels title
            kind - type of new panel - see ToolbarPanel constructor.
        """
        if not self.main_page:
            self.append('main tools')
        return self.main_page.create_panel(title, kind)

    def bind(self, fun, id=wx.ID_ANY, e=None):
        """Bind event handler to toolbar

        Args:
            fun - handler function
            id - identifier of event
            e - type of event
        """
        if e:
            self.parent.Bind(e, fun, id=id)
        else:
            self.parent.Bind(wx.EVT_MENU, fun, id=id)

    def un_bind(self, id=wx.ID_ANY, e=None):
        """Unbind event handler from toolbar."""
        if e:
            self.parent.Unbind(e, id=id)
        else:
            self.parent.Unbind(wx.EVT_MENU, id=id)

    def create_html_win(self, toolbar_page, address_or_parser, parameters):
        """Create html page in toolbar. Not all toolbars may be used

        Args:
            toolbar_page - name of toolbar page
            address_or_parser - addres of http page
            parameters - parameters for http request
        """
        page=None
        if not toolbar_page:
            u_name = 'main tools'
            page_name = _('main tools')
            panel_name = 'main tools'
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

            def init_page():
                page2.init_frame()
                page2.activate_page()
                #wx.GetApp().GetTopWindow()._mgr.GetPane("desktop").Show()
                page2.Update()

            wx.CallAfter(init_page)

            return page2

        return None

    def new_child_page(self,address_or_parser,title='',param=None):
        """Crate new chid page, for toolbar child page is transfered to desktop window"""
        return wx.GetApp().GetTopWindow().new_main_page(address_or_parser, title,param)
