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

try:
    from html.parser import HTMLParser, HTMLParseError
except:
    from HTMLParser import HTMLParser, HTMLParseError

from schlib.schhtml.basehtmltags import BaseHtmlElemParser, BaseHtmlAtomParser, \
    register_tag_map
from schlib.schhtml.render_helpers import RenderBackground, RenderBorder, \
    RenderCellSpacing, RenderPadding, RenderMargin, get_size
from schlib.schhtml.basedc import SubDc
from .p_tags import ParBase
from schlib.schhtml.htmltools import HtmlProxyParser


class BodyTag(ParBase):

    def __init__(
        self,
        parent,
        parser,
        tag,
        attrs,
        ):
        ParBase.__init__(self, parent, parser, tag, attrs)
        self.child_tags += [
            'p',
            'table',
            'h1',
            'h2',
            'h3',
            'h4',
            'h5',
            'h6',
            'calc',
            'ul',
            'ol',
            'newpage',
            'page',
            'ctr*',
            'dl',
            'dt',
            'dd',
            'form',
            'hr',
            'pre',
            'div'
            ]
        self.page = 1
        self.y = 0
        self.border = 0
        self.cellspacing = 0
        self.dc_page = None
        (width, height) = parent.dc.get_size()
        self.render_helpers = [RenderMargin(self), RenderBorder(self),
                               RenderBackground(self), RenderPadding(self)]
        self.extra_space = get_size(self.render_helpers)
        self.margins = [self.extra_space[0], self.extra_space[1],
                        self.extra_space[2], self.extra_space[3]]
        self.dc = parent.dc.subdc(0, 0, width, height, False)
        (self.width, self.height) = self.dc.get_size()
        if self.width >= 0:
            self.width = width - 2 * (self.margins[2] + self.margins[0])
        else:
            self.width = -1
        self.height = (height - self.margins[3]) - self.margins[1]
        self.new_page = 0
        self.reg_id(self.dc)
        self.reg_end()
        self._maxwidth = 0
        self._maxheight = 0
        self.header = None
        self.footer = None
        self.header_height = 0
        self.footer_height = 0
        self.in_footer = False
        self.base_state = None

    def set_dc_info(self, dc_info):
        ParBase.set_dc_info(self, dc_info)
        self.get_style_id()

    def data_from_child(self, child, data):
        if child.tag == 'header':
            self.header = data.getvalue()
            if 'height' in child.attrs:
                self.header_height = int(child.attrs['height'])
        else:
            self.footer = data.getvalue()
            if 'height' in child.attrs:
                self.footer_height = int(child.attrs['height'])
            if self.footer_height == 0:
                self.footer_height = self.height / 10

    def page_changed(self):
        if not self.base_state:
            self.base_state = self.dc.state()
        if self.new_page == 0:
            self.render_new_page()

    def print_header(self):
        if self.header:
            self.dc.paging = False
            self.y = 0
            proxy = HtmlProxyParser(self)
            proxy.feed(self.header)
            self.render_atom_list()
            proxy.close()
            if self.header_height != 0:
                self.y = self.header_height
            self.dc.paging = True

    def print_footer(self):
        if self.footer:
            self.dc.paging = False
            self.y = self.height - self.footer_height
            self.in_footer = True
            proxy = HtmlProxyParser(self)
            proxy.feed(self.footer)
            proxy.close()
            self.render_atom_list()
            self.in_footer = False
            self.dc.paging = True

    def _get_pseudo_margins(self):
        return [self.extra_space[0], self.extra_space[1], self.extra_space[2]
                 + self.y, self.extra_space[3]]

    def get_client_height(self):
        if not self.dc_page:
            self.render_new_page()
        return self.dc_page.dy

    def close(self):
        if self.parser.parse_only:
            return
        if self.atom_list:
            self.child_ready_to_render(None)
        if self.footer:
            self.print_footer()
        (w, h) = self.dc.get_max_sizes()
        if w > self._maxwidth:
            self._maxwidth = w + self.extra_space[0] + self.extra_space[1]
        else:
            self._maxwidth += self.extra_space[0] + self.extra_space[1]
        if h > self._maxheight:
            self._maxheight = h + self.extra_space[2] + self.extra_space[3]
        else:
            self._maxheight += self.extra_space[2] + self.extra_space[3]

        self.parser.set_max_rendered_size(self._maxwidth, self._maxheight)

    def render_new_page(self):
        new_page = self.new_page
        if new_page != 0:
            if self.footer:
                self.print_footer()
        if new_page != 0 and self.dc.paging:
            self.page += 1
            self.dc.start_page()
        self.dc_page = self.dc
        for r in self.render_helpers:
            self.dc_page = r.render(self.dc_page)
        if self.dc.paging:
            self.y = 0
            self.new_page = 1
            self.print_header()

    def render_atom_list(self):
        if self.atom_list:
            dy = ParBase.calc_height(self)
            if self.dc.paging and dy > self.height - self.footer_height - self.y:
                self.render_new_page()
            render_helpers = self.render_helpers
            self.render_helpers = []
            self.render(self.dc_page.subdc(0, self.y, self.width, dy))
            self.render_helpers = render_helpers
            self.new_page = 2
            self.y += dy
            self.atom_list = None
            if self.y > self._maxheight:
                self._maxheight = self.y

    def child_ready_to_render(self, child):
        if self.parser.parse_only:
            return

        if self.dc:
            if self.new_page == 0:
                self.render_new_page()
            self.render_atom_list()
            if child:
                cont = True
                while cont:
                    (width, min, max) = child.get_width()
                    if max >= 0 and max < self.width:
                        w = max
                    elif min >= 0 and min > self.width:
                        w = min
                    else:
                        w = width
                    child.set_width(w)
                    if w + self.extra_space[0] + self.extra_space[1]\
                         > self._maxwidth:
                        self._maxwidth = w + self.extra_space[0]\
                             + self.extra_space[1]
                    dy = child.get_height()
                    child.set_height(dy)
                    if not self.dc.paging or dy <= self.height - self.footer_height - self.y\
                         or self.new_page != 2:
                        (dy, cont) = child.render(self.dc_page.subdc(0, self.y,
                                self.width, dy))
                        self.new_page = 2
                        if dy > 0:
                            self.y += dy
                    else:
                        self.render_new_page()
                        cont = True
                    if self.y > self._maxheight:
                        self._maxheight = self.y


