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

from schlib.schdjangoext.tools import gettempdir

def norm_path(url):
    """Normalize url"""
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


def open_and_create_dir(filename, mode):
    """Open file - if path doesn't exist - path is created

    Args:
        filename - path and name of file
        mode - see mode for standard python function: open
    """
    print(filename)
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
    return open(filename, mode)


def get_temp_filename(base_name=None):
    """Get temporary file name

    Args:
        base_name - if not Null returning name contains base_name
    """
    boundary = email.generator._make_boundary()
    if base_name:
        return os.path.join(gettempdir(),boundary+"_"+base_name)
    else:
        return os.path.join(gettempdir(),boundary)



def delete_from_zip(zip_name, del_file_names):
    """Delete one file from zip

    Args:
        zip_name - name of zip file
        del_file_names - name of file to delete
    """
    del_file_names2 = [pos.lower() for pos in del_file_names]

    tmpname = get_temp_filename()
    zin = zipfile.ZipFile (zip_name, 'r')
    zout = zipfile.ZipFile (tmpname, 'w', zipfile.ZIP_STORED)
    for item in zin.infolist():
        if not item.filename.lower() in del_file_names2:
            buffer = zin.read(item.filename)
            zout.writestr(item, buffer)
    zout.close()
    zin.close()
    os.remove(zip_name)
    os.rename(tmpname,zip_name)
    return 1


def _clear_content(b):
    return b.replace(b' ', b'').replace(b'\n', b'').replace(b'\t', b'').replace(b'\r',b'')


def _cmp_txt_str_content(b1, b2):
    _b1 = _clear_content(b1)
    _b2 = _clear_content(b2)
    if _b1==_b2:
        return True
    else:
        return False


def extractall(zip_file, path=None, members=None, pwd=None, exclude=None, backup_zip=None, backup_exts=None):
    """Extract content from zip file

    Args:
        zip_file - path to zip file
        path - destination path to extract zip content
        members - if None: extract all zip members else: extract only files which are in members list
        pwd  - password for zip, can be None if password is not set
        exclude - do not extract files which are in exclude list
        backup_zip -
            Files extracted from zip can overwrite existings ones. If backup_zip is set to ZipFile object,
            this function test if new content is equal with old before overwriting. If there are diferences,
            old contents is saved to backup_zip. After operation backup_zip contains all changed files by
            extracting zip file.
        backup_exts - if  parametr is set, backed to backup_zip are only files which are on backup_ext list.
    """
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
                            if not _cmp_txt_str_content(bytes, bytes2):
                                backup_zip.writestr(zipinfo, bytes2)
                zip_file.extract(zipinfo, path, pwd)


class ZipWriter:
    """Helper class to create zip files"""

    def __init__(self, filename, basepath="", exclude=[]):
        """Constructor

        Args:
            filename - path to zip file
            basepath
        """
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
                self.zip_file.writestr(file_name[self.base_len+1:], data)

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


#Perhaps for delete
class Cmp(object):
    def __init__(self, masks, key, convert_to_re=False):
        if masks:
            self.masks = []
            for mask in masks:
                if convert_to_re:
                    x = mask[1:].replace('.', '\\.').replace('*', '.*').replace('?', '.')
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

