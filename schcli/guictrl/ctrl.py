#!/usr/bin/python
# -*- coding: utf-8 -*-
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation; either version 3, or (at your option) any later
# version.
#
# This progr                                                                        am is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of ME                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             RCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.

#Pytigon - wxpython and django application framework

#author: "Sławomir Chołaj (slawomir.cholaj@gmail.com)"
#copyright: "Copyright (C) ????/2012 Sławomir Chołaj"
#license: "LGPL 3.0"
#version: "0.1a"

#from cStringIO import StringIO
#from urlparse import urlparse
#from urllib import unquote
from base64 import b64encode
import os
import platform
import datetime
import string

import wx
import six
from schlib.schtools import schjson


#from wx import calendar, combo, gizmos
if six.PY2:
    from wx.combo import ComboCtrl, BitmapComboBox
    from wx.gizmos import TreeListCtrl, EditableListBox
    from wx.calendar import CalendarCtrl
    from wx import DatePickerCtrl
else:
    from wx import ComboCtrl
    from wx.adv import BitmapComboBox, CalendarCtrl, EditableListBox, DatePickerCtrl
    from wx.lib.agw.hypertreelist import HyperTreeList as TreeListCtrl


import wx.lib.agw.pycollapsiblepane as PCP

#else:
#    from wx.combo import ComboCtrl, BitmapComboBox
#    from wx import DatePickerCtrl
#    from wx.gizmos import TreeListCtrl, EditableListBox
#    from wx.gizmos import EditableListBox 
#    from agw.customtreectrl import CustomTreeCtrl as TreeListCtrl
#    from wx.lib.agw.hypertreelist import HyperTreeList as TreeListCtrl
#    from wx.calendar import CalendarCtrl

#from wx.lib.agw.hypertreelist import HyperTreeList as TreeListCtrl
#from wx.lib import intctrl, ticker, masked, colourselect, filebrowsebutton
from wx.lib import ticker, masked, colourselect, filebrowsebutton

#from schlib.schclilib import htmltab, list_parser, createparm, schhtml_parser
from schlib.schtools import createparm
from schlib.schhttptools.schhtml_parser import ShtmlParser

from schcli.guilib import event
from schcli.guictrl.grid import grid, datasource, tabproxy
from schcli.guiframe import form, page

from schcli.guictrl.grid.gridlist import SimpleDataTable
from schcli.guictrl.grid.gridpanel import SchGridPanel
from schcli.guictrl.popup.popuphtml import DataPopupControl

import wx.lib.imagebrowser
import wx.lib.platebtn as platebtn
import wx.lib.buttons  as  buttons

from schlib.schhtml.wxdc import DcDc
from schlib.schhtml.htmlviewer import HtmlViewerParser

from schcli.guictrl.basectrl import SchBaseCtrl
from schcli.guictrl.button.toolbarbutton import BitmapTextButton
from schcli.guilib.tools import bitmap_from_href

from schcli.guictrl.composite.base import COMPOSITE_PANEL


def SELECT(*args, **kwds):
    size = 1
    multiple = False

    if 'param' in kwds:
        param = kwds['param']
        if 'multiple' in param:
            multiple = True
        if 'size' in param:
            size = int(param['size'])
        if multiple and size == 1:
            size = 10
    else:
        size = 1
        multiple = False

    if size == 1:
        kwds['readonly'] = True
        return DBCHOICE(*args, **kwds)
    else:
        kwds['length'] = size
        return HTMLLISTBOX(*args, **kwds)


def BUTTON(*args, **kwds):
    if 'src' in kwds:
        ctrl = BITMAPBUTTON(*args, **kwds)
    else:
        ctrl = SIMPLE_BUTTON(*args, **kwds)
    return ctrl

def _make_button_class(base_class, is_bitmap_button=False, is_close_button=False, icon_size=2):
    class BUTTONCLASS(base_class, SchBaseCtrl):
        def __init__(self, *args, **kwds):
            SchBaseCtrl.__init__(self, args, kwds)
            if is_bitmap_button:
                self._set_bitmap()
                if base_class == buttons.GenBitmapButton or base_class == BitmapTextButton:
                    if "style" in kwds:
                        style = kwds["style"] | wx.NO_BORDER
                        kwds["style"] = style
                    else:
                        style = wx.NO_BORDER
                        kwds["style"] = wx.NO_BORDER
                    kwds["bitmap"] = self.bmp
                elif base_class == buttons.GenBitmapTextButton:
                    kwds["bitmap"] = self.bmp
                elif base_class == platebtn.PlateButton:
                    kwds["style"] = platebtn.PB_STYLE_SQUARE | platebtn.PB_STYLE_GRADIENT
                    #| platebtn.PB_STYLE_NOBG
                    kwds["bmp"] = self.bmp
                else:
                    if "style" in kwds:
                        style = kwds["style"]
                    else:
                        kwds["style"] = 0
                        style = 0
                    kwds["bitmap"] = self.bmp

                if base_class != wx.BitmapButton:
                    if self.label:
                        kwds['label']=self.label.replace('&','')
#                        if base_class == BitmapTextButton:
#                            self.SetToolTip(wx.ToolTip(self.label))
            else:
                if "style" not in kwds:
                    kwds["style"] = 0
                    style = 0
                if self.label:
                    kwds['label']=self.label.replace('&','')
                if self.nr_id:
                    try:
                        nr_id = int(self.nr_id)
                    except:
                        if 'wx.' in self.nr_id:
                            nr_id=eval(self.nr_id)
                        else:
                            nr_id = None
                    if nr_id != None:
                        kwds['id']=nr_id

            if 'fields' in kwds:
                self.fields = kwds['fields']
                del kwds['fields']
            else:
                self.fields = None

            base_class.__init__(self, *args, **kwds)

            if self.defaultvalue:
                self.SetDefault()
                self.parent.any_parent_command('set_default_button',self)

            if is_bitmap_button and self.label:
                self.SetToolTip(self.label.replace('&',''))

            if is_close_button:
                self.Bind(wx.EVT_BUTTON, self.on_exit)
            else:
                self.Bind(wx.EVT_BUTTON, self.on_click, self)

            if self.label and base_class == BitmapTextButton:
                self.SetToolTip(wx.ToolTip(self.label.replace('&','')))

            if self.label and '&' in self.label:
                id = self.label.find('&')
                l = self.label[id+1:id+2]
                if l:
                    aTable = [ (wx.ACCEL_ALT, ord('N'), self.on_acc_click),]
                    self.set_acc_key_tab(aTable)

            self.Init2()


        def on_acc_click(self, event):
            evt = wx.PyCommandEvent(wx.EVT_BUTTON.typeId, self.GetId())
            wx.PostEvent(self, evt)

        def _set_bitmap(self):
            self.bmp = None
            if is_bitmap_button:
                if is_close_button:
                    self.src="client://emblems/emblem-unreadable.png"
                if self.src:
                    #print(self.src)
                    self.bmp = bitmap_from_href(self.src, icon_size)

        def process_refr_data(self, *args, **kwds):
            self.init_base(args, kwds)

            if is_bitmap_button:
                self._set_bitmap()

                if base_class == platebtn.PlateButton:
                    kwds["bmp"] = self.bmp
                else:
                    kwds["bitmap"] = self.bmp

            if 'fields' in kwds:
                self.fields = kwds['fields']
                del kwds['fields']
            else:
                self.fields = None

            if 'href' in kwds:
                self.href = kwds['href']
                del kwds['href']

            if self.defaultvalue:
                self.SetDefault()
                #self.parent.any_parent_command('SetDefaultButton',self)

            self.Init2()

        def Init2(self):
            if self.href=="_hide":
                self.Hide()
            else:
                self.Show()
            if self.href=="_disable":
                self.Enable(False)
            else:
                self.Enable(True)
            if not self.style:
                self.style=0

        def CanAcceptFocus(self):
            return False

        if is_close_button:
            def on_exit(self, event):
                def fun():
                    self.GetParent().any_parent_command('on_child_form_cancel')
                wx.CallAfter(fun)
        else:
            def on_click(self, event):
                upload = False
                if self.valuetype == 'upload':
                    upload = True
                self.get_parent_form().href_clicked(self, { 'href': self.href, 'target': self.target}, upload, self.fields, self.param)

    return BUTTONCLASS

SIMPLE_BUTTON = _make_button_class(wx.Button)

BITMAPBUTTON = _make_button_class(wx.BitmapButton, is_bitmap_button=True)
PLATEBUTTON = _make_button_class(platebtn.PlateButton, is_bitmap_button=True)
GENBITMAPBUTTON = _make_button_class(buttons.GenBitmapButton, is_bitmap_button=True)
GENBITMAPTEXTBUTTON = _make_button_class(buttons.GenBitmapTextButton, is_bitmap_button=True)
GENBITMAPBUTTONTXT = _make_button_class(BitmapTextButton, is_bitmap_button=True)
GENBITMAPBUTTONTXT_SMALL = _make_button_class(BitmapTextButton, is_bitmap_button=True, icon_size=1)