register_tag_map('body', BodyTag)


class FormTag(BaseHtmlElemParser):

    def __init__(
        self,
        parent,
        parser,
        tag,
        attrs,
        ):
        BaseHtmlElemParser.__init__(self, parent, parser, tag, attrs)
        self.child_tags = parent.child_tags
        self.child_tags += [
            'table',
        ]
        self.fields = None
        self.field_names = {}
        self.upload = None
        self.parent.reg_field = self.reg_field
        self.parent.get_fields = self.get_fields
        self.parent.gethref = self.gethref
        self.parent.set_upload = self.set_upload
        self.parent.get_upload = self.get_upload
        self.parent.form_obj=self

    def close(self):
        self.parent.form_obj=None

    def handle_data(self, data):
        pass

    def handle_starttag(
        self,
        parser,
        tag,
        attrs,
        ):
        obj = BaseHtmlElemParser.handle_starttag(self, parser, tag, attrs)
        if obj:
            obj.parent = self.parent
        return obj

    def reg_field(self, field):
        if field in self.field_names:
            self.field_names[field] = self.field_names[field] + 1
            field2 = field + '__' + str(self.field_names[field])
        else:
            self.field_names[field] = 1
            field2 = field
        if not field.startswith('_'):
            if self.fields:
                self.fields = self.fields + ',' + field2
            else:
                self.fields = field2
        return field2

    def get_fields(self):
        method = 'GET'
        if 'method' in self.attrs:
            method = self.attrs['method']
        if self.fields:
            return method + ':' + self.fields
        else:
            return None

    def gethref(self):
        return self.attrs['action']

    def set_upload(self, upload):
        self.upload = upload

    def get_upload(self):
        return self.upload


register_tag_map('form', FormTag)

