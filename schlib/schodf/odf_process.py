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

"""Module contain class and functions for odf file transformations.

"""

from zipfile import ZipFile, ZIP_DEFLATED
import re
import shutil
import xml.dom.minidom
import base64

from schlib.schfs.vfstools import delete_from_zip


def _enumerate_childs(node, tab=None):
    if tab == None:
        rettab = []
    else:
        rettab = tab
    for child in node.childNodes:
        rettab.append(child)
        if child.hasChildNodes():
            _enumerate_childs(child, rettab)
    return rettab


class DocTransform:
    """Transformate odf file"""

    def __init__(self, file_name_in, file_name_out=None):
        """Constructor

        Args:
            file_name_in - input file name
            file_name_out - output file name - if none output file name is composed from input file name.
        """
        self.file_name_in = file_name_in
        if file_name_out == None:
            self.file_name_out = file_name_in.replace('_', '')
        else:
            self.file_name_out = file_name_out
        self.process_tables = None
        self.doc_type = 1

    def set_doc_type(self, doc_type):
        """
            doc_type:
                0 - other
                1 - spreadsheet
                2 - writer
        """
        self.doc_type = doc_type

    def set_process_tables(self, tables):
        self.process_tables = tables

    def nr_col(self):
        return """{{ tbl.IncCol()}}"""

    def nr_row(self, il=1):
        return """{{ tbl.IncRow(%d)}}{{ tbl.SetCol(1) }}""" % il

    def zer_row_col(self):
        return """{{ tbl.SetRow(1) }}{{ tbl.SetCol(1) }}"""

    def doc_process(self, doc, debug):
        pass

    def spreadsheet_process(self, doc, debug):
        elementy = doc.getElementsByTagName('text:p')
        for element in elementy:
            if element.parentNode.nodeName == 'office:annotation':
                data = ""
                for child in _enumerate_childs(element):
                    if hasattr(child, 'data'):
                        data+=child.data

                if data!="" and '!' in data:
                    data = data[data.find('!'):]
                    poziom = 1
                    if len(data) > 1 and data[1] == '!':
                        if len(data) > 2 and data[2] == '!':
                            poziom = 3
                        else:
                            poziom = 2
                    if '@' in data[poziom:]:
                        skladniki = data[poziom:].split('@')
                    else:
                        skladniki = data[poziom:].split('$')
                    x = element.parentNode
                    y = element.parentNode.parentNode
                    y.removeChild(x)
                    if poziom > 1:
                        y = y.parentNode
                    if poziom > 2:
                        y = y.parentNode
                    new_cell = doc.createElement('tmp')
                    y.parentNode.replaceChild(new_cell, y)
                    new_cell.appendChild(doc.createTextNode(skladniki[0]))
                    new_cell.appendChild(y)
                    if len(skladniki) > 1:
                        new_cell.appendChild(doc.createTextNode(skladniki[1]))
        elementy = doc.getElementsByTagName('table:table-cell')
        for element in elementy:
            nr = element.getAttribute('table:number-columns-repeated')
            if nr:
                nr = int(nr)
                if nr>1000:
                    element.setAttribute('table:number-columns-repeated', '1000')

            if element.getAttribute('office:value-type') == 'string':
                for child in _enumerate_childs(element):  # .childNodes:
                    if child and child.firstChild and hasattr(child.firstChild, 'data'):
                        if child.firstChild.data and len(child.firstChild.data) > 0 and \
                                (child.firstChild.data[0] == '*' or child.firstChild.data[0] == ':' or
                                child.firstChild.data[0] == '@' or child.firstChild.data[0] == '$'):
                            if child.firstChild.data[0] == ':' or child.firstChild.data[0] == '*':
                                new_cell = doc.createElement('table:table-cell')
                                if child.firstChild.data[0] == ':':
                                    new_cell.setAttribute('office:value-type',
                                            'float')
                                    new_cell.setAttribute('office:value',
                                            str(child.firstChild.data[1:]))
                                    new_text = doc.createElement('text:p')
                                else:
                                    new_cell.setAttribute('office:value-type',
                                            'string')
                                    new_text = doc.createElement('text:p')
                                    new_text.appendChild(doc.createTextNode(str(child.firstChild.data[1:])))
                                if debug:
                                    new_annotate = doc.createElement('office:annotation')
                                    new_text_a = doc.createElement('text:p')
                                    new_text_a.appendChild(doc.createTextNode(child.firstChild.data[2:-1]))
                                    new_annotate.appendChild(new_text_a)
                                new_cell.appendChild(new_text)
                                if debug:
                                    new_cell.appendChild(new_annotate)
                                new_cell.setAttribute('table:style-name', element.getAttribute('table:style-name'))
                                new_cell2 = doc.createElement('tmp')
                                new_cell2.appendChild(new_cell)
                                new_cell2.appendChild(doc.createTextNode(self.nr_col()))
                                element.parentNode.replaceChild(new_cell2,element)
                            if child.firstChild.data[0] == '@' or child.firstChild.data[0] == '$':
                                new_cell = doc.createElement('table:table-cell')
                                new_cell.setAttribute('office:value-type', 'float')
                                new_cell.setAttribute('office:value', '0')
                                if child.firstChild.data[0] == '@':
                                    new_cell.setAttribute('table:formula', 'oooc:=' + child.firstChild.data[1:])
                                else:
                                    new_cell.setAttribute('table:formula', 'msoxl:=' + child.firstChild.data[1:])
                                new_text = doc.createElement('text:p')
                                if debug:
                                    new_annotate = doc.createElement('office:annotation')
                                    new_text_a = doc.createElement('text:p')
                                    new_text_a.appendChild(doc.createTextNode(child.firstChild.data[1:].\
                                            replace('^', '')))
                                    new_annotate.appendChild(new_text_a)
                                new_cell.appendChild(new_text)
                                if debug:
                                    new_cell.appendChild(new_annotate)
                                new_cell.setAttribute('table:style-name', element.getAttribute('table:style-name'))
                                new_cell2 = doc.createElement('tmp')
                                new_cell2.appendChild(new_cell)
                                new_cell2.appendChild(doc.createTextNode(self.nr_col()))
                                element.parentNode.replaceChild(new_cell2, element)

        elementy = doc.getElementsByTagName('table:table-row')
        for element in elementy:
            parent = element.parentNode
            new_cell = doc.createElement('tmp')
            nr = element.getAttribute('table:number-rows-repeated')
            if nr:
                nr = int(nr)
                if nr>1000:
                    element.setAttribute('table:number-rows-repeated', '1000')
            else:
                nr = 1
            parent.replaceChild(new_cell, element)
            new_cell.appendChild(element)
            new_cell.appendChild(doc.createTextNode(self.nr_row(nr)))

        elementy = doc.getElementsByTagName('table:table')
        for element in elementy:
            parent = element.parentNode
            new_cell = doc.createElement('tmp')
            new_cell.appendChild(doc.createTextNode(self.zer_row_col()))
            parent.replaceChild(new_cell, element)
            new_cell.appendChild(element)
        if self.process_tables != None:
            elementy = doc.getElementsByTagName('table:table')
            for element in elementy:
                if not element.getAttribute('table:name') in self.process_tables:
                    new_cell = doc.createElement('tmp')
                    element.parentNode.replaceChild(new_cell, element)

    def process_template(self, doc_str, context):
        pass

    def process(self, context, debug):
        """Transform input file

        Args:
            context - python dict with variables used for transformation
            debut - print debug information
        """
        shutil.copyfile(self.file_name_in, self.file_name_out)
        z = ZipFile(self.file_name_out, 'r')
        doc_content = z.read('content.xml').decode('utf-8')
        z.close()
        
        if delete_from_zip(self.file_name_out, 'content.xml')==0:
            return

        doc = xml.dom.minidom.parseString(doc_content.replace('&apos;', "'").\
                replace('_start_', '{{').replace('_end_', '}}'))
        
        if self.doc_type==1:
            self.spreadsheet_process(doc, debug)
        if self.doc_type==2:
            self.doc_process(doc, debug)
        
        doc_str = doc.toxml().replace('<tmp>', '').replace('</tmp>', '')

        p = re.compile('\^(.*?\(.*?\))')
        doc_str = p.sub(r'${\1}', doc_str)
        doc_str = doc_str.replace('{{', '{% expr_escape ').replace('}}', ' %}')

        x = self.process_template(doc_str, context)
        if not x:
            x = doc_str

        files = []
        if '[[[' in x and ']]]' in x:
            data = [ pos.split(']]]')[0] for pos in x.split('[[[')[1:] ]
            data2 = [ pos.split(']]]')[-1] for pos in x.split('[[[')]
            fdata = []
            i = 1
            for pos in data:
                x = pos.split(',', 1)
                ext = x[0].split(';')[0].split('/')[-1]
                name = 'Pictures/pytigon_%d.%s' % (i, ext)
                fdata.append(name)
                files.append([name, x, ext])
                i += 1

            data3 = [None] * (len(data)+len(data2))
            data3[::2] = data2
            data3[1::2] = fdata
            x = "".join(data3)

        z = ZipFile(self.file_name_out, 'a', ZIP_DEFLATED)
        z.writestr('content.xml', x.encode('utf-8'))

        for pos in files:
            z.writestr(pos[0], base64.b64decode(pos[1].encode('utf-8')))

        z.close()

        return 1

if __name__ == '__main__':
    x = DocTransform("./test/test.ods", "./test/test_out.ods")
    context = { 'test': 1 }
    x.process(context, False)
