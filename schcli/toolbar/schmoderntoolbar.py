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
import wx.lib.agw.ribbon as RB
from wx.lib.agw.ribbon import art
from schcli.guilib.schevent import *
from schcli.toolbar.basetoolbar import ToolbarInterface, TYPE_TOOLBAR, \
    TYPE_BUTTONBAR, TYPE_PANELBAR

_ = wx.GetTranslation

MswStyle = True
OrgLikePrimary = None

def like_primary(
    primary_hsl,
    h,
    s,
    l,
    x=None,
    ):
    if x != None:
        c1 = OrgLikePrimary(primary_hsl, h, 0, l * 1.5, x)
    else:
        c1 = OrgLikePrimary(primary_hsl, h, 0, l * 1.5)
    c2 = wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DFACE)
    r2 = c2.Red()
    g2 = c2.Green()
    b2 = c2.Blue()
    if r2 == 0:
        r2 = 1
    if g2 == 0:
        g2 = 1
    if b2 == 0:
        b2 = 1
    m = ((1.0 * c1.Red()) / r2 + (1.0 * c1.Green()) / g2 + (1.0 * c1.Blue())
          / b2) / 3
    x1 = int(c2.Red() * m)
    x2 = int(c2.Green() * m)
    x3 = int(c2.Blue() * m)
    if x1 > 255:
        x1 = 255
    if x2 > 255:
        x2 = 255
    if x3 > 255:
        x3 = 255
    c3 = wx.Colour(x1, x2, x3)
    return c3


