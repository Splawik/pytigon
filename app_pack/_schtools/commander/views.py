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


class FileManager(forms.Form):
    folder = forms.CharField(label='Folder', required=True, )
    sort = forms.ChoiceField(label='Sort', required=True, choices=models.file_manager_sort_choices)
    
    
    

def view_filemanager(request, *argi, **argv):
    return PFORM(request, FileManager, 'commander/formfilemanager.html', {})








def grid(request, folder, value):
    
    return vfstable_view(request, folder, value)
    






def open(request, file_name):
    
    return vfsopen(request, file_name)
    






def save(request, file_name):
    
    return vfssave(request, file_name)
    






def open_page(request, file_name, page):
    
    return vfsopen_page(request, file_name, page)
    


 
