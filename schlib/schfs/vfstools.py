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

import re
import os.path
import tempfile
import email.generator
import zipfile
import six

def replace_dot(url):
    ldest = []
    if url == '' or url == None:
        return ''
    url2 = url.replace(' ', '%20').replace('://', '###').replace('\\','/')
    if not '.' in url2:
        return url2.replace('###', '://').replace('%20', ' ')
    lsource = url2.split('/')
    for l in lsource:
        if l == '..':
            ldest.pop()
        else:
            if l != '.':
                ldest.append(l)
    ret = None
    for l in ldest:
        if ret == None:
            ret = l
        else:
            ret = ret + '/' + l
    if ret != None:
        if ret == '':
            return '/'
        else:
            return ret.replace('###', '://').replace('%20', ' ')
    else:
        return ''

def get_temp_filename(base_name=None):
    boundary = email.generator._make_boundary()
    if base_name:
        return os.path.join(tempfile.gettempdir(),six.text_type(boundary)+"_"+base_name)
    else:
        return os.path.join(tempfile.gettempdir(),six.text_type(boundary))

class Cmp(object):

    def __init__(
        self,
        masks,
        key,
        convert_to_re=False,
        ):

        if masks:
            self.masks = []
            for mask in masks:
                if convert_to_re:
                    x = mask[1:].replace('.', '\\.').replace('*', '.*'
                            ).replace('?', '.')
                else:
                    x = mask[1:]
                self.masks.append((mask[0], re.compile(x)))
        else:
            self.masks = None
        if key:
            self.key = key.lower()
        else:
            self.key = None

    def re_cmp(self, value1, mask):
        ret = mask.match(value1)
        if ret:
            return True
        else:
            return False

    def masks_filter(self, file_name):
        if self.masks:
            sel = False
            for filter in self.masks:
                if filter[0] == '+':
                    if self.re_cmp(file_name, filter[1]):
                        sel = True
                else:
                    if self.re_cmp(file_name, filter[1]):
                        sel = False
            return sel
        else:
            return False

    def key_filter(self, file_name):
        if self.key:
            if file_name.lower().startswith(self.key):
                return True
            else:
                return False
            return True

    def filter(self, file_name):
        if self.key_filter(file_name) and self.masks_filter(file_name):
            return True
        return False


def delete_from_zip(zip_name, del_file_name):
    tmpname = get_temp_filename()
    zin = zipfile.ZipFile (zip_name, 'r')
    zout = zipfile.ZipFile (tmpname, 'w', zipfile.ZIP_STORED)
    for item in zin.infolist():
        if item.filename.lower() != del_file_name.lower():
            buffer = zin.read(item.filename)
            zout.writestr(item, buffer)
            #print(">>>", item.filename)
    zout.close()
    zin.close()
    os.remove(zip_name)
    os.rename(tmpname,zip_name)
    return 1

