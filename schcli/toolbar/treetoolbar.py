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
from wx.lib.agw import customtreectrl as CT
from wx.lib.agw.ribbon import art

from schcli.guilib.events import *
from schcli.toolbar.basetoolbar import BaseHtmlPanel, ToolbarBar, ToolbarPage, ToolbarPanel, ToolbarButton

_ = wx.GetTranslation


def _tree_list(tree, parent_item, list = None):
    if list == None:
        list2 = []
    else:
        list2 = list

    item, cookie = tree.GetFirstChild(parent_item)
    while item and item.IsOk():
        list2.append(item)
        if tree.ItemHasChildren(item):
            _tree_list(tree, item, list2)
        item, cookie = tree.GetNextChild(parent_item, cookie)

    return list2


class TreeHtmlPanel(BaseHtmlPanel):
    def get_width(self):
        return self.page.parent_bar.get_bar_width()

    def get_height(self):
        return self.page.parent_bar.get_bar_height()

    def set_page(self, html_page):
        super().set_page(html_page)
        #self.page.parent_bar.update()
        #self.page.parent_bar.SetActivePage(self.page)


class TreeToolbarButton(ToolbarButton):
    def __init__(self, parent_panel, id, title, bitmap, bitmap_disabled = None, kind=ToolbarButton.TYPE_SIMPLE):
        ToolbarButton.__init__(self, parent_panel, id, title, bitmap, bitmap_disabled, kind)


class TreeToolbarPanel(ToolbarPanel):
    def __init__(self, parent_page, title, kind=ToolbarPanel.TYPE_PANEL_TOOLBAR):
        ToolbarPanel.__init__(self, parent_page, title, kind)
        bar =  self.parent_page.parent_bar
        self.tree_item = bar.append_to_tree(parent_page.tree_item, title)

    def _append(self, b):
        item = None
        if self.kind in (ToolbarPanel.TYPE_PANEL_TOOLBAR, ToolbarPanel.TYPE_PANEL_BUTTONBAR):
            if b.kind == ToolbarButton.TYPE_SIMPLE:
                item = self.parent_page.parent_bar.append_to_tree(self.tree_item, b.title, b.bitmap, ct_type=0)
            elif b.kind == ToolbarButton.TYPE_DROPDOWN:
                item = self.parent_page.parent_bar.append_to_tree(self.tree_item, b.title, b.bitmap, ct_type=0)
            elif b.kind == ToolbarButton.TYPE_HYBRID:
                item = self.parent_page.parent_bar.append_to_tree(self.tree_item, b.title, b.bitmap, ct_type=0)
            elif b.kind == ToolbarButton.TYPE_TOOGLE:
                item = self.parent_page.parent_bar.append_to_tree(self.tree_item, b.title, b.bitmap, ct_type=1)
            elif b.kind == ToolbarButton.TYPE_PANEL:
                pass
            elif b.kind == ToolbarButton.TYPE_SEPARATOR:
                item = self.parent_page.parent_bar.AppendSeparator(self.tree_item)

        if item:
            self.parent_page.parent_bar.SetItemHyperText(item, True)
            self.parent_page.parent_bar.SetPyData(item, b.id)

    def create_button(self, id, title, bitmap=None, bitmap_disabled=None, kind=ToolbarButton.TYPE_SIMPLE):
        b = TreeToolbarButton(self, id, title, bitmap, bitmap_disabled, kind)
        self._append(b)
        return b

    def add_separator(self):
        b = TreeToolbarButton(self, 0, '', None, None, kind=ToolbarButton.TYPE_SEPARATOR)
        self._append(b)
        return b


class TreeToolbarPage(ToolbarPage):
    def __init__(self, parent_bar, title, kind=ToolbarPage.TYPE_PAGE_NORMAL):
        ToolbarPage.__init__(self, parent_bar, title, kind)
        self.tree_item = parent_bar.append_to_tree(parent_bar.tree_main_page, title)

    def create_panel(self, title, kind=ToolbarPanel.TYPE_PANEL_TOOLBAR):
        return TreeToolbarPanel(self, title, kind)

    def create_html_panel(self, title):
        p = wx.Panel(self.parent_bar, size=wx.Size(200,200))
        self.parent_bar.AppendItem(self.tree_item, title, 0, p)
        self.parent_bar.Expand(self.tree_item)
        return TreeHtmlPanel(self, p)


