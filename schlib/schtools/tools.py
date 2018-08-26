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


import types
import sys
import os
import platform
import inspect

from base64 import b64encode, b64decode


def split2(txt, sep):
    """split txt to two part based on first occurrence of sep in txt. If sep doesn't exist in txt,
    returned second part is ''
    """
    id = txt.find(sep)
    if id>=0:
        return (txt[:id], txt[id+len(sep):])
    else:
        return (txt,"")


def extend_fun_to(obj):
    """Function decorator - extend obj with defined function.

    Args:
        obj - obj which shoud be extended

    Example:
        class A:
            pass

        a = A()

        @extend_fun_to(a):
        def test(self, s):
            print(s)

        a.test("Hello world!")
    """
    def fun(func):
        setattr(obj, func.__name__, types.MethodType(func, obj))
        return func
    return fun


def bencode(s):
    """encode string s by b64encode function"""
    if type(s)==str:
        return b64encode(s.encode('utf-8')).decode('utf-8')
    else:
        return b64encode(s).decode('utf-8')


def bdecode(s):
    """decode string encoded by bencode function"""
    if type(s)==str:
        return b64decode(s.encode('utf-8')).decode('utf-8')
    else:
        return b64decode(s).decode('utf-8')


def clean_href(href):
    """return href.replace('\n', '').strip()"""
    return href.replace('\n', '').strip()


def is_null(value, value2):
    """
    if value:
        return value
    else:
        return value2
    """
    if value:
        return value
    else:
        return value2

def get_executable():
    x = sys.executable
    p = x.replace('\\','/').split('/')[-1]
    if 'python' in p:
        return x
    else:
        if platform.system() == "Windows":
            return os.__file__[:-9] + 'python.exe'
        else:
            return os.__file__[:-6].replace('/lib/python', '/bin/python')


def norm_indent(text):
    text_tab = text
    if type(text) == str:
        text_tab = text.replace('\r', '').split('\n')
    indent = -1
    ret = []
    for pos in text_tab:
        if indent < 0:
            x1 = len(pos)
            x2 = len(pos.lstrip())
            indent = x1-x2
        ret.append(pos[indent:])
    if indent >= 0:
        return "\n".join(ret)
    else:
        return ""

def get_request():
    frame = None
    r = None
    try:
        for f in inspect.stack()[1:]:
            frame = f[0]
            code = frame.f_code

            if code.co_varnames[:1] == ("request",):
                r = frame.f_locals["request"]
            elif code.co_varnames[:2] == ("self", "request",):
                r = frame.f_locals["request"]
            if r and hasattr(r, 'session'):
                return r
            else:
                r = None
    finally:
        if frame:
            del frame
    return None

def get_session():
    request = get_request()
    if request:
        return request.session
    else:
        return None

def is_in_dicts(elem, dicts):
    for dict in dicts:
        if elem in dict:
            return True
    return False

def get_from_dicts(elem, dicts):
    for dict in dicts:
        if elem in dict:
            return dict[elem]
    return False
