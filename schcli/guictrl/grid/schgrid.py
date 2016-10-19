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
import wx.grid
import traceback
from schcli.guictrl.grid import popupdata
from schcli.guilib import schevent


from .renderers import ExtStringRenderer, IconAndStringRenderer, \
    MultiLineStringRenderer
import schlib.schtools.tools as tools
from wx.grid import PyGridTableBase, GridCellAttr, GridTableMessage, \
    GRIDTABLE_NOTIFY_ROWS_DELETED, GRIDTABLE_NOTIFY_ROWS_APPENDED

# from tempfile import NamedTemporaryFile
#


class SchTableGrid(wx.grid.Grid):

    sort_color = 'ORANGE'
    bar_color = wx.Colour(230, 230, 255)
    GET_ID = 0
    VIEW = 1
    EDIT = 2

    def __init__(
        self,
        table,
        address,
        parent,
        typ=EDIT,
        id=-1,
        pos=wx.DefaultPosition,
        size=wx.DefaultSize,
        style=wx.WANTS_CHARS | wx.TAB_TRAVERSAL,
        name=wx.PanelNameStr,
        ):

#
# style= wx.TAB_TRAVERSAL | wx.SIMPLE_BORDER,

        self.address = address
        wx.grid.Grid.__init__(
            self,
            parent,
            id,
            pos,
            size,
            style,
            name,
            )
# wx.grid.Grid.__init__(self, parent, id, pos, size)

        self.SetScrollLineY(1)
        self.RegisterDataType('s', IconAndStringRenderer(),
                              wx.grid.GridCellTextEditor())
# self.RegisterDataType("x", ExtStringRenderer(),
# popupdata.GenericPopupCellEditor()) self.RegisterDataType("y",
# ExtStringRenderer(), popupdata.ListPopupCellEditor())
# self.RegisterDataType("f", ExtStringRenderer(),
# popupdata.GenericPopupCellEditor())

        self.RegisterDataType('x', ExtStringRenderer(),
                              popupdata.GenericPopupCellEditor())
        self.RegisterDataType('y', ExtStringRenderer(),
                              popupdata.ListPopupCellEditor())
        self.RegisterDataType('f', ExtStringRenderer(),
                              popupdata.GenericPopupCellEditor())
        self.RegisterDataType('str', wx.grid.GridCellStringRenderer(),
                              wx.grid.GridCellTextEditor())
        self.RegisterDataType('string', wx.grid.GridCellStringRenderer(),
                              wx.grid.GridCellTextEditor())
        self.RegisterDataType('datetime', wx.grid.GridCellStringRenderer(),
                              wx.grid.GridCellTextEditor())
        self.RegisterDataType('date', wx.grid.GridCellStringRenderer(),
                              popupdata.DatePopupDataCellEditor())
        #self.RegisterDataType('date', wx.grid.GridCellStringRenderer(),
        #                      wx.grid.GridCellTextEditor())
        self.RegisterDataType('int', ExtStringRenderer(),
                              popupdata.GenericPopupCellEditor())
        self.RegisterDataType('bool', wx.grid.GridCellBoolRenderer(),  wx.grid.GridCellBoolEditor())

        if hasattr(table, 'proxy'):
            self.SetTable(table, True)
            sizes = table.proxy.GetColSize()
            names = table.GetColNames()
            for i in range(len(sizes)):
                if 7 * len(str(names[i + 1])) > 7 * int(sizes[i]):
                    l = len(str(names[i + 1]))
                    self.SetColSize(i, 7 * l)
                else:
                    l = int(sizes[i])
                    self.SetColSize(i, 7 * l)
        else:
            if table.auto_size == 'short':
                self.SetTable(table, False)
                self.SetMargins(0, 0)
                self.AutoSizeColumns(False)
                self.AutoSizeRows(True)
                height = 5
                for row in range(0, table.per_page):
                    h = self.GetRowSize(row)
                    if h > height:
                        height = h
                width = []
                for col in range(0, self.GetNumberCols()):
                    width.append(self.GetColSize(col))
                table.enable(True)
                self.SetTable(table, True)
                self.SetDefaultRowSize(height, True)
                i = 0
                for w in width:
                    self.SetColSize(i, w)
                    i += 1
            else:
                table.enable(True)
                self.SetTable(table, True)
                self.AutoSizeColumns(False)
                self.AutoSizeRows(True)

        try:
            self.SetSelectionMode(wx.grid.Grid.GridSelectRows)
        except:
            self.SetSelectionMode(wx.grid.Grid.wxGridSelectRows)
        
        self.Bind(wx.grid.EVT_GRID_SELECT_CELL, self.on_select_cell)
        self.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.on_cell_left_click)

        self.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK, self.on_cell_left_dclick)
        self.Bind(wx.grid.EVT_GRID_RANGE_SELECT, self.on_range_selected)
        self.Bind(wx.grid.EVT_GRID_CMD_LABEL_LEFT_CLICK, self.on_label_left_click)
        self.Bind(wx.grid.EVT_GRID_CMD_LABEL_RIGHT_CLICK, self.on_label_right_click)
        self.Bind(wx.grid.EVT_GRID_CMD_LABEL_LEFT_DCLICK, self.on_label_left_dclick)
        self.Bind(wx.grid.EVT_GRID_CMD_CELL_RIGHT_CLICK, self.on_cell_right_click)


        #self.Bind(schevent.EVT_REFRPARM, self.begin_edit)
        self.Bind(wx.EVT_MENU, self.begin_edit)

        #self.Bind(wx.EVT_RIGHT_UP, self.on_right_up)
        #self.Bind(wx.grid.EVT_GRID_EDITOR_HIDDEN, self.on_hide_editor)
        #try:
        #    wx.grid.EVT_GRID_CMD_CELL_CHANGED(self, -1, self.on_cell_change)
        self.Bind(wx.grid.EVT_GRID_CMD_CELL_CHANGED, self.on_cell_change)
        #except:
        #    wx.grid.EVT_GRID_CELL_CHANGE(self, self.on_cell_change)

        self.Bind(wx.grid.EVT_GRID_CELL_CHANGING, self.on_cell_change)

        self.Bind(wx.EVT_KEY_DOWN, self.on_key_down)
        self.GetGridWindow().Bind(wx.EVT_LEFT_UP, self.OnLUp)

        column_label_window = self.GetGridColLabelWindow()
        #wx.EVT_PAINT(column_label_window, self.on_column_header_paint)
        self.Bind(wx.EVT_PAINT, self.on_column_header_paint, column_label_window)

