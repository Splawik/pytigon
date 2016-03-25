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

from schlib.schhtml.parser import Parser, content_tostring
from schlib.schhtml.htmltools import Td


class SimpleTabParserBase(Parser):
    def __init__(self):
        Parser.__init__(self)
        self.tables = []

    def _preprocess(self, td):
        return content_tostring(td).strip()

    def feed(self, html_txt):
        self.init(html_txt)
        for elem in self._tree.iterfind(".//table"):
            table = []
            for elem2 in elem.iterfind(".//tr"):
                tr = []
                for elem3 in elem2.iterfind(".//th"):
                    tr.append(self._preprocess(elem3))
                for elem3 in elem2.iterfind(".//td"):
                    tr.append(self._preprocess(elem3))
                table.append(tr)
            self.tables.append(table)


class SimpleTabParser(SimpleTabParserBase):

    def _preprocess(self, td):
        return Td(content_tostring(td).strip(), td.attrib)