class RibbonInterface(ToolbarInterface):

    class Page(object):

        class Panel(object):

            def __init__(
                self,
                page,
                title,
                type=TYPE_BUTTONBAR,
                ):
                self.type = type
                self.page = page
                if type == TYPE_PANELBAR:
                    self.panel = SchRibbonPanel(
                        page.page,
                        wx.ID_ANY,
                        title,
                        wx.NullBitmap,
                        wx.DefaultPosition,
                        wx.DefaultSize,
                        RB.RIBBON_PANEL_NO_AUTO_MINIMISE,
                        )
                else:
                    self.panel = RB.RibbonPanel(
                        page.page,
                        wx.ID_ANY,
                        title,
                        wx.NullBitmap,
                        wx.DefaultPosition,
                        wx.DefaultSize,
                        RB.RIBBON_PANEL_NO_AUTO_MINIMISE,
                        )
                self.toolbar = None

            def process_window_event(self, event):
                ret = self.old_process_window_event(event)
                id = event.GetId()

                if (id >= ID_START and id <ID_END) or (id >= wx.ID_LOWEST and id < wx.ID_HIGHEST ):
                    if not ret:
                        win = wx.Window.FindFocus()
                        if win:
                            if type(event)==wx.UpdateUIEvent:
                                ret = win.ProcessEvent(event)
                            else:
                                ret = win.ProcessEvent(event)
                        if not ret:
                            if type(event)==wx.UpdateUIEvent:
                                if type(self.toolbar)==RB.RibbonToolBar:
                                    self.toolbar.EnableTool(event.GetId(), False)
                                elif type(self.toolbar)==RB.RibbonButtonBar:
                                    self.toolbar.EnableButton(event.GetId(), False)
                return ret

            def init_toolbar(self):
                #print(wx.GetApp().GetTopWindow())
                #wx.GetApp().GetTopWindow().idle_objects.append(self)
                topwin = self.page.page.Parent.Parent.idle_objects.append(self)
                self.toolbar.Bind(wx.EVT_CLOSE, self.on_close)
                self.old_process_window_event = self.toolbar.ProcessEvent
                self.toolbar.ProcessEvent = self.process_window_event

            def on_close(self, event):
                if self in wx.GetApp().GetTopWindow().idle_objects:
                    del wx.GetApp().GetTopWindow().idle_objects[self]
                event.Skip()

            def on_idle(self):
                self.toolbar.UpdateWindowUI(wx.UPDATE_UI_FROMIDLE)

            def append(
                self,
                id,
                name,
                bitmap,
                bitmap_disabled=wx.NullBitmap,
                item_type='SIMPLEBUTTON',
                title=None
                ):
                if not self.toolbar:
                    if self.type == TYPE_TOOLBAR:
                        self.toolbar = RB.RibbonToolBar(self.panel)
                    elif self.type == TYPE_BUTTONBAR:
                        self.toolbar = RB.RibbonButtonBar(self.panel)
                    elif self.type == TYPE_PANELBAR:
                        self.toolbar = RB.RibbonPanelBar(self.panel)
                    self.init_toolbar()
                if item_type == 'SIMPLEBUTTON':
                    self.toolbar.AddSimpleButton(id, name, bitmap, '')
                elif item_type == 'TOOL':
                    self.toolbar.AddTool(id, bitmap, bitmap_disabled, name)
                elif item_type == 'HYBRIDTOOL':
                    self.toolbar.AddHybridTool(id, bitmap, name)
                elif item_type == 'BUTTON':
                    self.toolbar.AddButton(id, name, bitmap, bitmap_disabled)
                elif item_type == 'SEPARATOR':
                    #xxx
                    pass
                else:
                    pass

            def add_tool(
                self,
                id,
                title,
                bitmaps,
                ):
                self.append(id, title, bitmaps[0], bitmaps[1], 'TOOL')

            def add_hybrid_tool(
                self,
                id,
                title,
                bitmaps,
                ):
                self.append(id, title, bitmaps[0], bitmaps[1], 'HYBRIDTOOL')

            def add_button(
                self,
                id,
                title,
                bitmaps,
                ):
                self.append(id, title, bitmaps[0], bitmaps[1], 'BUTTON')

            def add_panel(self, controls):
                s = wx.BoxSizer(wx.VERTICAL)
                for c in controls:
                    s.Add(c, 0, wx.LEFT | wx.TOP | wx.EXPAND | wx.RIGHT, 2)
                self.panel.SetSizer(s)
                s.Fit(self.panel)
                minsize = self.panel.GetSize()
                self.panel.SetMinSize(wx.Size(minsize.width, minsize.height))

            def add_separator(self):
                self.append(0, '', None, None, 'SEPARATOR')

        def __init__(
            self,
            bar,
            title,
            page=None,
            ):
            self.bar = bar
            if page:
                self.page = page
            else:
                self.page = RB.RibbonPage(bar.bar, wx.ID_ANY, title)

        def create_panel(self, title, type=TYPE_BUTTONBAR):
            return self.Panel(self, title, type)

    def __init__(self, parent, gui_style):
        self.bar = SchRibbonBar(parent, wx.ID_ANY)
        self.toolbars = {}
        ToolbarInterface.__init__(self, parent, gui_style)

    def close(self):
        self.bar.Destroy()
        self.bar = None

    def create_page(self, title):
        if title == 'main':
            page = self.Page(self, title, self.bar.main_page)
        else:
            page = self.Page(self, title)
        if not self.main_page:
            self.main_page = page
        return page

    def bind(
        self,
        fun,
        id=wx.ID_ANY,
        e=None
        ):
        if e:
            self.parent.Bind(e, fun, id=id)
        else:
            self.parent.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, fun, id=id)
            self.parent.Bind(RB.EVT_RIBBONTOOLBAR_CLICKED, fun, id=id)

    def realize_bar(self):
        self.bar.Realize()

    def get_toolbars(self):
        return self.toolbars

    def connect_object_to_panel(self, panel, object):
        #pass
        return self.standard_buttons.connect_object_to_panel(panel, object)

    def add_tool(
        self,
        bar,
        id,
        caption,
        art_id,
        size,
        ):
        return self.bar.AddTool(bar, id, caption, art_id, size)

    def add_hybrid_tool(
        self,
        bar,
        id,
        caption,
        art_id,
        size,
        ):
        return self.bar.AddHybridTool(bar, id, caption, art_id, size)

    def add_button(
        self,
        bar,
        id,
        caption,
        art_id,
        size,
        ):
        return self.bar.add_button(bar, id, caption, art_id, size)

    def new_tool_bar(self, toolbar_page, caption):
        return self.bar.NewToolBar(toolbar_page, caption)

    def new_tool_panel(self, toolbar_page, caption):
        return SchRibbonPanel(
            toolbar_page,
            wx.ID_ANY,
            caption,
            wx.NullBitmap,
            wx.DefaultPosition,
            wx.DefaultSize,
            RB.RIBBON_PANEL_NO_AUTO_MINIMISE,
            )

    def add_panel(self, panel, controls):
        s = wx.BoxSizer(wx.VERTICAL)
        self.add_spacer(s)
        for c in controls:
            s.Add(c, 0, wx.RIGHT | wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
        panel.SetSizer(s)
        s.Fit(panel)
        minsize = panel.GetSize()
        panel.SetMinSize(wx.Size(minsize.width, minsize.height))

    def new_button_bar(self, toolbar_page, caption):
        return self.bar.NewButtonBar(toolbar_page, caption)

    def Bind(
        self,
        fun,
        id,
        e=None,
        ):
        if e:
            self.bar.Bind(e, fun, id=id)
        else:
            self.bar.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, fun, id=id)

    def bind_dropdown(self, fun, id):
        self.bar.Bind(RB.EVT_RIBBONTOOLBAR_DROPDOWN_CLICKED, fun, id=id)

    def un_bind(self, id, e=None):
        if e:
            self.bar.Unbind(e, id=id)
        else:
            self.bar.Unbind(RB.EVT_RIBBONBUTTONBAR_CLICKED, id=id)

    def status_tool_disabled(self):
        return RB.RIBBON_TOOLBAR_TOOL_DISABLED

    def status_tool_enabled(self):
        return 0

    def add_spacer(self, bar):
        bar.AddSpacer(1)

    def popup_menu(self, event, menu):
        event.PopupMenu(menu)