#NOBG_BUTTON = GENBITMAPBUTTON
NOBG_BUTTON = GENBITMAPBUTTONTXT
NOBG_BUTTON_TXT = GENBITMAPBUTTONTXT
#CLOSEBUTTON = _make_button_class(buttons.GenBitmapButton, is_bitmap_button=True, is_close_button = True)
CLOSEBUTTON = _make_button_class(BitmapTextButton, is_bitmap_button=True, is_close_button = True)


def _make_menu_button_class(base_class):
    class _MENUBUTTON(base_class):
        def __init__(self,  *args, **kwds):
            base_class.__init__(self, *args, **kwds)
            ldata = self.get_ldata()
            self._menu = None
            self.href_dict = {}
            if ldata:
                menu = wx.Menu()
                for row in ldata:
                    menu.Append(wx.NewId(), row[0], row[2]['href'])
                    self.href_dict[row[0]] = row[2]
                self.SetMenu(menu)

            self.Bind(wx.EVT_MENU, self.on_menu)
            self.Bind(wx.EVT_BUTTON, self.on_button)

        def on_button(self, evt):
            self.ShowMenu()

        def on_menu(self, evt):
            e_obj = evt.GetEventObject()
            mitem = e_obj.FindItemById(evt.GetId())
            if mitem != wx.NOT_FOUND:
                label = mitem.GetItemLabel()
                item = self.href_dict[label]
                self.GetParent().href_clicked(self, item)

        def SetMenu(self, menu):
            self._menu = menu

        def ShowMenu(self):
            self.PopupMenu(self._menu, 1, self.GetSize()[1]-1)
    return _MENUBUTTON

MENUBUTTON = _make_menu_button_class(SIMPLE_BUTTON)
MENUTOOLBARBUTTON = _make_menu_button_class(GENBITMAPBUTTONTXT)



class CHECKBOX(wx.CheckBox, SchBaseCtrl):

    def __init__(self, *args, **kwds):
        SchBaseCtrl.__init__(self, args, kwds)
        if 'checked' in kwds:
            del kwds['checked']
            checked = True
        else:
            checked = False

        if self.label:
            kwds['label']=self.label

        if 'value' in kwds:
            self.value=kwds['value']
            del kwds['value']
        else:
            self.value = None


        if not self.label:
            if 'style' in kwds:
                kwds['style'] |= wx.ALIGN_RIGHT
            else:
                kwds['style'] = wx.ALIGN_RIGHT

        wx.CheckBox.__init__(self, *args, **kwds)
        if checked:
            self.SetValue(True)

    def process_refr_data(self, *args, **kwds):
        self.init_base(args, kwds)
        if 'checked' in kwds:
            del kwds['checked']
            checked = True
        else:
            checked = False
        if 'value' in kwds:
            self.value=kwds['value']
            del kwds['value']
        else:
            self.value = None

        if checked:
            self.SetValue(True)

    def GetValue(self):
        value = wx.CheckBox.GetValue(self)
        if value == True:
            if self.value:
                return str(self.value)
            else:
                return True
        else:
            return None

    def SetValue(self, value):
        if value.__class__== bool:
            return wx.CheckBox.SetValue(self, value)
        else:
            self.value=value


class CHECKLISTBOX(wx.CheckListBox, SchBaseCtrl):

    def __init__(self, *args, **kwds):
        SchBaseCtrl.__init__(self, args, kwds)
        tdata = self.get_tdata()
        if tdata:
            choices = []
            for row in tdata:
                choices.append(row[0].data)
            kwds["choices"] = choices

        if 'style' in kwds:
            kwds['style'] |= wx.WANTS_CHARS
        else:
            kwds['style'] = wx.WANTS_CHARS
        wx.CheckListBox.__init__(self, *args, **kwds)

    def process_refr_data(self, *args, **kwds):
        self.init_base(args, kwds)
        self.Clear()
        tdata = self.get_tdata()
        if tdata:
            for row in tdata:
                self.Append(row[0].data)

    def Refresh(self):
        self.Clear()
        self.RefreshTDATA()
        tdata = self.get_tdata()
        if tdata:
            for row in tdata:
                self.Append(row[0].data)


ArtIDs = [ "wx.ART_ADD_BOOKMARK",
           "wx.ART_DEL_BOOKMARK",
           "wx.ART_HELP_SIDE_PANEL",
           "wx.ART_HELP_SETTINGS",
           "wx.ART_HELP_BOOK",
           "wx.ART_HELP_FOLDER",
           "wx.ART_HELP_PAGE",
           "wx.ART_GO_BACK",
           "wx.ART_GO_FORWARD",
           "wx.ART_GO_UP",
           "wx.ART_GO_DOWN",
           "wx.ART_GO_TO_PARENT",
           "wx.ART_GO_HOME",
           "wx.ART_FILE_OPEN",
           "wx.ART_FILE_SAVE",
           "wx.ART_FILE_SAVE_AS",
           "wx.ART_PRINT",
           "wx.ART_HELP",
           "wx.ART_TIP",
           "wx.ART_REPORT_VIEW",
           "wx.ART_LIST_VIEW",
           "wx.ART_NEW_DIR",
           "wx.ART_HARDDISK",
           "wx.ART_FLOPPY",
           "wx.ART_CDROM",
           "wx.ART_REMOVABLE",
           "wx.ART_FOLDER",
           "wx.ART_FOLDER_OPEN",
           "wx.ART_GO_DIR_UP",
           "wx.ART_EXECUTABLE_FILE",
           "wx.ART_NORMAL_FILE",
           "wx.ART_TICK_MARK",
           "wx.ART_CROSS_MARK",
           "wx.ART_ERROR",
           "wx.ART_QUESTION",
           "wx.ART_WARNING",
           "wx.ART_INFORMATION",
           "wx.ART_MISSING_IMAGE",
           "wx.ART_COPY",
           "wx.ART_CUT",
           "wx.ART_PASTE",
           "wx.ART_DELETE",
           "wx.ART_NEW",
           "wx.ART_UNDO",
           "wx.ART_REDO",
#           "wx.ART_CLOSE",
           "wx.ART_QUIT",
           "wx.ART_FIND",
           "wx.ART_FIND_AND_REPLACE",
           ]

class BITMAPCOMBOBOX(BitmapComboBox, SchBaseCtrl):

    def __init__(self, *args, **kwds):
        SchBaseCtrl.__init__(self, args, kwds)
        BitmapComboBox.__init__(self, *args, **kwds)
        self.init_default_icons = False
        self.accept_focus = False

    def after_create(self):
        super(BITMAPCOMBOBOX, self).after_create()
        if self.init_default_icons:
            self.init_wx_icons()
            self.init_embeded_icons()
            self.init_fa_icons()

    def init_wx_icons(self):
        for id in ArtIDs:
            artid = eval(id)
            bmp = wx.ArtProvider.GetBitmap(artid, wx.ART_TOOLBAR, (22,22))
            #bmp = wx.ArtProvider.GetBitmap(artid, wx.ART_OTHER)
            self.Append(id, bmp, id)

    def init_embeded_icons(self):
        base_path = wx.GetApp().scr_path+'/schappdata/media/22x22/'
        #print "init_embeded_icons:", base_path
        return self._init_icons(base_path, 'client://')

    def init_fa_icons(self):
        base_path = wx.GetApp().scr_path+'/static/fonts/font-awesome/fonts/22x22/'
        #print "init_embeded_icons:", base_path
        return self._init_icons(base_path, 'fa://')


    def init_extern_icons(self, base_path, prefix):
        return self._init_icons(base_path, prefix)

    def _init_icons(self, base_path, prefix, subpath=None):
        if subpath:
            dirname = os.path.join(base_path, subpath)
        else:
            dirname = base_path

        if os.path.exists(dirname):
            for ff in os.listdir(dirname):
                if os.path.isdir(os.path.join(dirname, ff)):
                    if subpath:
                        self._init_icons(base_path, prefix, os.path.join(subpath,ff))
                    else:
                        self._init_icons(base_path, prefix, ff)
                else:
                    if '.png' in ff.lower():
                        try:
                            path = dirname + "/" + ff
                            image = wx.Image(path)
                            bmp = wx.BitmapFromImage(image)
                            if subpath:
                                id = prefix+subpath+"/"+ff
                            else:
                                id = prefix + ff
                            self.Append(id.replace('\\','/'), bmp, id)
                        except:
                            pass

class GAUGE(wx.Gauge, SchBaseCtrl):

    def __init__(self, *args, **kwds):
        SchBaseCtrl.__init__(self, args, kwds)
        wx.Gauge.__init__(self, *args, **kwds)


    def process_refr_data(self, *args, **kwds):
        self.init_base(args, kwds)
        if self.value:
            self.SetValue(self.value)


