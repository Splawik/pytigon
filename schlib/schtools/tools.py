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

import os
import zipfile
import re

def split_tag(s, start, end):
    i1 = s.find(start)
    if i1 >= 0:
        i2 = s.find(end, i1)
        if i2 >= 0:
            return (s[:i1], s[i1 + len(start):i2], s[i2 + len(end):])
    return (s, None, '')

def _clear_content(b):
    return b.replace(b' ', b'').replace(b'\n', b'').replace(b'\t', b'').replace(b'\r',b'')

def cmp_txt_str_content(b1, b2):
    _b1 = _clear_content(b1)
    _b2 = _clear_content(b2)
    if _b1==_b2:
        return True
    else:
        return False

def extractall(
    zip_file,
    path=None,
    members=None,
    pwd=None,
    exclude=None,
    backup_zip=None,
    backup_exts=None,
    ):
    if members is None:
        members = zip_file.namelist()
    for zipinfo in members:
        if zipinfo.endswith('/') or zipinfo.endswith('\\'):
            if not os.path.exists(path + '/' + zipinfo):
                os.makedirs(path + '/' + zipinfo)
        else:
            test=True
            if exclude:
                for pos in exclude:
                    if re.match(pos, zipinfo, re.I) != None:
                        test=False
                        break
            if test:
                if backup_zip:
                    if not backup_exts or zipinfo.split('.')[-1] in backup_exts:
                        out_name = os.path.join(path, zipinfo)
                        if os.path.exists(out_name):
                            bytes = zip_file.read(zipinfo, pwd)
                            with open(out_name, 'rb') as f:
                                bytes2 = f.read()
                            if not cmp_txt_str_content(bytes, bytes2):
                                backup_zip.writestr(zipinfo, bytes2)
                zip_file.extract(zipinfo, path, pwd)


class ZipWriter:
    def __init__(self, filename, basepath="", exclude=[]):
        self.filename = filename
        self.basepath = basepath
        self.base_len = len(self.basepath)
        self.zip_file = zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED)
        self.exclude = exclude

    def close(self):
        self.zip_file.close()

    def write(self, file_name, name_in_zip=None):
        test = True
        for pos in self.exclude:
            if re.match(pos, file_name, re.I) != None:
                test=False
                break
        if test:
            f = open(file_name, "rb")
            data = f.read()
            f.close()
            if name_in_zip:
                self.zip_file.writestr(name_in_zip, data)
            else:
                self.zip_file.writestr(file_name[self.base_len:], data)

    def toZip(self, file):
        if os.path.isfile(file):
            self.write(file)
        else:
            self.addFolderToZip(file)

    def addFolderToZip(self, folder):
        for file in os.listdir(folder):
            full_path = os.path.join(folder, file)
            if os.path.isfile(full_path):
                self.write(full_path)
            elif os.path.isdir(full_path):
                self.addFolderToZip(full_path)

def split2(txt, sep):
    id = txt.find(sep)
    if id>=0:
        return (txt[:id], txt[id+1:])
    else:
        return (txt,"")