# self.SelectRow(0)
#
# self.Bind(wx.EVT_NAVIGATION_KEY, self.OnNavigate)
        self.BlockEvent = False
        self.typ = typ
        self.readonly = False
        self.process_get = False
        self.LastAction = ''
        self.SetRowLabelSize(1)
        self.panel = None
        self.oldrow = -1
# if size==wx.DefaultSize: size2 = self.GetBestSize()
        self.SetSize((400, 300))
        
        self.default_command = 'edit'

# self.SetDefaultCellBackgroundColour(wx.Colour(255,0,0))
# self.SetGridLineColour(wx.Colour(255,0,0))
#
# self.SetSize(size2) print "BestSize:", size2 self.AutoSizeRows(True)
# self.ForceRefresh()
#
# def SetGridCursor(self, row, col): #print "SetGridCursor:", row, col if
# row==1: x = x /0 return wx.grid.Grid.SetGridCursor(self, row, col)
#
# def SelectRow(self, row): #print "SelectRow:", row if row==1: x = x /0 return
# wx.grid.Grid.SelectRow(self, row)
#
        self.SelectRow(0)

        #aTable = [
        #    #(0, wx.WXK_F2,  self.OnExtButtonClick),
        #    (wx.ACCEL_ALT, ord('J'), self.on_key_j),
        #    (wx.ACCEL_ALT, ord('K'), self.on_key_k),
        #    #(wx.ACCEL_CTRL, ord('N'), self.on_new),
        #    (wx.ACCEL_ALT, ord('L'), self.on_key_l),
        #    (wx.ACCEL_ALT, ord('H'), self.on_key_h),

        #    ]
        ##print("TEST", self.GetParent())
        ##self.GetParent().set_acc_key_tab(self, aTable)
        ##self.set_acc_key_tab(aTable)

        #if hasattr(self, 'set_acc_key_tab'):
        #    self.set_acc_key_tab(aTable)
        #else:
        #    self.GetParent().set_acc_key_tab(aTable)


    def begin_edit(self, event=None):
        if event==None:
            self.GetEventHandler().AddPendingEvent(wx.CommandEvent(wx.EVT_MENU.typeId))
        else:
            wx.CallAfter(self.EnableCellEditControl, enable=True)

    def set_typ(self, typ):
        self.typ = typ

    def get_min_size(self):
        return wx.Size(400, 300)

    def get_best_size(self):
        return wx.Size(400, 300)

    def set_panel(self, panel):
        self.panel = panel

    def get_html_parent(self):
        parent = self.GetParent()
        while parent != None:
            if parent.__class__.__name__ == 'SChHtmlWindow':
                return parent
            parent = parent.GetParent()
        return None

    def CanClose(self):
        if self.typ == self.VIEW or self.readonly:
            return True
        if self.GetTable().data_changed():
            msg = 'Data not saved, save now?'
            dlg = wx.MessageDialog(self, msg, 'SCSkr Question', wx.YES_NO
                                    | wx.YES_DEFAULT | wx.CANCEL
                                    | wx.ICON_QUESTION)
            ret = dlg.ShowModal()
            if ret == wx.ID_CANCEL:
                dlg.Destroy()
                return False
            elif ret == wx.ID_YES:
                self.GetTable().commit()
            dlg.Destroy()
            return True
        else:
            return True

    def goto_first_row(self):
        col = self.GetGridCursorCol()
        self.SetGridCursor(0, col)
        self.MakeCellVisible(0, col)

    def goto_last_row(self):
        col = self.GetGridCursorCol()
        self.SetGridCursor(self.GetNumberRows() - 1, col)
        self.MakeCellVisible(self.GetNumberRows() - 1, col)

    def goto_next_row(self):
        self.DisableCellEditControl()
        col = self.GetGridCursorCol()
        new_row = self.GetGridCursorRow() + 1
        if new_row < self.GetTable().GetNumberRows():
            self.SetGridCursor(new_row, col)
            self.MakeCellVisible(new_row, col)
            self.SelectRow(new_row)

    def goto_prev_row(self):
        self.DisableCellEditControl()
        col = self.GetGridCursorCol()
        new_row = self.GetGridCursorRow() - 1
        if new_row >= 0:
            self.SetGridCursor(new_row, col)
            self.MakeCellVisible(new_row, col)
            self.SelectRow(new_row)

    def on_cell_change(self, evt):
        row = evt.GetRow()
        col = evt.GetCol()
        #print("on_cell_change:", row, col)
        name = self.GetTable().GetColNames()[evt.GetCol() + 1]
        autocols = self.GetTable().GetAutoCols()
        if name in autocols:
            value = self.GetCellValue(evt.GetRow(), evt.GetCol())
            names = self.GetTable().GetColNames()[1:]
            rec = []
            for i in range(len(names)):
                rec.append(self.GetTable().GetValue(row, i))
            rec2 = self.GetTable().auto_update(name, names, rec)
            for i in range(len(rec2) - 1):
                self.GetTable().SetValue(row, i, rec2[i])
        evt.Skip()

    def on_navigate(self, evt):
        self.DisableCellEditControl()
        forward = evt.GetDirection()
        if forward:
            success = self.MoveCursorRight(False)
            if not success:
                new_row = self.GetGridCursorRow() + 1
                if self.GetGridCursorRow() < self.GetTable().GetNumberRows():
                    self.SetGridCursor(new_row, 0)
                    self.MakeCellVisible(new_row, 0)
                else:
                    pass
        else:
            success = self.MoveCursorLeft(False)
            if not success:
                new_row = self.GetGridCursorRow() - 1
                if new_row >= 0:
                    self.SetGridCursor(new_row, self.GetTable().GetNumberCols() - 1)
                    self.MakeCellVisible(new_row,
                            self.GetTable().GetNumberCols() - 1)
                else:
                    pass
        evt.Skip()

    def on_column_header_paint(self, evt):
        w = self.GetGridColLabelWindow()
        dc = wx.PaintDC(w)