class SchRibbonPanel(RB.RibbonPanel):

    def __init__(self, *argi, **argv):
        RB.RibbonPanel.__init__(self, *argi, **argv)

    def get_panel(self):
        return self.GetParent()

    def layout(self):
        wx.PyControl.Layout(self)

    def do_get_best_size(self):
        return self.GetMinSize()


class RibbonUserPanel(RB.RibbonControl):

    def __init__(
        self,
        parent,
        id=wx.ID_ANY,
        pos=wx.DefaultPosition,
        size=wx.DefaultSize,
        style=RB.RIBBON_PANEL_DEFAULT_STYLE,
        name='RibbonUserPanel',
        ):
        self.pos = pos
        self.size = wx.Size(size[0], size[1])
        RB.RibbonControl.__init__(
            self,
            parent,
            id,
            pos,
            size,
            wx.BORDER_NONE,
            name=name,
            )

    def get_min_size(self):
        return self.size

    def det_next_smaller_size(self, direction, relative_to):
        return self.GetMinSize()

    def do_get_next_larger_size(self, direction, relative_to):
        return self.GetMinSize()


class SchRibbonToolBar(RB.RibbonToolBar):

    def __init__(self, *argi, **argv):
        return RB.RibbonToolBar.__init__(self, *argi, **argv)

    def popup_menu(self, menu, pos):
        menu.Popup(self.ClientToScreen(pos), None)

    def on_paint(self, event):
        dc = wx.AutoBufferedPaintDC(self)
        if self._art == None:
            return
        self._art.DrawToolBarBackground(dc, self, wx.RectS(self.GetSize()))
        for group in self._groups:
            tool_count = len(group.tools)
            if tool_count != 0:
                self._art.DrawToolGroupBackground(dc, self,
                        wx.RectPS(group.position, group.size))
                for tool in group.tools:
                    rect = wx.RectPS(group.position + tool.position, tool.size)
                    if tool.state & RB.RIBBON_TOOLBAR_TOOL_DISABLED:
                        bitmap = tool.bitmap_disabled
                    else:
                        bitmap = tool.bitmap
                    self._art.DrawTool(
                        dc,
                        self,
                        rect,
                        bitmap,
                        tool.kind,
                        tool.state,
                        )

    def append_min_height(self, height):
        tool = RB.RibbonToolBarToolBase()
        tool.id = -1
        tool.bitmap = wx.EmptyBitmap(1, height)
        tool.bitmap_disabled = self.MakeDisabledBitmap(tool.bitmap)
        tool.help_string = ''
        tool.kind = RB.RIBBON_BUTTON_NORMAL
        tool.client_data = None
        tool.position = wx.Point(0, 0)
        tool.size = wx.Size(0, 0)
        tool.state = 0
        self._groups[-1].tools.append(tool)
        return tool


