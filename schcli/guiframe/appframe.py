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
    Top window
"""

import os
import sys
import platform

import wx
import wx.html2
import datetime
import time
#import agw.aui as aui
from wx.lib.agw import aui

from schcli.guilib.art_provider import ArtProviderFromIcon
from schcli.guilib.schevent import * #@UnusedWildImport
from schcli.guiframe.appnotebook import AppNotebook
from schcli.guiframe.appnotebookpage import NotebookPage
from schcli.guilib.tools import bitmap_from_href
from schcli.toolbar import toolbar_interface
from schlib.schfs.vfstools import get_temp_filename
from schlib.schtools.cc import compile
from schlib.schtools.tools import split2
from tempfile import NamedTemporaryFile

import six

_ = wx.GetTranslation

class SChMainPanel(wx.Window):
    def __init__(self, *argi, **argv):
        argv['name'] = 'schmainpanel'
        if 'style' in argv:
            argv['style'] |= wx.WANTS_CHARS
        wx.Window.__init__(self, *argi, **argv)

    def GetFrameManager(self):
        return self.GetParent().GetFrameManager()

    def GetMenuBar(self):
        return self.GetParent().GetMenuBar()


class SChAuiManager(aui.AuiManager):
    def __init__(self, *argi, **argv):
        aui.AuiManager.__init__(self, *argi, **argv)

    def AddPane(self, window, arg1=None, arg2=None):
        ret = aui.AuiManager.AddPane(self, window, arg1, arg2)
        if hasattr(window, 'SetPanel'):
            window.SetPanel(arg1)
        return ret

    def ActivatePane(self, window):
        #print "ActivatePane", window
        try:
            ret = aui.AuiManager.ActivatePane(self, window)
        except:
            ret = None
        return ret


class SchAppFrame(wx.Frame):
    """
        This is main window of pytigon application
    """

    def __init__(self, parent, gui_style="tree(toolbar,statusbar)", id= -1, title="", pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE |
                 wx.CLIP_CHILDREN | wx.WANTS_CHARS, name="MainWindow"):

    #def __init__(self, parent, gui_style="tree(toolbar,statusbar)", id= -1, title="", pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.RESIZE_BORDER | wx.CLIP_CHILDREN,
    #             name="MainWindow"):


        self.gui_style = gui_style

        wx.Frame.__init__(self, parent, id, title, pos, size, style | wx.WANTS_CHARS, name)
        self._id = wx.ID_HIGHEST
        #self._id = 32000

        self._perspectives = []
        self._mgr = SChAuiManager()

        self.x = 0
        self.idle_objects = []
        self.gui_style = gui_style
        self.command = []
        self.last_pane = None
        self.active_pane = None
        self.active_page = None
        self.active_child_ctrl = None
        self.toolbar_interface = None
        self.menubar_interface = None
        self.statusbar_interface = None
        self.menu_bar = None
        self.destroy_fun_tab = []
        self.after_init = False

        self.menu_bar_lp = 0
        self.toolbar_bar_lp = 1

        self.sys_command = dict({"EXIT": self.on_exit, "ABOUT": self.on_about})

        if 'dialog' in self.gui_style or 'one_form' in self.gui_style:
            hide_on_single_page = True
        else:
            hide_on_single_page = False

        if not hasattr(self._mgr, 'SetAGWFlags'):
            self._mgr.SetAGWFlags = self._mgr.SetFlags
            self._mgr.GetAGWFlags = self._mgr.GetFlags

        self._mgr.SetAGWFlags(self._mgr.GetAGWFlags() ^ aui.AUI_MGR_ALLOW_ACTIVE_PANE)

        self._panel = SChMainPanel(self)
        self._mgr.SetManagedWindow(self._panel)
        self.desktop = self.create_notebook_ctrl(hide_on_single_page)
        self.get_dock_art().SetMetric(aui.AUI_DOCKART_PANE_BORDER_SIZE, 0)

        self.Bind(aui.EVT_AUI_PANE_ACTIVATED, self.on_pane_activated)

        wx.ArtProvider.Push(ArtProviderFromIcon())

        icon = wx.Icon()
        b = wx.Bitmap(wx.Image(wx.GetApp().scr_path + '/schappdata/media/schweb.png'))
        icon.CopyFromBitmap(b)

        self.SetIcon(icon)

        if 'tray' in gui_style:
            #TODO
            self.tbIcon = wx.adv.TaskBarIcon()
            self.tbIcon.SetIcon(icon, "SCSkrypt")
            #self.tbIcon = None
        else:
            self.tbIcon = None

        if 'statusbar' in gui_style:
            self.statusbar = self._create_status_bar()
        else:
            self.statusbar = None

        wx.GetApp().SetTopWindow(self)


        self.SetMinSize(wx.Size(400, 300))

        if 'tree' in gui_style:
            s = wx.BoxSizer(wx.HORIZONTAL)
        else:
            s = wx.BoxSizer(wx.VERTICAL)

        if 'standard' in gui_style:
            if len(wx.GetApp().get_tab(self.toolbar_bar_lp))>1:
                from schcli.toolbar import schstandardtoolbar
                self.toolbar_interface = schstandardtoolbar.ToolBarInterface(self, gui_style)
                self.create_tool_bar()
                self.toolbar_interface.realize_bar()
            s.Add(self._panel, 1, wx.EXPAND)
            self._mgr.Update()
        elif 'modern' in gui_style:
            from schcli.toolbar.schmoderntoolbar import RibbonInterface
            self.toolbar_interface = RibbonInterface(self, gui_style)
            self.create_tool_bar()
            self.toolbar_interface.realize_bar()
            s.Add(self.toolbar_interface.get_bar(), 0, wx.EXPAND)
            s.Add(self._panel, 1, wx.EXPAND)
        elif 'tree' in gui_style:
            from schcli.toolbar.schtreetoolbar import TreeInterface
            leftPanel = wx.Panel(self._panel, style=wx.TAB_TRAVERSAL | wx.CLIP_CHILDREN, size=wx.Size(400, 250))
            self.toolbar_interface = TreeInterface(leftPanel, gui_style)
            self.create_tool_bar()
            self.toolbar_interface.realize_bar()
            leftBox = wx.BoxSizer(wx.VERTICAL)
            leftBox.Add(self.toolbar_interface.get_bar(), 1, wx.EXPAND)
            leftPanel.SetSizer(leftBox)
            self._mgr.AddPane(leftPanel, self.panel("Menu", "Menu").CaptionVisible(True).MinimizeButton(True).CloseButton(False).Left().BestSize((250, 40)).MinSize((250, 40)).Show())
            s.Add(self._panel, 1, wx.EXPAND)
        else:
            s.Add(self._panel, 1, wx.EXPAND)

        self.SetSizer(s)

        if len(wx.GetApp().get_tab(2))>1:
            self.menu_bar_lp = 2
        else:
            if wx.GetApp().menu_always:
                self.menu_bar_lp = 1

        if self.menu_bar_lp>0:
            from schcli.toolbar import schmenubar

            self.menu_bar = wx.MenuBar()
            self.menubar_interface = schmenubar.MenuInterface(self.menu_bar, gui_style)
            self.create_menu_bar()


        if not self.menubar_interface:
            self.menubar_interface = toolbar_interface.BarNullInterface()

        if not self.toolbar_interface:
            self.toolbar_interface = toolbar_interface.BarNullInterface()

        s_dx = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_X)
        s_dy = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_Y)

        self._mgr.AddPane(self.create_notebook_ctrl(), self.panel("Panel", "Tools").CaptionVisible(True).Left().MinSize((250,
                          s_dy / 2)).BestSize((s_dx / 2 - 50, s_dy - 100)).Show())
        self._mgr.AddPane(self.create_notebook_ctrl(), self.panel("Header", "Header").CaptionVisible(False).Top().Show())
        self._mgr.AddPane(self.create_notebook_ctrl(), self.panel("Footer", "Footer").CaptionVisible(False).Bottom().Show())
        self._mgr.AddPane(self.desktop, self.panel("desktop", "desktop").CenterPane().Show())

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
                if all_panes[ii].name != 'Menu':
                    all_panes[ii].Hide()

        ##if self.desktop.GetPageCount() > 0:
        self._mgr.GetPane("desktop").Show()
        #else:
        #    self._mgr.GetPane("desktop").Hide()

        perspective_default = self._mgr.SavePerspective()

        size = self.desktop.GetPageCount()
        for i in range(size): #@UnusedVariable
            self.desktop.DeletePage(0)
        self._perspectives.append(perspective_default)
        self._perspectives.append(perspective_all)
        self._perspectives.append(perspective_notoolbar)

        self.aTable = [
                  (wx.ACCEL_ALT, wx.WXK_PAGEUP, ID_PrevTab),
                  (wx.ACCEL_ALT, wx.WXK_PAGEDOWN, ID_NextTab),

                  (wx.ACCEL_ALT, wx.WXK_LEFT, ID_GotoPanel),
                  (wx.ACCEL_ALT, wx.WXK_RIGHT, ID_GotoDesktop),
                  (wx.ACCEL_ALT, wx.WXK_UP, ID_GotoHeader),
                  (wx.ACCEL_CTRL, ord('W'), ID_CloseTab),
                  (wx.ACCEL_CTRL, ord('N'), ID_WEB_NEW_WINDOW),
                  #(wx.ACCEL_CTRL, ord('J'), ID_KEY_J),
                  #(wx.ACCEL_CTRL, ord('K'), ID_KEY_K),
                  #(wx.ACCEL_CTRL, ord('H'), ID_KEY_H),
                  #(wx.ACCEL_CTRL, ord('L'), ID_KEY_L),
                  (wx.ACCEL_CTRL, wx.WXK_TAB, ID_NextTab),
                  (wx.ACCEL_CTRL | wx.ACCEL_SHIFT, wx.WXK_TAB, ID_PrevTab),
                  (wx.ACCEL_CTRL, wx.WXK_F6, ID_NextTab),
                  (wx.ACCEL_CTRL | wx.ACCEL_SHIFT, wx.WXK_F6, ID_PrevTab),
                  (wx.ACCEL_ALT, ord('h'), ID_PrevTab),
                  (wx.ACCEL_ALT, ord('l'), ID_NextTab),
                  (wx.ACCEL_ALT, ord('k'), ID_PrevPage),
                  (wx.ACCEL_ALT, ord('j'), ID_NextPage),
                  (wx.ACCEL_ALT, wx.WXK_BACK, ID_WEB_BACK),
                  (0, wx.WXK_F5, ID_RefreshTab)]

        home_dir = wx.GetApp().get_working_dir()

        dirnames = [wx.GetApp().scr_path + "/schappdata/schplugins/", home_dir + "plugins_cache/"]

        for dirname in dirnames:
            for ff in os.listdir(dirname):
                if os.path.isdir(os.path.join(dirname, ff)):
                    dirname2 = os.path.join(dirname, ff)
                    pliki = []
                    for f in os.listdir(dirname2):
                        pliki.append(f)
                    pliki.sort()

                    for f in pliki:
                        try_run=2
                        while try_run>0:
                            try:
                                if os.path.isdir(os.path.join(dirname2, f)):
                                    p = dirname2.split('/')
                                    mod_name = p[-2] + "." + p[-1] + "." + f
                                    x = p[-1] + '/' + f
                                    if p[-1] == 'auto' or (wx.GetApp().plugins and x in wx.GetApp().plugins):
                                        if '.__' in mod_name:
                                            break
                                        mod = __import__(mod_name)
                                        mod_path = mod_name.split('.')
                                        mod2 = getattr(mod, mod_path[1])
                                        mod3 = getattr(mod2, mod_path[2])
                                        destroy = mod3.init_plugin(wx.GetApp(), self, self.desktop, self._mgr, self.get_menu_bar(), self.toolbar_interface.get_toolbars(), self.aTable)
                                        if destroy != None:
                                            self.destroy_fun_tab.append(destroy)
                                break
                            except:
                                try_run = try_run - 1
                                if try_run == 1:
                                    compile(os.path.join(dirname2, f), wx.GetApp().scr_path)
                                else:
                                    import traceback
                                    print("Error load plugin: ", mod_name)
                                    print(sys.exc_info()[0])
                                    print(traceback.print_exc())

        self.SetAcceleratorTable(wx.AcceleratorTable(self.aTable))

        self._mgr.Update()

        self.t1 = wx.Timer(self)
        self.t1.Start(25)

        self.Bind(wx.EVT_TIMER, self.on_timer, self.t1)

        if 'tray' in gui_style:
            self.Bind(wx.EVT_CLOSE, self.on_taskbar_hide)
        else:
            self.Bind(wx.EVT_CLOSE, self.on_close)

        self._panel.Bind(wx.EVT_CHILD_FOCUS, self.on_child_focus)

        #self.Bind(wx.EVT_MAXIMIZE, self.on_maximize)


        #self.bind_command(self.on_command)

        self.bind_command(self.on_open, id=wx.ID_OPEN)
        self.bind_command(self.on_exit, id=wx.ID_EXIT)

        if self.toolbar_interface:
            self.toolbar_interface.bind(self.on_update_ui_true, wx.ID_EXIT, wx.EVT_UPDATE_UI)
            self.toolbar_interface.bind(self.on_update_ui_true, ID_WEB_NEW_WINDOW, wx.EVT_UPDATE_UI)

        self.bind_command(self.on_next_tab, id=ID_NextTab)
        self.bind_command(self.on_prev_tab, id=ID_PrevTab)
        self.bind_command(self.on_next_page, id=ID_NextPage)
        self.bind_command(self.on_prev_page, id=ID_PrevPage)
        self.bind_command(self.on_close_tab, id=ID_CloseTab)
        self.bind_command(self.on_refresh_tab, id=ID_RefreshTab)

        self.bind_command(self.on_goto_desktop, id=ID_GotoDesktop)
        self.bind_command(self.on_goto_head, id=ID_GotoHeader)
        self.bind_command(self.on_goto_panel, id=ID_GotoPanel)
        self.bind_command(self.on_goto_footer, id=ID_GotoFooter)


        self.bind_command(self.on_command, id=ID_WEB_NEW_WINDOW)

        self.Bind(wx.EVT_MENU_RANGE, self.on_show_elem, id=ID_ShowHeader, id2=ID_ShowToolbar2)
        self.bind_command(self.on_show_status_bar, id=ID_ShowStatusBar)

        self.Bind(wx.EVT_IDLE, self.on_idle)

        if self.menu_bar:
            self.SetMenuBar(self.menu_bar)

        #tray icon
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

        #wx.lib.inspection.InspectionTool().Show()

        self.SetExtraStyle(wx.WS_EX_PROCESS_UI_UPDATES)
        wx.UpdateUIEvent.SetUpdateInterval(50)
        wx.UpdateUIEvent.SetMode(wx.UPDATE_UI_PROCESS_SPECIFIED)
        wx.CallAfter(self.UpdateWindowUI)


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
                            self._on_html(_(url_page[0]) + ',' + app.base_address
                                            + url_page[1])
                            # sch
                            #pass
                wx.CallAfter(start_pages)

        event.Skip()

    def on_update_ui_true(self, event):
        event.Enable(True)

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

    def on_maximize(self, event):
        self.SetWindowStyle(wx.RESIZE_BORDER | wx.CLIP_CHILDREN)
        event.Skip()

    def on_restore(self, event):
        self.SetWindowStyle(wx.DEFAULT_FRAME_STYLE | wx.CLIP_CHILDREN)
        event.Skip()

    def get_frame_manager(self):
        return self._mgr

    def get_dock_art(self):
        return self._mgr.GetArtProvider()

    def SetActive(self, notebook, tab):
        if tab:
            tab.SetFocus()

    def create_notebook_ctrl(self, hideSingleTab=True):
        style = aui.AUI_NB_WINDOWLIST_BUTTON | aui.AUI_NB_CLOSE_ON_ALL_TABS
                #| aui.AUI_NB_DRAW_DND_TAB
        #if hideSingleTab:
        #    if hasattr(aui, 'AUI_NB_HIDE_ON_SINGLE_TAB'):
        #        style ^= aui.AUI_NB_HIDE_ON_SINGLE_TAB
        n = AppNotebook(self._panel, -1, wx.Point(0, 0), wx.Size(0,
            0), style=style)
        n.SetAGWWindowStyleFlag(style)
        #n.SetArtProvider(aui.ChromeTabArt())
        n.SetArtProvider(aui.VC71TabArt())
        #n.SetArtProvider(aui.VC8TabArt())
        #n.SetArtProvider(aui.FF2TabArt())
        #if hasattr(aui, 'VC71TabArt'):
        #    n.SetArtProvider(aui.VC71TabArt())
        return n

    def panel(self, name, caption):
        return aui.AuiPaneInfo().Name(name).Caption(caption)

    def is_exiting(self):
        return False

    def on_page_event(self, direction):
        w = wx.Window.FindFocus()
        parent = w
        while parent:
            if parent.__class__.__name__=='SchHtmlWindow':
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
        self.on_page_event(1)

    def on_prev_page(self, evt):
        self.on_page_event(-1)

    def on_next_tab(self, evt):
        desktop = wx.GetApp().GetTopWindow().desktop
        #id = desktop.GetSelection()
        id = desktop.GetPageIndex(desktop.GetCurrentPage())
        idn = 0
        if id != None and id >= 0:
            idn = id + 1
        if idn >= desktop.GetPageCount():
            idn = 0
        desktop.SetSelection(idn)
        return

    def on_prev_tab(self, evt):
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
        win = wx.Window_FindFocus()
        while win:
            if win.__class__.__name__ == 'AppNotebook':
                id = win.GetSelection()
                if id >= 0:
                    panel = win.GetPage(id)
                    panel.cancel(True)
                self.after_close(win)
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
        desktop = wx.GetApp().GetTopWindow().desktop
        idn = desktop.GetSelection()
        if idn >= 0:
            panel = desktop.GetPage(idn)
            panel.refresh_html()

    def get_active_ctrl(self):
        ctrl = None
        idn = self.desktop.GetSelection()
        if idn >= 0:
            panel = self.desktop.GetPage(idn)
            if panel:
                count = panel.get_page_count()
                if count > 0:
                    htmlwin = panel.get_page(count - 1)
                    if htmlwin:
                        #print("CTRL", htmlwin)
                        ctrl = htmlwin.get_last_control_with_focus()
                return ctrl
        return None

    def get_active_panel(self):
        idn = self.desktop.GetSelection()
        if idn >= 0:
            panel = self.desktop.GetPage(idn)
            if panel:
                count = panel.GetPageCount()
                if count > 0:
                    htmlwin = panel.GetPage(count - 1)
                    return htmlwin
        return None

    def new_main_page(self, address_or_parser, title="", parametry=None, panel="desktop"):
        #print(address_or_parser)
        #win = wx.GetApp().GetTopWindow().new_main_page("^standard/webview/widget_web.html", l[0])
        #win.Body.WEB.go(wx.GetApp().base_address + l[1])

        if type(address_or_parser) == str:
            address = address_or_parser
        else:
            address = address_or_parser.address

        if not address.startswith('^'):
            parm = split2(address,'?')
            pdict = {}
            if len(parm)==2:
                parm2 = parm[1].split(',')
                parm3 = [ pos.split('=') for pos in parm2 ]
                for pos in parm3:
                    if len(pos)==2:
                        pdict[pos[0]]=pos[1]
                    else:
                        pdict[pos[0]]=None
            if parametry and type(parametry)==dict:
                pdict.update(parametry)

            if ('schtml' in pdict and pdict['schtml'] != '1') or ((address.startswith('http') or address.startswith('file://')) and not address.startswith(wx.GetApp().base_address)):
                ret =  self.new_main_page("^standard/webview/widget_web.html", "Empty page")
                if address.startswith('http://') or address.startswith('https://') or address.startswith('file://'):
                    def _ret_fun():
                        ret.Body.WEB.go(address)
                    wx.CallAfter(_ret_fun)
                else:
                    def _ret_fun():
                        ret.Body.WEB.go(wx.GetApp().base_address + address)
                    wx.CallAfter(_ret_fun)
                return ret

        if len(title)<32:
            title2 = title
        else:
            title2 = title[:30] + '...'

        if panel.startswith("toolbar"):
            name = panel[7:]
            if name[0:1] == '_':
                return self.toolbar_interface.create_html_win(name[1:], address_or_parser, parametry)
            else:
                return self.toolbar_interface.create_html_win(None, address_or_parser, parametry)

        if panel == "Desktop2":
            _panel = 'desktop'
        else:
            _panel = panel

        n = self._mgr.GetPane(_panel).window
        #sel = n.GetSelection()

        if not self._mgr.GetPane(_panel).IsShown():
            refr = True
        else:
            refr = False

        okno = NotebookPage(n)
        #if panel == "Desktop2":
        #error in AGW
        if panel == "__Desktop2":
            if title is None:
                #if address_or_parser.__class__ == str or address_or_parser.__class__ == unicode:
                if isinstance(address_or_parser, six.string_types):
                    n.add_and_split(n, okno, "", wx.RIGHT)
                else:
                    n.add_and_split(n, okno, address_or_parser.title, wx.RIGHT)
            else:
                #n.add_and_split(okno, title2, wx.RIGHT)
                n.add_and_split(n, okno, title2, wx.RIGHT)
        else:
            if title is None:
                #if address_or_parser.__class__ == str or address_or_parser.__class__ == unicode:
                if isinstance(address_or_parser, six.string_types):
                    n.AddPage(okno, "", True)
                else:
                    n.AddPage(okno, address_or_parser.title, True)
            else:
                n.AddPage(okno, title2, True)

        if platform.system() == "Linux":
            okno.SetSize(0,0)
        #if address_or_parser.__class__ == str or address_or_parser.__class__ == unicode:
        if isinstance(address_or_parser, six.string_types):
            address = address_or_parser
        else:
            address = address_or_parser.address


        #okno.SetSize(10000,10000)

        #self.Refresh()
        #self.Update()

        okno.http = wx.GetApp().get_http_for_adr(address)

        if refr:
            self._mgr.GetPane(_panel).Show()
            self._mgr.Update()

        return okno.new_child_page(address_or_parser, None, parametry)
        #return okno.new_child_page(address_or_parser, None, parametry)
        #wx.CallAfter(okno.new_child_page, address_or_parser, None, parametry)
        #return

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
        self.Bind(wx.EVT_MENU, fun, id=id)
        self.toolbar_interface.bind(fun, id)

    def get_menu_bar(self):
        return self.toolbar_interface

    def on_child_focus(self, event):
        #print("on_child_focus:", event)
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


    def _append_command(self, typ, command):
        self.command.append((self._id, typ, command))
        self._id = self._id + 1
        return self._id-1

    def create_bars(self, bar, tab):
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
                    page = bar.create_page(row[0].data)
                if pos == 2:
                    panel = page.create_panel(row[1].data)
                if pos == 3:
                    try:
                        bitmap = (wx.GetApp().IMAGES)[int(row[4].data)]
                    except:
                        if row[4].data != "":
                            bitmap = bitmap_from_href(row[4].data)
                        else:
                            bitmap = (wx.GetApp().IMAGES)[0]
                    idn = self._append_command(row[5].data, row[6].data)
                    panel.append(idn, row[2].data, bitmap)
            bar.bind(self.on_command)



    def create_menu_bar(self):
        tab = wx.GetApp().get_tab(self.menu_bar_lp)[1:]
        bar = self.menubar_interface
        return self.create_bars(bar, tab)

    def create_tool_bar(self):
        tab = wx.GetApp().get_tab(self.toolbar_bar_lp)[1:]
        bar = self.toolbar_interface
        return self.create_bars(bar, tab)

    def bind_to_toolbar(self, funct, id):
        if 'toolbar' in self.gui_style:
            self.toolbar_interface.bind(funct, id)

    def _create_status_bar(self):
        statusbar = self.CreateStatusBar(2)
        statusbar.SetStatusWidths([-2, -3])
        statusbar.SetStatusText("Ready", 0)
        return statusbar


    def on_exit(self, event=None):
        print("Timer stop 0")
        self.t1.Stop()
        print("Timer stop 1")
        wx.GetApp().on_exit()
        self._mgr.UnInit()
        self.Destroy()
        if self.tbIcon:
            self.tbIcon.RemoveIcon()
            self.tbIcon = None

    def on_open(self, event):
        self.new_main_page(wx.GetApp().base_address + '/schcommander/table/FileManager/list//', "Commander", None, "Panel")


    def on_close(self, event):
        #print "############################ on close"
        #for f in self.destroy_fun_tab:
        #    wx.CallAfter(f)

        #self._mgr.UnInit()
        #self.Destroy()
        #if self.tbIcon:
        #    self.tbIcon.RemoveIcon()
        #    self.tbIcon = None


        self.on_exit()
        event.Skip()

    def on_show_elem(self, event):
        nazwa = ["Header", "Panel", "Footer", "tb1", "tb2"][event.GetId() - ID_ShowHeader]

        panel = self._mgr.GetPane(nazwa)

        panel.Show(not panel.IsShown())
        self._mgr.Update()

    def count_shown_panels(self, count_toolbars=True):
        count = 0
        for panel in self._mgr.GetAllPanes():
            if panel.IsShown():
                if (not "Toolbar" in panel.caption) or count_toolbars:
                    count += 1
        return count

    def on_show_status_bar(self, event):
        pass

    def _on_html(self, command):
        l = command.split(',')
        if len(l) > 2:
            parm = l[2]
            if parm == "":
                parm = None
        else:
            parm = None
        if len(l) > 3:
            panel = l[3]
        else:
            panel = "desktop"

        if l[1] != None and l[1][0] == ' ':
            l[1] = (l[1])[1:]
        if parm != None and parm[0] == ' ':
            parm = parm[1:]

        if 'schtml=1' in l[1] and not wx.GetApp().is_hybrid:
            self.new_main_page(l[1], l[0], parm, panel)
        else:
            win = wx.GetApp().GetTopWindow().new_main_page("^standard/webview/widget_web.html", l[0])
            win.Body.WEB.go(wx.GetApp().base_address + l[1])

    def _on_python(self, command):
        exec(command)

    def _on_sys(self, command):
        (self.sys_command)[command]()

    def on_command(self, event):
        id = event.GetId()
        #print("on_command:", id)
        if id - wx.ID_HIGHEST >= 0 and id - wx.ID_HIGHEST < len(self.command):
            cmd = (self.command)[id - wx.ID_HIGHEST]
            if cmd[1] == 'html':
                return self._on_html(cmd[2])
            if cmd[1] == 'python':
                return self._on_python(cmd[2])
            if cmd[1] == 'sys':
                return self._on_sys(cmd[2])
        else:
            if id == ID_Reset:
                from schcli.toolbar.schmoderntoolbar import RibbonInterface
                old_toolbar = self.toolbar_interface
                sizer = self.GetSizer()
                self.toolbar_interface = RibbonInterface(self, self.gui_style)
                self.create_tool_bar()
                self.toolbar_interface.realize_bar()
                sizer.Replace(old_toolbar.get_bar(), self.toolbar_interface.get_bar())
                self.toolbar_interface.get_bar().SetSize(old_toolbar.get_bar().GetSize())
                wx.CallAfter(old_toolbar.get_bar().Destroy)
                return
            elif id == ID_WEB_NEW_WINDOW:
                win = wx.GetApp().GetTopWindow().new_main_page("^standard/webview/widget_web.html", "Empty page")
                win.Body.new_child_page("^standard/webview/gotopanel.html", title="Go")
                return
        event.Skip()

    def on_about(self):
        msg = """This is a program \"Pytigon\"

