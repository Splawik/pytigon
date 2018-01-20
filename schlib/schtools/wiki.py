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

from django.conf import settings


"""Module contains helper functions to handling wiki.

Wiki:
  [[Wiki word]] link
  [[^Wiki word]] link w nowym oknie
  [[(nowy panel)Wiki word]] 
"""


def wiki_from_str(wiki_value):
    if wiki_value.startswith('?'):
        return wiki_value[2:]
    wordSize=16
    wiki_value2 = wiki_value.encode('ascii', 'xmlcharrefreplace').decode('utf-8').replace('&','').replace('#','').replace(';','')
    x = wiki_value2.split('-')[0].strip()
    words = x.split(' ')
    l=len(words)
    wordSize = int(32/l)
    words2 = []
    for word in words:
        if len(word) > 1:
            words2.append(word[0].upper() + word[1:wordSize])
        else:
            words2.append(word.upper())
    wiki = ''.join(words2)[:32]
    if wiki == '':
        wiki = 'index'
    return wiki


def make_href(wiki_value, new_win=True, section=None, btn = False, path=None):
    wiki = wiki_from_str(wiki_value)
    if path:
        wiki = path + '+' + wiki
    if settings.URL_ROOT_FOLDER and settings.URL_ROOT_FOLDER != '':
        p = '/' + settings.URL_ROOT_FOLDER
    else:
        p = ''

    if btn:
        btn_str = "class='btn btn-secondary' label='%s'" % wiki_value
    else:
        btn_str = "class='schbtn' label='%s' " % wiki_value

    if section:
        if new_win:
            return "<a href='%s/schwiki/%s/%s/view/?desc=%s' target='_top2' %s>%s</a>" % (p, section, wiki, wiki_value, btn_str, wiki_value)
        else:
            return "<a href='%s/schwiki/%s/%s/view/?desc=%s' target='_self' %s>%s</a>" % (p, section, wiki, wiki_value, btn_str, wiki_value)
    else:
        if new_win:
            return "<a href='../../%s/view/?desc=%s' target='_top2' %s>%s</a>" % (wiki, wiki_value, btn_str, wiki_value)
        else:
            return "<a href='../../%s/view/?desc=%s' target='_self' %s>%s</a>" % (wiki, wiki_value, btn_str, wiki_value)


def wikify(value, path=None, section=None):
    x = value.split('[[')
    if len(x) > 1:
        ret = []
        ret.append(x[0])
        for pos in x[1:]:
            y = pos.split(']]')
            if len(y) == 2 and len(y[0])>1:
                txt = y[0]
                if txt[0] == '^':
                    new_win = True
                    txt = txt[1:]
                else:
                    new_win = False
                if txt[0]=='#':
                    btn = True
                    txt = txt[1:]
                else:
                    btn = False

                if ';' in txt:
                    l = txt.split(';')
                    txt = l[0]
                    _section = l[1]
                else:
                    _section = section
                ret.append(make_href(txt, new_win=new_win, section=_section, btn=btn, path=path) + y[1])
            else:
                ret.append('[[' + pos)
        return ''.join(ret)
    else:
        return value
