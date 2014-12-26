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
from schcli.guilib.schevent import *
from schcli.toolbar.standardtoolbarbuttons import StandardButtons
from schcli.guiframe.htmlsash import SchSashWindow
import wx

_ = wx.GetTranslation

TYPE_TOOLBAR = 0
TYPE_BUTTONBAR = 1
TYPE_PANELBAR = 2


class ToolbarInterface(object):

    class Page(object):

        class Panel(object):

            def __init__(
                self,
                page,
                title,
                type=TYPE_TOOLBAR,
                ):
                self.page = page
                self.panel = wx.Menu()
                self.page.page.AppendMenu(wx.ID_ANY, title, self.panel)

            def append(
                self,
                id,
                title,
                bitmap=None,
                ):
                if bitmap:
                    item = wx.MenuItem(self.panel, id=id, text=title)
                    item.SetBitmap(bitmap)
                    self.panel.AppendItem(item)
                else:
                    self.panel.Append(id, title)

            def add_tool(
                self,
                id,
                title,
                bitmap_id,
                size,
                ):
                pass

            def add_hybrid_tool(
                self,
                id,
                title,
                bitmap_id,
                size,
                ):
                pass

            def add_button(
                self,
                id,
                title,
                bitmap_id,
                size,
                ):
                pass

            def add_panel(
                self,
                id,
                title,
                bitmap_id,
                size,
                ):
                pass

            def add_separator(self):
                pass


        def __init__(
            self,
            bar,
            title,
            type=TYPE_TOOLBAR,
            ):
            self.bar = bar
            self.page = wx.Menu()
            self.bar.bar.Append(self.page, title)

        def create_panel(self, title):
            return self.Panel(self, title)


    def __init__(self, parent, gui_style):
        self.parent = parent
        self.main_page = None
        self.gui_style = gui_style
        self.toolbars = {}
        self.standard_buttons = StandardButtons(self, gui_style)
        self.standard_buttons.create_file_panel(self.main_page)
        self.standard_buttons.create_edit_panel(self.main_page)
        self.standard_buttons.create_operations_panel(self.main_page)
        self.standard_buttons.create_browse_panel(self.main_page)
        self.standard_buttons.create_address_panel(self.main_page)
        self.user_panels = {}

    def create_page(self, title):
        page = self.Page(self, title)
        if not self.main_page:
            self.main_page = page
        return page

    def create_panel_in_main_page(self, title, type):
        if not self.main_page:
            self.create_page('main')
        return self.main_page.create_panel(title, type)
    
    def bind(
        self,
        fun,
        id=wx.ID_ANY,
        e=None
        ):
        print("###################### BIND")
        if e:
            self.parent.Bind(e, fun, id=id)
        else:
            self.parent.Bind(wx.EVT_MENU, fun, id=id)

    def update_bar(self, obj):
        obj.SetMenuBar(self.bar)

    def get_bar(self):
        return self.bar

    def create_html_win(
        self,
        toolbar_page,
        address_or_parser,
        parametry,
        ):
        if not toolbar_page:
            u_name = 'main'
            page_name = 'main'
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
            htmlsash = self.user_panels[u_name]
            bar_size = self.bar.GetSize()
            panel = htmlsash.GetParent()
            sizer = panel.GetSizer()
            dy = self.bar.get_bar_height() + 3
            htmlsash2 = SchSashWindow(panel, address_or_parser, parametry,
                                      size=wx.Size(900, dy))
            best = htmlsash2.Body.calculate_best_size()
            htmlsash2.SetSize(wx.Size(best[0], best[1]))
            sizer.Replace(htmlsash, htmlsash2)
            self.user_panels[u_name] = htmlsash2
            htmlsash.Destroy()
            self.bar.update()
            if hasattr(self.bar._pages, 'page'):
                for page in self.bar._pages:
                    if page.page.GetLabel() == page_name:
                        self.bar.SetActivePage(page.page)
            return htmlsash2
        if toolbar_page:
            page = self.create_page(page_name)
            self.bar.SetActivePage(page.page)
            bar = page.create_panel(panel_name, TYPE_PANELBAR)
        else:
            bar = self.create_panel_in_main_page('Tools', TYPE_PANELBAR)
            self.bar.SetActivePage(self.main_page.page)
        if hasattr(bar, 'panel'):
            panel = bar.panel
            bar_size = self.bar.GetSize()
            dy = self.bar.get_bar_height() + 3
            dx = self.bar.get_bar_width() + 3
            htmlsash = SchSashWindow(panel, address_or_parser, parametry,
                                     size=wx.Size(dx, dy))

            best = htmlsash.Body.calculate_best_size()
            htmlsash.SetSize(wx.Size(best[0], best[1]))
            panel.SetSize(wx.Size(best[0], best[1]))
            controls = (htmlsash, )
            bar.add_panel(controls)
            self.bar.update()
            self.user_panels[u_name] = htmlsash
            return htmlsash
        return None

    def remove_page(self, page):
        label = page.GetLabel()
        if label in self.user_panels:
            del self.user_panels[label]
        else:
            label2 = label + '__'
            for key in self.user_panels:
                if key.startswith(label2):
                    del self.user_panels[key]
                    break
        self.bar.remove_page(page)