""" + """Autor: Sławomir Chołaj

""" + \
            "The program uses the library wxpython " + wx.VERSION_STRING + "!"

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


    def get_start_position(self):
        self.x = self.x + 20
        x = self.x
        pt = self.ClientToScreen(wx.Point(0, 0))
        return wx.Point(pt.x + x, pt.y + x)

    def on_goto(self, panel_name):
        panel = self._mgr.GetPane(panel_name)
        if panel.window.GetPageCount() > 0:
            if not panel.IsShown():
                panel.Show(True)
                self._mgr.Update()
            panel.window.SetFocus()

    def on_goto_panel(self, event):
        self.on_goto('Panel')

    def on_goto_head(self, event):
        self.on_goto('Header')

    def on_goto_footer(self, event):
        self.on_goto('Footer')

    def on_goto_desktop(self, event):
        self.desktop.SetFocus()

    #def show_pdf2(self, page):
    #    http = wx.GetApp().get_http(self)
    #    http.Get(self, str(page), user_agent='webkit')
    #    p = http.Ptr()
    #    f = NamedTemporaryFile(delete=False)
    #    f.write(p)
    #    name = f.name
    #    f.close()
    #    http.ClearPtr()
    #    okno = self.new_main_page('^standard/pdfviewer/pdfviewer.html', page, None)
    #    #okno.Body['PDFVIEWER'].LoadFile(name, True)

    def show_pdf(self, page):
        http = wx.GetApp().get_http(self)
        http.get(self, str(page)) #, user_agent='webkit')
        okno = self.open_binary_data(http, page)

        def _after_init():
            okno.Body.WEB.execute_javascript("document.title = '%s';" % page)
        wx.CallAfter(_after_init)

        return okno


    def show_odf(self, page):
        http = wx.GetApp().get_http(self)
        http.get(self, str(page)) #, user_agent='webkit')
        return self.open_binary_data(http, page)
    
    def open_binary_data(self, http_ret, page):
        if 'application/vnd.oasis.opendocument' in http_ret.ret_content_type:

            cd = http_ret.http.headers.get('content-disposition')
            if cd:
                name = cd.split('filename=')[1]
            else:
                name = None
            p = http_ret.ptr()
                        
            postfix = name.split('_')[-1][-12:]
            fname = get_temp_filename(postfix)
            f = open(fname, "wb")        
            f.write(p)
            f.close()
                    
            file_name = fname
            if not name:
                name = file_name
            if not hasattr(wx.GetApp(),"download_files"):
                wx.GetApp().download_files = []
            wx.GetApp().download_files.append( (file_name, name, datetime.datetime.now() ) )
    
            return self.new_main_page('^standard/odf_view/odf_view.html', name, parametry=name)
        elif 'application/pdf' in http_ret.ret_content_type:
            p = http_ret.ptr()
            f = NamedTemporaryFile(delete=False)
            f.write(p)
            name = f.name
            f.close()
            href = "http://127.0.0.2/static/vanillajs_plugins/pdfjs/web/viewer.html?file="+name
            return self.new_main_page(href, name, parametry={ 'schtml': 0 } )

        elif 'zip' in http_ret.ret_content_type:
            p = http_ret.ptr()
            f = NamedTemporaryFile(delete=False)
            f.write(p)
            name = f.name
            f.close()
            return self.new_main_page('^standard/html_print/html_print.html', name, parametry=name)

        return True
