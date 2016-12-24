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

from schlib.schhtml.basehtmltags import BaseHtmlElemParser, register_tag_map
from .tags.block_tags import *
from .tags.table_tags import *
from .tags.p_tags import *
from .tags.css_tags import *
from .tags.atom_tags import *
from .tags.page_tags import *
from .tags.extra_tags import *


class HtmlTag(BaseHtmlElemParser):

    def __init__(self, parent, parser, tag, attrs):
        BaseHtmlElemParser.__init__(self, parent, parser, tag, attrs)
        self.child_tags = ['head', 'body', 'script']
        self.width = 2480
        self.height = 3508
        self.y = 0
        self.dc = None
        self.attrs['color'] = '#000'
        self.attrs['font-family'] = 'sans-serif'
        self.attrs['font-size'] = '100%'
        self.attrs['font-style'] = 'normal'
        self.attrs['font-weight'] = 'normal'
        self.attrs['text-decoration'] = 'none'

    def handle_data(self, data):
        pass

    def close(self):
        BaseHtmlElemParser.close(self)

    def set_dc(self, dc):
        (self.width, self.height) = dc.get_size()
        self.dc = dc


class HeaderTag(BaseHtmlElemParser):
    def __init__(self, parent, parser, tag, attrs):
        BaseHtmlElemParser.__init__(self, parent, parser, tag, attrs)
        self.child_tags = ['style', 'link']

    def close(self):
        pass



class CommentTag(BaseHtmlElemParser):
    def __init__(self, parent, parser, tag, attrs):
        BaseHtmlElemParser.__init__(self, parent, parser, tag, attrs)

    def handle_starttag(self, parser, tag, attrs):
        return None

    def close(self):
        pass


register_tag_map('html', HtmlTag)
register_tag_map('head', HeaderTag)
register_tag_map('comment', CommentTag)
