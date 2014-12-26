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

from django import forms
from base64 import b32encode, b32decode
from schlib.schfs.vfs import VfsManager, MainDir, get_dir
from schlib.schfs.zip import VfsPluginZip
from schlib.schfs.sevenzip import VfsPluginSevenZip
from schlib.schfs.tar import VfsPluginTar
from django.utils.translation import ugettext_lazy as _


sort_CHOICES = (('N', _('Name')), ('S', _('Size')), ('T', _('Time')))

vfsman = VfsManager()
vfsman.install_plugin(VfsPluginZip())
vfsman.install_plugin(VfsPluginSevenZip())
vfsman.install_plugin(VfsPluginTar())

class FileManagerForm(forms.Form):

    folder = forms.CharField(required=False)
    sort = forms.ChoiceField(label=_('Sort'), choices=sort_CHOICES,
                             required=False)

    def get_table(self, folder):
        f = get_dir(folder, vfsman)
        files = []
        folders = []
        for pos in f.get_dirs():
            folders.append(pos)

        for pos in f.get_files():
            files.append(pos)

        return (folders, files)

    def process_empty(self, request, param=None):
        if param and param != '' and param != '_':
            dir = b32decode(param.split('/')[0])
        else:
            dir = '/'
        tabela = self.get_table(dir)
        self.data = {
            'folder': dir,
            'folders': tabela[0],
            'files': tabela[1],
            'tabela': tabela,
            }
        return self.data

    def process(self, request, param=None):
        folder = self.cleaned_data['folder']
        sort = self.cleaned_data['sort']
        if folder == None or folder == '':
            folder = '/'
        tabela = self.get_table(folder)
        return {
            'folder': folder,
            'sort': sort,
            'folders': tabela[0],
            'files': tabela[1],
            'tabela': tabela,
            }