class LISTBOX(wx.ListBox, SchBaseCtrl):

    def __init__(self, *args, **kwds):
        SchBaseCtrl.__init__(self, args, kwds)
        self._norefresh = False
        self.retvalues = []
        self.sel = []
        tdata = self.get_tdata()
        i = 0
        if tdata:
            choices = []

            for row in tdata:
                value = row[0].data.split('::')

                if len(value) == 2:
                    self.retvalues.append(value[0])
                    value = value[1]
                else:
                    self.retvalues.append(str(i))
                    value = value[0]

                if value[:2] == "!!":
                    choices.append(str(value[2:]))
                    self.sel.append(i)
                else:
                    choices.append(str(value))

                i = i + 1

            kwds["choices"] = choices

        if self.param and 'multiple' in self.param:
            style = 0
            if "style" in kwds:
                style = kwds["style"]
            style = style | wx.LB_MULTIPLE
            kwds["style"] = style

        wx.ListBox.__init__(self, *args, **kwds)

        for s in self.sel:
            self.SetSelection(s)

    def FindAndSelect(self, item):
        l = self.GetStrings()
        for i in range(len(l)):
            if l[i].startswith(item):
                self.SetSelection(i)
                return

    def BlockRefresh(self, block=True):
        self._norefresh = block

    def Refresh(self):
        if self._norefresh:
            self.Clear()
            self.RefreshTDATA()
            tdata = self.get_tdata()

            if tdata:
                for row in tdata:
                    self.Append(row[0].data)

    def GetValue(self):
        ret = []
        sel = self.GetSelections()
        for s in sel:
            ret.append((self.retvalues)[s])

        return ret


class LIST(wx.ListCtrl, SchBaseCtrl):

    def __init__(self, *args, **kwds):
        SchBaseCtrl.__init__(self, args, kwds)

        if "style" in kwds:
            kwds["style"] = kwds["style"] | wx.LC_REPORT
        else:
            kwds["style"] = wx.LC_REPORT
        kwds["size"]=wx.Size(-1,-1)

        wx.ListCtrl.__init__(self, *args, **kwds)

        tdata = self.get_tdata()
        l = 0
        if tdata:
            test = False
            for row in tdata:

                if test == False:
                    test = True
                    l = len(row)
                    for i in range(l):
                        self.InsertColumn(i, row[i].data)
                else:
                    index = self.InsertStringItem(0, row[0].data)
                    for i in range(1, l):
                        self.SetStringItem(index, i, row[i].data)

            for i in range(0, l):
                self.SetColumnWidth(i, -1)

    def Refresh(self):
        self.ClearAll()
        self.RefreshTDATA()
        tdata = self.get_tdata()
        if tdata:
            test = False
            for row in tdata:
                if test == False:
                    test = True
                    l = len(row)
                    for i in range(l):
                        self.InsertColumn(i, row[i].data)
                else:
                    index = self.InsertStringItem(0, row[0].data)
                    for i in range(1, l):
                        self.SetStringItem(index, i, row[i].data)

    def process_refr_data(self, *args, **kwds):
        self.init_base(args, kwds)
        tdata = self.get_tdata()
        return self.do_refresh(tdata)


class TABLE(SchGridPanel, SchBaseCtrl):

    def get_table_lp(self):
        return self._table_lp

    def set_table_lp(self, table_lp):
        self._table_lp = table_lp

    table_lp = property(get_table_lp, set_table_lp)

    def __init__(self, *args, **kwds):
        SchBaseCtrl.__init__(self, args, kwds)        
        if self.param and 'table_lp' in self.param:
            self.table_lp = int(self.param['table_lp'])
        else:
            self.table_lp = 0

        if 'name' in kwds:
            name = kwds['name']
        else:
            name = 'LIST'

        if 'size' in kwds:
            SchGridPanel.__init__(self, args[0], size=kwds['size'],  name=name)
        else:
            SchGridPanel.__init__(self, args[0], name=name)


        tdata = self.get_tdata()
        if not tdata:
            print("no tdata:", self.href, self.src)
        #for row in tdata:
        #    for item in row:
        #        print "}}}",
        #        for child in item.childs:
        #            print child.__class__.__name__,
        #        print "."
        #print tdata
        #try:
        if tdata:
            #print "++++++++++++++++++++++++++++++++"
            #print tdata
            #print "++++++++++++++++++++++++++++++++"
            table = SimpleDataTable(self, tdata)
            if self.param and 'param' in self.param and 'no_actions' in self.param['param']:
                table.set_no_actions(True)

            #if self.readonly:
            #    table.set_read_only(self.readonly)
            #else:
            #   table.set_read_only(False)
        else:
            table = None
        #else:
        #    table = None
                #table = SimpleDataTable(self, [])
        #except:
        #    print "######################################################"
        #    print "ERROR:", self.href
        #    #print tdata
        #    print "######################################################"

        self.grid = grid.SchTableGrid(table, "", self, typ=grid.SchTableGrid.VIEW, style=wx.TAB_TRAVERSAL | wx.FULL_REPAINT_ON_RESIZE)

        self.GetParent().get_page().register_signal(self, "refresh_controls")
        self.create_toolbar(self.grid)
        #wx.CallAfter(self.CreateToolbar, self.grid)
        self.Bind(wx.EVT_CLOSE, self.on_close)

        self._table = table

    def on_close(self, event):
        self.GetParent().get_page().unregister_signal(self, "refresh_controls")
        event.Skip()

    def GetMinSize(self):
        return SchGridPanel.GetMinSize(self)
    

    def process_refr_data(self, *args, **kwds):
        self.init_base(args, kwds)
        tdata = self.get_tdata()
        return self.do_refresh(tdata)


    def do_refresh(self, tdata):
         
        oldRow = self.grid.GetGridCursorRow()

        self._table.replace_tab(tdata)
        #table = SimpleDataTable(self, tdata)
        #self.grid.SetTable(table)
        #print "UUU:", table

        #return
        #self._table.refresh_page_data(tdata)
        #self.grid.SetTable(self._table)

        self.grid.AutoSizeColumns(False)
        self.grid.AutoSizeRows(True)
        if self.grid.LastAction == 'insert':
            newRow = self.grid.GetGridCursorRow() + 1
            if newRow < self.grid.GetTable().GetNumberRows():
                self.grid.SetGridCursor(newRow, 0)
                self.grid.MakeCellVisible(newRow, 0)
        if self.grid.LastAction == 'edit':
            if oldRow < self.grid.GetTable().GetNumberRows():
                self.grid.SetGridCursor(oldRow, 0)
                self.grid.MakeCellVisible(oldRow, 0)


    def refresh_from_source(self, html_src):
        self.refresh_tdata(html_src)
        tdata = self.get_tdata()
        return self.do_refresh(tdata)


    def refresh_controls(self):
        self.GetParent().enable_ctrls((self,))
        ret = self.GetParent().get_page()._refresh_html()
        self.GetParent().enable_ctrls(None)
        return ret


class RADIOBOX(wx.RadioBox, SchBaseCtrl):

    def __init__(self, *args, **kwds):
        SchBaseCtrl.__init__(self, args, kwds)
        tdata = self.get_tdata()
        if tdata:
            choices = []

            for row in tdata:
                choices.append(row[0].data)

            kwds["choices"] = choices
        wx.RadioBox.__init__(self, *args, **kwds)

    def Refresh(self):
        self.Clear()
        self.RefreshTDATA()
        tdata = self.get_tdata()
        if tdata:

            for row in tdata:
                self.Append(row[0].data)


class RADIOBUTTON(wx.RadioButton, SchBaseCtrl):

    def __init__(self, *args, **kwds):
        #print "RADIOBUTTON!!!!!!!!!!!!!!!!!!!!!"
        SchBaseCtrl.__init__(self, args, kwds)
        parent = args[0]
        if 'name' in kwds:
            name = kwds['name']
            #print "RADIOBUTTON", name
            if not hasattr(parent,name.split('__')[0]):
                if 'style' in kwds:
                    kwds['style'] |= wx.RB_GROUP
                else:
                    kwds['style'] = wx.RB_GROUP

        if 'checked' in kwds:
            del kwds['checked']
            checked = True
        else:
            checked = False
        if 'value' in kwds:
            self.value=kwds['value']
            del kwds['value']
        else:
            self.value = None

        wx.RadioButton.__init__(self, *args, **kwds)
        if checked:
            self.SetValue(True)

    def GetValue(self):
        value = wx.RadioButton.GetValue(self)
        #print "GetValue:", value, self.value
        if value == True:
            if self.value:
                return str(self.value)
            else:
                return None
        else:
            return None

    def SetValue(self, value):
        if value.__class__== bool:
            return wx.RadioButton.SetValue(self, value)
        else:
            self.value=value


