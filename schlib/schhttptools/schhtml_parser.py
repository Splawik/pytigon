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
from schlib.schhtml.parser import Parser, Elem, Script, tostring


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
            try:
                self._title = self._tree.findtext('.//title').strip()
            except:
                self._title = ""
        return self._title

    def get_body(self):
        return (Elem(self._data[0]), Script(self._data[1]))

    def get_header(self):
        return (Elem(self._data[2]), Script(self._data[3]))

    def get_footer(self):
        return (Elem(self._data[4]), Script(self._data[5]))

    def get_panel(self):
        return (Elem(self._data[6]), Script(self._data[7]))

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
