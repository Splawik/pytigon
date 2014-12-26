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


class HtmlModParser(HTMLParser):

    def __init__(self, url=None):
        HTMLParser.__init__(self)
        if url:
            req = urlopen(url)
            self.feed(req.read().decode('utf-8'))

    def parse_endtag(self, i):
        try:
            ret = HTMLParser.parse_endtag(self, i)
        except:
            ret = i + 1
        return ret


    def handle_entityref(self, name):
        if name in ('gt', 'lt', 'amp', 'quot'):
            self.handle_data('&'+name+';')


class HtmlProxyParser(HTMLParser):

    def __init__(self, tag):
        HTMLParser.__init__(self)
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

    def close(self):
        self.parser.tag_parser=self.org_tag_parser
        self.tag_obj.dc.restore_state(self.org_state)
        return HTMLParser.close(self)

class Td:

    def __init__(
        self,
        data,
        attr,
        childs=None,
        ):
        self.data = data
        self.attr = attr
        self.childs = childs

    def __repr__(self):
        return "Td:"+self.data