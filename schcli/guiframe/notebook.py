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
SchNotebook object used as a top window in panels: 'desktop', 'panel', 'header' and 'footer'
"""

import wx
import wx.lib.agw.aui as aui
from wx.lib.agw.aui import framemanager
from schlib.schtools.wiki import wiki_from_str
from schcli.guiframe.manager import SChAuiBaseManager
from wx.lib.agw.aui.aui_constants import *


class SchNotebook(aui.AuiNotebook):
    """SchNotebook class"""

    def __init__(self, parent, pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.BORDER_NONE|wx.TAB_TRAVERSAL|wx.WANTS_CHARS):
        """Constructor

        Args:
            parent: parent window
            pos: position of window
            size: size of window
            style: see wx.Window style
        """
        self._curpage = -1
        self._tab_id_counter = AuiBaseTabCtrlId
        self._dummy_wnd = None
        self._hide_tabs = False
        self._sash_dclick_unsplit = False
        self._tab_ctrl_height = 20
        self._requested_bmp_size = wx.Size(-1, -1)
        self._requested_tabctrl_height = -1
        self._textCtrl = None
        self._tabBounds = (-1, -1)

        self.panel = None
        self.active = False
        self.closing = False
        self.last_active = None

        wx.Panel.__init__(self, parent, wx.ID_ANY, pos, size, style, name="SchNotebook")
        self._mgr = SChAuiBaseManager()

        self._tabs = aui.AuiTabContainer(self)
        self.InitNotebook(AUI_NB_DEFAULT_STYLE)

        self.Bind(aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.on_closing)
        self.Bind(aui.EVT_AUINOTEBOOK_TAB_DCLICK, self.on_dclick)
        self.Bind(aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.on_changed)
        self.Bind(aui.EVT_AUINOTEBOOK_PAGE_CHANGING, self.on_changing)
        self.Bind(wx.EVT_NAVIGATION_KEY, self.on_navigete)

        self.SetWindowStyleFlag(wx.WANTS_CHARS)
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BACKGROUND))


    def on_closing(self, event):
        idn = event.GetSelection()
        if idn >= 0:
            page = self.GetPage(idn)
            self.closing = True
            if page.close_no_del(True):
                self.GetParent().GetParent().after_close(self)
                event.Veto()

    def on_changed(self, event):
        sel = event.GetSelection()
        old_sel = event.GetOldSelection()
        if old_sel >= 0:
            self.GetPage(old_sel).Refresh()
        if sel >= 0:
            self.GetPage(sel).Refresh()
            self.activate_page(self.GetPage(sel))
        event.Skip()

    def on_changing(self, event):
        if self.closing:
            self.closing = False
            sel = event.GetSelection()
            oldsel = event.GetOldSelection()
            if oldsel == -1:
                new_page = self.GetPage(sel)
                tab = self.FindTab(new_page)[0]
                if tab:
                    count = tab.GetPageCount()
                    if count > 0:
                        new_sel = count - 1
                        if new_sel > sel:
                            self.SetSelection(new_sel)
                            event.Veto()
                            return
        event.Skip()

    def DeletePage(self, sel):
        page = self.GetPage(sel)
        if page == self.last_active:
            self.last_active = None

        def _close():
            self.panel.Hide()
            wx.GetApp().GetTopWindow()._mgr.Update()
            for pane_name in ["desktop", "panel", "menu", "header", "footer"]:
                pane_info = wx.GetApp().GetTopWindow()._mgr.GetPane(pane_name)
                if pane_info.IsOk() and pane_info.IsShown():
                    pane_info.window.SetFocus()

        if len(self._tabs._pages)==1:
            wx.CallAfter(_close)

        return aui.AuiNotebook.DeletePage(self, sel)

    def on_dclick(self, event):
        try:
            txt = self.GetPageText(event.GetSelection())
            mp, adr = wx.GetApp().read_html(self, '/schwiki/help/' + wiki_from_str(txt) + '/view/', None)
            if not txt.startswith('?'):
                wiki = wiki_from_str(txt)
                wx.GetApp().GetTopWindow().new_main_page(mp, '?: ' + wiki, panel='desktop2')
        except:
            pass

    def SetPanel(self, panel):
        self.panel = panel

    def GetPanel(self):
        return self.panel

    def set_active(self, active):
        self.active = active
        if active:
            w = self.GetCurrentPage()
            self.activate_page(w)
            self.GetParent().GetParent().SetActive(self, w)

    def activate_page(self, page):
        if self.last_active:
            self.last_active.deactivate_page()
        self.last_active = page
        if page:
            page.activate_page()

    def add_and_split(self, page, title, direction):
        """Add page to the notebook and split notebook window

        Args:
            page - page to be added
            title - title of new tab
            direction - split direction: wx.LEFT, wx.TOP, wx.RIGHT, wx.Bottom
        """
        self.closing = False
        if self.GetPageCount() < 1:
            return
        cli_size = self.GetClientSize()
        if self.GetPageCount() > 2:
            split_size = self.CalculateNewSplitSize()
        else:
            split_size = self.GetClientSize()
            split_size.x /= 2
            split_size.y /= 2
        new_tabs = aui.TabFrame(self)
        new_tabs.SetTabCtrlHeight(self._tab_ctrl_height)
        self._tab_id_counter += 1
        new_tabs._tabs = aui.AuiTabCtrl(self, self._tab_id_counter)
        new_tabs._tabs.SetArtProvider(self._tabs.GetArtProvider().Clone())
        new_tabs._tabs.SetAGWFlags(self._agwFlags)
        dest_tabs = new_tabs._tabs
        pane_info = framemanager.AuiPaneInfo().CaptionVisible(False).BestSize(split_size.GetWidth(), split_size.GetHeight())
        if direction == wx.LEFT:
            pane_info.Left()
            mouse_pt = wx.Point(0, cli_size.y / 2)
        elif direction == wx.RIGHT:
            pane_info.Right()
            mouse_pt = wx.Point(cli_size.x, cli_size.y / 2)
        elif direction == wx.TOP:
            pane_info.Top()
            mouse_pt = wx.Point(cli_size.x / 2, 0)
        elif direction == wx.BOTTOM:
            pane_info.Bottom()
            mouse_pt = wx.Point(cli_size.x / 2, cli_size.y)
        #self._mgr.AddPane(new_tabs, pane_info, mouse_pt)
        #self._mgr.Update()
        page_info = aui.AuiNotebookPage()
        page_info.window = page
        page_info.caption = title
        page_info.active = False
        page_info.control = None
        idn = self.GetPageCount()
        self._tabs.InsertPage(page, page_info, idn)
        dest_tabs.AddPage(page, page_info)
        self.SetPageTextColour(idn, wx.Colour(0, 96, 0))
        page.Reparent(self)
        self.DoSizing()
        dest_tabs.Refresh()
        #self.SetSelectionToPage(page_info)
        self.UpdateHintWindowSize()

        self._mgr.AddPane(new_tabs, pane_info, mouse_pt)
        self._mgr.Update()


    def on_navigete(self, evt):
        forward = evt.GetDirection()
        self.activate_page(self.GetCurrentPage())
        evt.Skip()

    def Freeze(self):
        pass

    def Thaw(self):
        pass
