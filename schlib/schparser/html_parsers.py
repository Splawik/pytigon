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


from schlib.schhtml.parser import Parser, content_tostring, Elem, Script, tostring
from schlib.schhtml.htmltools import Td


class SimpleTabParserBase(Parser):
    """Parses html for tables. Found tables save to self.tables variable"""
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
    """Like SimpleTabParserBase but td saves as Td object. SimpleTabParserBase saves td as string"""
    def _preprocess(self, td):
        return Td(content_tostring(td).strip(), td.attrib)


class TreeParser(Parser):
    """Parses html for ul. Found ul save to self.list variable"""
    def __init__(self):
        self.tree_parent = [['TREE', []]]
        self.list = self.tree_parent
        self.stack = []
        self.attr_to_li = []
        self.enable_data_read = False
        Parser.__init__(self)

    def handle_starttag(self, tag, attrs):
        self.attr_to_li += attrs
        if tag == 'ul':
            self.stack.append(self.list)
            self.list = self.list[-1][1]
            self.enable_data_read = False
        else:
            if tag == 'li':
                self.enable_data_read = True
                self.list.append(['', [], []])
                self.attr_to_li = []

    def handle_endtag(self, tag):
        if tag == 'ul':
            self.list = self.stack.pop()
        if tag == 'li':
            self.list[-1][2] = self.attr_to_li
            self.attr_to_li = []
        self.enable_data_read = False

    def handle_data(self, data):
        if self.enable_data_read:
            self.list[-1][0] = self.list[-1][0] + data.rstrip(' \n')


def _remove(parent, elem):
    parent.remove(elem)
    #try:
    #    elem.getparent().remove(elem)
    #except:
    #    parent = elem.find("..")
    #    parent.remove(elem)
    #    #tree.remove(elem)
    #    #elem.attrib['__parent'].remove(elem)

class ShtmlParser(Parser):
    """Parser for SchPage window. Divides the page into parts: header, footer, panel, body and script. Reads variables
    from meta tag"""
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


    def out_reparent(self, selectors):
        ret = []

        for selector in selectors:
            tmp = self._tree.find(selector)
            tmp2 = None
            if tmp != None:
                _remove(self._tree, tmp)
                tmp2 = tmp.find(".//script[@language='python']")
                if tmp2 != None:
                    _remove(self._tree, tmp2)
                for elem in tmp.iterfind(".//script"):
                    _remove(self._tree, elem)
            ret.append(tmp)
            ret.append(tmp2)

        tmp2 = self._tree.find(".//script[@language='python']")
        if tmp2 != None:
            _remove(self._tree, tmp2)
        tmp = self._tree.find(".//body")
        if tmp == None:
            tmp = self._tree
        for elem in tmp.iterfind(".//script"):
            _remove(self._tree, elem)
        ret.insert(0, tmp2)
        ret.insert(0, tmp)
        return ret


    def _reparent(self, selectors):
        ret = []

        for selector in selectors:
            tmp = None
            tmp2 = None
            _tmp = self._tree.find(selector+"/..")
            if _tmp != None:
                tmp = _tmp.find(selector.replace('.//', './'))
            if tmp != None:
                _remove(self._tmp, tmp)
                _tmp2 = tmp.find(".//script[@language='python']/..")
                if _tmp2 != None:
                    tmp2 = _tmp2.find("./script[@language='python']")
                if tmp2 != None:
                    _remove(_tmp2, tmp2)
                for _elem in tmp.iterfind(".//script/.."):
                    elem = _elem.find("./script")
                    if elem != None:
                        _remove(_elem, elem)
            ret.append(tmp)
            ret.append(tmp2)

        _tmp2 = self._tree.find(".//script[@language='python']/..")
        if _tmp2 != None:
            tmp2 = _tmp2.find("./script[@language='python']")
        else:
            tmp2 = None
        if tmp2 != None:
            _remove(_tmp2, tmp2)
        tmp = self._tree.find(".//body")
        if tmp == None:
            tmp = self._tree
        for _elem in tmp.iterfind(".//script/.."):
            elem = _elem.find("./script")
            if elem != None:
                _remove(_elem, elem)
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
        """Get body fragment"""
        return (Elem(self._data[0]), Script(self._data[1]))

    def get_header(self):
        """Get header fragment"""
        return (Elem(self._data[2]), Script(self._data[3]))

    def get_footer(self):
        """Get footer fragment"""
        return (Elem(self._data[4]), Script(self._data[5]))

    def get_panel(self):
        """Get panel fragment"""
        return (Elem(self._data[6]), Script(self._data[7]))

    def get_body_attrs(self):
        """Get body attributes"""
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