class SLIDER(wx.Slider, SchBaseCtrl):

    def __init__(self, *args, **kwds):
        SchBaseCtrl.__init__(self, args, kwds)
        wx.Slider.__init__(self, *args, **kwds)


class SPINBUTTON(wx.SpinButton, SchBaseCtrl):

    def __init__(self, *args, **kwds):
        SchBaseCtrl.__init__(self, args, kwds)
        wx.SpinButton.__init__(self, *args, **kwds)


class SPIN(wx.SpinCtrl, SchBaseCtrl):

    def __init__(self, *args, **kwds):
        SchBaseCtrl.__init__(self, args, kwds)
        wx.SpinCtrl.__init__(self, *args, **kwds)


class STATICTEXT(wx.StaticText, SchBaseCtrl):

    def __init__(self, *args, **kwds):
        SchBaseCtrl.__init__(self, args, kwds)
        wx.StaticText.__init__(self, *args, **kwds)
        if self.label:
            self.SetLabel(self.label)


class ERRORLIST(BitmapTextButton, SchBaseCtrl):
    def __init__(self, *args, **kwds):
        SchBaseCtrl.__init__(self, args, kwds)

        self.bmp = bitmap_from_href("client://status/dialog-error.png",1)

        kwds["style"] = wx.NO_BORDER
        kwds["bitmap"] = self.bmp

        BitmapTextButton.__init__(self, *args, **kwds)
        if self.ldata:
            self.SetToolTip(wx.ToolTip(self.ldata[0][0]))
        else:
            if 'data' in self.param:
                self.SetToolTip(wx.ToolTip(self.param['data']))


class TEXT(SchBaseCtrl, wx.TextCtrl):

    def __init__(self, *args, **kwds):
        SchBaseCtrl.__init__(self, args, kwds)
        if self.param and 'param' in self.param and 'PROCESS_ENTER' in self.param['param']:
            kwds['style']=wx.TE_PROCESS_ENTER        
        wx.TextCtrl.__init__(self, *args, **kwds)
        if self.hidden:
            self.Enable(False)
        if self.maxlength:
            self.SetMaxLength(int(self.maxlength))

    def SetValue(self, value):
        #if value.__class__==str:
        if not isinstance(value, six.text_type):
            return wx.TextCtrl.SetValue(self, value.decode('utf-8'))
        else:
            return wx.TextCtrl.SetValue(self, value)

    def GetBestSize(self):
        size = super().GetBestSize()
        return (4*size[0], size[1])

class SEARCH(wx.SearchCtrl, SchBaseCtrl):

    def __init__(self, *args, **kwds):
        SchBaseCtrl.__init__(self, args, kwds)
        if wx.Platform in ['__WXGTK__',]:
            kwds['size']=(200, 28)
        else:
            kwds['size']=(200, -1)
        kwds['style']=wx.TE_PROCESS_ENTER
        #|wx.WANTS_CHARS
        wx.SearchCtrl.__init__(self, *args, **kwds)
        #self.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, self.OnCancel)

        if wx.Platform in ['__WXGTK__', '__WXMSW__']:
             for child in self.GetChildren():
                 if isinstance(child, wx.TextCtrl):
                     child.Bind(wx.EVT_KEY_DOWN, self.on_key_down_base)
                     break

    #def OnCancel(self, event):
    #    event.Skip()


class PASSWORD(TEXT, SchBaseCtrl):

    def __init__(self, *args, **kwds):
        if "style" in kwds:
            kwds["style"] = kwds["style"] | wx.TE_PASSWORD
        else:
            kwds["style"] = wx.TE_PASSWORD

        TEXT.__init__(self, *args, **kwds)


class TREE(wx.TreeCtrl, SchBaseCtrl):

    def _append_list(self, parent, list):
        for row in list:
            #print row
            child = self.AppendItem(parent, row[0])
            self.SetPyData(child, dict(row[2]))
            if len(row[1]) > 0:
                self.SetItemImage(child, self.fldridx, wx.TreeItemIcon_Normal)
                self.SetItemImage(child, self.fldropenidx, wx.TreeItemIcon_Expanded)
                self._append_list(child, row[1])
            else:
                self.SetItemImage(child, self.fileidx, wx.TreeItemIcon_Normal)
                self.SetItemImage(child, self.fileidxmark, wx.TreeItemIcon_Selected)

    def __init__(self, *args, **kwds):
        SchBaseCtrl.__init__(self, args, kwds)
        kwds["style"] = wx.TR_HIDE_ROOT | wx.TR_DEFAULT_STYLE
        # | wx.WANTS_CHARS
        wx.TreeCtrl.__init__(self, *args, **kwds)

        isz = (16, 16)
        il = wx.ImageList(isz[0], isz[1])
        self.fldridx = il.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, isz))
        self.fldropenidx = il.Add(wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_OTHER, isz))
        self.fileidx = il.Add(wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, isz))
        self.fileidxmark = il.Add(wx.ArtProvider.GetBitmap(wx.ART_TICK_MARK, wx.ART_OTHER, isz))

        self.SetImageList(il)
        self.il = il

        self.root = self.AddRoot("/")

        ldata = self.get_ldata()
        if ldata:
            self._append_list(self.root, ldata)

        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.on_activated)

    def on_activated(self, event):
        item_id = event.GetItem()
        if item_id.IsOk():
            item = self.GetPyData(item_id)
            #print "OnActivated:", item
            if 'href' in item:
                self.GetParent().href_clicked(self, item)
        event.Skip()


class COLOURSELECT(colourselect.ColourSelect, SchBaseCtrl):

    def __init__(self, *args, **kwds):
        SchBaseCtrl.__init__(self, args, kwds)
        if 'name' in kwds:
            del kwds['name']
        colourselect.ColourSelect.__init__(self, id=-1, *args, **kwds)


class GENERICDIR(wx.GenericDirCtrl, SchBaseCtrl):

    def __init__(self, *args, **kwds):
        SchBaseCtrl.__init__(self, args, kwds)
        wx.GenericDirCtrl.__init__(self, *args, **kwds)


class TREELIST(TreeListCtrl, SchBaseCtrl):

    def AppendList(self, parent, list):
        for row in list:
            l = row[0].split('||')
            child = self.AppendItem(parent, l[0])
            #print "AppendItem:", l[0]
            #self.SetPyData(child, None)
            try:
                self.SetItemData(child, None)
            except:
                pass

            for i in range(len(l) - 1):
                #self.SetItemText(child, i+1, l[i + 1])
                self.SetItemText(child, l[i + 1], i+1)

            if len(row[1]) > 0:
                self.SetItemImage(child, self.fldridx, wx.TreeItemIcon_Normal)

                self.AppendList(child, row[1])
            else:
                self.SetItemImage(child, self.fileidx, wx.TreeItemIcon_Normal)

    #def GetParent(self):
    #    return self._parent
    
    def __init__(self, *args, **kwds):
        SchBaseCtrl.__init__(self, args, kwds)
        #self._parent =  args[0]
        #kwds["style"] = wx.TR_HIDE_ROOT | wx.TR_DEFAULT_STYLE
        #kwds["style"] = wx.TR_DEFAULT_STYLE
        #try:
        #    kwds["style"] = wx.adv.TL_DEFAULT_STYLE
        #except:
        #kwds["style"] = wx.TR_DEFAULT_STYLE | wx.TR_HIDE_ROOT
        kwds['agwStyle'] = wx.TR_HIDE_ROOT
        TreeListCtrl.__init__(self, *args, **kwds)

        isz = (16, 16)
        il = wx.ImageList(isz[0], isz[1])
        self.fldridx = il.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, isz))
        self.fldropenidx = il.Add(wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_OTHER, isz))
        self.fileidx = il.Add(wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, isz))
        self.fileidxmark = il.Add(wx.ArtProvider.GetBitmap(wx.ART_TICK_MARK, wx.ART_OTHER, isz))

        self.SetImageList(il)
        self.il = il

        l = self.label.split('||')
        for pos in l:
            try:
                self.AppendColumn(pos)
            except:
                self.AddColumn(pos)
        #self.SetMainColumn(0)
        self.SetColumnWidth(0, 175)

        #print(dir(self))
        self.root = self.AddRoot("/")
        #self.root = self.GetRootItem()
        #self.root = self.AddRoot("/")
        #self.root = self.AppendItem(self.GetRootItem(), "/")
        #self.root = self.GetRootItem()
        #print "root:",  self.root

        ldata = self.get_ldata()
        if ldata:
            self.AppendList(self.root, ldata)
        self.Refresh()


class CALENDAR(CalendarCtrl, SchBaseCtrl):

    def __init__(self, *args, **kwds):
        SchBaseCtrl.__init__(self, args, kwds)
        try:
            CalendarCtrl.__init__(self, style=wx.adv.CAL_MONDAY_FIRST | wx.adv.CAL_SHOW_HOLIDAYS | wx.adv.CAL_SEQUENTIAL_MONTH_SELECTION, *args, **kwds)
        except:
            CalendarCtrl.__init__(self, style=wx.calendar.CAL_MONDAY_FIRST | wx.calendar.CAL_SHOW_HOLIDAYS | wx.calendar.CAL_SEQUENTIAL_MONTH_SELECTION, *args, **kwds)