class TreeToolbarBar(ToolbarBar, CT.CustomTreeCtrl):
    def __init__(self, parent, gui_style):
        agwStyle =  CT.TR_HIDE_ROOT | CT.TR_HAS_BUTTONS | CT.TR_HAS_VARIABLE_ROW_HEIGHT | CT.TR_NO_LINES
        CT.CustomTreeCtrl.__init__(self, parent, agwStyle=agwStyle)

        self._indent = 8
        self.tree_main_page = self.AddRoot('The Root Item')
        self.images = wx.ImageList(32, 32)
        self.image_id = 0
        self.show_titles = True

        c2 = wx.SystemSettings.GetColour(wx.SYS_COLOUR_MENU)
        m = 1.0
        x1 = (int(c2.Red() * m) + 255) / 2
        x2 = (int(c2.Green() * m) + 255) / 2
        x3 = (int(c2.Blue() * m) + 255) / 2
        c = wx.Colour(x1, x2, x3)
        self.bg = c
        self.SetBackgroundColour(c)
        c3 = wx.Colour(0, 0, 0)
        self._hypertextnewcolour = c3
        self._hypertextvisitedcolour = c3

        ToolbarBar.__init__(self, parent, gui_style)
        self.EnableSelectionVista(True)

        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.Bind(CT.EVT_TREE_ITEM_HYPERLINK, self.on_hyper_link)

        wx.GetApp().GetTopWindow().idle_objects.append(self)


    def append_to_tree(self, parent_elem, title, bitmap=None, ct_type=0):
        if bitmap is not None and bitmap.IsOk():
            if bitmap.GetWidth() < 32 or bitmap.GetHeight() < 32:
                b = wx.BitmapFromImage(bitmap.ConvertToImage().Rescale(32, 32))
            else:
                b = bitmap
            self.images.Add(b)
            item = self.AppendItem(parent_elem, title if self.show_titles else '', image=self.image_id, ct_type=ct_type)
            self.image_id += 1
        else:
            item = self.AppendItem(parent_elem, title if self.show_titles else '', ct_type=ct_type)
        return item


    def create_page(self, title, kind=ToolbarPage.TYPE_PAGE_NORMAL):
        return TreeToolbarPage(self, title, kind)

    def CanAcceptFocus(self):
        return True

    def CanAcceptFocusFromKeyboard(self):
        return self.CanAcceptFocus()

    def on_close(self, event):
        if self in wx.GetApp().GetTopWindow().idle_objects:
            del wx.GetApp().GetTopWindow().idle_objects[self]
        event.Skip()

    def get_max_width(self, respect_expansion_state=True):
        return 400

    def realize(self):
        self.AssignImageList(self.images)
        self.ExpandAll()
        self.SetSize((300, 400))
        x = self.GetMaxWidth()

    def on_hyper_link(self, event):
        wx.Event.EventType
        item = event.GetItem()
        if item: wx.CallAfter(self.send_menu_event, item)

    def send_menu_event(self, item):
        e = wx.CommandEvent(wx.EVT_MENU.typeId, self.GetPyData(item))
        ret = self.ProcessEvent(e)
        if not ret:
            win = wx.GetApp().GetTopWindow().get_active_ctrl()
            if win and issubclass(type(win), SchBaseCtrl):
                win.ProcessEvent(e)

    def on_idle(self):
        refresh = False
        for item in _tree_list(self, self.tree_main_page):
            id = self.GetPyData(item)
            if id:
                if (id >= ID_START and id < ID_END) or (id >= wx.ID_LOWEST and id < wx.ID_HIGHEST ):
                    event = wx.UpdateUIEvent(id)
                    event.Enable(False)
                    event.SetEventObject(self.GetParent())

                    if self.ProcessWindowEvent(event):
                        if item.IsEnabled() != event.GetEnabled():
                            refresh = True
                        item.Enable(event.GetEnabled())
                    else:
                        enable = False
                        win = wx.Window.FindFocus()
                        if win and issubclass(type(win), SchBaseCtrl):
                            if  win.ProcessEvent(event):
                                if event.GetEnabled():
                                    enable = True
                        if enable:
                            if not item.IsEnabled():
                                refresh = True
                            item.Enable(True)
                        else:
                            if item.IsEnabled():
                                refresh = True
                            item.Enable(False)
        if refresh:
            self.Refresh()

    def set_active_page(self, page):
        pass

    def get_bar_height(self):
        return 600

    def get_bar_width(self):
        return 150

    def remove_page(self, title):
        for p in self.pages:
            if p.title == title:
                self.Delete(p.tree_item)
                break
        super().remove_page(title)

    def create(self):
        self.AssignImageList(self.images)
        self.ExpandAll()
        self.SetSize((300, 400))
        x = self.GetMaxWidth()

    def close(self):
        self.Close()

    def update(self):
        size = self.GetSize()
        self.SetSize(wx.Size(size.GetWidth() - 1, size.GetHeight()))
        self.SetSize(wx.Size(size.GetWidth(), size.GetHeight()))

    def bind_ui(self, fun, id=wx.ID_ANY):
        self.parent.Bind(wx.EVT_UPDATE_UI, fun, id=id)

    def bind(self, fun, id=wx.ID_ANY, e=None):
        if e:
            self.parent.Bind(e, fun, id=id)
        else:
            self.parent.Bind(wx.EVT_MENU, fun, id=id)

    def bind_dropdown(self, fun, id):
        self.parent.Bind(wx.EVT_MENU, fun, id=id)

    def un_bind(self, id, e=None):
        if e:
            self.Unbind(e, id=id)
        else:
            self.Unbind(wx.EVT_MENU, id=id)

