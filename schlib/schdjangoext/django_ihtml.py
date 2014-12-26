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

from schlib.schindent.indent_style import ConwertToHtml

SimpleCloseElem = ['br', 'meta', 'input']
AutoCloseDjangoElem = [
    'for',
    'if',
    'ifequal',
    'ifnotequal',
    'ifchanged',
    'block',
    'filter',
    'with',
    ]

NoAutoCloseDjangoElem = [
    'else',
    ]



def ihtml_to_html(file_name, input_str=None, lang='en'):
    conwert = ConwertToHtml(file_name, SimpleCloseElem, AutoCloseDjangoElem, NoAutoCloseDjangoElem, input_str, lang)
    try:
        conwert.process()
        return conwert.to_str()
    except:
        import traceback
        import sys
        print(sys.exc_info())
        print(traceback.print_exc())
        return ""
