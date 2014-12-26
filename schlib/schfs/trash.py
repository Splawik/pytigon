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
import shutil
import datetime


class DeleteToTrash(object):

    def __init__(self):
        try:
            self.home = os.environ['HOME']
        except:
            self.home = ''
        self.path = self.home + '/.local/share'
        try:
            x = os.environ['$XDG_DATA_HOME']
        except:
            x = None
        if x:
            self.path = x
        self.delete_path = self.path + '/Trash/files'
        self.info_path = self.path + '/Trash/info'
        self.info_suffix = '.trashinfo'

    def delete(self, file_path):
        name = os.path.basename(file_path)
        name2 = None
        del_name = os.path.join(self.delete_path, name)
        i = 0
        while os.path.exists(del_name):
            i = i + 1
            name2 = name + '_' + str(i)
            del_name = os.path.join(self.delete_path, name2)
        if name2:
            name = name2
        del_info = os.path.join(self.info_path, name + self.info_suffix)
        if os.path.isdir(file_path):
            shutil.move(file_path, del_name)
        else:
            shutil.move(file_path, del_name)
        x = open(del_info, 'w')
        if x:
            x.write('[Trash Info]\n')
            x.write('Path=%s\n' % file_path)
            x.write('DeletionDate=%s\n'
                     % datetime.datetime.now().strftime('%Y-%m-%dT%T'))
            x.close()


