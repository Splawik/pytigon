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


from schlib.schhtml.basehtmltags import BaseHtmlElemParser, BaseHtmlAtomParser, register_tag_map
from schlib.schhtml.atom import  Atom
from schlib.schhtml.render_helpers import RenderBackground, RenderBorder, get_size, sizes_from_attr
from collections import deque
from .p_tags import Par
from .block_tags import BodyTag


class TdRef(object):

    def __init__(self, tdref, parent, col, col_to_parent, row_to_parent, rowspan=0):
        self.parent = parent
        self.col = col
        self.col_to_parent = col_to_parent
        self.row_to_parent = row_to_parent
        self.rowspan = rowspan
        self.colspan = 0
        self.from_ref = None
        if tdref.__class__ == TdRef:
            self.tdref = tdref.tdref
            self.from_ref = True
        else:
            self.tdref = tdref
        self.width = -1
        self.height = -1
        self.data = self.tdref.data

    def calc_height(self):
        return self.tdref.calc_height()


class TdEmptyTag(object):

    def __init__(self):
        self.colspan = 1
        self.rowspan = 1
        self.width = 0
        self.attrs = {}

    def calc_width(self, force=None):
        return [0, 0, 0]

    def calc_height(self):
        return 0

    def render(self, dc):
        return (0, False)

    def set_width(self, width):
        self.width = 0

    def get_width(self):
        return [self.width, self.width, self.width]

    def get_height(self):
        return 0

    def to_txt(self):
        return ""
    
    def to_obj_tab(self):
        return {}


class TrRef(object):

    def __init__(self, row, attrs):
        self.row = row
        self.height = -1
        self.attrs = attrs

    def __getitem__(self, id):
        return self.row[id]

    def __setitem__(self, id, value):
        self.row[id] = value

    def __len__(self):
        return len(self.row)


