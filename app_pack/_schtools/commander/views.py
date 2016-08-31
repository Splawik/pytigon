#!/usr/bin/python

# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django import forms
from django.template.loader import render_to_string
from django.template import Context, Template
from django.template import RequestContext
from django.conf import settings
from django.views.generic import TemplateView

from schlib.schviews.form_fun import form_with_perms
from schlib.schviews.viewtools import dict_to_template, dict_to_odf, dict_to_pdf, dict_to_json, dict_to_xml
from schlib.schviews.viewtools import render_to_response

from django.utils.translation import ugettext_lazy as _

from . import models
import os
import sys
import datetime

from schlib.schfs.vfstable import vfstable_view, vfsopen, vfssave, vfsopen_page
 

PFORM = form_with_perms('commander') 


class FileMmanager(forms.Form):
    folder = forms.CharField(label='Folder', required=True, )
    sort = forms.ChoiceField(label='Sort', required=True, choices=models.file_manager_sort_choices)
    
    def process(self, request, queryset=None):
    
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

def view_filemmanager(request, *argi, **argv):
    return PFORM(request, FileMmanager, 'commander/formfilemmanager.html', {})








def grid(request, folder, value):
    
    return vfstable_view(request, folder, value)
    






def open(request, file_name):
    
    return vfsopen(request, file_name)
    






def save(request, file_name):
    
    return vfssave(request, file_name)
    






def open_page(request, file_name, page):
    
    return vfsopen_page(request, file_name, page)
    


 
