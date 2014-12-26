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

import sys
import traceback
import tempfile

from .htmltools import superstrip, HtmlModParser
from .html_tags import HtmlTag
from schlib.schhtml.basehtmltags import get_tag_preprocess_map
from .basedc import NullDc, BaseDc

#from .cairodc import CairoDc, get_PdfCairoDc
# from wxdc import GraphicsContextDC
#from .wxdc import DcDc
# from wxgc import GraphicsContextDC

from .htmltools import superstrip
from tempfile import NamedTemporaryFile
import os
from .css import Css
from schlib.schhttptools.httpclient import HttpClient
import io

from schlib.schhtml.pdfdc import PdfDc

#run_cairo = True

init_css_str_base = \
    """
    body {font-family:sans-serif;font-size:100%; padding:2;}
    table {border:5;vertical-align:top; padding:2;}
    td table { padding: 2; }
    th {border:5; cellpadding:2;}
    td {border:5; vertical-align:top; cellpadding:2;}
    strong,b {font-weight:bold;}
    p { cellpadding:5; border:1; width:100%; align: left; }
    h1 {font-size:300%; font-weight: bold; cellpadding:12;}
    h2 {font-size:240%; font-weight: bold; cellpadding:10;}
    h3 {font-size:190%; font-weight: bold; cellpadding:8;}
    h4 {font-size:150%; font-weight: bold; cellpadding:6;}
    h5 {font-size:120%; font-weight: bold; cellpadding:4;}
    h6 {font-size:100%; font-weight: bold; cellpadding:2;}
    a { color:#0000ff; text-decoration: underline; }
    ul {border:0;}
    li {cellpadding:5; width:93%-60; }
    dt {font-weight:bold; width:45%;}
    dd {width:45%; cellpadding:10; }
    calc { cellpadding:5; border:1; width:100%; }
"""

class HtmlViewerParser(HtmlModParser):

    def __init__(
        self,
        dc=None,
        dc_info=None,
        url=None,
        calc_only=False,
        parse_only=False,
        init_css_str=None,
        css_type=0,
        ):
        self.tag_parser = None
        self.url = url
        self.parse_only = parse_only
        if self.parse_only:
            self.calc_only = True
        else:
            self.calc_only = calc_only
        if dc != None:
            self.dc = dc
        else:
            self.dc = BaseDc()
        if self.calc_only:
            self.dc = NullDc(self.dc)

        if dc_info:
            self.dc_info = dc_info
        else:
            self.dc_info = self.dc.get_dc_info()
        self.css = Css()
        if init_css_str:
            if css_type == 0:
                self.css.parse_str(init_css_str)
            else:
                self.css.parse_indent_str(init_css_str)
        else:
            if css_type == 0:
                self.css.parse_str(init_css_str_base)
            else:
                self.css.parse_indent_str(init_css_str_base)
        self.obj_id_dict = {}
        self.obj_action_dict = {}

# self.preprocess_dict = {}

        self.parent_window = None
        self._max_width = 0
        self._max_height = 0
        self.lp = 1
        self.table_lp = 0
        self.http = None
        self.tdata_tab = []
        HtmlModParser.__init__(self, url)
        self.debug = False
        if self.debug:
            print("html")
# def add_preprocess_pos(self, src_tag, tst_fun): self.preprocess_dict[src_tag]
# = tst_fun

    def register_tdata(
        self,
        tdata,
        tag,
        attrs,
        ):
        self.tdata_tab.append((tdata, tag, attrs))

    def set_http_object(self, http):
        self.http = http

    def get_http_object(self):
        if not self.http:
            self.http = HttpClient(self.url)
        return self.http

    def set_max_rendered_size(self, width, height):
        self._max_width = width
        self._max_height = height

    def get_max_rendered_size(self):
        return (self._max_width, self._max_height)

    def set_parent_window(self, win):
        self.parent_window = win

    def get_parent_window(self):
        return self.parent_window

    def reg_id_obj(
        self,
        id,
        dc,
        obj,
        ):
        self.obj_id_dict[id] = obj
        obj.last_rendered_dc = dc
        obj.rendered_rects.append((dc.x, dc.y, dc.dx, dc.dy))

    def reg_action_obj(
        self,
        action,
        dc,
        obj,
        ):
        if action in self.obj_action_dict:
            self.obj_action_dict[action].append(obj)
        else:
            self.obj_action_dict[action] = [obj]
        obj.last_rendered_dc = dc
        obj.rendered_rects.append((dc.x, dc.y, dc.dx, dc.dy))

    def handle_starttag(self, tag, lattrs):
        if tag.lower() in ('img', 'image', 'input', 'br', 'link'):
            return self.handle_startendtag(tag, lattrs)
        else:
            return self._handle_starttag(tag, lattrs)

    def _handle_starttag(self, tag, lattrs):
        try:
            attrs = {}
            for pos in lattrs:
                if pos[0].lower() == 'style':
                    for s in pos[1].split(';'):
                        s2 = s.split(':')
                        if len(s2) == 2:
                            attrs[s2[0].lower()] = s2[1]
                else:
                    class_name = pos[0].lower()
                    if pos[1].__class__ == str:
                        #try:
                        #    if class_name == 'class':
                        #        attrs[class_name] = pos[1].decode('utf-8').split(' ')[0]
                        #    else:
                        #        attrs[class_name] = pos[1].decode('utf-8')
                        #except:
                        if class_name == 'class':
                            attrs[class_name] = pos[1].split(' ')[0]
                        else:
                            attrs[class_name] = pos[1]

                    else:
                        if class_name == 'class':
                            attrs[class_name] = pos[1].split(' ')[0]
                        else:
                            attrs[class_name] = pos[1]

            tmap = get_tag_preprocess_map()
            tag2 = tag.lower()
            if tag2 in tmap:
                (tag2, attrs) = tmap[tag2](self.tag_parser, attrs)

            if self.tag_parser:
                obj = self.tag_parser.handle_starttag(self, tag2, attrs)
                if self.debug:
                    self.print_obj(obj,True)
                if obj:
                    obj.close_tag = tag
                    if obj.sys_id < 0:
                        obj.sys_id = self.lp
                        self.lp += 1
                    self.tag_parser = obj
                    self.tag_parser.set_dc_info(self.dc_info)
            else:
                if tag.lower() == 'html':
                    self.tag_parser = HtmlTag(None, self, tag.lower(), attrs)
                    self.tag_parser.set_dc(self.dc)
        except:
            (exc_type, exc_value, exc_tb) = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_tb)

    def handle_startendtag(self, tag, lattrs):
        self._handle_starttag(tag, lattrs)
        self.handle_endtag(tag)

    def handle_endtag(self, tag):
        try:
            if self.tag_parser:
                tag_parser = self.tag_parser
                obj = self.tag_parser.handle_endtag(tag.lower())
                if self.debug and obj!=tag_parser:
                    self.print_obj(tag_parser, False)
                self.tag_parser = obj
                tag_parser.finish()
        except:
            (exc_type, exc_value, exc_tb) = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_tb)
        if tag.lower() in ('table', 'tdata'):
            self.table_lp += 1

    def handle_data(self, data):
        try:
            if self.tag_parser:
# self.tag_parser.handle_data(data.decode('utf-8'))
                if data.__class__ == str:
                    #try:
                    #    self.tag_parser.handle_data(data.decode('utf-8'))
                    #except:
                    self.tag_parser.handle_data(data)
                else:
                    self.tag_parser.handle_data(data)
        except:
            (exc_type, exc_value, exc_tb) = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_tb)

    def close(self):
        if self.dc:
            self.dc.close()

    def get_max_sizes(self):
        sizes = self.dc.get_max_sizes()
        sizes2 = self.get_max_rendered_size()
# print "GetMaxSizes:", sizes, sizes2
        return (max(sizes[0], sizes2[0]), max(sizes[1], sizes2[1]))

    def print_obj(self, obj, start=True):
        if obj:
            if start:
                tab = -1
                parent = obj
                while parent:
                    tab = tab+1
                    parent = parent.parent
                print('|   '*tab, obj.tag, obj.attrs)
            else:
                tab = -1
                parent = obj
                while parent:
                    tab = tab+1
                    parent = parent.parent
                print('|   '*tab, "/", obj.tag, "(", obj.height, ")")

def stream_from_html(
    html,
    input_stream=None,
    css=None,
    #width=2480,
    #height=3508,
    width=int(210*72/25.4),
    height=int(297*72/25.4),
    stream_type='pdf'
    ):


    if '<html'.encode('ascii') in html:
        html2 = html.decode('utf-8')
    else:
        html2 = '<html><body>' + html.decode('utf-8') +"</body></html>"

    if 'orientation:landscape' in html2 or 'orientation: landscape' in html2:
        width2 = height
        height2 = width
    else:
        width2 = width
        height2 = height

    if input_stream:
        result = input_stream
    else:
        result = io.BytesIO()
        #result = tempfile.TemporaryFile()

    surf=None
    if stream_type=='pdf':
        #surf = cairo.PDFSurface(result, width, height)
        #ctx = cairo.Context(surf)
        #dc = CairoDc(ctx=ctx, calc_only=False, width=width, height=height)
        #dc = get_PdfCairoDc(result, width, height)
        #tempfile.gettempdir()
        #result = tempfile.TemporaryFile()
        result_buf = tempfile.NamedTemporaryFile(delete=False)
        pdf_name = result_buf.name
        result_buf.close()


        dc = PdfDc(calc_only=False, width=width2, height=height2, output_name=pdf_name)
        #dc = get_PdfCairoDc(pdf_name, width, height)
    else:
        #dc = CairoDc(calc_only=False, width=width, height=height,
        #             output_name='c:\\temp\\test.pdf')
        from schlib.schhtml.cairodc import CairoDc
        dc = CairoDc(calc_only=False, width=width2, height=height2)
        #dc = DcDc(calc_only=False, width=width, height=height)
        #dc = DcDc(calc_only=False, width=width, height=height,
        #          output_name='test.png')

    dc.set_paging(True)
    p = HtmlViewerParser(dc=dc, calc_only=False)
    p.feed(html2)
    p.close()
    if stream_type=='pdf':
        #dc.surf.finish()

        #dc.close()
        f = open(pdf_name,"rb")
        result.write(f.read())
        f.close()
        os.unlink(pdf_name)
    else:
        f = NamedTemporaryFile(delete=False)
        name = f.name
        f.close()
        
        dc.end_page()
        dc.save(name)
        
        f = open(name,"rb")
        buf = f.read()
        result.write(buf)
        f.close()

        os.unlink(name)
    return result


def tdata_from_html(html, http):
    #dc = DcDc(calc_only=True, width=-1, height=-1)
    dc = PdfDc(calc_only=True, width=-1, height=-1)
    p = HtmlViewerParser(dc=dc, parse_only=True)
    p.set_http_object(http)
    p.feed(html)
    ctrls = p.tdata_tab
    p.close()
    tab = None
    for pos in ctrls:
        if pos[1] == 'ctrltable':
            tab = pos[0]
            break
    if tab and len(tab) > 0:
        return tab
    else:
        return None


