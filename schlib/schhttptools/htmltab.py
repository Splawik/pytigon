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
import io

try:
    from html.parser import HTMLParser
    HTMLParseError = None
except:
    from HTMLParser import HTMLParser, HTMLParseError

from schlib.schhtml.htmltools import Td


class SimpleTabParser(HTMLParser):

    def __init__(self, main_tags=None):
        self.tables = []
        self.curtable = []
        self.currow = []
        self.cur_elem = ''
        self.in_td = False
        self.cur_attr = None
        if main_tags == None:
            self.main_tags = ('TABLE', )
        else:
            self.main_tags = main_tags
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        if tag.upper() in self.main_tags:
            pass
        elif tag.upper() == 'TR':
            pass
        elif tag.upper() == 'TD' or tag.upper() == 'TH':
            self.cur_elem = ''
            self.cur_attr = dict(attrs)
            self.in_td = True
        elif tag.upper() == 'A' or tag.upper() == 'FONT' or tag.upper()\
             == 'STRONG':
            if self.in_td:
                if tag.upper() == 'A':
                    a_attrs = dict(attrs)
                    if 'action' not in self.cur_attr:
                        self.cur_attr['action'] = {}
                    if 'name' in a_attrs:
                        name = a_attrs['name']
                        title = ''
                        if 'title' in a_attrs:
                            title = a_attrs['title']
                        href = ''
                        if 'href' in a_attrs:
                            href = a_attrs['href']
                        self.cur_attr['action'][name] = ('openurl', href,
                                title, a_attrs)
                else:
                    if tag.upper() == 'FONT':
                        for attr in attrs:
                            self.cur_attr[attr[0]] = attr[1]
                    else:
                        self.cur_attr['strong'] = 's'
        elif tag.upper() == 'IMG':
            for attr in attrs:
                if attr[0].lower() == 'src':
                    if self.cur_attr:
                        self.cur_attr['image'] = attr[1]

    def handle_endtag(self, tag):
        if tag.upper() in self.main_tags:
            self.tables.append(self.curtable)
            self.curtable = []
        elif tag.upper() == 'TR':
            self.curtable.append(self.currow)
            self.currow = []
        elif tag.upper() == 'TD' or tag.upper() == 'TH':
            self.currow.append(Td(self.cur_elem.strip(), self.cur_attr))
            self.cur_elem = ''
            self.cur_attr = None
            self.in_td = False

    def handle_data(self, data):
        if self.in_td:
            self.cur_elem = self.cur_elem + data.replace('\n', '').replace('\r', '')

    def feed(self, html_str):
        try:
            HTMLParser.feed(self, html_str)
            self.close()
        except:
        #except HTMLParseError as msg:
            print("ERROR:", sys.exc_info()[0])
            #print(html_str.split('\n')[msg.lineno - 2].encode('utf-8'))
            #print(html_str.split('\n')[msg.lineno - 1].encode('utf-8'))
            #print(html_str.split('\n')[msg.lineno - 0].encode('utf-8'))



class SimpleTabParser2(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.in_td=False
        self.current_row = []
        self.current_tab = []
        self.tables = []
        self.current_data = io.StringIO()

    def handle_starttag(self, tag, attrs):
        if tag=='td' or tag=='th':
            self.in_td = True
        else:
            if self.in_td:
                self.current_data.write(self.get_starttag_text())

    def handle_endtag(self, tag):
        if tag=='td' or tag=='th':
            self.current_row.append(self.current_data.getvalue().strip())
            self.current_data = io.StringIO()
            self.in_td = False
        elif tag=='tr':
            self.current_tab.append(self.current_row)
            self.current_row = []
        elif tag=='table':
            self.tables.append(self.current_tab)
            self.current_tab = []
        else:
            if self.in_td:
                self.current_data.write("</%s>" % tag)

    def handle_data(self, data):
        if self.in_td:
            self.current_data.write(data)

    def print(self):
        for row in self.tables[-1]:
            print("-------------------------------------------------------------")
            for pos in row:
                print("[", pos.replace('\n','')[:20],"]",)
            print("-------------------------------------------------------------")