# dc.SetBrush(wx.Brush(wx.RED)) return
        client_rect = w.GetClientRect()
# dc.DrawRectangle(0,0,clientRect.GetWidth(), clientRect.GetHeight()) return
        font = wx.NORMAL_FONT
        tot_col_size = -self.GetViewStart()[0]\
             * self.GetScrollPixelsPerUnit()[0]
        fs = font.GetPointSize()
        fs2 = int(0.8 * fs)
        for col in range(self.GetNumberCols()):
            dc.SetBrush(wx.Brush(self.sort_color, wx.TRANSPARENT))
            dc.SetTextForeground(wx.BLACK)
            col_size = self.GetColSize(col)
            rect = (tot_col_size, 0, col_size, 32)
            dc.SetPen(wx.GREY_PEN)
            dc.DrawLine(rect[0], rect[1], rect[0] + rect[2], rect[1])
            dc.SetPen(wx.WHITE_PEN)
            dc.DrawLine(rect[0], rect[1] + 1, rect[0] + rect[2], rect[1] + 1)
            dc.DrawLine(rect[0], rect[1] + 1, rect[0], rect[1] + rect[3])
            dc.SetPen(wx.GREY_PEN)
            dc.DrawLine(rect[0], (rect[1] + rect[3]) - 1, rect[0] + rect[2],
                        (rect[1] + rect[3]) - 1)
            dc.DrawLine((rect[0] + rect[2]) - 1, rect[1], (rect[0] + rect[2])
                         - 1, rect[1] + rect[3])
            dc.SetPen(wx.BLACK_PEN)
            tot_col_size += col_size
            srt = self.GetTable().get_sort_nr(col)
            if srt != 0:
                font.SetWeight(wx.BOLD)
                left = rect[0] + 3
                top = rect[1] + 3
                dc.SetBrush(wx.Brush(self.sort_color, wx.SOLID))
                if srt > 0:
                    dc.DrawPolygon([(left, top), (left + 6, top), (left + 3, top
                                    + 4)])
                else:
                    dc.DrawPolygon([(left + 3, top), (left + 6, top + 4),
                                   (left, top + 4)])
                if srt < 0:
                    srt = srt * -1
                dc.SetFont(wx.SMALL_FONT)
                dc.DrawText(str(srt), left + 8, top)
                rect = (rect[0], top + 2, rect[2], rect[3])
                s = self.GetColLabelValue(col)
                if s.find('\n') >= 0:
                    font.SetPointSize(fs2)
                else:
                    font.SetPointSize(fs)
                dc.SetFont(font)
                #print ">", self.GetColLabelValue(col), rect
                dc.DrawLabel('%s' % self.GetColLabelValue(col), rect, alignment=wx.ALIGN_CENTER)
                #dc.DrawRectangle(rect)
                
                #self.DrawTextRectangle(
                #    dc,
                #    '%s' % self.GetColLabelValue(col),
                #    rect,
                #    wx.ALIGN_CENTER,
                #    wx.ALIGN_CENTER,
                #    wx.HORIZONTAL,
                #    )
            else:
                font.SetWeight(wx.NORMAL)
                font.SetPointSize(fs)
                dc.SetFont(font)

                #print ">", self.GetColLabelValue(col), rect
                dc.DrawLabel('%s' % self.GetColLabelValue(col), rect, alignment=wx.ALIGN_CENTER)
                #dc.DrawRectangle(rect)

                #self.DrawTextRectangle(
                #    dc,
                #    '%s' % self.GetColLabelValue(col),
                #    rect,
                #    wx.ALIGN_CENTER,
                #    wx.ALIGN_CENTER,
                #    wx.HORIZONTAL,
                #    )

