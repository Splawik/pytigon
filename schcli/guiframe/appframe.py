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
This module contains SchAppFrame class. When pytigon application starts, new top frame window (class SchAppFrame) is created.
During the initialisation process all defined for application plugins are started.
"""

import os
import sys
import platform
from tempfile import NamedTemporaryFile
from pydispatch import dispatcher

import wx
import wx.html2
import datetime
from wx.lib.agw import aui

from schlib.schfs.vfstools import get_temp_filename
from schlib.schtools.cc import compile
from schlib.schtools.tools import split2
from schlib.schtasks.task import get_process_manager

from schcli.guilib.image import ArtProviderFromIcon
from schcli.guilib.events import * #@UnusedWildImport
from schcli.guiframe.notebook import SchNotebook
from schcli.guiframe.notebookpage import SchNotebookPage
from schcli.guiframe.manager import SChAuiManager
from schcli.guilib.image import bitmap_from_href

from schcli.guiframe.baseframe import SchBaseFrame

_ = wx.GetTranslation


class _SChMainPanel(wx.Window):
    def __init__(self, app_frame, *argi, **argv):
        argv['name'] = 'schmainpanel'
        if 'style' in argv:
            argv['style'] |= wx.WANTS_CHARS
        self.app_frame = app_frame
        wx.Window.__init__(self, *argi, **argv)
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BACKGROUND))

    def GetFrameManager(self):
        return self.GetParent().GetFrameManager()

    def GetMenuBar(self):
        return self.GetParent().GetMenuBar()

    def Freeze(self):
        pass

    def Thaw(self):
        pass


class SchAppFrame(SchBaseFrame):
    """
        This is main window of pytigon application
    """

    def __init__(self, gui_style="tree(toolbar,statusbar)", title="", pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.DEFAULT_FRAME_STYLE | wx.CLIP_CHILDREN | wx.WANTS_CHARS,):
        """Constructor

        Args:
            gui_style - there is string with some key words. If specyfied key word exist some functionality of
            SChAppFrame are turned on.

            List of key words:

                dialog - application with one form

                one_form - some as dialog

                tray - application have system tray icon with some actions

                statusbar - show the status bar

                tree - menu in tree form

                standard - standard for platform interface

                modern - replace standard toolbar with ribbon bar

                toolbar - show the tool bar

            title - the window title

            pos - the window position

            size - the window size

            style - see wx.Frame constructor
        """

        SchBaseFrame.__init__(self, None, gui_style, wx.ID_ANY, title, pos, size, style, "MainWindow")
        #self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BACKGROUND))

        self._id = wx.ID_HIGHEST
        self._perspectives = []
        self._menu_bar_lp = 0
        self._toolbar_bar_lp = 1
        self._proc_mannager = None

        self.gui_style = gui_style
        self.idle_objects = []
        self.gui_style = gui_style
        self.command = {}
        #self.command_enabled_always = []
        self.last_pane = None
        self.active_pane = None
        self.active_page = None
        self.active_child_ctrl = None

        self.toolbar_interface = None
        self.menubar_interface = None
        self.statusbar_interface = None

        self.destroy_fun_tab = []
        self.after_init = False

        self.sys_command = dict({"EXIT": self.on_exit, "ABOUT": self.on_about})

        if 'dialog' in self.gui_style or 'one_form' in self.gui_style:
            hide_on_single_page = True
        else:
            hide_on_single_page = False

        self._panel = _SChMainPanel(self, self)
        self._mgr = SChAuiManager()
        self._mgr.SetManagedWindow(self._panel)

        if not hasattr(self._mgr, 'SetAGWFlags'):
            self._mgr.SetAGWFlags = self._mgr.SetFlags
            self._mgr.GetAGWFlags = self._mgr.GetFlags

        self._mgr.SetAGWFlags(self._mgr.GetAGWFlags() ^ aui.AUI_MGR_ALLOW_ACTIVE_PANE)

        self.desktop = self._create_notebook_ctrl(hide_on_single_page)
        self.get_dock_art().SetMetric(aui.AUI_DOCKART_PANE_BORDER_SIZE, 0)

        wx.ArtProvider.Push(ArtProviderFromIcon())

        icon = wx.Icon()
        b = wx.Bitmap(wx.Image(wx.GetApp().scr_path + '/schappdata/media/schweb.png'))
        icon.CopyFromBitmap(b)
        self.SetIcon(icon)

        if 'tray' in gui_style:
            self.tbIcon = wx.adv.TaskBarIcon()
            self.tbIcon.SetIcon(icon, "Pytigon")
        else:
            self.tbIcon = None

        if 'statusbar' in gui_style:
            self.statusbar = self._create_status_bar()
        else:
            self.statusbar = None

        wx.GetApp().SetTopWindow(self)

        self.setup_frame()

        if 'tree' in gui_style:
            self._sizer = wx.BoxSizer(wx.HORIZONTAL)
        else:
            self._sizer = wx.BoxSizer(wx.VERTICAL)

        if 'standard' in gui_style:
            if len(wx.GetApp().get_tab(self._toolbar_bar_lp))>1:
                from schcli.toolbar import standardtoolbar
                self.toolbar_interface = standardtoolbar.StandardToolbarBar(self, gui_style)
                self._create_tool_bar()
                self.toolbar_interface.create()
            self._sizer.Add(self._panel, 1, wx.EXPAND)
            self._mgr.Update()
        elif 'generic' in gui_style:
            if len(wx.GetApp().get_tab(self._toolbar_bar_lp))>1:
                from schcli.toolbar import generictoolbar
                self.toolbar_interface = generictoolbar.GenericToolbarBar(self, gui_style)
                self._create_tool_bar()
                self.toolbar_interface.create()
            self._sizer.Add(self._panel, 1, wx.EXPAND)
            self._mgr.Update()
        elif 'modern' in gui_style:
            from schcli.toolbar.moderntoolbar import ModernToolbarBar
            self.toolbar_interface = ModernToolbarBar(self, gui_style)
            self._create_tool_bar()
            #self.toolbar_interface.realize_bar()
            self.toolbar_interface.create()
            self._sizer.Add(self.toolbar_interface, 0, wx.EXPAND)
            self._sizer.Add(self._panel, 1, wx.EXPAND)
        elif 'tree' in gui_style:
            from schcli.toolbar.treetoolbar import TreeToolbarBar
            self.toolbar_interface = TreeToolbarBar(self._panel, gui_style)
            self._create_tool_bar()
            self.toolbar_interface.create()
            self._mgr.AddPane(self.toolbar_interface, self._create_pane_info("menu", _("Menu")).CaptionVisible(True).MinimizeButton(True).CloseButton(False).Left().BestSize((250, 40)).MinSize((250, 40)).Show())
            self._sizer.Add(self._panel, 1, wx.EXPAND)
        else:
            self._sizer.Add(self._panel, 1, wx.EXPAND)

        self.SetSizer(self._sizer)

        if len(wx.GetApp().get_tab(2))>1:
            self._menu_bar_lp = 2
        else:
            if wx.GetApp().menu_always:
                self._menu_bar_lp = 1

        if self._menu_bar_lp>0:
            from schcli.toolbar import menubar
            self.menubar_interface = menubar.MenuToolbarBar(self, gui_style)
            self._create_menu_bar()


        s_dx = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_X)
        s_dy = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_Y)

        self._mgr.AddPane(self._create_notebook_ctrl(), self._create_pane_info("panel", _("Tools")).CaptionVisible(True).
            Left().MinSize((400, s_dy / 2)).BestSize((s_dx / 2 - 50, s_dy - 100)).Show())
        self._mgr.AddPane(self._create_notebook_ctrl(), self._create_pane_info("header", _("Header")).CaptionVisible(False).
            Top().MinSize((s_dx, s_dy / 10)).BestSize((s_dx, s_dy/5)).Show())
        self._mgr.AddPane(self._create_notebook_ctrl(), self._create_pane_info("footer", _("Footer")).CaptionVisible(False).
            Bottom().MinSize((s_dx, s_dy / 10)).BestSize((s_dx, s_dy/5)).Show())
        self._mgr.AddPane(self.desktop, self._create_pane_info("desktop", _("Desktop")).CenterPane().Show())
        perspective_notoolbar = self._mgr.SavePerspective()

        if 'toolbar' in gui_style and 'standard' in gui_style:
            i = 1
            while(True):
                name = "tb" + str(i)
                tbpanel = self._mgr.GetPane(name)
                if tbpanel.IsOk():
                    tbpanel.Show()
                else:
                    break
                i += 1

        perspective_all = self._mgr.SavePerspective()
        all_panes = self._mgr.GetAllPanes()

        for ii in range(len(all_panes)):
            if not all_panes[ii].IsToolbar():
                if all_panes[ii].name != 'menu':
                    all_panes[ii].Hide()

        self._mgr.GetPane("desktop").Show()

        perspective_default = self._mgr.SavePerspective()

        size = self.desktop.GetPageCount()
        for i in range(size): #@UnusedVariable
            self.desktop.DeletePage(0)

        self._perspectives.append(perspective_default)
        self._perspectives.append(perspective_all)
        self._perspectives.append(perspective_notoolbar)

        self.init_acc_keys()
        self.init_plugins()
        self.SetAcceleratorTable(wx.AcceleratorTable(self.aTable))

        self._mgr.Update()

        self.t1 = wx.Timer(self)
        self.t1.Start(250)

        self.Bind(wx.EVT_TIMER, self.on_timer, self.t1)
        self.Bind(aui.EVT_AUI_PANE_ACTIVATED, self.on_pane_activated)
        self.Bind(wx.EVT_IDLE, self.on_idle)
        self.Bind(wx.EVT_MENU_RANGE, self.on_show_elem, id=ID_SHOWHEADER, id2=ID_SHOWTOOLBAR2)

        if 'tray' in gui_style:
            self.Bind(wx.EVT_CLOSE, self.on_taskbar_hide)
        else:
            self.Bind(wx.EVT_CLOSE, self.on_close)

        self._panel.Bind(wx.EVT_CHILD_FOCUS, self.on_child_focus)

        self.bind_command(self.on_open, id=wx.ID_OPEN)
        self.bind_command(self.on_exit, id=wx.ID_EXIT)

        #if self.toolbar_interface:
            #self.toolbar_interface.bind_ui(self.on_update_ui_command, wx.ID_ANY)

            #for pos in [wx.ID_EXIT, ID_WEB_NEW_WINDOW, wx.ID_OPEN]:
            #    self.command_enabled_always.append(pos)

        self.bind_command(self.on_next_tab, id=ID_NEXTTAB)
        self.bind_command(self.on_prev_tab, id=ID_PREVTAB)
        self.bind_command(self.on_next_page, id=ID_NEXTPAGE)
        self.bind_command(self.on_prev_page, id=ID_PREVPAGE)
        self.bind_command(self.on_close_tab, id=ID_CLOSETAB)
        self.bind_command(self.on_refresh_tab, id=ID_REFRESHTAB)

        self.bind_command(self.on_goto_desktop, id=ID_GOTODESKTOP)
        self.bind_command(self.on_goto_head, id=ID_GOTOHEADER)
        self.bind_command(self.on_goto_panel, id=ID_GOTOPANEL)
        self.bind_command(self.on_goto_footer, id=ID_GOTOFOOTER)

        self.bind_command(self.on_command, id=ID_WEB_NEW_WINDOW)

        self.bind_command(self.on_show_status_bar, id=ID_SHOWSTATUSBAR)

        if self.menubar_interface:
            self.SetMenuBar(self.menubar_interface)

        if self.tbIcon:
            wx.adv.EVT_TASKBAR_LEFT_DCLICK(self.tbIcon, self.on_taskbar_toogle)
            wx.adv.EVT_TASKBAR_RIGHT_UP(self.tbIcon, self.on_taskbar_show_menu)

            self.menu_tray = wx.Menu()
            self.menu_tray.Append(ID_TASKBAR_SHOW, _('Show It'))
            wx.EVT_MENU(self, ID_TASKBAR_SHOW, self.on_taskbar_show)
            self.menu_tray.Append(ID_TASKBAR_HIDE, _('Minimize It'))
            wx.EVT_MENU(self, ID_TASKBAR_HIDE, self.on_taskbar_hide)
            self.menu_tray.AppendSeparator()
            self.menu_tray.Append(ID_TASKBAR_CLOSE, _('Close It'))
            wx.EVT_MENU(self, ID_TASKBAR_CLOSE, self.on_close)

        self.SetExtraStyle(wx.WS_EX_PROCESS_UI_UPDATES)
        wx.UpdateUIEvent.SetUpdateInterval(50)
        wx.UpdateUIEvent.SetMode(wx.UPDATE_UI_PROCESS_SPECIFIED)
        wx.CallAfter(self.UpdateWindowUI)
        self.Layout()


    def setup_frame(self):
        self.SetMinSize(wx.Size(800, 700))


    def init_acc_keys(self):
        self.aTable = [
            (wx.ACCEL_ALT, wx.WXK_PAGEUP, ID_PREVTAB),
            (wx.ACCEL_ALT, wx.WXK_PAGEDOWN, ID_NEXTTAB),

            (wx.ACCEL_ALT, wx.WXK_LEFT, ID_GOTOPANEL),
            (wx.ACCEL_ALT, ord('t'), ID_GOTOPANEL),
            (wx.ACCEL_ALT, wx.WXK_RIGHT, ID_GOTODESKTOP),
            (wx.ACCEL_ALT, ord('d'), ID_GOTODESKTOP),
            (wx.ACCEL_ALT, wx.WXK_UP, ID_GOTOHEADER),
            (wx.ACCEL_CTRL, ord('w'), ID_CLOSETAB),
            (wx.ACCEL_CTRL, ord('n'), ID_WEB_NEW_WINDOW),
            (wx.ACCEL_CTRL, wx.WXK_TAB, ID_NEXTTAB),
            (wx.ACCEL_CTRL | wx.ACCEL_SHIFT, wx.WXK_TAB, ID_PREVTAB),
            (wx.ACCEL_CTRL, wx.WXK_F6, ID_NEXTTAB),
            (wx.ACCEL_CTRL | wx.ACCEL_SHIFT, wx.WXK_F6, ID_PREVTAB),
            (wx.ACCEL_ALT, ord('h'), ID_PREVTAB),
            (wx.ACCEL_ALT, ord('l'), ID_NEXTTAB),
            (wx.ACCEL_ALT, ord('k'), ID_PREVPAGE),
            (wx.ACCEL_ALT, ord('j'), ID_NEXTPAGE),
            (wx.ACCEL_ALT, wx.WXK_BACK, ID_WEB_BACK),
            (0, wx.WXK_F5, ID_REFRESHTAB)]

    def on_idle(self, event):
        for obj in self.idle_objects:
            obj.on_idle()

        if not self.after_init:
            self.after_init = True
            app = wx.GetApp()
            if len(app.start_pages) > 0:
                def start_pages():
                    for page in app.start_pages:
                        url_page = page.split(';')
                        if len(url_page) == 2:
                            self._on_html(_(url_page[0]) + ',' + app.base_address + url_page[1])
                wx.CallAfter(start_pages)

        event.Skip()


    def on_pane_activated(self, event):
        active_pane = event.GetPane()

        if self.active_pane != active_pane:
            if self.active_pane and hasattr(self.active_pane, 'set_active'):
                self.active_pane.set_active(False)
                if self.active_pane.GetCurrentPage():
                    self.active_pane.GetCurrentPage().Refresh()

            self.active_pane = active_pane

            if active_pane and hasattr(active_pane, 'set_active'):
                active_pane.set_active(True)
                if active_pane.GetCurrentPage():
                    active_pane.GetCurrentPage().Refresh()

        event.Skip()

    def get_frame_manager(self):
        """returns frame manager - aui.framemanager.AuiManager derived object"""
        return self._mgr

    def get_dock_art(self):
        """return art provider related to the asociated frame manager"""
        return self._mgr.GetArtProvider()

    def SetActive(self, notebook, tab):
        if tab:
            tab.SetFocus()

    def _create_notebook_ctrl(self, hideSingleTab=True):
        style = aui.AUI_NB_WINDOWLIST_BUTTON | aui.AUI_NB_CLOSE_ON_ALL_TABS
        n = SchNotebook(self._panel, wx.Point(0, 0), wx.Size(0,0), style=style)
        n.SetAGWWindowStyleFlag(style)
        n.SetArtProvider(aui.VC71TabArt())
        return n

    def _create_pane_info(self, name, caption):
        return aui.AuiPaneInfo().Name(name).Caption(caption)


    def _on_page_event(self, direction):
        """scroll active form"""
        w = wx.Window.FindFocus()
        parent = w
        while parent:
            if parent.__class__.__name__=='SchForm':
                if hasattr(parent, "on_page_event"):
                    parent.on_page_event(direction)
                    return
                else:
                    y = parent.GetViewStart()[1]*parent.GetScrollPixelsPerUnit()[1]
                    dy = parent.GetScrollPageSize(wx.VERTICAL)*parent.GetScrollPixelsPerUnit()[1]
                    y = y + direction * dy
                    if y<0: y=0
                    if parent.GetScrollPixelsPerUnit()[1]!=0:
                        parent.Scroll(-1, y/parent.GetScrollPixelsPerUnit()[1])
                    else:
                        parent.Scroll(-1, y)
                    return
            else:
                parent = parent.GetParent()

    def on_next_page(self, evt):
        """scroll active form one page down"""
        self._on_page_event(1)

    def on_prev_page(self, evt):
        """scroll active form one page up"""
        self._on_page_event(-1)

    def on_next_tab(self, evt):
        """select a next tab in desktop notebook"""
        desktop = wx.GetApp().GetTopWindow().desktop
        id = desktop.GetPageIndex(desktop.GetCurrentPage())
        idn = 0
        if id != None and id >= 0:
            idn = id + 1
        if idn >= desktop.GetPageCount():
            idn = 0
        desktop.SetSelection(idn)
        return

    def on_prev_tab(self, evt):
        """select a previous tab in desktop notebook"""
        desktop = wx.GetApp().GetTopWindow().desktop
        id = desktop.GetSelection()
        idn = 0
        if id >= 0:
            idn = id - 1
        if idn < 0:
            idn = desktop.GetPageCount() - 1
        desktop.SetSelection(idn)
        return

    def on_close_tab(self, evt):
        """close active tab in active notebook"""
        win = wx.Window.FindFocus()
        while win:
            if win.__class__.__name__ == 'SchNotebook':
                id = win.GetSelection()
                if id >= 0:
                    panel = win.GetPage(id)
                    panel.close_child_page(True)
                return
            win = win.GetParent()

    def after_close(self, win):
        count = win.GetPageCount()
        if count < 1:
            apppanel = win.GetPanel()
            if apppanel:
                apppanel.Hide()
                self._mgr.Update()

    def on_refresh_tab(self, evt):
        """Refresh content of active form"""
        desktop = wx.GetApp().GetTopWindow().desktop
        idn = desktop.GetSelection()
        if idn >= 0:
            panel = desktop.GetPage(idn)
            panel.refresh_html()

    def get_active_ctrl(self):
        """Get active widget"""
        ctrl = None
        idn = self.desktop.GetSelection()
        if idn >= 0:
            panel = self.desktop.GetPage(idn)
            if panel:
                count = panel.get_page_count()
                if count > 0:
                    htmlwin = panel.get_page(count - 1)
                    if htmlwin:
                        ctrl = htmlwin.get_last_control_with_focus()
                return ctrl
        return None

    def get_active_panel(self):
        """get active form"""
        idn = self.desktop.GetSelection()
        if idn >= 0:
            panel = self.desktop.GetPage(idn)
            if panel:
                count = panel.GetPageCount()
                if count > 0:
                    htmlwin = panel.GetPage(count - 1)
                    return htmlwin
        return None

    def new_main_page(self, address_or_parser, title="", parameters=None, panel="desktop"):
        """Open a new page in main

        Args:
            address_or_parser: can be: address of http page (str type) or
            :class:'~schlib.schparser.html_parsers.ShtmlParser'
            title - new tab title
            parameters - parameters of http request
            panel - options are: 'desktop', 'panel', 'header', 'footer'
        Returns:
            created form :class:'~schcli.guiframe.htmlsash.SchPage'
        """

        if type(address_or_parser) == str:
            address = address_or_parser
        else:
            address = address_or_parser.address

        pdict = {}
        parm = split2(address,'?')
        if len(parm)==2:
            parm2 = parm[1].split(',')
            parm3 = [ pos.split('=') for pos in parm2 ]
            for pos in parm3:
                if len(pos)==2:
                    pdict[pos[0]]=pos[1]
                else:
                    pdict[pos[0]]=None
        if parameters and type(parameters)==dict:
            pdict.update(parameters)

        if 'schtml' in pdict:
            _panel = pdict['schtml']
        else:
            _panel = panel

        if _panel == "desktop2" or _panel == '1':
            _panel = 'desktop'

        if panel=='pscript':
            http = wx.GetApp().get_http(self)
            http.get(self, address)
            ptr = http.str()
            exec(ptr)
            http.clear_ptr()
            return

        if not address.startswith('^'):
            if (not _panel or _panel.startswith('browser')) or ((address.startswith('http') or address.startswith('file://')) and not address.startswith(wx.GetApp().base_address)):
                if '_' in _panel:
                    _panel = _panel.split('_')[1]
                else:
                    _panel = 'desktop'
                ret =  self.new_main_page("^standard/webview/widget_web.html", "Empty page", panel=_panel)
                if address.startswith('http://') or address.startswith('https://') or address.startswith('file://'):
                    def _ret_fun():
                        ret.body.WEB.go(address)
                    wx.CallAfter(_ret_fun)
                else:
                    def _ret_fun():
                        ret.body.WEB.go(wx.GetApp().base_address + address)
                    wx.CallAfter(_ret_fun)
                return ret

        if len(title)<32:
            title2 = title
        else:
            title2 = title[:30] + '...'

        if panel.startswith("toolbar"):
            name = panel[7:]
            if name[0:1] == '_':
                return self.toolbar_interface.create_html_win(name[1:], address_or_parser, parameters)
            else:
                return self.toolbar_interface.create_html_win(None, address_or_parser, parameters)


        n = self._mgr.GetPane(_panel).window

        if not self._mgr.GetPane(_panel).IsShown():
            refr = True
        else:
            refr = False

        if title2 in [ pos.caption for pos in n._tabs._pages ]:
            for id, pos in enumerate(n._tabs._pages):
                if pos.caption==title2:
                    n.SetSelection(id)
                    n.activate_page(pos.window)
            if refr:
                self._mgr.GetPane(_panel).Show()
                self._mgr.Update()
            return False

        page = SchNotebookPage(n)
        if panel == "desktop2":
            if title is None:
                if type(address_or_parser)==str:
                    n.add_and_split(page, "", wx.RIGHT)
                else:
                    n.add_and_split(page, address_or_parser.title, wx.RIGHT)
            else:
                n.add_and_split(page, title2, wx.RIGHT)
        else:
            if title is None:
                if type(address_or_parser)==str:
                    n.AddPage(page, "", True)
                else:
                    n.AddPage(page, address_or_parser.title, True)
            else:
                n.AddPage(page, title2, True)

        if type(address_or_parser)==str:
            address = address_or_parser
        else:
            address = address_or_parser.address

        page.http = wx.GetApp().get_http_for_adr(address)

        if refr:
            self._mgr.GetPane(_panel).Show()
        self._mgr.Update()

        return page.new_child_page(address_or_parser, None, parameters)

    def on_taskbar_hide(self, event):
        self.Hide()

    def on_taskbar_toogle(self, event):
        if self.IsShown():
            self.Hide()
        else:
            self.Show()

    def on_taskbar_show_menu(self, event):
        self.PopupMenu(self.menu_tray)

    def on_taskbar_show(self, event):
        self.Show()

    def bind_command(self, fun, id=wx.ID_ANY):
        """bind command event, unlike wxPython Bind this function bind command to menu and toolbar interface"""
        self.Bind(wx.EVT_MENU, fun, id=id)
        self.toolbar_interface.bind(fun, id)

    def get_menu_bar(self):
        """return toolbar interface"""
        return self.menubar_interface

    def get_tool_bar(self):
        """return toolbar interface"""
        return self.toolbar_interface

    def on_child_focus(self, event):
        pane = self._mgr.GetPane(event.GetWindow())
        if pane.IsOk():
            if self.active_pane:
                name = self.active_pane.Name
            else:
                name = ""
            if name != pane.Name:
                self.last_pane = self.active_pane
                self.active_pane = pane

        self.active_child_ctrl = event.GetWindow()
        event.Skip()

    def on_timer(self, evt):
        if platform.system() == "Windows":
            wx.html2.WebView.New("messageloop")

        x = dispatcher.getReceivers(signal='PROCESS_INFO')
        if len(x)>0:
            if not self._proc_mannager:
                self._proc_mannager = get_process_manager()
            x = self._proc_mannager.list_threads(all=False)
            dispatcher.send('PROCESS_INFO',self, x)

    def _append_command(self, typ, command):
        id = wx.NewId()
        self.command[id] = (typ, command)
        return id

    def _create_bars(self, bar, tab):
        for row in tab:
            if len(row[0].data) > 0:
                pos = 1
            else:
                if len(row[1].data) > 0:
                    pos = 2
                else:
                    if len(row[2].data) > 0:
                        pos = 3
                    else:
                        pos = -1
            if pos >= 0:
                if pos == 1:
                    page = bar.append(row[0].data)
                if pos == 2:
                    panel = page.append(row[1].data)
                if pos == 3:
                    try:
                        bitmap = (wx.GetApp().images)[int(row[4].data)]
                    except:
                        if row[4].data != "":
                            bitmap = bitmap_from_href(row[4].data)
                        else:
                            bitmap = (wx.GetApp().images)[0]
                    idn = self._append_command(row[5].data, row[6].data)
                    panel.append(idn, row[2].data, bitmap)
            bar.bind(self.on_command)

    def _create_menu_bar(self):
        tab = wx.GetApp().get_tab(self._menu_bar_lp)[1:]
        bar = self.menubar_interface
        return self._create_bars(bar, tab)

    def _create_tool_bar(self):
        tab = wx.GetApp().get_tab(self._toolbar_bar_lp)[1:]
        bar = self.toolbar_interface
        return self._create_bars(bar, tab)

    def bind_to_toolbar(self, funct, id):
        """bind function to toolbar button

        Args:
            funct - function (event handler) to bind
            id - toolbar button id
        """
        if 'toolbar' in self.gui_style:
            self.toolbar_interface.bind(funct, id)

    def _create_status_bar(self):
        statusbar = self.CreateStatusBar(2)
        statusbar.SetStatusWidths([-2, -3])
        statusbar.SetStatusText("Ready", 0)
        return statusbar




    def _exit(self, event=None):
        self.t1.Stop()
        wx.GetApp().on_exit()
        self._mgr.UnInit()
        if self.tbIcon:
            self.tbIcon.RemoveIcon()
            self.tbIcon = None
        self.Destroy()

    def on_open(self, event):
        self.new_main_page(wx.GetApp().base_address + '/commander/form/FileManager/', "Commander", None, "panel")

    def on_exit(self, event=None):
        self._exit()

    def on_close(self, event):
        self._exit()
        event.Skip()

    def on_show_elem(self, event):
        name = ["header", "panel", "footer", "tb1", "tb2"][event.GetId() - ID_SHOWHEADER]
        panel = self._mgr.GetPane(name)
        panel.Show(not panel.IsShown())
        self._mgr.Update()

    def count_shown_panels(self, count_toolbars=True):
        """count visible panels"""
        count = 0
        for panel in self._mgr.GetAllPanes():
            if panel.IsShown():
                if (not "Toolbar" in panel.caption) or count_toolbars:
                    count += 1
        return count

    def on_show_status_bar(self, event):
        if not self.statusbar:
            self._create_status_bar()

    def _on_html(self, command):
        l = command.split(',')
        if len(l) > 2:
            parm = l[2]
            if parm == "":
                parm = None
        else:
            parm = None

        if l[1] != None and l[1][0] == ' ':
            l[1] = (l[1])[1:]
        if parm != None and parm[0] == ' ':
            parm = parm[1:]

        return self.new_main_page(l[1], l[0], parm)

    def _on_python(self, command):
        exec(command)

    def _on_sys(self, command):
        (self.sys_command)[command]()

    def on_command(self, event):
        id = event.GetId()
        if id in self.command:
            cmd = self.command[id]
            if cmd[0] == 'html':
                return self._on_html(cmd[1])
            if cmd[0] == 'python':
                return self._on_python(cmd[1])
            if cmd[0] == 'sys':
                return self._on_sys(cmd[1])
        else:
            if id == ID_RESET:
                from schcli.toolbar.moderntoolbar import RibbonInterface
                old_toolbar = self.toolbar_interface
                sizer = self.GetSizer()
                self.toolbar_interface = RibbonInterface(self, self.gui_style)
                self._create_tool_bar()
                self.toolbar_interface.realize_bar()
                sizer.Replace(old_toolbar.get_bar(), self.toolbar_interface.get_bar())
                self.toolbar_interface.get_bar().SetSize(old_toolbar.get_bar().GetSize())
                wx.CallAfter(old_toolbar.get_bar().Destroy)
                return
            elif id == ID_WEB_NEW_WINDOW:
                win = wx.GetApp().GetTopWindow().new_main_page("^standard/webview/widget_web.html", "Empty page")
                win.body.new_child_page("^standard/webview/gotopanel.html", title="Go")
                return
        event.Skip()

    def on_about(self):
        msg = "Pytigon runtime\nSławomir Chołaj\nslawomir.cholaj@gmail.com\n\n" + \
              "The program uses wxpython library version:" + wx.VERSION_STRING
        dlg = wx.MessageDialog(self, msg, "Pytigon", wx.OK | wx.ICON_INFORMATION) % wx.GetApp().title
        dlg.ShowModal()
        dlg.Destroy()

    def on_key_down(self, event):
        for a in self.aTable:
            if event.KeyCode == a[1]:
                if event.AltDown() and (a[0] & wx.ACCEL_ALT == 0):
                    continue
                if event.ControlDown() and (a[0] & wx.ACCEL_CTRL == 0):
                    continue
                if event.ShiftDown() and (a[0] & wx.ACCEL_SHIFT == 0):
                    continue
                self.ProcessEvent(wx.CommandEvent(wx.wxEVT_COMMAND_MENU_SELECTED, a[2]))
                return
        event.Skip()

    #def get_start_position(self):
    #    self.x = self.x + 20
    #    x = self.x
    #    pt = self.ClientToScreen(wx.Point(0, 0))
    #    return wx.Point(pt.x + x, pt.y + x)

    def goto_panel(self, panel_name):
        """Activate panel

        Args:
            panel_name: name of panel to activate
        """
        panel = self._mgr.GetPane(panel_name)
        if panel.window.GetPageCount() > 0:
            if not panel.IsShown():
                panel.Show(True)
                self._mgr.Update()
            panel.window.SetFocus()

    def on_goto_panel(self, event):
        panel = self._mgr.GetPane('panel')
        if panel.IsShown():
            self.goto_panel('panel')
        else:
            panel = self._mgr.GetPane('menu')
            if panel and panel.IsShown():
                panel.window.SetFocus()

    def on_goto_head(self, event):
        self.goto_panel('header')

    def on_goto_footer(self, event):
        self.goto_panel('footer')

    def on_goto_desktop(self, event):
        self.desktop.SetFocus()

    def show_pdf(self, page):
        """show pdf downloaded from web server

        Args:
            page: web page address
        """
        http = wx.GetApp().get_http(self)
        http.get(self, str(page)) #, user_agent='webkit')
        form_frame = self._open_binary_data(http, page)

        def _after_init():
            form_frame.body.WEB.execute_javascript("document.title = '%s';" % page)
        wx.CallAfter(_after_init)

        return form_frame


    def show_odf(self, page):
        """show odf document downloaded from web server

        Args:
            page: web page address
        """
        http = wx.GetApp().get_http(self)
        http.get(self, str(page)) #, user_agent='webkit')
        return self._open_binary_data(http, page)
    
    def _open_binary_data(self, http_ret, page):
        if 'application/vnd.oasis.opendocument' in http_ret.ret_content_type:

            cd = http_ret.http.headers.get('content-disposition')
            if cd:
                name = cd.split('filename=')[1]
            else:
                name = None
            p = http_ret.ptr()
                        
            postfix = name.split('_')[-1][-12:]
            fname = get_temp_filename(postfix)
            with open(fname, "wb") as f:
                f.write(p)

            file_name = fname
            if not name:
                name = file_name
            if not hasattr(wx.GetApp(),"download_files"):
                wx.GetApp().download_files = []
            wx.GetApp().download_files.append( (file_name, name, datetime.datetime.now() ) )
    
            return self.new_main_page('^standard/odf_view/odf_view.html', name, parameters=name)
        elif 'application/pdf' in http_ret.ret_content_type:
            p = http_ret.ptr()
            f = NamedTemporaryFile(delete=False)
            f.write(p)
            name = f.name
            f.close()
            href = "http://127.0.0.2/static/vanillajs_plugins/pdfjs/web/viewer.html?file="+name
            return self.new_main_page(href, name, parameters={ 'schtml': 0 } )

        elif 'zip' in http_ret.ret_content_type:
            p = http_ret.ptr()
            f = NamedTemporaryFile(delete=False)
            f.write(p)
            name = f.name
            f.close()
            return self.new_main_page('^standard/html_print/html_print.html', name, parameters=name)

        return True

    def get_main_panel(self):
        return self._panel