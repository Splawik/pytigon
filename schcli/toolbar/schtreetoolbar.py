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
import sys

from wx.lib.agw import customtreectrl as CT
from schcli.guilib.schevent import *
from schcli.toolbar.basetoolbar import ToolbarInterface, TYPE_TOOLBAR, \
    TYPE_BUTTONBAR, TYPE_PANELBAR
from schcli.guilib.schevent import *
from schcli.guictrl.schbasectrl import SchBaseCtrl

_ = wx.GetTranslation

class TreePanel(wx.Panel):

    def __init__(self, tree, size):
        wx.Panel.__init__(self, tree, size=size)
        self.item = None

    def set_item(self, item):
        self.item = item

    def get_panel(self):
        return self.item

    def new_child_page(
        self,
        address_or_parser,
        title='',
        param=None,
        ):
        return wx.GetApp().GetTopWindow().new_main_page(address_or_parser, title,
                param)


class TreeGroup(object):

    def __init__(self, tree, elem):
        self.tree = tree
        self.group_root_elem = elem


class TreeInterface(ToolbarInterface):

    class Page(object):

        class Panel(object):

            def __init__(
                self,
                page_interface,
                title,
                type=TYPE_TOOLBAR,
                ):
                self.page_interface = page_interface
                self.page = page_interface.page
                self.label = title
                if title:
                    if type == TYPE_PANELBAR:
                        self.panel = TreePanel(self.page.tree, size=(10, 200))
                        child = \
                            self.page.tree.AppendItem(self.page.group_root_elem,
                                '', wnd=self.panel)
                        self.panel.set_item(self)
                        self.page.tree.Expand(self.page.group_root_elem)
                    else:
                        child = \
                            self.page.tree.AppendItem(self.page.group_root_elem,
                                title)
                    self.child_page = TreeGroup(self.page.tree, child)
                else:
                    self.child_page = self.page

            def get_parent(self):
                return self.page.tree

            def get_label(self):
                return self.page_interface.title

            def append(
                self,
                id,
                title,
                bitmap=None,
                ):
                if bitmap != None:
                    item = \
                        self.page.tree.append(self.child_page.group_root_elem,
                            title, bitmap)
                else:
                    item = \
                        self.page.tree.append_item(self.child_page.group_root_elem,
                            title)
                self.page.tree.SetItemHyperText(item, True)
                self.page.tree.SetPyData(item, id)

            def add_tool(
                self,
                id,
                title,
                bitmaps,
                ):
                self.append(id, title, bitmaps[0])

            def add_hybrid_tool(
                self,
                id,
                title,
                bitmaps,
                ):
                self.append(id, title, bitmaps[0])

            def add_button(
                self,
                id,
                title,
                bitmaps,
                ):
                self.append(id, title, bitmaps[0])

            def add_panel(self, controls):
                s = wx.BoxSizer(wx.VERTICAL)
                for c in controls:
                    s.Add(c, 0, wx.LEFT | wx.TOP | wx.EXPAND | wx.RIGHT, 2)
                self.panel.SetSizer(s)
                minsize = self.panel.GetSize()
                self.panel.SetMinSize(wx.Size(minsize.width, minsize.height))

            def add_separator(self):
                pass

            def bind(self, *argi, **argv):
                pass

        def __init__(self, bar, title):
            self.bar = bar
            self.title = title
            child = self.bar.bar.AppendItem(self.bar.bar.main_page, title)
            self.page = TreeGroup(self.bar.bar, child)
            self.panels = {}

        def create_panel(self, title, type=TYPE_TOOLBAR):
            if title in self.panels:
                panel = self.panels[title]
                panel.AddSeparator()
                return panel
            else:
                if title == self.title:
                    panel = self.Panel(self, None, type)
                else:
                    panel = self.Panel(self, title, type)
                self.panels[title] = panel
                return panel

    def __init__(self, parent, gui_style):
        self.bar = SchTreeBar(parent, wx.ID_ANY)
        self.pages = {}
        ToolbarInterface.__init__(self, parent, gui_style)
        self.toolbars = None

    def create_page(self, title):
        if title in self.pages:
            page = self.pages[title]
        else:
            if title == 'main':
                page = self.Page(self, _('Tools main'))
            else:
                page = self.Page(self, title)
            self.pages[title] = page
        if not self.main_page:
            self.main_page = page
        return page

    def bind(
        self,
        fun,
        id=wx.ID_ANY,
        e=None,
        ):
        if e:
            self.parent.Bind(e, fun, id=id)
        else:
            self.parent.Bind(wx.EVT_MENU, fun, id=id)


    def un_bind(self, id, e=None):
        if e:
            self.parent.Unbind(e, id=id)
        else:
            self.parent.Unbind(wx.EVT_MENU, id=id)

    def update_bar(self, obj):
        pass

    def realize_bar(self):
        self.bar.realize()

    def get_toolbars(self):
        return self.toolbars

    def get_bar(self):
        return self.bar

    def connect_object_to_panel(self, panel, object):
        return self.standard_buttons.connect_object_to_panel(panel, object)

    def Bind(
        self,
        fun,
        id,
        e=None,
        ):
        if e:
            self.bar.Bind(e, fun, id=id)
        else:
            self.bar.Bind(wx.EVT_MENU, fun, id=id)
        pass