class EDITABLELISTBOX(EditableListBox, SchBaseCtrl):

    def __init__(self, *args, **kwds):
        SchBaseCtrl.__init__(self, args, kwds)
        EditableListBox.__init__(self, *args, **kwds)


class FILEBROWSEBUTTON(filebrowsebutton.FileBrowseButton, SchBaseCtrl):

    def __init__(self, *args, **kwds):
        SchBaseCtrl.__init__(self, args, kwds)
        filebrowsebutton.FileBrowseButton.__init__(self, *args, **kwds)

    def GetValue(self):
        return '@'+super(FILEBROWSEBUTTON, self).GetValue()


class IMAGEBROWSEBUTTON(FILEBROWSEBUTTON, SchBaseCtrl):

    def OnBrowse (self, event = None):
        """ Going to browse for file... """
        current = self.GetValue()
        directory = os.path.split(current)
        if os.path.isdir( current):
            directory = current
            current = ''
        elif directory and os.path.isdir( directory[0] ):
            current = directory[1]
            directory = directory [0]
        else:
            directory = self.startDirectory
            current = ''

        dlg = wx.lib.imagebrowser.ImageDialog(self, current)

        if dlg.ShowModal() == wx.ID_OK:
            self.SetValue(dlg.GetFile())
        dlg.Destroy()



class MASKTEXT(masked.TextCtrl, SchBaseCtrl):

    def __init__(self, *args, **kwds):
        SchBaseCtrl.__init__(self, args, kwds)
        if self.valuetype:
            if self.src:
                if self.src.startswith('!'):
                    kwds['autoformat'] = self.src[1:]
                else:
                    kwds['mask'] = self.src
        masked.TextCtrl.__init__(self, *args, **kwds)
        self._autofit = False


class NUM(wx.SpinCtrl, SchBaseCtrl):

    def __init__(self, *args, **kwds):
        SchBaseCtrl.__init__(self, args, kwds)
        if self.param and 'param' in self.param and 'PROCESS_ENTER' in self.param['param']:
            kwds['style']=wx.TE_PROCESS_ENTER
        if self.readonly:
            style = 0
            if "style" in kwds:
                style = kwds["style"]
            style = style | wx.TE_READONLY
            kwds["style"] = style      
        wx.SpinCtrl.__init__(self, *args, **kwds)


class KWOTA(masked.NumCtrl, SchBaseCtrl):

    def __init__(self, *args, **kwds):
        SchBaseCtrl.__init__(self, args, kwds)
        prec = 2
        width = 10
        if 'prec' in kwds:
            prec = kwds['prec']
            del kwds['prec']
        if 'width' in kwds:
            width = kwds['width']
            del kwds['width']

        kwds["integerWidth"] = width
        kwds["fractionWidth"] = prec

        masked.NumCtrl.__init__(self, *args, **kwds)


class TIME(masked.TimeCtrl, SchBaseCtrl):

    def __init__(self, *args, **kwds):
        SchBaseCtrl.__init__(self, args, kwds)
        masked.TimeCtrl.__init__(self, *args, **kwds)


class STYLEDTEXT(wx.TextCtrl, SchBaseCtrl):
        def __init__(self, *args, **kwds):
            SchBaseCtrl.__init__(self, args, kwds)
            if "style" in kwds:
                style = kwds["style"]
                style = style | wx.TE_MULTILINE
                kwds["style"] = style
            else:
                kwds["style"] = wx.TE_MULTILINE
            wx.TextCtrl.__init__(self, *args, **kwds)
            if 'data' in self.param:
                self.SetValue(self.param['data'].encode('utf-8'))

        def SetValue(self, value):
            if value.startswith('\n'):
                value2 = value[1:]
            else:
                value2 = value
            if value2.__class__==str:
                return wx.TextCtrl.SetValue(self, value2.decode('utf-8'))
            else:
                return wx.TextCtrl.SetValue(self, value2)

AUTOCOMPLETE = STYLEDTEXT
STANDARDSTYLEDTEXT = STYLEDTEXT

def TEXTAREA(*args, **kwds):
    if 'param' in kwds:
        if 'data' in kwds['param']:
            data = kwds['param']['data'].replace('\r', '')
            if data.startswith('\n'):
                data = data[1:]
                kwds['param']['data'] = data

    if "src" in kwds:
        if kwds['src'] in ('c', 'python', 'html'):
            ret=STYLEDTEXT(*args, **kwds)
        else:
            ret=AUTOCOMPLETE(*args, **kwds)
    else:
        ret=STYLEDTEXT(*args, **kwds)
    return ret


class TICKER(ticker.Ticker, SchBaseCtrl):

    def __init__(self, *args, **kwds):
        SchBaseCtrl.__init__(self, args, kwds)
        ticker.Ticker.__init__(self, *args, **kwds)

    def SetValue(self, value):
        self.SetText(value)

    def CanClose(self):
        self.Stop()
        return True

#class HTMLLISTBOX(wx.HtmlListBox, SchBaseCtrl):
#class HTMLLISTBOX(wx.SimpleHtmlListBox, SchBaseCtrl):
#class HTMLLISTBOX(wx.ListBox, SchBaseCtrl):


init_css_str="""
body {font-family:sans-serif;font-size:150%; padding:1;}
table {border:0;vertical-align:top; padding:1;}
td table { padding: 1; }
th {border:0; cellpadding:1;}
td {border:0; vertical-align:top; cellpadding:1;}
strong,b {font-weight:bold;}
p { cellpadding:1; border:0; width:100%; }
"""

class HTMLLISTBOX(wx.VListBox, SchBaseCtrl):

    def __init__(self, *args, **kwds):
        SchBaseCtrl.__init__(self, args, kwds)
        self.choices = []
        self.getItemFunct = None

        if self.param and 'multiple' in self.param:
            style = 0
            if "style" in kwds:
                style = kwds["style"]
            style = style | wx.LB_MULTIPLE
            kwds["style"] = style

        if "size" in kwds:
            size = kwds['size']
            if size[1]==-1:
                kwds['size'] = (size[0], 100)

        tdata = self.get_tdata()
        if tdata:
            for row in tdata:
                self.AppendHtml(row[0].data)

        wx.VListBox.__init__(self, *args, **kwds)

        self.SetItemCount(len(self.choices))
        i=0
        for choice in self.choices:
            if choice[1]:
                #print "SetSelection:", i
                self.SetSelection(i)
            i+=1

        #print "Y1"
        self.ScrollToRow(0)
        #print "Y3"

    def _AppendHtml(self, id, sel, html_txt):
        self.choices.append((id, sel, html_txt.replace('[', '<').replace(']', '>')) )

    def AppendHtml(self, html_txt):
        #if ':' in html_txt:
        #    x = html_txt.split(':')
        #    if x[1].startswith('!!'):
        #        self._AppendHtml(x[0],True, x[1][2:])
        #    else:
        #        self._AppendHtml(x[0],False, x[1])
        #else:
        self._AppendHtml(-1, False, html_txt)

    def AppendText(self, txt):
        self.AppendHtml(txt.replace('\n',''))
        self.SetItemCount(len(self.choices))
        self.Refresh()


    def AppendTexts(self, txt_list):
        for txt in txt_list:
            self.AppendHtml(txt.replace('\n',''))
        self.SetItemCount(len(self.choices))
        self.SetSelection(len(self.choices)-1)
        self.Refresh()

    def GetValue(self):
        ret = []
        if self.HasMultipleSelection():
            item, cookie = self.GetFirstSelected()
            while ( item != wx.NOT_FOUND ):
                ret.append(self.choices[item][0])
                item, cookie = self.GetNextSelected(cookie)
        return ret


    def _calc_or_draw(self, n, dc, rect, calc_only):
        w = self.GetSize()[0]
        value = "<html><body>"+(self.choices)[n][2]+"</body></html>"
        wxdc = DcDc(dc, calc_only=calc_only, width=w, height=-1)

        if rect:
            wxdc2 = wxdc.subdc(rect.X+2, rect.Y, rect.Width-4, rect.Height)
        else:
            wxdc2 = wxdc

        p = HtmlViewerParser(dc=wxdc2, calc_only=calc_only, init_css_str=init_css_str)
        p.set_http_object(wx.GetApp().http)
        p.set_parent_window(self)
        try:
            p.feed(value)
        except:
            print("ERROR:", value)

        w2,h2=p.get_max_sizes()
        return w2, h2


    def OnMeasureItem(self, n):
        dc = wx.ClientDC(self)
        w,h = self._calc_or_draw(n, dc, None, True)
        return h

    def OnDrawItem(self, dc, rect, n):
        self._calc_or_draw(n, dc, rect, False)

    def CanAcceptFocus(self):
        return False

    def GetBestSize(self):
        return (400, 200)

    def process_refr_data(self, *args, **kwds):
        self.init_base(args, kwds)
        self.choices = []
        tdata = self.get_tdata()
        if tdata:
            for row in tdata:
                self.AppendHtml(row[0].data)
        self.SetItemCount(len(self.choices))
        self.SetSelection(len(self.choices)-1)

    def ScrollToLine(self, line_no):
        nr = line_no
        count = self.GetItemCount()
        if count>0:
            if nr >= count:
                nr = count-1
            if nr < 0:
                nr=0
            self.SetSelection(nr)

