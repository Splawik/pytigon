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


#import schserw.schsys.initdjango
#django_ok = initdjango.init_django()

def decode(var):
    if var.__class__ == str:
        return var.decode('utf-8')
    else:
        return var


def encode(var):
    if var.__class__ == str:
        return var.encode('utf-8')
    else:
        return var


def decode_table(tab, list_to_decode):
    ret = []
    for row in tab:
        r = []
        for i in range(len(row)):
            if i in list_to_decode:
                if row[i]:
                    r.append(decode(row[i]))
                else:
                    r.append('')
            else:
                r.append(row[i])
        ret.append(r)
    return ret


ModuleTitle = 'System'
Title = 'System tools'
Perms = True
Index = 'index'
Urls = (
         #('../admin?schtml=1', 'Administracja', 'auth.add_user', 'client://categories/applications-other.png'),
         #('../admin/password_change?schtml=1', 'Zmień hasło', None, 'client://categories/applications-other.png'),
         #('do_logout?schtml=1', 'Wyloguj się', None, 'client://categories/applications-other.png')
)
