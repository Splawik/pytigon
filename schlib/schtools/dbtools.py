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


class _RowProxy():
    def __init__(self, row):
        self.raw_row = row

    def __getattr__(self, attr_name):
        return getattr(self.raw_row, attr_name)

    def __getitem__(self, key):
        return self.raw_row[int(key)]


def result_proxy(tab):
    for pos in tab:
        yield _RowProxy(pos)


if __name__ == '__main__':
    test = [[1,2],[3,4],[5,6]]

    gen = result_proxy(test)

    for pos in gen:
        print(pos[0], pos[1])