class HTML(page.SchPage, SchBaseCtrl):
    def __init__(self, *args, **kwds):
        SchBaseCtrl.__init__(self, args, kwds)
        page.SchPage.__init__(self, args[0], self.src, None, name=kwds['name'])
        if self.src:
            value = self.load_string_from_server(self.src)
            self._set_value(value, False)
        elif self.param and 'data' in self.param and len(self.param['data'])>0:
            self._set_value(self.param['data'], False)
        else:
            self._value = None
        self.body.Refresh()
        self.body.Update()
        #self.best_size = self.body._calculate_size(kwds['size'].GetWidth())

    #def GetBestSize(self):
    #    return self.best_size

    def CanAcceptFocus(self):
        return False

    def SetValue(self, value):
        self._set_value(value)

    def _set_value(self, value, refresh=True):
        if not '<html' in value:
            self._value = "<html><body>%s</body></html>" % value
        else:
            self._value = value        
        mp = ShtmlParser()
        mp.process(self._value)
        mp.address = None
        body = mp.get_body()
        self.body.show_page(body)
        if refresh:
            self.body.wxdc = None
            self.body.draw_background()

    def GetValue(self):
        return self._value




PDFVIEWER = None

if wx.Platform == '__WXMSW2__':
    from wx.lib.pdfwin import PDFWindow

    class PDFVIEWER(PDFWindow, SchBaseCtrl):

        def __init__(self, *args, **kwds):
            SchBaseCtrl.__init__(self, args, kwds)
            PDFWindow.__init__(self, *args, **kwds)
            if self.href != None:
                self.LoadFile(self.href)
                self.SetSize((800, 600))
                self.setView('Fit')


try:
    import wx.media

    class MEDIA(wx.media.MediaCtrl, SchBaseCtrl):

        def __init__(self, *args, **kwds):
            SchBaseCtrl.__init__(self, args, kwds)
            wx.media.MediaCtrl.__init__(self, *args, **kwds)
            if self.href != None:
                if not self.Load(self.href):
                    print("error:", self.href)
                else:#
                    self.SetBestFittingSize()
                    self.Play()

except:
    pass


class NOTEBOOK(wx.Notebook, SchBaseCtrl):

    def __init__(self, *args, **kwds):
        SchBaseCtrl.__init__(self, args, kwds)
        self.childs = []
        wx.Notebook.__init__(self, *args, **kwds)
        if self.tdata:
            for row in self.tdata:
                h = page.SchPage(self, row[1].data, {})
                self.AddPage(h,row[0].data)
                self.childs.append(h)


class GRID(grid.SchTableGrid, SchBaseCtrl):

    def __init__(self, *args, **kwds):
        #self.obj = SchBaseCtrl(self, args, kwds)
        SchBaseCtrl.__init__(self, args, kwds)
        parent = args[0]
        parm = createparm.create_parm(self.src, parent.get_parm_obj())
        if parm:
            self.proxy = tabproxy.DataProxy(wx.GetApp().get_http(parent), str(parm[0]))
            self.proxy.set_address_parm(parm[2])
        else:

            self.proxy = tabproxy.DataProxy(wx.GetApp().get_http(parent), str(self.src))
        table = datasource.DataSource(self.proxy)

        #print "XX1", self.readonly
        if self.readonly:
            kwds['typ']=self.VIEW
            table.set_read_only(True)
        else:
            table.set_read_only(False)

        #schgrid.SChTableGrid.__init__(self, table, self.src, *args, **kwds)

        super().__init__(table, self.src, *args, **kwds)

        self.GetParent().any_parent_command("register_refr_obj", self)

    def process_refr_data(self, *args, **kwds):
        self.init_base(args, kwds)


        parm = createparm.create_parm(self.src, self.GetParent().get_parm_obj())
        if parm:
            self.proxy = tabproxy.DataProxy(wx.GetApp().get_http(self), str(parm[0]))
            self.proxy.SetAddressParm(parm[2])
        else:

            self.proxy = tabproxy.DataProxy(wx.GetApp().get_http(self), str(self.src))
        table = datasource.DataSource(self.proxy)
        self.SetTable(table)

    def RefrObj(self):
        if self.GetParent().IsShown():
            parm = createparm.create_parm(self.src, self.GetParent().get_parm_obj())
            if parm:
                if self.proxy.set_address_parm(parm[2]):
                    self.GetTable().refresh(False)

    def OnSize(self, event=None):
        """ Handles The wx.EVT_SIZE Event For TabCtrl. """

        if event != None:
            size = event.GetSize()
            old = self.GetSize()
            if old[1] != size[1] - 8:
                self.SetSize((size[0], size[1] - 8))
                self.GetParent().RefrPage()
            event.Skip()


class UPDATEGRIDBUTTON(wx.Button, SchBaseCtrl):

    def __init__(self, *args, **kwds):
        #self.obj = SchBaseCtrl(self, args, kwds)
        SchBaseCtrl.__init__(self, args, kwds)
        wx.Button.__init__(self, *args, **kwds)

        self.Bind(wx.EVT_BUTTON, self.OnClick, self)
        self.Enable()

    def OnClick(self, event):
        rec = dict()
        keys = list(self.GetParent().GetWidgets().keys())
        for k in keys:
            ctrl = self.GetParent().GetItem(k)
            if hasattr(ctrl, "GetValue"):
                rec[k] = self.GetParent().GetItem(k).GetValue()
        self.GetParent().GetPrevWin().ActiveCtrl.OnUpRecFromForm(rec)
        self.GetParent().any_parent_command("OnCancel", None)


class POPUPHTML(DataPopupControl, SchBaseCtrl):

    def __init__(self, *args, **kwds):
        '''Obowi\xc4\x85zkowy parametr: href - adres bazowy
        href + "dialog" - adres pod kt\xc3\xb3rym wy\xc5\x9bwietli si\xc4\x99 okienko dialogowe
        href+ "test?value=" - adres pod kt\xc3\xb3rym znajduje si\xc4\x99 lista warto\xc5\x9bci
                             spe\xc5\x82niaj\xc4\x85ca warunek
      '''

        #self.obj = SchBaseCtrl(self, args, kwds)
        SchBaseCtrl.__init__(self, args, kwds)
        DataPopupControl.__init__(self, *args, **kwds)
        if self.param:
            if 'IN_NEW_WIN' in self.param:
                self.simpleDialog=False

    def GetBestSize(self):
        dx, dy = DataPopupControl.GetBestSize(self)
        return (250, dy)



if platform.system() == "Linux":
    class DATEPICKER(POPUPHTML):

        def __init__(self, *args, **kwds):
            kwds['href'] = "/schsys/datedialog/"

            if "style" in kwds:
                kwds["style"] = kwds["style"] | wx.WANTS_CHARS
            else:
                kwds["style"] = wx.WANTS_CHARS

            if 'size' in kwds:
                kwds['size'] = wx.Size(150, kwds['size'].height)
            else:
                kwds['size'] = wx.Size(150, -1)

            POPUPHTML.__init__(self, *args, **kwds)

            if self.value:
                self.set_rec(self.value, [self.value,])
            else:
                self.set_rec(wx.DateTime.Today().FormatISODate(), [wx.DateTime.Today().FormatISODate(),], False)

            self.to_masked(autoformat='EUDATEYYYYMMDD.')

        def GetValue(self):
            value = self.get_rec()
            #print value
            if value.__class__== tuple and len(value)>0:
                return value[1][0]
            else:
                return value
            return None

        def GetBestSize(self):
            dx, dy = POPUPHTML.GetBestSize(self)
            return (130, dy)
else:
    class DATEPICKER(DatePickerCtrl, SchBaseCtrl):
        def __init__(self, *args, **kwds):
            SchBaseCtrl.__init__(self, args, kwds)
            #if 'size' in kwds:
            kwds['size']=(120,-1)
            try:
                kwds['style']= wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY | wx.adv.DP_ALLOWNONE
            except:
                kwds['style']= wx.DP_DROPDOWN | wx.DP_SHOWCENTURY | wx.DP_ALLOWNONE
            DatePickerCtrl.__init__(self, *args, **kwds)

        def SetValue(self, value):
            if value:
                date = wx.DateTime()
                #print value.__class__, value
                date.ParseDate(value)
                DatePickerCtrl.SetValue(self,date)
            else:
                DatePickerCtrl.SetValue(self, None)


        def GetValue(self):
            value = DatePickerCtrl.GetValue(self)
            if value:
                return value.FormatISODate()
            else:
                return None


