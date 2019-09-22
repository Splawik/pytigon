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

from schelements.models import DocHead
from schreports.models import Report
from pytigon_lib.schviews import make_path










def duplicate_rep(request, parm):
    
    def copy_rep(source, dest):
        dest.parent = source.parent
        dest.order = source.order
        dest.report_def_name = source.report_def_name
        dest.date = source.date
        dest.jsondata = source.jsondata
    
    id = int(parm)
    doc = DocHead.objects.filter(pk=id)
    
    if len(doc)==1:
        d = doc[0]
        rep = Report.objects.filter(order=d.id)
        if len(rep)==1:
            doc2 = DocHead()
            doc2.doc_type_parent = d.doc_type_parent
            doc2.org_chart_parent = d.org_chart_parent
            doc2.description = d.description
            doc2.date = datetime.datetime.now()
            doc2.status= 'edit'
            doc2.operator = request.user.username
            doc2.param1 = d.param1
            doc2.param2 = d.param2
            doc2.param3 = d.param3
            doc2.jsondata = d.jsondata
            doc2.save()
                
            rep2 = Report()
            copy_rep(rep[0], rep2)
            rep2.order = doc2.id
            rep2.save()
            
            subreps = Report.objects.filter(parent=rep[0])    
            if len(subreps)>0:
                for subrep in subreps:
                    subrep2 = Report()
                    copy_rep(subrep, subrep2)
                    subrep2.parent = rep2
                    subrep2.save()
                
    url = make_path('ok')
    return HttpResponseRedirect(url)
    


 
