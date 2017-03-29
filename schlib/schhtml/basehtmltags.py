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

import fnmatch

from schlib.schhtml.atom import AtomList


class BaseHtmlElemParser(object):
    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, x):
        self._height = x

    def __init__(self,parent,parser,tag,attrs):
        self._height = -1
        self.parent = parent
        self.parser = parser
        self.tag = tag
        self.close_tag = tag
        self.attrs = attrs
        css_attrs = self.parser.css.get_dict(self)
        for pos in css_attrs:
            if not pos in self.attrs:
                self.attrs[pos] = css_attrs[pos]
        self.child_tags = []
        self.data = []
        self.width = -1
        self.height = -1
        self.dy = 0
        if 'width' in attrs:
            if '%' in attrs['width']:
                parent_width = self.get_parent_width()
            else:
                parent_width = 0
            if parent_width >= 0:
                self.width = self._norm_sizes([attrs['width']], parent_width)[0]
        if 'height' in attrs:
            if '%' in attrs['height']:
                parent_height = self.get_parent_height()
            else:
                parent_height = 0
            if parent_height >= 0:
                self.height = self._norm_sizes([attrs['height']],
                        parent_height)[0]
        self.rendered_childs = []

        self.dc_info = None
        self.last_rendered_dc = None
        self.rendered_rects = []
        self.reg_flag = True
        self.sys_id = -1
        self.hover = False
        self.hover_css_attrs = {}
        self.gparent = self
        self.form_obj = None

    def set_hover(self, enable=True):
        self.hover = enable

    def can_hover(self):
        if len(self.hover_css_attrs) > 0:
            return True
        return False

    def get_parent_width(self):
        parent = self.parent
        while parent:
            try:
                if parent.width >= 0:
                    parent_width = parent.get_client_width()[0]
                    if parent_width >= 0:
                        return parent_width
            except:
                pass
            parent = parent.parent
        return -1

    def get_parent_height(self):
        parent = self.parent
        while parent:
            if parent.height >= 0:
                parent_height = parent.get_client_height()
                if parent_height >= 0:
                    return parent_height
            parent = parent.parent
        return -1

    def _get_pseudo_margins(self):
        return [0, 0, 0, 0]

    def _get_parent_pseudo_margins(self):
        m = self._get_pseudo_margins()
        if self.parent:
            margins = self.parent._get_parent_pseudo_margins()
            m[0] += margins[0]
            m[1] += margins[1]
            m[2] += margins[2]
            m[3] += margins[3]
        return m

    def get_atrr(self, name):
        obj = self
        while obj:
            if name in obj.attrs:
                return obj.attrs[name].lower()
            obj = obj.get_parent()
        return None

    def get_style_id(self):
        color = self.get_atrr('color')
        font_family = self.get_atrr('font-family')
        font_size = self.get_atrr('font-size')
        font_style = self.get_atrr('font-style')
        font_weight = self.get_atrr('font-weight')
        text_decoration = self.get_atrr('text-decoration')
        if not color[0] == '#':
            color = '#000'
        if not font_family in ('serif', 'sans-serif', 'monospace', 'cursive', 'fantasy'):
            font_family = 'sans-serif'
        if not '%' in font_size:
            font_size = 100
        else:
            try:
                font_size = int(font_size.replace('%', ''))
            except:
                font_size = 100
        if 'italic' in font_style:
            font_style = 1
        else:
            font_style = 0
        if 'bold' in font_weight:
            font_weight = 1
        else:
            font_weight = 0
        if 'underline' in text_decoration or 'oblique' in text_decoration:
            text_decoration = 1
        else:
            text_decoration = 0
        p = '%s;%s;%d;%d;%d;%d' % (color,font_family,font_size,font_style,font_weight,text_decoration,)
        id = self.dc_info.get_style_id(p)
        return id

    def get_id(self):
        if 'id' in self.attrs:
            return self.attrs['id'].lower()
        else:
            return None

    def get_cls(self):
        if 'class' in self.attrs:
            return self.attrs['class'].lower()
        else:
            return None

    def get_tag(self):
        return self.tag.lower()

    def get_parent(self):
        return self.parent

    def class_from_tag_name(self, tag):
        if tag in tag_class_map:
            return tag_class_map[tag]
        elif tag[:3] + '*' in tag_class_map:
            return tag_class_map[tag[:3] + '*']
        else:
            return None

    def handle_starttag(self,parser,tag,attrs):
        if tag in self.child_tags or tag=='comment':
            if tag=='script':
                print("tag:", tag)
            handler = self.class_from_tag_name(tag)
            if handler:
                return handler(self, parser, tag, attrs)
            else:
                return None
        elif tag[:3] + '*' in self.child_tags:
            return self.class_from_tag_name(tag[:3] + '*')(self, parser, tag, attrs)
        else:
            if tag.startswith('_') and tag in tag_class_map:
                return self.class_from_tag_name(tag)(self, parser, tag, attrs)
            else:
                return None

    def handle_endtag(self, tag):
        if tag == self.close_tag:
            self.close()
            return self.parent
        else:
            return self

    def handle_data(self, data):
        self.data.append(data)

    def close(self):
        if self.parent:
            self.parent.child_ready_to_render(self)

    def finish(self):
        pass

    def child_ready_to_render(self, child):
        self.rendered_childs.append(child)
        if not ('page-break-inside' in child.attrs and child.attrs['page-break-inside'] == 'avoid'):
            self.parent.child_ready_to_render(self)

    def render(self, dc):
        if len(self.rendered_childs):
            for child in self.rendered_childs:
                ret = self.rendered_child.render(dc.subdc(0, 0, self.child_dx,
                        self.child_dy))
                self.dy += self.child_dy
                self.rendered_child = None
            return ret
        return True

    def refresh(self):
        if self.last_rendered_dc:
            self.render(self.last_rendered_dc)

    def reg_id(self, dc):
        if self.reg_flag and 'id' in self.attrs:
            self.parser.reg_id_obj(self.attrs['id'], dc, self)

    def reg_action(self, action, dc):
        if self.reg_flag:
            self.parser.reg_action_obj(action, dc, self)

    def reg_end(self):
        self.reg_flag = False

    def _norm_sizes(self, sizes, dxy):
        ret = []
        for pos in sizes:
            t = str(pos).split('%')
            if len(t) == 2:
                if dxy >= 0:
                    x = int((float(t[0]) * dxy) / 100)
                else:
                    x = -1
                if x >= 0 and len(t[1]) > 0:
                    x += int(t[1])
            else:
                x = int(float(t[0].replace('px', '').replace('em', '')))
            ret.append(x)
        return ret

    def set_width(self, width):
        self.width = width

    def get_width(self):
        if self.width >= 0:
            return [self.width, self.width, self.width]
        else:
            if 'width' in self.attrs:
                (parent_width, parent_min, parent_max) = self.parent.get_client_width()
                width = self._norm_sizes([self.attrs['width']], parent_width)[0]
                min = self._norm_sizes([self.attrs['width']], parent_min)[0]
                max = self._norm_sizes([self.attrs['width']], parent_max)[0]
                return [width, min, max]
            return self.calc_width()

    def get_client_width(self):
        return self.get_width()

    def get_client_height(self):
        return self.get_height()

    def set_height(self, height):
        self.height = height

    def get_height(self):
        if self.height >= 0:
            return self.height
        else:
            if 'height' in self.attrs:
                parent_height = self.parent.get_height()
                height = self._norm_sizes([self.attrs['height']],
                        parent_height)[0]
                return height
            return self.calc_height()

    def calc_width(self):
        """return: bestwidth, minwidth, maxwidth"""
        return (-1, -1, -1)

    def calc_height(self):
        """return height"""
        return 10

    def set_dc_info(self, dc_info):
        self.dc_info = dc_info


