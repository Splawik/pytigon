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

from django.http import HttpResponse


def open_db_field(
    app,
    table,
    object_id,
    field,
    ):
    pass


def save_db_field(
    app,
    table,
    object_id,
    field,
    txt,
    ):
    pass


def vfsopen(request, file):
    try:
        file2 = b32decode(file).decode('utf-8')
        plik = OpenFile(file2, vfsman)
        buf = plik.read()
        plik.close()
    except:
        buf = ''
    return HttpResponse(buf)


def vfssave(request, file):
    buf = 'ERROR'
    plik = None
    if request.POST:
        try:
            data = request.POST['data']
            file2 = b32decode(file).decode('utf-8')
            plik = OpenFile(file2, vfsman)
            plik.write(data)
            plik.close()
            buf = 'OK'
        except:
            buf = 'ERROR: ' + str(sys.exc_info()[0])
            if plik:
                plik.close()
    return HttpResponse(buf)


