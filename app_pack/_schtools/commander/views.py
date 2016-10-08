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
from schlib.schfs.zip import VfsPluginZip
from schlib.schfs.vfs import VfsManager, get_dir


 

PFORM = form_with_perms('commander') 


class FileManager(forms.Form):
    folder = forms.CharField(label='Folder', required=True, )
    sort = forms.ChoiceField(label='Sort', required=True, choices=models.file_manager_sort_choices)
    
    
    

def view_filemanager(request, *argi, **argv):
    return PFORM(request, FileManager, 'commander/formfilemanager.html', {})


class Move(forms.Form):
    dest = forms.ChoiceField(label='Destination', required=True, choices=[])
    
    
    

def view_move(request, *argi, **argv):
    return PFORM(request, Move, 'commander/formmove.html', {})


class Copy(forms.Form):
    dest = forms.ChoiceField(label='Destination', required=True, choices=[])
    
    
    

def view_copy(request, *argi, **argv):
    return PFORM(request, Copy, 'commander/formcopy.html', {})


class MkDir(forms.Form):
    name = forms.CharField(label='Folder name', required=True, max_length=None, min_length=None)
    
    def process(self, request, queryset=None):
    
        name = self.cleaned_data['name']
        base_folder = request.session.get('commander_mkdir', None)
        if base_folder: 
            man = VfsManager()
            man.install_plugin(VfsPluginZip())
            x = get_dir(base_folder, man)
            x.mk_dir(name)
        
        request.session['commander_mkdir'] = None
        
        return { "OK": True }
    
    def preprocess_request(self, request):
        if 'dir' in request.POST:
            request.session['commander_mkdir'] = request.POST['dir']
            return None
        else:
            return request.POST

def view_mkdir(request, *argi, **argv):
    return PFORM(request, MkDir, 'commander/formmkdir.html', {})


class Rename(forms.Form):
    name = forms.CharField(label='Name', required=True, max_length=None, min_length=None)
    
    
    

def view_rename(request, *argi, **argv):
    return PFORM(request, Rename, 'commander/formrename.html', {})


class NewFile(forms.Form):
    name = forms.CharField(label='Name', required=True, max_length=None, min_length=None)
    
    
    

def view_newfile(request, *argi, **argv):
    return PFORM(request, NewFile, 'commander/formnewfile.html', {})


class Delete(forms.Form):
    recycle_bin = forms.BooleanField(label='Recycle bin', required=True, initial=True,)
    
    
    

def view_delete(request, *argi, **argv):
    return PFORM(request, Delete, 'commander/formdelete.html', {})








def grid(request, folder, value):
    
    return vfstable_view(request, folder, value)
    






def open(request, file_name):
    
    return vfsopen(request, file_name)
    






def save(request, file_name):
    
    return vfssave(request, file_name)
    






def open_page(request, file_name, page):
    
    return vfsopen_page(request, file_name, page)
    


 
