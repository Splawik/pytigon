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
import io


class Page(BaseHtmlElemParser):

    def __init__(self, parent, parser, tag, attrs):
        BaseHtmlElemParser.__init__(self, parent, parser, tag, attrs)
        self.child_tags = ['header', 'footer']
        self.body = parent

    def data_from_child(self, child, data):
        self.parent.data_from_child(child, data)

    def close(self):
        pass

    def finish(self):
        self.body.page_changed()


class NewPage(BaseHtmlElemParser):

    def __init__(self, parent, parser, tag, attrs):
        BaseHtmlElemParser.__init__(self, parent, parser, tag, attrs)
        self.body = parent

    def close(self):
        pass

    def finish(self):
        self.body.render_new_page()


class HeaderFooter(BaseHtmlElemParser):

    def __init__(self, parent, parser, tag, attrs):
        BaseHtmlElemParser.__init__(self, parent, parser, tag, attrs)
        self.data = io.StringIO()

    def handle_starttag(self, parser, tag, attrs):
        self.data.write('<' + tag)
        for pos in attrs:
            if attrs[pos] != None:
                self.data.write(' ' + pos + '="' + attrs[pos] + '"')
            else:
                self.data.write(' ' + pos)
        self.data.write('>')
        return None

    def handle_endtag(self, tag):
        if tag == self.tag:
            self.parent.data_from_child(self, self.data)
            return self.parent
        else:
            self.data.write('</' + tag + '>')
            return self

    def handle_data(self, data):
        self.data.write(data)

    def close(self):
        pass


register_tag_map('page', Page)
register_tag_map('header', HeaderFooter)
register_tag_map('footer', HeaderFooter)
register_tag_map('newpage', NewPage)