class DATETIMEPICKER(POPUPHTML):

    def __init__(self, *args, **kwds):
        kwds['href'] = "/schsys/datedialog/"

        if "style" in kwds:
            kwds["style"] = kwds["style"] | wx.WANTS_CHARS
        else:
            kwds["style"] = wx.WANTS_CHARS

        if 'size' in kwds:
            kwds['size'] = wx.Size(200, kwds['size'].height)
        else:
            kwds['size'] = wx.Size(200, -1)

        POPUPHTML.__init__(self, *args, **kwds)

        self.to_masked(autoformat='EUDATE24HRTIMEYYYYMMDD.HHMM')

        if self.value:
            self.set_rec(self.value, [self.value,])
        else:
            now = datetime.datetime.now().isoformat().replace('T',' ').replace('-','.')[:16]
            self.set_rec(now, [now,], False)

    def GetValue(self):
        value = self.get_rec()
        value2 = self.GetTextCtrl().GetValue()
        if value2 and value2[0]!=' ':
            if value.__class__ in (tuple,list) and len(value)>1:
                return value[1][0]
            else:
                return [datetime.datetime.strptime(value2, "%Y.%m.%d %H:%M"),]
        return None

    def GetBestSize(self):
        dx, dy = POPUPHTML.GetBestSize(self)
        return (180, dy)


class CHOICE(POPUPHTML):

    def __init__(self, *args, **kwds):

        if not ('href' in kwds or 'href' in kwds):
            kwds['href'] = "/schsys/listdialog/"

        if "style" in kwds:
            kwds["style"] = kwds["style"] | wx.WANTS_CHARS
        else:
            kwds["style"] = wx.WANTS_CHARS

        if 'size' not in kwds:
        #    kwds['size'] = wx.Size(250, kwds['size'].height)
        #else:
            kwds['size'] = wx.Size(250, -1)

        kwds['dialog_with_value'] = False
        POPUPHTML.__init__(self, *args, **kwds)

        choices = None
        self._norefresh = False
        self.retvalues = []
        self.sel = None
        tdata = self.get_tdata()
        i = 0
        self.choices = None
        if tdata:
            choices = []

            for row in tdata:
                value = row[0].data
                if value.find("!!") >= 0:
                    value = value.replace("!!", "")
                    sel = value.split(':')
                    if len(sel)>1:
                      ComboCtrl.SetValue(self, sel[1].lstrip())
                      self.set_rec(sel[1], sel, dismiss=False)
                    else:
                      ComboCtrl.SetValue(self, sel[0], dismiss=False)
                      self.set_rec(sel[0], sel)

                value = value.split(':')
                if len(value)>1:
                    choices.append((value[1].lstrip(), value))
                else:
                    choices.append((value[0], value))

                i = i + 1

            self.choices = choices
        else:
            self.choices = []

        aTable = [
                (0, wx.WXK_F2,  self.on_ext_button_click),
                 ]
        self.set_acc_key_tab(aTable)


    def on_ext_button_click(self, event):
        ret = self.alternate_button_click()
        if self.sash:
            self.sash.body.choices = self.choices
            wx.CallAfter(self.sash.body.refr)
        else:
            self.popup.html.body.choices = self.choices
            wx.CallAfter(self.sash.body.refr)
        return ret


    def OnButtonClick(self):
        if self.simpleDialog:
            ret = POPUPHTML.OnButtonClick(self)
            self.popup.html.body.choices = self.choices
            wx.CallAfter(self.popup.html.body.refr)
        else:
            ret = POPUPHTML.OnButtonClick(self)
            self.sash.body.choices = self.choices
            wx.CallAfter(self.popup.html.body.refr)
        return ret

    def GetValue(self):
        if self.readonly:
            value = self.get_rec()
            return value[0]
        else:
            return POPUPHTML.GetValue(self)
        return None


class DBCHOICE(CHOICE):
    def GetValue(self):
        if self.readonly:
            value = self.get_rec()
            if value.__class__==tuple and len(value)>0:
                return value[1][0]
            if len(value)>0:
                return value[0]
            else:
                return None
        else:
            return POPUPHTML.GetValue(self)
        return None

class DBCHOICE_EXT(POPUPHTML):
    def __init__(self, *args, **kwds):
        if 'style' in kwds:
            kwds['style'] = kwds['style'] | wx.CB_READONLY
        else:
            kwds['style'] = wx.CB_READONLY

        POPUPHTML.__init__(self, *args, **kwds)


    def SetValue(self, value):
        #print value, value.__class__
        if '!!' in value:
            id = value.split(':')[0]
            name = value[len(id)+1:].replace('!!','')
            self.set_rec(name, [id,name], dismiss=False)
        else:
            POPUPHTML.SetValue(self, value)

    def GetValue(self):
        if self.readonly:
            value = self.get_rec()
            if value.__class__==tuple and len(value)>0:
                return value[1][0]
            if len(value)>0:
                return value[0]
            else:
                return None
        else:
            return POPUPHTML.GetValue(self)
        return None

    def get_parm(self, parm):
        if len(self.rec_value)>0:
            id = self.rec_value[0]
            return b64encode(str(id).encode('utf-8')) if parm=='value' else None
        else:
            return None



class COLLAPSIBLE_PANEL(wx.CollapsiblePane, SchBaseCtrl):

    def __init__(self, *args, **kwds):
        SchBaseCtrl.__init__(self, args, kwds)
        kwds['label'] = self.label
        kwds['style'] = wx.CP_DEFAULT_STYLE|wx.CP_NO_TLW_RESIZE
        if 'size' in kwds:
            tmp =  kwds['size']
            self._size = [tmp[0], tmp[1]]
            del kwds['size']
        else:
            self._size = [400,300]

        self._height = 0

        if 'collapse_height' in self.param:
            self._size[1] = int(self.param['collapse_height'])

        wx.CollapsiblePane.__init__(self, *args, **kwds)
        try:
            self.GetPane().SetBackgroundStyle(wx.BG_STYLE_ERASE)
        except:
            self.GetPane().SetBackgroundStyle(wx.BG_STYLE_CUSTOM)

        if 'data' in self.param and self.param['data'].strip():
            self.set_html(self.param['data'])
        else:
            self.html = None
            self.SetSize((0,0))
            self.Hide()
        self.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.OnPaneChanged)

    def set_html(self, html_txt):
        mp = ShtmlParser()
        mp.process("<html><body>" + self.param['data'].decode('utf-8') +"</body></html>")
        mp.address = None
        if not self.html:
            self.html=page.SchPage(self.GetPane(), mp, {})
            self.html.init_frame()
            self.html.activate_page()
            width = self._size[0] if self._size[0] > 0 else 400
            self._height = self._size[1] if self._size[1] > 0 else 300
            self.html.SetSize((width, self._height))
            sizer = wx.BoxSizer()
            sizer.Add(self.html, 1, wx.EXPAND | wx.ALL, 5)
            self.GetPane().SetSizer(sizer)
            self.OnPaneChanged(None)
        else:
            self.html.set_adr_and_param(mp, None)
            self.OnPaneChanged(None)
            #self.html.refresh_html()


    def GetBestSize(self):
        ret = wx.CollapsiblePane.GetBestSize(self)
        if self.IsExpanded():
            print(self._height, ret[0], ret[1]+self._height)
            return (ret[0], ret[1]+self._height)
        elif not self.IsShown():
            return (0,0)
        else:
            if ret[1]-self._height>0:
                return (ret[0], ret[1]-self._height)
            else:
                return (ret[0], ret[1])

    def OnPaneChanged(self, event):
        if self.html:
            self.GetParent().GetParent().refresh_html()
            self.html.refresh_html()

    def SetValue(self, value):
        if not self.html:
            pass

    def process_refr_data(self, *args, **kwds):
        if 'param' in kwds:
            self.param = kwds['param']
            if 'data' in self.param and self.param['data'].strip():
                self.Show(True)
                self.set_html(self.param['data'])
        #print("----------------------------------------------")
        #print(self, args, kwds)
        #print("----------------------------------------------")


class ListBoxNoFocus(wx.ListBox):

    def CanAcceptFocus(self):
        return False


