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
from autocomplete import TextCtrlAutoComplete
from schcli.guilib.image import bitmaps_from_art_id
from schcli.guilib.tools import colour_to_html
from wx.lib.agw import flatmenu as FM

_ = wx.GetTranslation

if wx.Platform == '__WXMSW__':
    MswStyle = True
else:
    MswStyle = True

tab = [
    'www.allegro.pl',
    'www.onet.pl',
    'www.google.pl',
    'www.sourceforge.org',
    'www.freshmeat.net',
    '127.0.0.2',
    '127.0.0.1:8000',
    'books.evc-cit.info/index.html',
    'www.un.org/Depts/Cartographic/map/profile/poland.pdf',
    ]

TYPE_TOOLBAR = 0
TYPE_BUTTONBAR = 1
TYPE_PANELBAR = 2

class WebHistory(object):

    def __iter__(self):
        for x in tab:
            yield x

    def __getitem__(self, id):
        if id < 4:
            return tab[id]
        else:
            x = id / 0
            return None

    def __len__(self):
        return 4

    def __contains__(self, x):
        if x in tab:
            return True
        else:
            return False


class SchAutoComplete(TextCtrlAutoComplete):

    def __init__(self, *argi, **argv):
        self.dynamic_choices = WebHistory()
        argv['choices'] = self.dynamic_choices
        TextCtrlAutoComplete.__init__(self, *argi, **argv)
        self.SetEntryCallback(self.setDynamicChoices)
        self.SetMatchFunction(self.match)
        self.Bind(wx.EVT_KEY_DOWN, self.on_return_key_down, self)

    def on_return_key_down(self, event):
        if not self.dropdown.IsShown() and event.GetKeyCode() == wx.WXK_RETURN:
            self.fun(self.GetValue())
        else:
            event.Skip()

    def set_callback_fun(self, fun):
        self.fun = fun

    def match(self, text, choice):
        t = text.lower()
        c = choice.lower()
        if c.startswith(t):
            return True
        if c.startswith(r'http://'):
            c = c[7:]
        if c.startswith(t):
            return True
        if c.startswith('www.'):
            c = c[4:]
        return c.startswith(t)

    def set_dynamic_choices(self):
        ctrl = self
        text = ctrl.GetValue().lower()
        current_choices = ctrl.GetChoices()
        choices = [choice for choice in self.dynamic_choices
                   if self.match(text, choice)]
        if choices != current_choices:
            ctrl.SetChoices(choices)

    def _set_value_from_selected(self):
        x = TextCtrlAutoComplete._setValueFromSelected(self)
        self.fun(self.GetValue())
        return x


class EmpytControl(object):

    def __init__(self):
        self.value = None

    def SetValue(self, value):
        self.value = value

    def GetValue(self):
        return self.value


class EmptyBar(object):

    def __init__(self):
        pass

    def refr(self):
        pass


