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


from schlib.schhtml.parser import Parser

try:
    from urllib.request import urlopen
except:
    from urllib import urlopen


def superstrip(s):
    f = (16, 8, 4, 2)
    s2 = s.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    for pos in f:
        oldlen = -1
        newlen = 0
        while newlen != oldlen:
            oldlen = len(s2)
            s2 = s2.replace(' ' * pos, ' ')
            newlen = len(s2)
    return s2.strip()


class HtmlModParser(Parser):
    def __init__(self, url=None):
        Parser.__init__(self)
        if url:
            req = urlopen(url)
            self.feed(req.read().decode('utf-8'))


class HtmlProxyParser(Parser):
    def __init__(self, tag):
        Parser.__init__(self)
        
        self.tag_obj = tag
        self.parser = tag.parser 
        self.org_tag_parser=self.parser.tag_parser
        self.parser.tag_parser = tag
        self.org_state = tag.dc.state()
        tag.dc.restore_state(tag.base_state)

    def handle_starttag(self, tag, attrs):
        return self.parser.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        return self.parser.handle_endtag(tag)

    def handle_data(self, data):
        return self.parser.handle_data(data)

    def feed(self, html_txt):                
        _tree = self._tree
        _cur_elem = self._cur_elem        
        _header = self.tag_obj.header
        _footer  = self.tag_obj.footer
        self.tag_obj.header = ""
        self.tag_obj.footer  = ""
        super().feed(html_txt)
        self.tag_obj.header = _header
        self.tag_obj.footer  =_footer
        self._tree = _tree
        self._cur_elem = _cur_elem        
        
    def close(self):
        self.parser.tag_parser=self.org_tag_parser
        self.tag_obj.dc.restore_state(self.org_state)


class Td:
    def __init__(self, data, attr, childs=None):
        self.data = data
        self.attr = attr
        self.childs = childs

    def __repr__(self):
        return "Td:"+self.data
