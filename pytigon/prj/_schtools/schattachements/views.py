#!/usr/bin/python

# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django import forms
from django.template import RequestContext
from django.views.generic import TemplateView

from pytigon_lib.schviews.form_fun import form_with_perms
from pytigon_lib.schviews.viewtools import render_to_response
from pytigon_lib.schdjangoext.tools import make_href

from django.utils.translation import ugettext_lazy as _

from . import models
import os
import datetime

from wsgiref.util import FileWrapper
import mimetypes
 










def download(request, pk):
    
    obj= models.Attachements.objects.get(id=pk)
    wrapper      = FileWrapper(open(obj.file.path, "rb")) 
    content_type = mimetypes.guess_type(obj.file.path)[0] 
    response     = HttpResponse(wrapper,content_type=content_type)  
    response['Content-Length']      = os.path.getsize(obj.file.path)    
    response['Content-Disposition'] = "attachment; filename=%s" %  obj.file.name
    return response
    


 