class StandardButtons(object):

    def __init__(self, toolbar_interface, gui_style):
        self.toolbar_interface = toolbar_interface
        self.gui_style = gui_style
        self.ti = self.toolbar_interface
        self.tbs = self.ti.toolbars
        self._object_list = {}
        self.webobject = None
        self.file = True if 'file' in self.gui_style else False
        self.clipboard = True if 'clipboard' in self.gui_style else False
        self.operations = True if 'operations' in self.gui_style else False
        self.browse = True if 'browse' in self.gui_style else False
        self.nav = True if 'nav' in self.gui_style else False
        self.address_bar = True if 'address_bar' in self.gui_style else False
        self.bg = colour_to_html(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DFACE))
        self.bg_info = colour_to_html(wx.SystemSettings.GetColour(wx.SYS_COLOUR_INFOBK))
        self.bg_h = colour_to_html(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))
        self.progress = 0
        self.info = ''
        self.address_txt = ''

    def make_ui_handler(self, fun_name, event_id, propagete=False):
        def on_update_ui(event):
            win = wx.Window.FindFocus()
            while(win):
                if hasattr(win, fun_name):
                    if getattr(win, fun_name)():
                        event.Enable(True)
                        return
                if propagete:
                    win=win.GetParent()
                else:
                    break
            event.Enable(False)

        self.toolbar_interface.parent.Bind(wx.EVT_UPDATE_UI, on_update_ui, id=event_id)

    def make_handler(self, fun_name, event_id, propagate=False):
        def on_command(event):
            win = wx.Window.FindFocus()
            while(win):
                if hasattr(win, fun_name):
                    getattr(win, fun_name)()
                if propagate:
                    win = win.GetParent()
                else:
                    break
        self.toolbar_interface.bind(on_command, id=event_id)

    def make_handlers(self, event_id, fun_name, fun_name2=None, propagate=False):
        self.make_handler(fun_name, event_id, propagate)
        if fun_name2:
            self.make_ui_handler(fun_name2, event_id, propagate)

    def create_file_panel(self, toolbar_page):
        if self.file:
            bar = self.ti.create_panel_in_main_page(_('File'), TYPE_TOOLBAR)
            self.tbs['file'] = {}
            self.tbs['file']['bar'] = bar
            if 'exit' in self.gui_style:
                self.tbs['file']['exit'] = bar.add_simple_tool(wx.ID_EXIT, _('Exit'),
                    bitmaps_from_art_id(wx.ART_QUIT, wx.Size(32, 32)))
            test = False
            if 'open' in self.gui_style:
                bar.add_separator()
                self.tbs['file']['open'] = bar.add_simple_tool(wx.ID_OPEN, _('Open'),
                    bitmaps_from_art_id(wx.ART_FILE_OPEN, wx.Size(32, 32)))
                test = True
            if 'save' in self.gui_style:
                if not test:
                    bar.add_separator()
                self.tbs['file']['save'] = bar.add_simple_tool(wx.ID_SAVE, _('Save'),
                    bitmaps_from_art_id(wx.ART_FILE_SAVE, wx.Size(32, 32)))
                self.make_handlers(wx.ID_SAVE, 'Save', 'CanSave', propagate=True)
                if 'save_as' in self.gui_style:
                    self.tbs['file']['save_as'] = bar.add_simple_tool(wx.ID_SAVEAS, _('Save as'),
                        bitmaps_from_art_id(wx.ART_FILE_SAVE_AS, wx.Size(32, 32)))
                    self.make_handlers(wx.ID_SAVEAS, 'SaveAs', 'CanSaveAs', propagate=True)
                test = True
            if 'print' in self.gui_style:
                if test:
                    bar.add_separator()
                    self.tbs['file']['print'] = bar.AddHybridTool(ID_PRINT, _('Print'),
                        bitmaps_from_art_id(wx.ART_PRINT, wx.Size(32, 32)))
                    bar.add_separator()
                else:
                    self.tbs['file']['print'] = bar.AddHybridTool(ID_PRINT, _('Print'),
                        bitmaps_from_art_id(wx.ART_PRINT, wx.Size(32, 32)))
                self.make_handlers(ID_PRINT, 'Print', 'CanPrint', propagate=True)
                self.ti.bind_dropdown(self.on_print, ID_PRINT)

    def create_edit_panel(self, toolbar_page):
        if self.clipboard:
            self.tbs['clipboard'] = {}
            bar = self.ti.create_panel_in_main_page(_('Clipboard'), TYPE_BUTTONBAR)
            bar.Refr = self.clipboard_refr
            self.tbs['clipboard']['bar'] = bar
            self.tbs['clipboard']['copy'] = bar.add_simple_tool(wx.ID_COPY, _('Copy'),
                bitmaps_from_art_id(wx.ART_COPY, wx.Size(32, 32)))
            self.tbs['clipboard']['cut'] = bar.add_simple_tool(wx.ID_CUT, _('Cut'),
                bitmaps_from_art_id(wx.ART_CUT, wx.Size(32, 32)))
            self.tbs['clipboard']['paste'] = bar.add_simple_tool(wx.ID_PASTE, _('Paste'),
                bitmaps_from_art_id(wx.ART_PASTE, wx.Size(32, 32)))

            self.make_handlers(wx.ID_COPY, 'Copy', 'CanCopy')
            self.make_handlers(wx.ID_CUT, 'Cut', 'CanCut')
            self.make_handlers(wx.ID_PASTE, 'Paste', 'CanPaste')

    def create_operations_panel(self, toolbar_page):
        if self.operations:
            self.tbs['operations'] = {}
            bar = self.ti.CreatePanelInMainPage(_('Operations'), TYPE_TOOLBAR)
            self.tbs['operations']['bar'] = bar
            self.tbs['operations']['undo'] = bar.add_simple_tool(wx.ID_UNDO, _('Undo'),
                    bitmaps_from_art_id(wx.ART_UNDO, wx.Size(32, 32)))
            self.tbs['operations']['redo'] = bar.add_simple_tool(wx.ID_REDO, _('Redo'),
                    bitmaps_from_art_id(wx.ART_REDO, wx.Size(32, 32)))
            self.tbs['operations']['find'] = bar.add_hybrid_tool(ID_FIND, _('Find'),
                    bitmaps_from_art_id(wx.ART_FIND, wx.Size(32, 32)))
            bar.AddSeparator()
            self.tbs['operations']['filemanager'] = bar.add_simple_tool(wx.ID_ANY,
                    _('File manager'), bitmaps_from_art_id(wx.ART_FOLDER_OPEN, wx.Size(32, 32)))
            self.tbs['operations']['editor'] = bar.add_simple_tool(wx.ID_ANY, _('Editor'),
                    bitmaps_from_art_id(wx.ART_NORMAL_FILE, wx.Size(32, 32)))
            self.ti.bind_dropdown(self.on_find, ID_FIND)

            self.make_handlers(wx.ID_UNDO, 'Undo', 'CanUndo')
            self.make_handlers(wx.ID_REDO, 'Redo', 'CanRedo')
            self.make_handlers(ID_FIND, 'Find', 'CanFind')

    def create_browse_panel(self, toolbar_page):
        if self.browse or self.nav:
            self.tbs['browser'] = {}
            bar = self.ti.create_panel_in_main_page(_('Browser'), TYPE_BUTTONBAR)
            bar.Refr = self.web_refr
            self.webobject = None
            self.tbs['browser']['bar'] = bar
            self.tbs['browser']['back'] = bar.add_simple_tool(ID_WEB_BACK, _('Back'),
                bitmaps_from_art_id(wx.ART_GO_BACK, wx.Size(32, 32)))
            self.tbs['browser']['forward'] = bar.add_simple_tool(ID_WEB_FORWARD, _('Forward'),
                bitmaps_from_art_id(wx.ART_GO_FORWARD, wx.Size(32,32)))
            self.make_handlers(ID_WEB_BACK, 'WebBack', 'CanWebBack', propagate=True)
            self.make_handlers(ID_WEB_FORWARD, 'WebForward', 'CanWebForward', propagate=True)

            if self.browse:
                self.tbs['browser']['stop'] = bar.add_simple_tool(ID_WEB_STOP, _('Stop'),
                    bitmaps_from_art_id(wx.ART_CROSS_MARK, wx.Size(32, 32)))
                self.tbs['browser']['refresh'] = bar.add_simple_tool(ID_WEB_REFRESH, _('Refresh'),
                    bitmaps_from_art_id(wx.ART_GO_TO_PARENT, wx.Size(32, 32)))
                self.tbs['browser']['addbookmark'] =  bar.add_simple_tool(ID_WEB_ADDBOOKMARK, _('Add bookmark'),
                    bitmaps_from_art_id(wx.ART_ADD_BOOKMARK, wx.Size(32,32)))
                self.tbs['browser']['newpage'] = bar.add_simple_tool(ID_WEB_NEW_WINDOW, _('New page'),
                    bitmaps_from_art_id(wx.ART_NEW, wx.Size(32, 32)))

                self.make_handlers(ID_WEB_STOP, 'WebStop', 'CanWebStop', propagate=True)
                self.make_handlers(ID_WEB_REFRESH, 'WebRefresh', 'CanWebRefresh', propagate=True)
                self.make_handlers(ID_WEB_ADDBOOKMARK, 'WebAddBookmark', 'CanWebAddBookmark', propagate=True)
                self.make_handlers(ID_WEB_NEW_WINDOW, 'WebNewWindow', "IsFocusable", propagate=None)
        else:
            self.tbs['browser'] = {}
            self.tbs['browser']['bar'] = EmptyBar()

    def create_address_panel(self, toolbar_page):
        if self.address_bar:
            bar = self.ti.create_panel_in_main_page(_('Address'),
                    TYPE_PANELBAR)
            if hasattr(bar, 'panel'):
                width = 350
                panel = bar.panel
                self.address = SchAutoComplete(panel, size=wx.Size(width, -1))
                self.address.SetCallbackFun(self.OpenPage)
                self.tbs['browser']['address'] = self.address
                self.webmenu = FM.FlatMenuBar(panel, spacer=5)
                self.webmenu.GetRendererManager().SetTheme(FM.Style2007)
                self.tbs['browser']['webmenu'] = self.webmenu
                webmenu_source = self.WebMenu()
                self.web_info = wx.html.HtmlWindow(panel,
                        style=wx.html.HW_SCROLLBAR_NEVER, size=(width, 25))
                self.web_info.SetBorders(0)
                self._info_clear()
                self.MemkeMenu(self.webmenu, webmenu_source)
                controls = (self.address, self.web_info, self.webmenu)
                controls = (self.webmenu, self.web_info, self.address)
                bar.AddPanel(controls)
            else:
                self.tbs['browser']['address'] = EmpytControl()
                self.web_info = None
        else:
            self.tbs['browser']['address'] = EmpytControl()
            self.web_info = None

    def load_page(self, address):
        if 'browser' in self._object_list and self._object_list['browser']:
            self._object_list['browser'].Go(address)

    def _title_from_address(self, address):
        x = address.replace(r'http://', '')
        if len(x) > 20:
            x = x[:16] + ' ...'
        return x

    def _status(self, tab):
        start_status = []
        dis = self.ti.status_tool_disabled()
        for pos in tab:
            start_status.append(self.tbs[pos[1]][pos[2]].state & dis)
            if pos[0]:
                self.tbs[pos[1]][pos[2]].state &= ~dis
            else:
                self.tbs[pos[1]][pos[2]].state |= dis
        i = 0
        for pos in tab:
            if start_status[i] != self.tbs[pos[1]][pos[2]].state & dis:
                self.tbs[pos[1]]['bar'].Refresh()
                return
            i += 1

    def clipboard_refr(self, editctrl):
        if self.clipboard:
            tab_status = []
            if editctrl:
                tab_status.append((hasattr(editctrl, 'CanCopy')
                                   and editctrl.CanCopy(), 'clipboard', 'copy'))
                tab_status.append((hasattr(editctrl, 'CanCut')
                                   and editctrl.CanCut(), 'clipboard', 'cut'))
                tab_status.append((hasattr(editctrl, 'CanPaste')
                                   and editctrl.CanCut(), 'clipboard', 'paste'))
            else:
                tab_status.append((False, 'clipboard', 'copy'))
                tab_status.append((False, 'clipboard', 'cut'))
                tab_status.append((False, 'clipboard', 'paste'))
            return self._status(tab_status)

    def opeartions_refr(self, editctrl):
        if self.operations:
            tab_status = []
            if editctrl:
                tab_status.append((hasattr(editctrl, 'CanRedo')
                                   and editctrl.CanCopy(), 'operations', 'redo'
                                  ))
                tab_status.append((hasattr(editctrl, 'CanUndo')
                                   and editctrl.CanCut(), 'operations', 'undo'))
            else:
                tab_status.append((False, 'operations', 'redo'))
                tab_status.append((False, 'operations', 'undo'))
            return self._status(tab_status)

    def web_refr(self, webobject):
        if self.browse or self.nav:
            tab_status = []
            if webobject:
                tab_status.append((webobject.CanGoBack(), 'browser', 'back'))
                tab_status.append((webobject.CanGoForward(), 'browser',
                                  'forward'))
                if self.browse:
                    tab_status.append((True, 'browser', 'stop'))
                    tab_status.append((True, 'browser', 'refresh'))
                    tab_status.append((True, 'browser', 'addbookmark'))
                    tab_status.append((True, 'browser', 'newpage'))
            else:
                tab_status.append((False, 'browser', 'back'))
                tab_status.append((False, 'browser', 'forward'))
                if self.browse:
                    tab_status.append((False, 'browser', 'stop'))
                    tab_status.append((False, 'browser', 'refresh'))
                    tab_status.append((False, 'browser', 'addbookmark'))
                    tab_status.append((False, 'browser', 'newpage'))
            return self._status(tab_status)

    def address_refr(self, panel):
        if self.address_bar:
            if panel is not None and hasattr(panel.body, 'WEB'):
                ctrl = panel.body.WEB
                if hasattr(ctrl, 'GetStatus'):
                    status = ctrl.GetStatus()
                    if status['progress'] >= 0:
                        self._info_proc(status['txt'].replace('INFO:', ''
                                        ).replace('ERROR:', ''),
                                        status['progress'])
                    else:
                        if status['txt'] and status['txt'] != '':
                            if 'ERROR:' in status['txt']:
                                self._info_alarm(status['txt'].replace('ERROR:'
                                        , ''))
                            else:
                                self._info_txt(status['txt'].replace('INFO:', ''
                                        ))
                        else:
                            self._info_clear()
                    if self.address_txt != status['address']:
                        if status['address']:
                            self.address.SetValue(status['address'])
                            self.address_txt = status['address']
                        else:
                            self.address.SetValue('')
                            self.address_txt = ''
            else:
                if self.address_txt != '':
                    self.address.SetValue('')
                    self.address_txt = ''
                self._info_clear()

    def _info_proc(self, txt, proc):
        if self.web_info and (txt != self.info or proc != self.progress):
            if txt and txt != '':
                self.web_info.SetPage("<body bgcolor='%s'><table width='100%%'><tr><td bgcolor='%s' width='%s%%'></td><td ></td></tr><tr><td colspan='2' td bgcolor='%s'><small>%s</small></td></tr></table></body>"
                                       % (self.bg, self.bg_h, proc,
                                      self.bg_info, txt))
            else:
                self.web_info.SetPage("<body bgcolor='%s'><table width='100%%'><tr><td bgcolor='%s' width='%s%%'></td><td ></td></tr></table></body>"
                                       % (self.bg, self.bg_h, proc))
            self.info = txt
            self.progress = proc

    def _info_txt(self, txt):
        if self.web_info and txt != self.info:
            self.web_info.SetPage("<body bgcolor='%s'><table width='100%%'><tr><td bgcolor='%s'><strong><small>%s</small></strong></tr></td></table></body>"
                                   % (self.bg, self.bg_info, txt))
            self.info = txt
            self.progress = -1

    def _info_alarm(self, txt):
        if self.web_info and txt != self.info:
            self.web_info.SetPage("<body bgcolor='%s'><table width='100%%'><tr><td bgcolor='%s'><strong><small>%s</small></strong></tr></td></table></body>"
                                   % (self.bg, self.bg_info, txt))
            self.info = txt
            self.progress = -1

    def _info_clear(self):
        if self.web_info and (self.info != '' or self.progress != -1):
            self.web_info.SetPage("<body bgcolor='%s'></body>" % self.bg)
            self.info = ''
            self.progress = -1

    def open_page(self, page):
        name = self._title_from_address(page)
        okno = \
            wx.GetApp().GetTopWindow().new_main_page('^standard/webview/widget_web.html'
                , name)
        okno.body.WEB.Go(page)
        return True


    def on_print(self, event):
        menu = FM.FlatMenu()
        menu.Append(wx.ID_ANY, _('Print'), _('Print'), wx.ITEM_NORMAL)
        menu.Append(wx.ID_ANY, _('Print preview'), _('Print preview'), wx.ITEM_NORMAL)
        menu.Append(wx.ID_ANY, _('Printer settings'), _('Printer settings'),
                    wx.ITEM_NORMAL)
        self.ti.popup_menu(event, menu)

    def on_find(self, event):
        menu = FM.FlatMenu()
        menu.Append(wx.ID_ANY, _('Find'), _('Find'), wx.ITEM_NORMAL)
        menu.Append(wx.ID_ANY, _('Replace'), _('Replace'), wx.ITEM_NORMAL)
        event.PopupMenu(menu)

    def memke_menu(self, menubar, menulist):
        for item in menulist:
            menu = FM.FlatMenu()
            for pos in item[1]:
                menuitem = FM.FlatMenuItem(menu, pos[1], pos[0], pos[0],
                        wx.ITEM_NORMAL)
                menu.AppendItem(menuitem)
            menubar.Append(menu, item[0])

    def web_menu(self):
        menu = (  # ('Page source', ID_PAGE_SOURCE),
            (_('View'), ((_('Zoom'), ID_ZOOM), (_('Block elements'), ID_PAGE_BLOCK),
             (_('View elements'), ID_PAGE_VIEW), (_('View page source'),
             ID_WEB_SOURCE), (_('Edit page'), ID_WEB_EDIT))),
            (_('History'), ((_('Show history panel'), ID_HISTORY_SHOW),
             (_('Clear history'), ID_CLEAR_HISTORY))),
            (_('Bookmarks'), ((_('Add to bookmarks'), ID_BOOKMARK_ADD),
             (_('Show bookmarks panel'), ID_SHOW_BOOKMARKS))),
            (_('Downloads'), ((_('Show download panel'), ID_SHOW_DOWNLOAD), (_('Options')
             , ID_DOWNLOAD_OPTIONS))),
            (_('Tools'), ((_('Show download panel'), ID_SHOW_DOWNLOAD), (_('Options'),
             ID_DOWNLOAD_OPTIONS))),
            (_('Options'), ((_('General'), ID_GENERAL_OPTIONS), (_('Black list'),
             ID_DOWNLOAD_OPTIONS))),
            )
        return menu

    def realize(self):
        pass