class TableTag(BaseHtmlAtomParser):

    def __init__(self, parent, parser, tag, attrs):
        BaseHtmlAtomParser.__init__(self, parent, parser, tag, attrs)
        self.child_tags = ['tr', 'caption', 'li', 'ctr*']
        self.caption = None
        if self.parent.__class__ in (BodyTag,):
            self.subtab = False
        else:
            self.subtab = True
        rb = RenderBorder(self)
        self.border = rb.get_size()
        if 'cellspacing' in attrs:
            self.cellspacing = sizes_from_attr(attrs['cellspacing'])
        else:
            self.cellspacing = [0, 0, 0, 0]
        if 'cellpadding' in attrs:
            self.cellpadding = sizes_from_attr(attrs['cellpadding'])
        else:
            self.cellpadding = [0, 0, 0, 0]
        if 'padding' in attrs:
            self.padding = sizes_from_attr(attrs['padding'])
        else:
            self.padding = [0, 0, 0, 0]
        self.tr_list = []
        self.tr_queue = deque()
        self.col_count = -1
        self.sizes = None
        self.sizes_ok = False
        self.dy_rendered = 0
        self.in_close = False
        self.start = True
        self.end = False
        self.render_helpers = [RenderBackground(self)]
        self.atom = None
        self.lp = 0

    def _get_pseudo_margins(self):
        return [self.border[0] + self.padding[0], self.border[1]
                 + self.padding[1], self.border[2] + self.padding[2],
                self.border[3] + self.padding[3]]

    def get_width(self):
        if self.width >= 0:
            return [self.width, self.width, self.width]
        else:
            if 'width' in self.attrs:
                (parent_width, parent_min, parent_max) = \
                    self.parent.get_client_width()
                width = self._norm_sizes([self.attrs['width']], parent_width)[0]
                min = self._norm_sizes([self.attrs['width']], parent_min)[0]
                max = self._norm_sizes([self.attrs['width']], parent_max)[0]
                return [width, min, max]
            return self.parent.get_client_width()

    def get_client_width(self):
        (opt, min, max) = self.get_width()
        w = self.border[0] + self.border[1] + self.padding[0] + self.padding[1]
        if opt > 0:
            opt -= w
        if min > 0:
            min -= w
        if max > 0:
            max -= w
        return [opt, min, max]

    def calc_col_sizes(self):
        if self.col_count <= 0:
            return
        if not self.sizes_ok:
            if not self.sizes:
                self.sizes = [[-1, -1, -1]] * self.col_count
            for i in range(0, self.col_count):
                if self.sizes[i][0] < 0:
                    (opt, min, max) = (0, 0, 0)
                    for pos in self.tr_list:
                        if pos[i].__class__ != TdRef and pos[i].colspan == 1:
                            s = pos[i].get_width()
                            if opt < s[0]:
                                opt = s[0]
                            if min < s[1]:
                                min = s[1]
                            if max < s[2]:
                                max = s[2]
                            self.sizes[i] = [opt, min, max]
            for i in range(0, len(self.tr_list)):
                for j in range(0, self.col_count):
                    pos = self.tr_list[i][j]
                    if pos.__class__ != TdRef and pos.colspan > 1:
                        s = pos.get_width()
                        s2 = [0, 0, 0]
                        for k in range(0, pos.colspan):
                            s2[0] += self.sizes[j + k][0]
                            s2[1] += self.sizes[j + k][1]
                            s2[2] += self.sizes[j + k][2]
                        delta = [0, 0, 0]
                        for k in range(0, 3):
                            if s[k] > s2[k]:
                                delta[k] = (s[k] - s2[k]) / pos.colspan
                        if delta[0] != 0 or delta[1] != 0 or delta[2] != 0:
                            l = 1
                            if delta[l] != 0:
                                for k in range(0, pos.colspan):
                                    self.sizes[j + k][l] += delta[l]
            (opt, min, max) = (0, 0, 0)
            for pos in self.sizes:
                opt += pos[0]
                min += pos[1]
                max += pos[2]
            if self.width < 0:
                if self.parent.width >= 0:
                    parent_width = self.get_parent_width()
                    if opt > parent_width or max > parent_width:
                        self.width = parent_width
                    else:
                        self.width = opt + self.border[0] + self.border[1]\
                             + self.padding[0] + self.padding[1]
                else:
                    self.width = opt + self.border[0] + self.border[1]\
                         + self.padding[0] + self.padding[1]
            if self.width > 0:
                width2 = (((self.width - self.border[0]) - self.border[1])
                           - self.padding[0]) - self.padding[1]
                if width2 < min:
                    for pos in self.sizes:
                        pos[0] = pos[1]
                else:
                    if width2 <= opt:
                        if opt - min == 0:
                            proc = 1
                        else:
                            proc = ((width2 - min) * 1.0) / (opt - min)
                        for pos in self.sizes:
                            pos[0] = pos[1] + (pos[0] - pos[1]) * proc
                    else:
                        if width2 <= max:
                            proc = ((width2 - opt) * 1.0) / (max - opt)
                            for pos in self.sizes:
                                pos[0] = pos[0] + (pos[2] - pos[0]) * proc
                        else:
                            proc = (width2 * 1.0) / max
                            for pos in self.sizes:
                                pos[0] = pos[2] * proc
            self.sizes_ok = True

    def close(self):
        self.in_close = True
        if self.subtab:
            self.calc_col_sizes()
            self.height = self.get_height()
            self.atom = Atom(self, self.width, 0, self.height, 0, None)
            self.make_atom_list()
            self.atom_list.append_atom(self.atom)
            self.parent.append_atom_list(self.atom_list)
        else:
            self.calc_col_sizes()
            BaseHtmlAtomParser.close(self)

    def calc_width(self):
        self.calc_col_sizes()
        return (self.width, self.width, self.width)

    def calc_height(self):
        self._calculate_rows_height()
        size = self._iter()
        y = 0
        for row in self.tr_list[:size]:
            sy = self._row_height(row)
            y += sy
        if self.start:
            y += self.border[2] + self.padding[2]
        if self.end:
            y += self.border[3] + self.padding[3]
        return y

    def child_ready_to_render(self, child):
        if self.col_count < 0:
            i = 0
            for pos in child.td_list:
                i += pos.colspan
            self.col_count = i
        if len(self.tr_queue) > 0:
            row = self.tr_queue.popleft()
        else:
            row = [None] * self.col_count
        i = 0
        rowspan = 1
        for pos in child.td_list:
            try:
                while row[i] != None:
                    i += 1
            except:
                continue
            row[i] = pos
            if pos.colspan > 1:
                for j in range(1, pos.colspan):
                    row[i + j] = TdRef(pos, self, i + j, j, 0, pos.rowspan)
            i += pos.colspan
            if pos.rowspan > rowspan:
                rowspan = pos.rowspan
        row2 = []
        for pos in row:
            if pos:
                row2.append(pos)
            else:
                row2.append(TdEmptyTag())
        self.tr_list.append(TrRef(row2, child.attrs))
        if rowspan > 1:
            delta = (rowspan - len(self.tr_queue)) - 1
            if delta > 0:
                for j in range(0, delta):
                    self.tr_queue.append([None] * self.col_count)
            tr = self.tr_list[-1]
            for i in range(0, self.col_count):
                if tr[i].rowspan > 1:
                    for j in range(0, tr[i].rowspan - 1):
                        if tr[i].__class__ == TdRef:
                            col_to_parent = tr[i].col_to_parent
                        else:
                            col_to_parent = 0
                        self.tr_queue[j][i] = TdRef(tr[i], self, i, col_to_parent, j + 1, 0)
        if self.width >= 0 and len(self.tr_queue) == 0:
            if not self.sizes_ok and self.col_count > 0:
                if not self.sizes:
                    self.sizes = [[-1, -1, -1]] * self.col_count
                no_size_count = 0
                no_size_id = -1
                width_tab = 0
                for i in range(0, self.col_count):
                    td = self.tr_list[-1][i]
                    if td and td.width > 0:
                        self.sizes[i] = td.get_width()
                    if self.sizes[i][0] < 0:
                        no_size_count += 1
                        no_size_id = i
                    else:
                        width_tab += self.sizes[i][0]
                if no_size_count == 1:
                    self.sizes[no_size_id][0] = ((((self.width - width_tab)
                             - self.border[0]) - self.border[1])
                             - self.padding[0]) - self.padding[1]
                    self.sizes[no_size_id][1] = self.sizes[no_size_id][0]
                    self.sizes[no_size_id][2] = self.sizes[no_size_id][0]
                    self.tr_list[-1][i].set_width(self.width - width_tab)
                    no_size_count = 0
                if no_size_count == 0:
                    self.sizes_ok = True
            if self.sizes_ok and not self.subtab:
                BaseHtmlAtomParser.child_ready_to_render(self, child)
        self.lp += 1

    def _row_height(self, row):
        if row.height >= 0:
            return row.height
        else:
            dy = 0
            for i in range(0, self.col_count):
                if row[i].__class__ != TdRef and row[i].rowspan == 1:
                    width = 0
                    for j in range(0, row[i].colspan):
                        width += self.sizes[i + j][0]
                    row[i].set_width(width)
                    sy = row[i].get_height()
                    if sy > dy:
                        dy = sy
            row.height = dy
            return dy

    def _row_rowspan_height(self, rows):
        dy = 0
        for i in range(0, self.col_count):
            if rows[0][i].__class__ != TdRef and rows[0][i].rowspan > 1:
                width = 0
                for j in range(0, rows[0][i].colspan):
                    width += self.sizes[i + j][0]
                sy = rows[0][i].get_height()
                sy2 = 0
                for j in range(0, rows[0][i].rowspan):
                    sy2 += self._row_height(rows[j])
                if sy > sy2:
                    delta = (sy - sy2) / rows[0][i].rowspan
                    for j in range(0, rows[0][i].rowspan):
                        rows[j].height = rows[j].height + delta

    def _calculate_rows_height(self):
        for row in self.tr_list:
            self._row_height(row)
        for i in range(0, len(self.tr_list)):
            self._row_rowspan_height(self.tr_list[i:])

    def _iter(self):
        if self.subtab:
            self.end = True
            return len(self.tr_list)
        else:
            rows = 0
            stack = 1
            for row_id in range(0, len(self.tr_list)):
                row = self.tr_list[row_id]
                max_row_span = 1
                for td in row:
                    if td.rowspan > max_row_span:
                        max_row_span = td.rowspan
                stack += max_row_span - 2
                rows += 1
                if stack == 0 and not ('page-break-inside' in row.attrs and row.attrs['page-break-inside'] == 'avoid'):
                    if self.in_close and len(self.tr_list) == rows:
                        self.end = True
                    return rows
            if self.in_close:
                self.end = True
            return rows

    def render(self, dc_parm):
        self.reg_id(dc_parm)
        self.reg_end()
        if 'border-color' in self.attrs:
            rgb = dc_parm.rgbfromhex(self.attrs['border-color'])
        else:
            rgb = (0, 0, 0)
        if not self.sizes:
            if self.border[2] > 0:
                dc_parm.set_color(rgb[0], rgb[1], rgb[2], 255)
                dc_parm.set_line_width(self.border[0])
                dc_parm.add_line(self.padding[0], self.padding[2], (self.width
                                  - self.padding[0]) - self.padding[1], 0)
                dc_parm.draw()
            return (self.padding[2] + self.padding[3], False)
        self._calculate_rows_height()
        dc2 = dc_parm
        for r in self.render_helpers:
            dc2 = r.render(dc2)
        width = 0
        if self.width < 0:
            for pos in self.sizes:
                width += pos[0]
            self.width = width
        if self.border[0] > 0:
            brd = self.border[0]
            brd1 = brd / 2
            brd2 = brd - brd1
        else:
            brd = brd1 = brd2 = 0
        if self.border[0] + self.padding[0] > 0:
            if self.border[0] > 0:
                dc_parm.set_color(rgb[0], rgb[1], rgb[2], 255)
                dc_parm.set_line_width(self.border[0])
                if self.subtab:
                    dc_parm.add_line(self.padding[0] + brd1, self.padding[2] + brd1, 0,
                            ((dc_parm.dy - self.padding[2]) - self.padding[3]) - brd)
                    dc_parm.add_line((dc_parm.dx - 1 * self.padding[1]) - brd2, self.padding[2] + brd1, 0,
                            ((dc_parm.dy - self.padding[2]) - self.padding[3]) - brd)
                else:
                    if not self.start:
                        if self.end:
                            dc_parm.add_line(self.padding[0] + brd1, -1 * brd2, 0, dc_parm.dy - self.padding[3])
                            dc_parm.add_line((self.width - 1 * self.padding[1]) - brd2, -1 * brd2, 0,
                                    dc_parm.dy - self.padding[3])
                        else:
                            dc_parm.add_line(self.padding[0] + brd1, -1 * brd2, 0, dc_parm.dy)
                            dc_parm.add_line((self.width - 1 * self.padding[1]) - brd2, -1 * brd2, 0, dc_parm.dy)
                dc_parm.draw()
            dc = dc_parm.subdc(self.border[0] + self.padding[0], 0, (((dc_parm.dx - self.border[0]) - self.border[1]) -
                    self.padding[0]) - self.padding[1], dc_parm.dy)
        else:
            dc = dc_parm
        if self.start:
            if self.border[2] > 0:
                dc_parm.set_color(rgb[0], rgb[1], rgb[2], 255)
                dc.set_line_width(self.border[0])
                dc.add_line(-1 * brd2, self.padding[2] + brd1, ((self.width - self.padding[0]) -
                        self.padding[1]) - brd, 0)
                dc.draw()
            self.start = False
            if not self.subtab:
                self.height = -1
                return (self.border[2] + self.padding[2], True)
            else:
                dc = dc.subdc(0, self.padding[2] + self.border[2], dc.dx, dc.dy - self.padding[2])
        size = self._iter()
        y = 0
        for row_id in range(0, size):
            row = self.tr_list[row_id]
            x = 0
            sy = self._row_height(row)
            for col in range(0, self.col_count):
                if row[col].__class__ != TdRef:
                    if row[col].colspan > 1:
                        dx = 0
                        for i in range(0, row[col].colspan):
                            dx += self.sizes[col + i][0]
                    else:
                        dx = self.sizes[col][0]
                    if row[col].rowspan > 1:
                        dy = sy
                        for i in range(1, row[col].rowspan):
                            dy += self._row_height(self.tr_list[row_id + i])
                    else:
                        dy = sy
                    row[col].render(dc.subdc(x, y, dx, dy))
                x += self.sizes[col][0]
            y += sy
        if len(self.tr_list) > size:
            self.tr_list = self.tr_list[size:]
            cont = True
        else:
            self.tr_list = []
            cont = False
        self.dy_rendered += dc.get_size()[1]
        if self.end:
            if self.border[0] > 0:
                dc_parm.set_color(rgb[0], rgb[1], rgb[2], 255)
                dc.set_line_width(self.border[0])
                dc_parm.add_line(self.padding[0] + brd1, (dc_parm.dy - self.padding[3]) - brd2,
                        ((self.width - self.padding[0]) - self.padding[1]) - brd, 0)
                dc_parm.draw()
            y += self.border[3] + self.padding[3]
        self.height = -1
        return (y, cont)

    def draw_atom(self, dc, style, x, y, dx, dy):
        if not self.sizes:
            return
        self.calc_col_sizes()
        xx = 0
        for col in range(0, self.col_count):
            xx += self.sizes[col][0]
        dc2 = dc.subdc(x, y, self.width, self.height)
        cont = True
        while cont:
            (dy, cont) = self.render(dc2)
            dc2.y += dy