# print "OnPaint"

    def on_select_cell(self, evt):

        #print("OnSelectCell", evt.GetRow(), evt.GetCol())

        if self.BlockEvent == True:
            evt.Skip()
            return
        newrow = evt.GetRow()
        if self.oldrow != newrow:
            if self.panel:
                self.panel.refresh(newrow)
            self.SelectRow(evt.GetRow())
        evt.Skip()

    def on_range_selected(self, evt):
        if evt.Selecting():
            if evt.GetTopRow() != evt.GetBottomRow():
                self.ClearSelection()
                for row in range(evt.GetTopRow(), evt.GetBottomRow() + 1):
                    self.GetTable().sel_row(row)
                if self.GetGridCursorRow() == evt.GetTopRow():
                    self.SelectRow(evt.GetBottomRow())
                    self.SetGridCursor(evt.GetBottomRow(),
                                       self.GetGridCursorCol())
                else:
                    self.SelectRow(evt.GetTopRow())
                    self.SetGridCursor(evt.GetTopRow(), self.GetGridCursorCol())
        evt.Skip()

    def on_cell_left_click(self, evt):
        row1 = self.GetGridCursorRow()
        row2 = evt.GetRow()
        self.SelectRow(evt.GetRow())
        self.SetGridCursor(evt.GetRow(), evt.GetCol())
        self.SetFocus()
        if evt.ControlDown():
            self.GetTable().sel_row(row2)
        if evt.ShiftDown():
            if row1 > row2:
                (row1, row2) = (row2, row1)
            for row in range(row1, row2 + 1):
                self.GetTable().sel_row(row)
        if not evt.ControlDown() and not evt.ShiftDown():
            s = self.GetTable().GetValue(evt.GetRow(), evt.GetCol())
            if type(s)==str and s.strip() == '+':
                attr = self.GetTable().get_ext_attr(evt.GetRow(), evt.GetCol())
                td = self.GetTable().data[evt.GetRow()][evt.GetCol()]
                childs = self.GetTable().get_childs(evt.GetRow(), evt.GetCol())
                if childs:
                    for child_id in childs:
                        child = childs[child_id]
                        if 'href' in child.attrs:
                            self.GetParent().GetParent().href_clicked(self, child.attrs)
                            break
            else:
                if self.typ == self.GET_ID:
                    print("self.action('get')")
                    self.action('get')

    def OnLUp(self, event):
        pass

    def on_cell_left_dclick(self, evt):
        if self.typ == self.VIEW or self.typ == self.GET_ID or self.readonly:
            self.SelectRow(evt.GetRow())
            self.SetGridCursor(evt.GetRow(), evt.GetCol())
            self.SetFocus()
            value = self.GetTable().GetValue(self.GetGridCursorRow(), 0)
            if value and value.strip() == '-':
                self.action('insert')
            else:
                if self.typ == self.GET_ID:
                    self.action('get')
                else:
                    if self.action_exists('get_row'):
                        self.action('get_row')
                    else:
                        self.action(self.default_command)
        else:
            #self.EnableCellEditControl(enable=True)
            self.SetGridCursor(evt.GetRow(), evt.GetCol())
            #wx.CallAfter(self.EnableCellEditControl, enable=True)
            self.begin_edit()


    def on_key_j(self, evt):
        row = self.GetGridCursorRow()
        if row+1 < self.GetTable().GetNumberRows():
            self.MoveCursorDown(False)

    def on_key_k(self, evt):
        row = self.GetGridCursorRow()
        if row > 0:
            self.MoveCursorUp(False)

    def on_key_h(self, evt):
        col = self.GetGridCursorCol()
        if col > 0:
            self.MoveCursorLeft(False)

    def on_key_l(self, evt):
        col = self.GetGridCursorCol()
        if col+1 < self.GetTable().GetNumberCols():
            self.MoveCursorRight(False)


    def on_key_down(self, evt):
        if evt.KeyCode in (wx.WXK_UP,wx.WXK_DOWN, wx.WXK_LEFT, wx.WXK_RIGHT) and not evt.AltDown() and not evt.ControlDown() and not evt.ShiftDown():
            row = self.GetGridCursorRow()
            col =  self.GetGridCursorCol()
            if evt.KeyCode ==  wx.WXK_DOWN:
                self.on_key_j(evt)
            if evt.KeyCode ==  wx.WXK_UP:
                self.on_key_k(evt)
            if evt.KeyCode ==  wx.WXK_RIGHT:
                self.on_key_l(evt)
            if evt.KeyCode ==  wx.WXK_LEFT:
                self.on_key_h(evt)
            return

        if evt.AltDown() and evt.KeyCode != wx.WXK_RETURN:
            wx.GetApp().GetTopWindow().on_key_down(evt)
            return
        if evt.KeyCode == wx.WXK_TAB and evt.ControlDown():
            evt.Skip()
            return
        if evt.KeyCode == wx.WXK_RETURN and not evt.AltDown():
            if self.typ == self.VIEW:
                value = self.GetTable().GetValue(self.GetGridCursorRow(), 0)
                if value and value.strip() == '-':
                    self.action('insert')
                else:
                    if self.action_exists('get_row'):
                        self.action('get_row')
                    else:
                        self.action(self.default_command)
                return
            if self.typ == self.GET_ID:
                if hasattr(self.Parent, 'ReturnRec'):
                    rec = self.GetTable().get_rec(self.GetGridCursorRow())
                    nr = rec[0]
                    s = self.GetTable().GetRecAsStr(nr)
                    self.Parent.ReturnRec((nr, s, rec))
                else:
                    self.action('get')
                return
            if evt.ControlDown():  # the edit control needs this key
                evt.Skip()
                return
            self.DisableCellEditControl()
            success = self.MoveCursorRight(evt.ShiftDown())
            if not success:
                new_row = self.GetGridCursorRow() + 1
                if new_row < self.GetTable().GetNumberRows():
                    self.SetGridCursor(new_row, 0)
                    self.MakeCellVisible(new_row, 0)
                else:
                    pass
            return
        if evt.KeyCode == wx.WXK_DELETE:
            if self.typ == self.VIEW or self.typ == self.GET_ID:
                if not self.readonly:
                    self.action('delete')
                evt.Skip()
                return
            if not evt.ControlDown():
                evt.Skip()
                return
            row = self.GetGridCursorRow()
            if row >= 0:
                self.DeleteRows(row, 1)
                if row < self.GetTable().GetIlRec():
                    self.SetGridCursor(row + 1, 0)
                    self.MakeCellVisible(row + 1, 0)
        if evt.KeyCode == wx.WXK_F4 or evt.KeyCode == wx.WXK_RETURN\
             and evt.AltDown():
            row = self.GetGridCursorRow()
            rec = self.GetTable().get_rec(row)
            names = self.GetTable().GetColNames()[1:]
            parm = dict()
            parm['rec'] = rec
            self.GetHtmlParent().ActiveCtrl = self
            okno = self.GetHtmlParent().new_child_page(self.address + '../'
                     + str(rec[0]) + '/edit/', '', param=parm)
            return
        if evt.KeyCode == wx.WXK_HOME and not evt.ControlDown():
            self.goto_first_row()
