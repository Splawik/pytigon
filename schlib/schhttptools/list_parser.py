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

#try:
#    from html.parser import HTMLParser
#    HTMLParseError = None
#except:
#    from HTMLParser import HTMLParser, HTMLParseError

from schlib.schhtml.parser import Parser

class TreeParser(Parser):

    def __init__(self):
        self.TreeParent = [['TREE', []]]
        self.Lista = self.TreeParent
        self.Stos = []
        self.attr_to_li = []
        self.EnableDataRead = False
        Parser.__init__(self)

    def handle_starttag(self, tag, attrs):
        self.attr_to_li += attrs
        if tag == 'ul':
            self.Stos.append(self.Lista)
            self.Lista = self.Lista[-1][1]
            self.EnableDataRead = False
        else:
            if tag == 'li':
                self.EnableDataRead = True
                self.Lista.append(['', [], []])
                self.attr_to_li = []

    def handle_endtag(self, tag):
        if tag == 'ul':
            self.Lista = self.Stos.pop()
        if tag == 'li':
            self.Lista[-1][2] = self.attr_to_li
            self.attr_to_li = []
        self.EnableDataRead = False

    def handle_data(self, data):
        if self.EnableDataRead:
            self.Lista[-1][0] = self.Lista[-1][0] + data.rstrip(' \n')