class TrTag(BaseHtmlElemParser):

    def __init__(self, parent, parser, tag, attrs):
        BaseHtmlElemParser.__init__(self, parent, parser, tag, attrs)
        self.child_tags = ['td', 'th']
        self.td_list = []

    def close(self):
        if len(self.td_list) > 0:
            BaseHtmlElemParser.close(self)

    def child_ready_to_render(self, child):
        self.td_list.append(child)

    def get_width(self):
        return self.parent.get_width()

    def get_client_width(self):
        return self.parent.get_client_width()

    def set_width(self, value):
        pass

    def _get_pseudo_margins(self):
        return [1, 1, 1, 1]

    width = property(get_width, set_width)


class TdTag(Par):

    def __init__(self, parent, parser, tag, attrs):
        Par.__init__(self, parent, parser, tag, attrs)
        self.border = [0, 0, 0, 0]
        self.padding = [0, 0, 0, 0]
        if 'colspan' in attrs:
            self.colspan = int(attrs['colspan'])
        else:
            self.colspan = 1
        if 'rowspan' in attrs:
            self.rowspan = int(attrs['rowspan'])
        else:
            self.rowspan = 1
        try:
            if not 'border' in attrs:
                self.attrs['border'] = self.parent.parent.border
            if not 'cellspacing' in attrs:
                self.attrs['cellspacing'] = self.parent.parent.cellspacing
            if not 'cellpadding' in attrs:
                self.attrs['cellpadding'] = self.parent.parent.cellpadding
        except:
            pass
        if 'width' in attrs:
            parent_width = parent.get_client_width()[0]
            if parent_width > 0:
                self.width = self._norm_sizes([attrs['width']], parent_width)[0]
        self.extra_space = get_size(self.render_helpers)

    def close(self):
        BaseHtmlAtomParser.close(self)

    def get_client_width(self):
        (opt, min, max) = self.get_width()
        if opt > 0:
            opt -= self.border[0] + self.border[1] + self.padding[0]\
                 + self.padding[1]
        if min > 0:
            min -= self.border[0] + self.border[1] + self.padding[0]\
                 + self.padding[1]
        if max > 0:
            max -= self.border[0] + self.border[1] + self.padding[0]\
                 + self.padding[1]
        return [opt, min, max]


class CaptionTag(BaseHtmlElemParser):

    def __init__(self, parent, parser, tag, attrs,):
        BaseHtmlElemParser.__init__(self, parent, parser, tag, attrs)
        self.td_list = []

    def close(self):
        self.parent.caption = ''.join(self.data)
        BaseHtmlElemParser.close(self)


register_tag_map('table', TableTag)
register_tag_map('caption', CaptionTag)
register_tag_map('tr', TrTag)
register_tag_map('td', TdTag)
register_tag_map('th', TdTag)
register_tag_map('hr', TableTag)