def _tree_generator(tree, parent_item):
    item, cookie = tree.GetFirstChild(parent_item)
    while item and item.IsOk():
        yield item
        if tree.ItemHasChildren(item):
            _tree_generator(tree, item)
        item, cookie = tree.GetNextChild(parent_item, cookie)


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

class SchTreeBar(CT.CustomTreeCtrl):

    def __init__(self, *argi, **argv):
        argv['agwStyle'] = CT.TR_HIDE_ROOT | CT.TR_HAS_BUTTONS\
             | CT.TR_HAS_VARIABLE_ROW_HEIGHT | CT.TR_NO_LINES
        CT.CustomTreeCtrl.__init__(self, *argi, **argv)
        self._indent = 8
        self.main_page = self.AddRoot('The Root Item')
        self.images = wx.ImageList(32, 32)
        self.image_id = 0
        self.show_titles = True
        self.Bind(CT.EVT_TREE_ITEM_HYPERLINK, self.on_hyper_link)
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
        self.EnableSelectionVista(True)
        #self.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)
        self.Bind(wx.EVT_CLOSE, self.on_close)
        wx.GetApp().GetTopWindow().idle_objects.append(self)


    def on_command(self, event):
        event.Skip()

    def on_close(self, event):
        if self in wx.GetApp().GetTopWindow().idle_objects:
            del wx.GetApp().GetTopWindow().idle_objects[self]
        event.Skip()


    #def on_left_down(self, event):
    #    point = event.GetPosition()
    #    (item, flag) = self.HitTest(point)
    #    if item and flag & CT.TREE_HITTEST_ONITEM != 0:
    #        if item.IsExpanded():
    #            self.Collapse(item)
    #        else:
    #            self.Expand(item)
    #    event.Skip()

    def append(
        self,
        elem,
        title,
        bitmap=None,
        ):
        if bitmap != None and bitmap.IsOk():
            if bitmap.GetWidth() < 32 or bitmap.GetHeight() < 32:
                b = wx.BitmapFromImage(bitmap.ConvertToImage().Rescale(32, 32))
            else:
                b = bitmap
            self.images.Add(b)
            item = self.AppendItem(elem, title if self.show_titles else '',
                                   image=self.image_id)
            self.image_id += 1
        else:
            item = self.AppendItem(elem, title if self.show_titles else '')
        item.Attr().SetBackgroundColour(self.bg)
        item.Attr().SetBorderColour(self.bg)
        return item

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
        for item in _tree_list(self, self.main_page):
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

    def remove_page(self, page):
        self.Delete(page.page_interface.page.group_root_elem)
        if page.label in page.page_interface.panels:
            del page.page_interface.panels[page.label]
        if page.GetLabel() in page.page_interface.bar.pages:
            del page.page_interface.bar.pages[page.GetLabel()]