class SchRibbonBar(RB.RibbonBar):

    def __init__(self, *argi, **argv):
        RB.RibbonBar.__init__(self, *argi, **argv)
        self.bestsize = None
        page = self.new_page(_('Tools main'))
        self.main_page = page
        self.Bind(wx.EVT_RIGHT_UP, self.on_r_up)


    def SetActivePage1(self, page):
        w = self.DoGetBestSize().GetHeight()
        RB.RibbonBar.SetActivePage1(self, page)
        if self.DoGetBestSize().GetHeight() > w:
            self.GetParent().Layout()

    def new_page(self, txt):
        return RB.RibbonPage(self, wx.ID_ANY, txt, wx.NullBitmap)

    def new_button_bar(self, page, txt):
        panel = RB.RibbonPanel(
            page,
            wx.ID_ANY,
            txt,
            wx.NullBitmap,
            wx.DefaultPosition,
            wx.DefaultSize,
            RB.RIBBON_PANEL_NO_AUTO_MINIMISE,
            )
        bar = RB.RibbonButtonBar(panel)
        return bar

    def new_tool_bar(self, page, txt):
        panel = RB.RibbonPanel(
            page,
            wx.ID_ANY,
            txt,
            wx.NullBitmap,
            wx.DefaultPosition,
            wx.DefaultSize,
            RB.RIBBON_PANEL_NO_AUTO_MINIMISE,
            )
        bar = SchRibbonToolBar(panel)
        bar.SetRows(2, 2)
        return bar

    def add_button(
        self,
        bar,
        id,
        txt,
        bmp,
        size,
        ):
        bitmap = wx.ArtProvider.GetBitmap(bmp, wx.ART_OTHER, size)
        img = bitmap.ConvertToImage()
        bitmap_disabled = \
            wx.BitmapFromImage(img.ConvertToGreyscale().AdjustChannels(1, 1, 1,
                               0.3))
        return bar.AddButton(id, txt, bitmap, bitmap_disabled=bitmap_disabled)


    def add_tool(
        self,
        bar,
        id,
        txt,
        bmp,
        size,
        ):
        bitmap = wx.ArtProvider.GetBitmap(bmp, wx.ART_OTHER, size)
        img = bitmap.ConvertToImage()
        bitmap_disabled = \
            wx.BitmapFromImage(img.ConvertToGreyscale().AdjustChannels(1, 1, 1,
                               0.3))
        return bar.AddTool(id, bitmap, bitmap_disabled, txt)

    def add_hybrid_tool(
        self,
        bar,
        id,
        txt,
        bmp,
        size,
        ):
        return bar.AddHybridTool(id, wx.ArtProvider.GetBitmap(bmp,
                                 wx.ART_OTHER, size), txt)

    def bind_to_toolbar(self, funct, id):
        self.Bind(RB.EVT_RIBBONTOOLBAR_DROPDOWN_CLICKED, funct, id=id)

    def on_command(self, event):
        event.Skip()

    def Realize(self):
        if MswStyle:
            global OrgLikePrimary
            if not OrgLikePrimary:
                OrgLikePrimary = RB.art_msw.LikePrimary
                RB.art_msw.LikePrimary = like_primary
            provider = RB.RibbonMSWArtProvider()
            (dummy, secondary, tertiary) = provider.GetColourScheme(None, 1, 1)
            colour = wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DFACE)
            #colour2 = wx.SystemSettings.GetColour(wx.SYS_COLOUR_MENUTEXT)
            colour2 = wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNTEXT)
            #colour2 = wx.Colour(0,0,0)
            provider.SetColourScheme(colour, secondary, colour2)
            provider._tab_label_colour = colour2
            provider._button_bar_label_colour = colour2
        else:
            provider = RB.RibbonAUIArtProvider()
        self.SetArtProvider(provider)
        RB.RibbonBar.Realize(self)

    
    def update(self):
        size = self.GetSize()
        self.SetSize(wx.Size(size.GetWidth() - 1, size.GetHeight()))
        self.SetSize(wx.Size(size.GetWidth(), size.GetHeight()))

    def on_r_up(self, event):
        menu = wx.Menu()
        menu.Append(ID_Reset, 'Restart toolbar')
        menu.Append(ID_Exit, 'Close app')
        menu.Append(ID_Help, 'Help')
        self.PopupMenu(menu)
        menu.Destroy()
        event.Skip()

    def get_bar_height(self):
        #s = (32, 32)
        s = (48,48)
        ret = self.GetArtProvider().GetButtonBarButtonSize(
            self,
            self,
            art.RIBBON_BUTTON_NORMAL,
            art.RIBBON_BUTTONBAR_BUTTON_LARGE,
            'TXT',
            s,
            s,
            )
        size_ret = ret[1]
        return size_ret.GetHeight()

    def get_bar_width(self):
        #return 800
        return 2000

    def new_child_page(
        self,
        address_or_parser,
        title='',
        param=None,
        ):
        return wx.GetApp().GetTopWindow().new_main_page(address_or_parser, title,
                param)

    def new_main_page(
        self,
        address_or_parser,
        title='',
        param=None,
        panel='Desktop',
        ):
        return wx.GetApp().GetTopWindow().new_main_page(address_or_parser, title,
                param, panel)

    def remove_page(self, page):
        self.SetActivePage(0)
        for page_info in self._pages:
            if page_info.page == page:
                self._pages.remove(page_info)
        self.Update()