class BaseHtmlAtomParser(BaseHtmlElemParser):
    def __init__(self,parent,parser,tag,attrs):
        BaseHtmlElemParser.__init__(self, parent, parser, tag, attrs)
        self.atom_list = None
        self.atom_dy = 0.5
        self.style = -1
        self.no_wrap = False
        if 'white-space' in self.attrs and self.attrs['white-space'] == 'pre':
            self.pre = True
        else:
            self.pre = False

    def make_atom_list(self):
        if not self.atom_list:
            self.atom_list = AtomList(self.dc_info, self.atom_dy, pre=self.pre)

    def handle_data(self, data):
        if not self.pre:
            data2 = data.strip()
        else:
            data2 = data
        if data2 and len(data2) > 0:
            if not self.pre and data[-1]==' ':
                data2 += ' '
            if self.style < 0:
                self.style = self.get_style_id()
            if data2 and data2 != '':
                self.make_atom_list()
                if len(self.attrs) > 0:
                    self.atom_list.append_text(data2, self.style, self)
                else:
                    self.atom_list.append_text(data2, self.style)

    def append_atom_list(self, atom_list):
        self.make_atom_list()
        for pos in atom_list.atom_list:
            self.atom_list.append_atom(pos)

    def set_atom_dy(self, dy):
        self.atom_dy = dy
        if self.atom_list:
            self.atom_list.set_line_dy(dy)


class AnyTag(BaseHtmlElemParser):

    def __init__(self, parent, parser, tag, attrs):
        BaseHtmlElemParser.__init__(self, parent, parser, tag, attrs)
        self.child_tags = ['a', 'p', 'pre','div']

    def close(self):
        pass


tag_class_map = {}


def register_tag_map(tag, cls):
    tag_class_map[tag] = cls


class TagPreprocesor():
    def __init__(self):
        self.tag_preprocess_map = {}
        self.tag_wildcards_preprocess_map = []

    def register(self, tag, fun):
        if '?' in tag or '*' in tag:
            self.tag_wildcards_preprocess_map.append([tag.lower(), fun])
        else:
            self.tag_preprocess_map[tag.lower()] = fun

    def get_handler(self, tag):
        if tag in self.tag_preprocess_map:
            return self.tag_preprocess_map[tag.lower()]
        else:
            for pos in self.tag_wildcards_preprocess_map:
                if fnmatch.fnmatch(tag.lower(), pos[0]):
                    return pos[1]
        return None


#tag_preprocess_map = {}
TAG_PREPROCESS_MAP = TagPreprocesor()

def register_tag_preprocess_map(tag, fun):
    global TAG_PREPROCESS_MAP
    TAG_PREPROCESS_MAP.register(tag, fun)
    #tag_preprocess_map[tag] = fun


def get_tag_preprocess_map():
    global TAG_PREPROCESS_MAP
    return TAG_PREPROCESS_MAP


