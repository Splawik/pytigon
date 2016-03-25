3#!/usr/bin/python
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

import io
from schlib.schhtml.htmltools import HtmlModParser
from schlib.schhtml.parser import Parser, tostring

class ShtmlParser(Parser):
    def __init__(self):
        super().__init__()
        self.address = None
        self._title = None
        self._data = None
        self.var = {}
        self.schhtml = None

    def _data_to_string(self, id):
        if self._data[id] != None:
            return tostring(self._data[id])
        return ""

    def _script_to_string(self, id):
        if self._data[id] != None:
            return self._data[id].text
        return ""


    def _reparent(self, selectors):
        ret = []

        for selector in selectors:
            tmp = self._tree.find(selector)
            tmp2 = None
            if tmp != None:
                tmp.getparent().remove(tmp)
                tmp2 = tmp.find(".//script[@language='python']")
                if tmp2 != None:
                    tmp2.getparent().remove(tmp2)
                for elem in tmp.iterfind(".//script"):
                    elem.getparent().remove(elem)
            ret.append(tmp)
            ret.append(tmp2)

        tmp2 = self._tree.find(".//script[@language='python']")
        if tmp2 != None:
            tmp2.getparent().remove(tmp2)
        tmp = self._tree.find(".//body")
        if tmp == None:
            tmp = self._tree
        for elem in tmp.iterfind(".//script"):
            elem.getparent().remove(elem)

        ret.insert(0, tmp2)
        ret.insert(0, tmp)
        return ret

    def process(self, html_txt, address=None):
        self.address = address
        self.init(html_txt)
        for elem in self._tree.iterfind(".//meta"):
            if 'name' in elem.attrib:
                name = elem.attrib['name'].lower()
                if 'content' in elem.attrib:
                    if name == 'schhtml':
                        self.schhtml = int(elem.attrib['content'])
                    else:
                        self.var[name] = elem.attrib['content']
                else:
                    self.var[name] = None
        self._data = self._reparent((".//frame[@id='header']",".//frame[@id='footer']",".//frame[@id='panel']",))


    @property
    def title(self):
        if not self._title:
            self._title = self._tree.findtext('.//title').strip()
        return self._title

    @property
    def body(self):
        return self._data_to_string(0)

    @property
    def body_script(self):
        return self._script_to_string(1)

    @property
    def header(self):
        return self._data_to_string(2)

    @property
    def header_script(self):
        return self._script_to_string(3)

    @property
    def footer(self):
        return self._data_to_string(4)

    @property
    def footer_script(self):
        return self._script_to_string(5)

    @property
    def panel(self):
        return self._data_to_string(6)

    @property
    def panel_script(self):
        return self._script_to_string(7)

    def get_body(self):
        return (self.body, self.body_script)

    def get_header(self):
        return (self.header, self.header_script)

    def get_footer(self):
        return (self.footer, self.footer_script)

    def get_panel(self):
        return (self.panel, self.panel_script)

    def get_body_attrs(self):
        b = self._tree.find('.//body')
        if b != None:
            return b.attrib
        else:
            return {}

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
