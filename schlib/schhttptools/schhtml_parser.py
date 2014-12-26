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

from __future__ import unicode_literals

try:
    from html.parser import HTMLParser, HTMLParseError
except:
    from HTMLParser import HTMLParser, HTMLParseError

import io
from schlib.schhtml.htmltools import HtmlModParser


class ShtmlParser(HtmlModParser):

    cdata_content_elements = ('script', 'style', 'pscript')
    not_process = ('thead', 'tbody')

    def __init__(self):
        self.var = {}
        self.title = ''
        self.schhtml = False
        self.header = io.StringIO()
        self.header_script = io.StringIO()
        self.header_exists = False
        self.body = io.StringIO()
        self.body_script = io.StringIO()
        self.body_attrs = {}
        self.footer = io.StringIO()
        self.footer_script = io.StringIO()
        self.footer_exists = False
        self.panel = io.StringIO()
        self.panel_script = io.StringIO()
        self.panel_exists = False
        self.status = 0
        self.status_in_script = 0
        self.count = 0
        self.address = None
        HtmlModParser.__init__(self)

    def get_panel(self):
        if self.panel_exists:
            return [self.panel, self.panel_script]
        else:
            return None

    def get_footer(self):
        if self.footer_exists:
            return [self.footer, self.footer_script]
        else:
            return None

    def get_header(self):
        if self.header_exists:
            return [self.header, self.header_script]
        else:
            return None

    def get_body(self):
        return [self.body, self.body_script]

    def get_body_attrs(self):
        return self.body_attrs

# def handle_startendtag(self, tag, lattrs): self.handle_starttag(tag, lattrs)
# self.handle_endtag(tag)

    def get_starttag_text(self):
        ret = HtmlModParser.get_starttag_text(self)
        ret = ret.replace('/>', '>').replace('/ >', '>')
        return ret

    def handle_starttag(self, tag, attrs):
        if tag in self.not_process:
            return
        if self.status_in_script:
            self.handle_data(self.get_starttag_text())
            return
        tagprint = tag
        if tag == 'meta':
            name = None
            content = None
            for a in attrs:
                if a[0] == 'name':
                    name = a[1]
                if a[0] == 'content':
                    content = a[1]
            if name:
                if name.lower() == 'schhtml':
                    self.schhtml = int(content)
                else:
                    self.var[str(name).lower()] = content
        if tag == 'body':
            self.body_attrs = dict(attrs)
        if tag == 'title':
            self.status = 1
            return
        if tag == 'script':
            for a in attrs:
                if a[0] == 'language' and a[1] == 'python':
                    self.status_in_script = 1
                    return
                else:
                    self.status_in_script = 2
                    return
        if tag == 'frame':
            id = None
            for a in attrs:
                if a[0] == 'id':
                    id = a[1]
            if id:
                if id == 'header':
                    self.status = 3
                    self.count = 1
                    tagprint = 'body'
                    self.header_exists = True
                    self.header.write('<html>')
                elif id == 'footer':
                    self.status = 4
                    self.count = 1
                    tagprint = 'body'
                    self.footer_exists = True
                    self.footer.write('<html>')
                elif id == 'panel':
                    self.status = 5
                    self.count = 1
                    tagprint = 'body'
                    self.panel_exists = True
                    self.panel.write('<html>')
                else:
                    if self.count > 0:
                        self.count += 1
            else:
                if self.count > 0:
                    self.count += 1
        if not self.status_in_script:
            if self.status == 0:
                self.body.write(self.get_starttag_text())
            if self.status == 3:
                self.header.write(self.get_starttag_text())
            if self.status == 4:
                self.footer.write(self.get_starttag_text())
            if self.status == 5:
                self.panel.write(self.get_starttag_text())

    def handle_endtag(self, tag):
        if tag in self.not_process:
            return
        if self.status_in_script and tag != 'script':
            self.handle_data('</' + tag + '>')
            return
        tagprint = tag
        status = self.status
        if tag == 'script':
            self.status_in_script = 0
            return
        if tag == 'title':
            self.status = 0
            return
        if tag == 'frame':
            if self.count > 0:
                self.count -= 1
                if self.count == 0:
                    self.status = 0
                    tagprint = 'body'
        if status == 0:
            self.body.write('</' + tagprint + '>')
        if status == 3:
            self.header.write('</' + tagprint + '>')
        if status == 4:
            self.footer.write('</' + tagprint + '>')
        if status == 5:
            self.panel.write('</' + tagprint + '>')

    def handle_data(self, data):
        if self.status_in_script:
            if self.status_in_script == 1:
                if self.status == 3:
                    self.header_script.write(data)
                elif self.status == 4:
                    self.footer_script.write(data)
                elif self.status == 5:
                    self.panel_script.write(data)
                else:
                    self.body_script.write(data)
        else:
            if self.status == 0:
                self.body.write(""+data)
            if self.status == 1:
                self.title = data.replace('\n', '').strip().replace('  ', ' ')
            if self.status == 3:
                self.header.write(data)
            if self.status == 4:
                self.footer.write(data)
            if self.status == 5:
                self.panel.write(data)

    def process(self, data, address=None):
        try:
            self.feed(data)
            self.close()
        except HTMLParseError as e:
            l = data.split('\n')
            print(e.msg)
            print('------------------------------------------------------')
            print(l[e.lineno - 2].encode('utf-8'))
            print(l[e.lineno - 1].encode('utf-8'))
            print('===>', l[e.lineno + 0].encode('utf-8'))
            print(l[e.lineno + 1].encode('utf-8'))
            print(l[e.lineno + 2].encode('utf-8'))
            print('------------------------------------------------------')
            print(data)
            print('------------------------------------------------------')
            return
        #try:
        #self.close()
        #except:
        #    print "######################################################"
        #    print data
        #    print "######################################################"
        #    pass
        if self.header_exists:
            self.header.write('</html>')
        if self.footer_exists:
            self.footer.write('</html>')
        if self.panel_exists:
            self.panel.write('</html>')
        self.address = address


if __name__ == '__main__':
    f = open('test.html', 'rt')
    data = f.read()
    f.close()
    mp = ShtmlParser()
    mp.Process(data)
    if 'TARGET' in mp.Var:
        print('HEJ:', mp.Var['TARGET'])
        print('<title***>', mp.title, '</title***>')
        print('<header***>', mp.header.getvalue(), '</header***>')
        print('<BODY***>', mp.body.getvalue(), '</BODY***>')
        print('<footer***>', mp.footer.getvalue(), '</footer***>')
        print('<panel***>', mp.panel.getvalue(), '</panel***>')
