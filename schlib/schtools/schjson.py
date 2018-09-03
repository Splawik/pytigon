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


"""Helper class for json encoder"""


try:
    import json
except:
    import django.utils.simplejson as json
try:
    from urllib.parse import quote_plus, unquote_plus
except:
    from urllib import quote_plus, unquote_plus
    
import datetime


class ComplexEncoder(json.JSONEncoder):
    complex_types = (
        'list',
        'unicode',
        'str',
        'int',
        'long',
        'float',
        'bool',
        'NoneType',
        )

    def default(self, obj):
        if not obj.__class__.__name__ in self.complex_types:
            if obj.__class__.__name__ == 'datetime':
                return {'object': repr(obj).replace(", tzinfo=<UTC>", "") }
            else:
                return {'object': repr(obj)}
        return json.JSONEncoder.default(self, obj)


def as_complex(dct):
    if 'object' in dct:
        return eval(dct['object'])
    return dct


def dumps(obj):
    """Encode python object to json format. Return enquoted json string

    Args:
        obj - python object to encode
    """
    return quote_plus(json.dumps(obj, cls=ComplexEncoder))


def loads(json_str):
    """Load json str and return decoded structure.

    Args:
        json_str: enquoted json encoded string

    """
    return json.loads(unquote_plus(json_str), object_hook=as_complex)


def json_dumps(obj, indent=None):
    """Encode python object to json format. Return encoded string.

    Args:
        obj - python object to encode
    """
    return json.dumps(obj, cls=ComplexEncoder, indent=indent)


def json_loads(json_str):
    """Load json str and return decoded structure.

    Args:
        json_str: json encoded string

    """
    return json.loads(json_str, object_hook=as_complex)