class Select2Popup(wx.MiniFrame):
    def __init__(self, parent, id, title, pos, size, style, combo, href_id):
        from schcli.guiframe.page import SchPage
        self.combo = combo
        self.point = pos
        self.href_id = href_id

        wx.MiniFrame.__init__(self, parent, id, title, pos, size, wx.RESIZE_BORDER )


        self.edit_ctrl = wx.TextCtrl(self, size=(440,-1), style=wx.TE_PROCESS_ENTER|wx.TE_PROCESS_TAB)
        self.list_ctrl = ListBoxNoFocus(self, size=(440,200), style=wx.LB_SINGLE)

        self.edit_ctrl.Bind(wx.EVT_KEY_DOWN, self.on_key_down)
        self.edit_ctrl.Bind(wx.EVT_TEXT_ENTER, self.on_enter)
        self.list_ctrl.Bind(wx.EVT_LISTBOX_DCLICK, self.on_enter)

        self.Bind(wx.EVT_ACTIVATE, self.on_activate)
        self.Bind(wx.EVT_TEXT, self.OnText)

        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self.edit_ctrl)
        box.Add(self.list_ctrl, 1, wx.ALL | wx.GROW, 1)
        self.SetSizer(box)
        self.SetAutoLayout(True)
        self.Fit()

    def on_enter(self, event):
        id = self.list_ctrl.GetSelection()
        if id != wx.NOT_FOUND:
            self.Dismiss()
            item_id = self.list_ctrl.GetClientData(id)
            item_str = self.list_ctrl.GetString(id)
            self.combo.set_value(item_id, item_str)


    def on_activate(self, event):
        if not event.GetActive():
            self.Hide()
            self.combo.SetFocus()
        else:
            #LayoutAlgorithm().LayoutWindow(self.html, self.html.body)
            pass
        event.Skip()

    def on_key_down(self, event):
        print(event.KeyCode)
        if event.KeyCode == wx.WXK_ESCAPE:
            self.Dismiss()
        elif event.KeyCode == wx.WXK_DOWN:
            id = self.list_ctrl.GetSelection()
            if id != wx.NOT_FOUND:
                if id < self.list_ctrl.GetCount()-1:
                    self.list_ctrl.SetSelection(id+1)
        elif event.KeyCode == wx.WXK_UP:
            id = self.list_ctrl.GetSelection()
            if id != wx.NOT_FOUND:
                if id > 0:
                    self.list_ctrl.SetSelection(id-1)
        elif event.KeyCode == wx.WXK_TAB:
            return self.on_enter(event)
        else:
            event.Skip()

    def OnText(self, event):
        event.Skip()
        s = event.GetString()
        href = '/select2/fields/auto.json?term=%s&page=1&context=&field_id=%s' % (s, self.href_id)
        http = wx.GetApp().get_http(self.combo)
        http.get(self, href)
        #self.Http.get(self, str(self.href) + "test/", {"value": x})
                #self.Http.Get(self, str(self.href) + "test/", {"value": b32encode(value).encode('utf-8')})
        tab = schjson.loads(http.str())
        print(tab)
        http.clear_ptr()
        if tab['err'] == 'nil':
            self.list_ctrl.Clear()
            if len(tab['results'])>0:
                for pos in tab['results']:
                    self.list_ctrl.Append(pos['text'], pos['id'])
                self.list_ctrl.SetSelection(0)

    def SetXY(self, point):
        self.point = point

    def Popup(self):
        self.Show()
        self.Move(self.point)

    def Dismiss(self):
        self.Hide()
        self.combo.SetFocus()

    def clear(self):
        self.edit_ctrl.ChangeValue("")
        self.list_ctrl.Clear()

class _SELECT2(ComboCtrl,  SchBaseCtrl):

    def __init__(self, *args, **kwds):

        SchBaseCtrl.__init__(self, args, kwds)

        if "style" in kwds:
            kwds['style'] |= wx.TE_PROCESS_ENTER
        else:
            kwds['style'] = wx.TE_PROCESS_ENTER

        if 'item_id' in self.param and self.param['item_id']!='None':
            self.item_id = int(self.param['item_id'])
            self.item_str = self.param['item_str']
        else:
            self.item_id = -1
            self.item_str = ""

        kwds['size'] = (445, -1)

        ComboCtrl.__init__(self, *args, **kwds)

        if self.GetTextCtrl():
            self.GetTextCtrl().SetForegroundColour(wx.Colour(0, 0, 0))

        self.popup = None
        self.button1 = None
        self.button2 = None

        #self.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        self.Bind(wx.EVT_CHAR, self.OnChar)

        if self.item_str:
            self.SetValue(self.item_str)

        self.Bind(wx.EVT_KEY_DOWN, self.on_key_down_base)

    def init(self, button1, button2):
        self.button1 = button1
        self.button2 = button2

    def on_key_down_base(self, event):
        if event.GetKeyCode() == wx.WXK_TAB:
            if event.ShiftDown():
                self.GetParent().GetParent().Navigate(self.GetParent(), True)
            else:
                self.GetParent().GetParent().Navigate(self.GetParent(), False)
        elif event.GetKeyCode() == wx.WXK_F2:
            self.button1.on_click(event)
        elif event.GetKeyCode() == wx.WXK_INSERT:
            self.button2.on_click(event)
        else:
            event.Skip()


    def set_value(self, item_id, item_str):
        self.item_id = item_id
        self.item_str = item_str
        self.SetValue(item_str)

    def GetValue(self):
        return self.item_id

    #def OnSetFocus(self, event):
    #    event.Skip()

    def OnChar(self, event):
        c = event.GetUnicodeKey()
        if c in string.printable:
            self._on_button_click()
            self.popup.edit_ctrl.AppendText(event.GetUnicodeKey())
        else:
            event.Skip()

    def OnButtonClick(self):
        ret = self._on_button_click()
        self.popup.edit_ctrl.SetValue("")
        return ret

    def _on_button_click(self):
        if not self.popup:
            pos = self.GetScreenPosition()
            pos = (pos[0], pos[1] + self.GetSize()[1])
            if self.GetTextCtrl():
                #href_id = self.data['']
                href_id = self.param['data'][0]['attrs']['data-select2-id']
                self.popup = Select2Popup(self.GetTextCtrl(), -1, "Wybierz pozycję", pos=pos, size=(450, 400), style=wx.DEFAULT_DIALOG_STYLE,
                                combo=self, href_id=href_id)
            else:
                self.popup = Select2Popup(self, -1, "Wybierz pozycję", pos=pos, size=(450, 400), style=wx.DEFAULT_DIALOG_STYLE,
                                combo=self, href_id=href_id)

        self.popup.clear()

        pos = self.GetScreenPosition()
        pos = (pos[0], pos[1] + self.GetSize()[1])
        pos = [pos[0], pos[1]]

        screen_dx = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_X)
        screen_dy = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_Y)

        try:
            popup_size = self.popup.GetSize()
        except:
            popup_size = self.popup.GetSizeTuple()

        if pos[0] + popup_size[0] > screen_dx:
            pos[0] = screen_dx - popup_size[0]
        if pos[1] + popup_size[1] > screen_dy:
            pos[1] = pos[1]-self.GetSize().GetHeight()-popup_size[1]

        self.popup.SetXY(pos)
        self.popup.Popup()


    def DoSetPopupControl(self, popup):
        pass

    def Dismiss(self):
        if self.popup:
            self.popup.Close()
            self.popup = None
        self.SetFocus()

def button_from_parm(parent, param):
    icon = param['childs'][0]['attrs']['class']
    href = param['attrs']['href']
    button = BUTTON(parent, src='fa://'+icon+'?size=0', href=href)
    return button


def SELECT2(*args, **kwds):
    data = kwds['param']['data']
    panel = COMPOSITE_PANEL(*args, size=(500, -1))
    ctrl = _SELECT2(panel, **kwds)
    button1 = button_from_parm(panel, param=data[1]['childs'][0])
    button2 = button_from_parm(panel, param=data[1]['childs'][1])
    ctrl.init(button1, button2)

    def ret_ok(id, title):
        ctrl.set_value(id, title)
        wx.CallAfter(ctrl.SetFocus)

    ctrl.ret_ok=ret_ok
    button1.ret_ok=ret_ok
    button2.ret_ok=ret_ok

    box = wx.BoxSizer(wx.HORIZONTAL)
    box.Add(ctrl, 0, wx.EXPAND)
    box.Add(button1)
    box.Add(button2)

    panel.SetSizer(box)
    panel.SetAutoLayout(True)
    panel.Fit()

    return panel


def COMPOSITE(*args, **kwds):
    cls = kwds['param']['class'].upper()
    if cls in globals():
        return globals()[cls](*args, **kwds)

def RIOT(*args, **kwds):
    http = wx.GetApp().get_http(args[0])
    http.get(args[0], "/schsys/widget_web?browser_type=1")
    buf = http.str()
    http.clear_ptr()
    elem = kwds['param']['riot_elem']
    buf=buf.replace('</body>', "<%s></%s><script>riot.mount('*');</script></body>" % (elem, elem))
    url='http://127.0.0.2/data?'+ b64encode(buf.encode('utf-8')).decode('utf-8')
    #kwds['url'] = url
    obj =  HTML2(*args, **kwds)
    obj.load_url(url)
    return obj
