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

from wsgiref.util import FileWrapper
import mimetypes
 










def download(request, pk):
    
    obj=models.Attachements.objects.get(id=pk)
    wrapper      = FileWrapper(open(obj.file.path, "rb")) 
    content_type = mimetypes.guess_type(obj.file.path)[0] 
    response     = HttpResponse(wrapper,content_type=content_type)  
    response['Content-Length']      = os.path.getsize(obj.file.path)    
    response['Content-Disposition'] = "attachment; filename=%s" %  obj.file.name
    return response
    


 