# row = self.GetGridCursorRow() self.SetGridCursor(row, 0)
# self.MakeCellVisible(row, 0)
            return
        if evt.KeyCode == wx.WXK_END and not evt.ControlDown():
            self.goto_last_row()
# row = self.GetGridCursorRow() self.SetGridCursor(row, self.GetNumberCols() -
# 1) self.MakeCellVisible(row, self.GetNumberCols() - 1)
            return
        if evt.KeyCode == wx.WXK_SPACE:
            row = self.GetGridCursorRow()
            if row >= 0:
                self.GetTable().sel_row(row)
                if row < self.GetNumberRows() - 1:
                    self.SetGridCursor(row + 1, self.GetGridCursorCol())
                return

# if evt.KeyCode == ord('F') or evt.KeyCode == ord('f'):
# self.GetTable().Filter() row = self.GetGridCursorRow() if row >= 0:
# self.GetTable().SelRow(row) return

        if (evt.KeyCode == ord('S') or evt.KeyCode == ord('s')) and evt.ControlDown():
            self.GetTable().commit()
            self.GetTable().refresh(True)
            evt.Skip()
            return

        if (evt.KeyCode == ord('R') or evt.KeyCode == ord('r')) and evt.ControlDown():
            self.GetTable().refresh(True)
            evt.Skip()
            return


        evt.Skip()
        return

    def on_update_rec_from_form(self, rec):
        row = self.GetGridCursorRow()
        names = self.GetTable().GetColNames()[1:]
        for i in range(len(names)):
            name = names[i]
            self.GetTable().SetValue(row, i, rec[name])
        self.ForceRefresh()

    def accepts_focus(self):
        return True


    def refr_count(
        self,
        old_count,
        count,
        store_pos=0,
        ):
        dy = old_count - count
        if dy != 0:
            if dy > 0:
                msg = GridTableMessage(self.GetTable(),
                                       GRIDTABLE_NOTIFY_ROWS_DELETED, count, dy)
                #print("del dy:", dy)
            else:
                msg = GridTableMessage(self.GetTable(),
                                       GRIDTABLE_NOTIFY_ROWS_APPENDED, -1 * dy)
                #print("append dy:", -1 * dy)
            try:
                self.ProcessTableMessage(msg)
            except:
                pass

            if count>0:
                if store_pos == 0:
                    self.SetGridCursor(0, 0)
                    self.MakeCellVisible(0, 0)
                elif store_pos == 1:
                    row = self.GetGridCursorRow()
                    if row >= count:
                        self.SetGridCursor(0, 0)
                        self.MakeCellVisible(0, 0)
                else:
                    row = self.GetGridCursorRow()
                    if row >= count:
                        self.SetGridCursor(count - 1 + self.CanAppend, 0)
                        self.MakeCellVisible(count - 1 + self.CanAppend, 0)
        if count>0:
            self.AutoSizeColumns(True)


    def on_label_left_click(self, evt):
        if evt.GetCol() >= 0:
            str = self.GetColLabelValue(evt.GetCol())
            if evt.ControlDown():
                self.GetTable().sort(evt.GetCol(), True)
            else:
                self.GetTable().sort(evt.GetCol(), False)
            evt.Skip()

    def on_label_right_click(self, evt):
        message = wx.MessageDialog(self, 'x', 'Komunikat')
        message.ShowModal()

    def on_label_left_dclick(self, evt):
        message = wx.MessageDialog(self, 'y', 'Komunikat')
        message.ShowModal()

    def on_cell_right_click(self, evt):
        message = wx.MessageDialog(self, 'a', 'Komunikat')
        message.ShowModal()

    def action_exists(self, command):
        akcja = self.GetTable().get_actions(self.GetGridCursorRow())
        if akcja and command in akcja:
            return True
        else:
            return False

    def action(self, command):
        akcja = self.GetTable().get_actions(self.GetGridCursorRow())
        if akcja and command in akcja:
            if akcja[command][0] == 'openurl':
                self.LastAction = command
                if command=='get_row':
                    p = akcja[command]
                    id = p[3]['data-id']
                    title = p[3]['data-text']
                    self.GetParent().get_parent_form().ret_ok(id, title)
                    return 1
                else:
                    ret = self.GetParent().GetParent().href_clicked(self, akcja[command][3])
                    ret = 1
                    return ret

            if akcja[command][0] == 'tableurl':
                self.GetTable().proxy.set_address(akcja[command][1])
                if hasattr(self.GetParent(), 'table_url'):
                    self.GetParent().table_url(akcja[command][1])
                self.GetTable().refresh(True)

            if akcja[command][0] == 'command':
                if hasattr(self.GetParent(), 'table_command'):
                    self.GetParent().table_command(akcja[command][1])

    def get_action_list(self, row=0):
        akcje = self.GetTable().get_action_list(row)
        if akcje:
            return (not self.readonly, akcje)
        else:
            return (not self.readonly, None)

    def get_actions(self, row=0):
        akcja = self.GetTable().get_actions(row)
        if akcja:
            return (not self.readonly, list(akcja.items()))
        else:
            return (not self.readonly, None)

    def get_table_and_state(self):
        tableandstate = []
        tableandstate.append((self.GetGridCursorRow(), self.GetGridCursorCol()))
        tableandstate.append(self.GetTable().get_table_and_state())
        return tableandstate

    def duplicate_table_and_state(self):
        tableandstate = []
        tableandstate.append((0, 0))
        tableandstate.append(self.GetTable().duplicate_table_and_state())
        return tableandstate

    def set_table_and_state(self, tableandstate):
        oldrowcount = self.GetTable().last_row_count
        oldtableandstate = self.get_table_and_state()
        self.SetGridCursor(tableandstate[0][0], tableandstate[0][1])
        self.GetTable().set_table_and_state(tableandstate[1])
        rowcount = self.GetTable().GetNumberRows()
        self.refr_count(oldrowcount, rowcount, store_pos=1)
        self.ForceRefresh()
        return oldtableandstate


