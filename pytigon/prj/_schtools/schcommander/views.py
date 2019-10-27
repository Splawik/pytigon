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

from pytigon_lib.schviews.form_fun import form_with_perms
from pytigon_lib.schviews.viewtools import dict_to_template, dict_to_odf, dict_to_pdf, dict_to_json, dict_to_xml
from pytigon_lib.schviews.viewtools import render_to_response
from pytigon_lib.schdjangoext.tools import make_href

from django.utils.translation import ugettext_lazy as _

from . import models
import os
import sys
import datetime

from pytigon_lib.schtable.vfstable import vfstable_view, vfsopen, vfssave, vfsopen_page
from schtools.models import Parameter
import django.contrib.auth
 

PFORM = form_with_perms('schcommander') 


class FileManager(forms.Form):
    folder = forms.CharField(label=_('Folder'), required=True, )
    sort = forms.ChoiceField(label=_('Sort'), required=True, choices=models.file_manager_sort_choices)
    
    
    

def view_filemanager(request, *argi, **argv):
    return PFORM(request, FileManager, 'schcommander/formfilemanager.html', {})


class Move(forms.Form):
    dest = forms.ChoiceField(label=_('Destination'), required=True, choices=[])
    
    
    
    def preprocess_request(self, request):
        if 'dir' in request.POST:
            dirs = request.POST['dir'].split(';')
            choices = [ [pos, pos] for pos in dirs ]
            self.data =  { 'dest': choices[0][0], }
            self.fields['dest'].choices = choices
            return None
        else:
            return request.POST

def view_move(request, *argi, **argv):
    return PFORM(request, Move, 'schcommander/formmove.html', {})


class Copy(forms.Form):
    dest = forms.ChoiceField(label=_('Destination'), required=True, choices=[])
    
    
    
    def preprocess_request(self, request):
        if 'dir' in request.POST:
            dirs = request.POST['dir'].split(';')
            choices = [ [pos, pos] for pos in dirs ]
            self.data =  { 'dest': choices[0][0], }
            self.fields['dest'].choices = choices
            return None
        else:
            return request.POST

def view_copy(request, *argi, **argv):
    return PFORM(request, Copy, 'schcommander/formcopy.html', {})


class MkDir(forms.Form):
    name = forms.CharField(label=_('Folder name'), required=True, max_length=None, min_length=None)
    
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
    return PFORM(request, MkDir, 'schcommander/formmkdir.html', {})


class Rename(forms.Form):
    name = forms.CharField(label=_('Name'), required=True, max_length=None, min_length=None)
    
    
    

def view_rename(request, *argi, **argv):
    return PFORM(request, Rename, 'schcommander/formrename.html', {})


class NewFile(forms.Form):
    name = forms.CharField(label=_('Name'), required=True, max_length=None, min_length=None)
    
    
    

def view_newfile(request, *argi, **argv):
    return PFORM(request, NewFile, 'schcommander/formnewfile.html', {})


class Delete(forms.Form):
    recycle_bin = forms.BooleanField(label=_('Recycle bin'), required=True, initial=True,)
    
    
    

def view_delete(request, *argi, **argv):
    return PFORM(request, Delete, 'schcommander/formdelete.html', {})


class Setup(forms.Form):
    path1 = forms.CharField(label=_('Path 1'), required=False, max_length=None, min_length=None)
    path2 = forms.CharField(label=_('Path 2'), required=False, max_length=None, min_length=None)
    path3 = forms.CharField(label=_('Path 3'), required=False, max_length=None, min_length=None)
    path4 = forms.CharField(label=_('Path 4'), required=False, max_length=None, min_length=None)
    glob = forms.BooleanField(label=_('Default for all users'), required=False, )
    
    def process(self, request, queryset=None):
    
        paths = [ self.cleaned_data['path1'], self.cleaned_data['path2'], self.cleaned_data['path3'], self.cleaned_data['path4'] ]
        glob = self.cleaned_data['glob']
        
        u = django.contrib.auth.get_user(request)
        
        if glob:
            base_key = 'commander/all/path'
        else:
            base_key = 'commander/%s/path' % u.username
        
        for i in range(4):
            objs = Parameter.objects.filter(key=base_key+str(i))
            if len(objs)>0:
                param = objs[0]
            else:
                param = Parameter()
                param.key = base_key + str(i)
            param.value = paths[i]
            param.save()
        
        return { "OK": True }
    
    def preprocess_request(self, request):
        if 'dir' in request.POST:
            panels = request.POST['dir'].split(';')
            self.data =  { 'path1': panels[0], 'path2': panels[1], 'path3': panels[2], 'path4': panels[3], }
            return None
        else:
            return request.POST
    
def view_setup(request, *argi, **argv):
    return PFORM(request, Setup, 'schcommander/formsetup.html', {})








def grid(request, folder, value):
    
    return vfstable_view(request, folder, value)
    






def open(request, file_name):
    
    return vfsopen(request, file_name)
    






def save(request, file_name):
    
    return vfssave(request, file_name)
    






def open_page(request, file_name, page):
    
    return vfsopen_page(request, file_name, page)
    


 
