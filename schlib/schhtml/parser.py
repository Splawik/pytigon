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
    from lxml import etree
    LXML = True
except:
    import xml.etree.ElementTree as etree
    from naivehtmlparser import NaiveHTMLParser
    LXML = False


import io
import re

class Parser:
    def __init__(self):
        self._tree = None
        self._cur_elem = None

    def get_starttag_text(self):
        if self._cur_elem:
            ret = ""
            for key, value in self._cur_elem.items():
                if value:
                    ret = ret + "%s=\"%s\" " % (key, value)
                else:
                    ret = ret + key + " "
            return "<%s %s>" % (self._cur_elem.tag, ret[0:-1])
        return ""

    def handle_starttag(self, tag, attrib):
        pass

    def handle_data(self, txt):
        pass

    def handle_endtag(self, tag):
        pass

    def _crawl_tree(self, tree):
        self._cur_elem = tree
        if type(tree.tag) is str:
            self.handle_starttag(tree.tag.lower(), tree.attrib)
            if tree.text:
                self.handle_data(tree.text)
            for node in tree:
                self._crawl_tree(node)
            self.handle_endtag(tree.tag)
        if tree.tail:
            self.handle_data(tree.tail)

    def crawl_tree(self, tree):
        self._tree = tree
        self._crawl_tree(self._tree)

    def from_html(self, html_txt):
        global LXML
        if LXML:
            parser = etree.HTMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True)
            return etree.parse(io.StringIO(html_txt), parser).getroot()
        else:
            parser = NaiveHTMLParser()
            root = parser.feed(html_txt)
            parser.close()
            return root


    def init(self, html_txt):
        if type(html_txt) == Elem:
            self._tree = self.from_html("<html></html>")
            self._tree.append(html_txt.elem)
        else:
            try:
                self._tree = self.from_html(html_txt)
            except:
                print(html_txt)
                self._tree = None

    def feed(self, html_txt):        
        self.init(html_txt)
        self._crawl_tree(self._tree)

    def close(self):
        self._tree = None




def tostring(elem):
    global LXML
    if LXML:
        return etree.tostring(elem,encoding='unicode', method="html", pretty_print=True)
    else:
        return etree.tostring(elem,encoding='unicode', method="html")


def content_tostring(elem):
    tab = []
    if elem.text:
        tab.append(elem.text)
    for pos in elem:
        tab.append(tostring(pos))
    if elem.tail:
        tab.append(elem.tail)
    return "".join(tab)


class Elem():
    def __init__(self, elem, tostring_fun = tostring):
        self.elem = elem
        self._elem_txt = None
        self._tostring_fun = tostring_fun

    def __str__(self):
        if self._elem_txt == None:
            if self.elem!=None:
                self._elem_txt = self._tostring_fun(self.elem)
            else:
                return ""
        return self._elem_txt

    def __len__(self):
        if self._elem_txt == None:
            self._elem_txt = self._tostring_fun(self.elem)
        return len(self._elem_txt)

    def __bool__(self):
        if self.elem == None:
            return False
        else:
            return True

    def super_strip(self, s):
        s = re.sub(r"(( )*(\\n)*)*", "", s)
        return s.strip()

    def tostream(self, output=None, elem=None, tab=0):
        if elem==None:
            elem=self.elem
        if output == None:
            output = io.StringIO()
        if type(elem.tag) is str:
            output.write(' '*tab)
            output.write(elem.tag.lower())
            first = True
            for key, value in elem.attrib.items():
                if first:
                    output.write(' ')
                else:
                    output.write(",,,")
                output.write(key)
                output.write('=')
                if type(value)==str:
                    output.write(value.replace('\n', '\\n'))
                else:
                    output.write(str(value).replace('\n', '\\n'))

                first=False
            if elem.text:
                x = self.super_strip(elem.text.replace('\n','\\n'))
                if x:
                    output.write("...")
                    output.write(x)
            output.write("\n")
            for node in elem:
                self.tostream(output, node, tab+4)
        if elem.tail:
            x = self.super_strip(elem.tail.replace('\n', '\\n'))
            if x:
                output.write(' '*tab)
                output.write('.')
                output.write(x)
                output.write('\n')
        return output


class Script(Elem):
    def __init__(self, elem, tostring_fun = content_tostring):
        super().__init__(elem, tostring_fun)
