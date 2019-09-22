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

import configparser
import zipfile
from pytigon_lib.schfs.vfstools import get_temp_filename
from pytigon_lib.schtools.install import extract_ptig
 

PFORM = form_with_perms('schinstall') 


class upload_ptig(forms.Form):
    status = forms.CharField(label=_('Status'), required=False, max_length=None, min_length=None)
    ptig = forms.FileField(label=_('Pytigon install file (*.ptig)'), required=False, widget=forms.ClearableFileInput(attrs={'accept': '.ptig'}))
    accept_license = forms.BooleanField(label=_('Accept license'), required=False, initial=False,)
    
    def process(self, request, queryset=None):
    
        status = self.cleaned_data['status']
        if status:
            if status == '1':
                if 'INSTALL_FILE_NAME' in request.session:
                    file_name = request.session['INSTALL_FILE_NAME']
                    archive = zipfile.ZipFile(file_name, 'r')
                    accept_license = self.cleaned_data['accept_license']
                    if accept_license:
                        initdata = archive.read('install.ini')
                        config = configparser.ConfigParser()
                        config.read_string(initdata.decode('utf-8'))
                        
                        if 'APPSET_NAME' in config['DEFAULT']:
                            appset_name = config['DEFAULT']['APPSET_NAME']
                            if appset_name:                
                                ret = extract_ptig(archive, appset_name)
                                return { 'object_list': ret, 'status': 2 }
                        return { 'object_list': [['Invalid install file'],], 'status': 2 }
                    else:
                        readmedata = archive.read('README.txt')
                        licensedata = archive.read('LICENSE.txt')
                        return { 'object_list': None, 'status': 1, 'readmedata': readmedata.decode('utf-8'), 'licensedata': licensedata.decode('utf-8'), 'first': False }
                return { 'object_list': None, 'status': None }
        else:
            if 'ptig' in request.FILES:
                ptig = request.FILES['ptig']         
                file_name = get_temp_filename("temp.ptig")
                request.session['INSTALL_FILE_NAME'] = file_name
                plik = open(file_name, 'wb')
                plik.write(ptig.read())
                plik.close()
                archive = zipfile.ZipFile(file_name, 'r')
                readmedata = archive.read('README.txt')
                licensedata = archive.read('LICENSE.txt')
                archive.close()
                self.initial = { 'accept_license': False, }
                return { 'object_list': None, 'status': 1, 'readmedata': readmedata.decode('utf-8'), 'licensedata': licensedata.decode('utf-8'), 'first': True }
            else:
                return { 'object_list': None, 'status': None }
    
    def clean(self):
        status = self.cleaned_data['status']
        if not status:
            ret = { 'status': None }
        else:
            if not self.cleaned_data['accept_license']:
                self._errors["accept_license"] = ["The license must be approved"]
            ret = self.cleaned_data
        return ret
    
    def process_invalid(self, request, param=None):
        return { 'object_list': [] }

def view_upload_ptig(request, *argi, **argv):
    return PFORM(request, upload_ptig, 'schinstall/formupload_ptig.html', {})




 
