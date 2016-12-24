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
    from urllib.parse import urlencode
except:
    from urllib import urlencode


class DictParm:
    def __init__(self, d):
        self.Dict = d

    def get_parm(self, parm):
        return self.Dict[parm]

    def has_parm(self, parm):
        return parm in self.Dict


def conwert_parm(parm):
    if type(parm).__name__ == "DateTime":
        return str(parm)[0:10]
    if type(parm) == list:
        return parm
    if type(parm) == bool:
        return parm
    return parm


def dict_from_parm(parm, fields):
    ret = {}
    for field in fields:
        if parm.HasParm(field):
            ret[field] = parm.HasParm(field)
    return ret


def create_parm(address, dic, no_encode=False):
    l = address.split('|')
    if len(l) > 1:
        p = l[1].split(',')
        parm = ''
        if '?' in address:
            znak = '&'
        else:
            znak = '?'
        test = 0
        en = dict()
        for pos in p:
            if dic.has_parm(pos):
                if dic.get_parm(pos) != None:
                    if '__' in pos:
                        pos2 = pos.split('__')[0]
                        if pos2 in en:
                            if en[pos2].__class__ == list:
                                en[pos2].append(conwert_parm(dic.get_parm(pos)))
                            else:
                                en[pos2] = [en[pos2], conwert_parm(dic.get_parm(pos))]
                        else:
                            en[pos2] = conwert_parm(dic.get_parm(pos))
                    else:
                        en[pos] = conwert_parm(dic.get_parm(pos))
        if no_encode:
            return (l[0], znak, en)
        else:
            parm = parm + urlencode(en, True)
            return (l[0], znak, parm)
    else:
        return None


def create_post_parm(address, dic):
    l = address.split('|')
    if len(l) > 1:
        p = l[1].split(',')
        return (l[0], dict_from_parm(p, dict))
    else:
        return (l, {})


