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

#author: "Sławomir Chołaj (slawomir.cholaj@gmail.com)"
#copyright: "Copyright (C) ????/2012 Sławomir Chołaj"
#license: "LGPL 3.0"
#version: "0.1a"

import wx
import wx.grid as gridlib
import copy
import schlib.schtools.createparm as createparm
from .gridtablebase import SchGridTableBase


class DataSource(SchGridTableBase):

    def __init__(self, proxy):
        SchGridTableBase.__init__(self)
        self.proxy = proxy
        self.proxy.SetParent(self)
        self.last_page_id = -1
        self.pages_nr = [-1, -1, -1, -1, -1]
        self.pages = [None, None, None, None, None]
        self.last_page = None
        self.max_count = self.proxy.get_max_count()
        self.rec_count = self.max_count

        self.default_rec = self.proxy.GetDefaultRec()

        self.attrs = {}
        self.setparm = False

        self.can_append = 1
        self.read_only = False
        self.is_valid = True

        self.last_row_count = self.max_count + self.can_append

    def invalidate(self):
        self.is_valid = False

    def _scroll(self, end):
        for i in range(end, 4):
            (self.pages)[4 - i] = (self.pages)[3 - i]
            (self.pages_nr)[4 - i] = (self.pages_nr)[3 - i]


    def refr_count(self, count, storePos=0):
        self.rec_count = count - self.can_append - self.append_count
        return SchGridTableBase.refr_count(self, count, storePos)

    def refresh(self, storePos):
        #store pos
        #0 - no store, cursor - pos 1
        #1 - store, if out of range - pos 1
        #2 - store, if out of range - pos = max
        self.commit()
        self.append_count = 0
        self.last_page_id = -1
        self.pages_nr = [-1, -1, -1, -1, -1]
        self.pages = [None, None, None, None, None]
        self.last_page = None
        self.max_count = self.proxy.get_max_count()
        self.rec_to_update = dict()
        self.rec_to_instert = dict()
        self.rec_to_delete = []
        self.refr_count(self.proxy.GetCount()+ self.can_append + self.append_count, storePos)
        self.GetView().ForceRefresh()

    def get_rec(self, nr_rec):
        if not self.is_valid:
            return None
        if nr_rec < self.rec_count or self.rec_count == self.max_count:
            strona = nr_rec // 256
            if strona == self.last_page_id:
                if self.last_page != None and nr_rec % 256 < len(self.last_page):
                    return (self.last_page)[nr_rec % 256]
                else:
                    return None
            else:
                if strona in self.pages_nr:
                    id = self.pages_nr.index(strona)
                    self.last_page = (self.pages)[id]
                    self.last_page_id = strona
                    self._scroll(4 - id)
                    (self.pages)[0] = self.last_page
                    (self.pages_nr)[0] = strona
                    return self.get_rec(nr_rec)
                else:
                    if self.setparm == False:
                        self.setparm = True
                        parm = createparm.create_parm(self.GetView().address, self.GetView().GetParent().get_parm_obj())
                        if parm:
                            self.proxy.set_address_parm(parm[2])

                    if self.proxy.is_valid:
                        nowaStrona = self.proxy.get_page(strona)
                    else:
                        self.is_valid = False
                        nowaStrona = None

                    if nowaStrona != None:
                        self._scroll(0)
                        (self.pages_nr)[0] = strona
                        (self.pages)[0] = nowaStrona
                        self.last_page = (self.pages)[0]
                        self.last_page_id = strona

                        if len(nowaStrona) < 256 and self.rec_count != strona * 256 + len(nowaStrona):
                            self.refr_count(self.proxy.GetCount()+self.can_append+self.append_count,2)
                        return self.get_rec(nr_rec)
                    else:
                        self.refr_count(self.proxy.GetCount(), 2)
                        return None
        else:
            return None

    def GetRecAsStr(self, nrRec):
        return self.proxy.GetRecAsStr(nrRec)

    def GetColNames(self):
        return self.proxy.GetColNames()

    def GetAutoCols(self):
        return self.proxy.GetAutoCols()

    def GetColTypes(self):
        return self.proxy.GetColTypes()

    def GetColIcons(self):
        return self.proxy.GetColIcons()

    def commit(self):
        if self.read_only:
            return

        test = False
        update = []

        if len(self.rec_to_instert) > 0 or len(self.rec_to_delete) > 0:
            test = True

        if test or len(self.rec_to_update) > 0:

            self.rec_count = self.rec_count + len(self.rec_to_instert)

            for rec in list(self.rec_to_update.keys()):
                update.append((self.rec_to_update)[rec])
            insert = []
            for rec in list(self.rec_to_instert.keys()):
                insert.append((self.rec_to_instert)[rec])
            delete = []
            for rec in self.rec_to_delete:
                delete.append(self.get_rec(rec)[0])
            self.proxy.sync_data(update, insert, delete)

            self.rec_to_update = dict()
            self.rec_to_instert = dict()
            self.rec_to_delete = []

    def data_changed(self):
        if self.read_only:
            return False
        if len(list(self.rec_to_update.keys())) > 0 or len(list(self.rec_to_instert.keys())) > 0 or len(self.rec_to_delete) > 0:
            return True
        else:
            return False

    def GetAttr(self, row, col, kind):
        if not self.is_valid:
          return SchGridTableBase.GetAttr(self, row, col, kind)
        if row < self.rec_count and (row not in self.rec_to_update) and ( not row in self.rec_to_delete ) and (not self._is_sel(row)):
            rec = self.get_rec(row)
            if rec:
                value = rec[col + 1]
                if value.__class__ in (tuple,list) :
                    if value[1] in self.attrs:
                        attr = self.attrs[value[1]]
                    else:
                        attr = gridlib.GridCellAttr()
                        atrybuty=value[1].split(',')
                        style = atrybuty[0]
                        bgcolor = None
                        color = None
                        if len(atrybuty)>1: bgcolor = atrybuty[1]
                        if len(atrybuty)>2: color = atrybuty[2]

                        if bgcolor and len(bgcolor)>1:
                            attr.SetBackgroundColour(bgcolor)
                        if color and len(color)>1:
                            attr.SetTextColour(color)
                        if style and len(style)>0:
                            if 's' in style:
                                font = self.GetView().GetDefaultCellFont()
                                font.SetWeight(wx.FONTWEIGHT_BOLD)
                                attr.SetFont(font)
                            if '>' in style:
                                attr.SetAlignment(wx.ALIGN_RIGHT, -1)
                            if '-' in style:
                                attr.SetAlignment(wx.ALIGN_CENTRE, -1)
                        (self.attrs)[value[1]] = attr
                else:
                    attr = self.attr_normal
            else:
                attr = self.attr_normal
            attr.IncRef()
            return attr
        else:
            return SchGridTableBase.GetAttr(self, row, col, kind)


    def get_rec_count(self):
        return self.rec_count

    def _get_number_rows(self):
        return self.rec_count + self.can_append + self.append_count

    def GetNumberCols(self):
        return len(self.GetColNames()) - 1

    def IsEmptyCell(self, row, col):
        rec = self.get_rec(row)
        if rec != None:
            if rec[col] == None:
                return True
            else:
                return False
        else:
            return True

    def get_action_list(self, row, col=None):
        return rec[rowlen+1]

    def get_actions(self, row, col=None):
        rowlen=len(self.GetColNames())
        rec = self.get_rec(row)
        if rec and len(rec)>rowlen+1:
            return rec[rowlen+1]
        else:
            return dict()

    def GetValue(self, row, col):

        if row < self.rec_count:
            if row in self.rec_to_update:
                rec = (self.rec_to_update)[row]
                #[col + 1]
            else:
                rec = self.get_rec(row)
            if rec != None:

                if rec[col + 1] == None:
                    return ""
                else:
                    ret = rec[col + 1]
                    if ret.__class__ == tuple or ret.__class__ == list:
                        ret = ret[0]
                    if type(ret) == str:
                        return ret
                    else:
                        return str(ret)
            else:
                return ""
        else:
            if row in self.rec_to_instert:
                return str((self.rec_to_instert)[row][col + 1])
            else:
                return ""


    def SetValue(self, row, col, value):
        if self.read_only:
            return

        if row >= self.rec_count:

            if row not in self.rec_to_instert:
                (self.rec_to_instert)[row] = copy.copy(self.default_rec)

            (self.rec_to_instert)[row][col + 1] = value

            if row == self.GetNumberRows() - 1:
                self.append_count = self.append_count + 1
                msg = gridlib.GridTableMessage(self, gridlib.GRIDTABLE_NOTIFY_ROWS_APPENDED, 1)
                self.GetView().ProcessTableMessage(msg)
        else:

            if row not in self.rec_to_update:
                (self.rec_to_update)[row] = self.get_rec(row)
            (self.rec_to_update)[row][col + 1] = value
            if row in self.rec_to_delete:
                self.rec_to_delete.remove(row)

    def CanGetValueAs(self, row, col, typeName):
        colType = self.GetColTypes()[col + 1].split(':')[0]
        if typeName == colType:
            return True
        else:
            return False

    def CanSetValueAs(self, row, col, typeName):
        return self.CanGetValueAs(row, col, typeName)


    def GetColLabelValue(self, col):
        return self.GetColNames()[col + 1]

    def GetValueAsBool(self, row, col):
        colType = self.GetColTypes()[col + 1].split(':')[0]
        if colType=='bool':
            ret = self.GetValue(row,col)
            if ret:
                return True
            else:
                return False
        else:
            return False


    def SetValueAsBool(self, row, col, value):
        self.SetValue(row, col, value)

    def GetTypeName(self, row, col):
        #try:
        #    ret = self.GetColTypes()[col + 1]
        #except:
        #    print("GetTypeName:", col, self.GetColTypes())
        #    ret = None
        #return ret
        #print(col, self.GetColTypes()[col + 1])

        try:
            return self.GetColTypes()[col + 1]
        except:
            print("GetTypeName:", col, self.GetColTypes())

    def DeleteRows(self, row, il):
        if self.read_only:
            return
        if row < self.rec_count:
            if row in self.rec_to_update:
                del (self.rec_to_update)[row]
            if row in self.rec_to_delete:
                self.rec_to_delete.remove(row)
            else:
                self.rec_to_delete.append(row)
            self.GetView().ForceRefresh()
            return True
        else:
            if row in self.rec_to_instert:
                msg = gridlib.GridTableMessage(self, gridlib.GRIDTABLE_NOTIFY_ROWS_DELETED, row, il)
                del (self.rec_to_instert)[row]
                self.append_count = self.append_count - 1
                self.GetView().ProcessTableMessage(msg)
                self.GetView().ForceRefresh()

                for pos in list(self.rec_to_instert.keys()):
                    if pos > row:
                        (self.rec_to_instert)[pos - 1] = (self.rec_to_instert)[pos]
                        del (self.rec_to_instert)[pos]

                return True
            return False

    def sort(self, column, append):
        SchGridTableBase.sort(self, column, append)
        sort = ""
        test = 0
        if len(self.tabsort) > 0:
            for i in self.tabsort:
                if test == 0:
                    test = 1
                else:
                    sort = sort + ','

                if i < 0:
                    sort = sort + "-" + self.GetColNames()[-1 * i]
                else:
                    sort = sort + self.GetColNames()[i]

            self.proxy.set_parm("sort", sort)

        self.refresh(0)


    def auto_update(self, col_name, col_names, rec):
        """po zmianie pozycji w kolumnie o nazwie col_name funkcja przetwarza aktualny rekord
      w wyniku zwracaj\xef\xbf\xbdc rekord przetworzony"""

        return self.proxy.auto_update(col_name, col_names, rec)



    def filter_cmp(self, pos, key):
        if self.filter_id >=0:
            elem = pos[self.filter_id]
            if elem.__class__ == tuple:
                elem=elem[0]
            if str(elem).upper().startswith(key.upper()):
                return True
            else:
                return False
        else:
            return False


    def filter(self, key):
        #print 'value', key
        self.key = key
        self.proxy.set_parm('value', key)
        self.refresh(0)


    def get_table_and_state(self):
        tableandstate = SchGridTableBase.get_table_and_state(self)

        tableandstate.append(self.proxy)
        tableandstate.append( (self.last_page_id, self.pages_nr, self.pages, self.last_page,
                             self.max_count, self.rec_count ) )
        return tableandstate

    def duplicate_table_and_state(self):
        tableandstate = SchGridTableBase.duplicate_table_and_state(self)
        self.proxy = self.proxy.clone()
        self.last_page_id = -1
        self.pages_nr = [-1, -1, -1, -1, -1]
        self.pages = [None, None, None, None, None]
        self.last_page = None
        self.max_count = self.proxy.get_max_count()
        self.rec_count = self.max_count
        return tableandstate


    def set_table_and_state(self, tableandstate):
        oldtableandstate = self.get_table_and_state()
        tbl = tableandstate[1:]
        self.proxy = tbl[0]
        self.last_page_id = tbl[1][0]
        self.pages_nr = tbl[1][1]
        self.pages = tbl[1][2]
        self.last_page = tbl[1][3]
        self.max_count = tbl[1][4]
        self.rec_count = tbl[1][5]

        SchGridTableBase.set_table_and_state(self, tableandstate)

        return oldtableandstate

    def run_cmd(self, cmd, parm=None, option=0):
        x = self.make_exec_cmd(cmd, option)
        if parm:
            x.append(parm)
        ret = self.proxy.exec(x)
        return ret


