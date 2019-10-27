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

from django.http import Http404
from pytigon_lib.schdjangoext.django_ihtml import ihtml_to_html
from pytigon_lib.schdjangoext.fastform import form_from_str
from schsimplescripts.script_tools import decode_script

SCRIPT_TEMPLATE = """
{%% extends 'schsimplescripts/script_form.html' %%}

{%% load exfiltry %%}
{%% load exsyntax %%}

%s

"""
 










def run(request, pk):
    
    script = models.Scripts.objects.get(pk=pk)
    form = None
    if script:
        form_class=form_from_str(script._form)    
        if form_class:
            if request.method == 'POST':
                form=form_class(request.POST)
                if form.is_valid():
                    argv = form.cleaned_data
                    exec(script._view)
                    v = locals().get('scripts_'+ script.name, None)
                    if v:
                        parms = v(request, form.cleaned_data)
                        parms['form'] = form
                        template_script = SCRIPT_TEMPLATE % script._template
                        template = Template(template_script)
                        context = RequestContext(request, parms)
                        ret_str = template.render(context)
                        return HttpResponse(ret_str)                
            else:
                form = form_class()
        return render_to_response('schsimplescripts/script_form.html',  {'form': form}, request=request)
    raise Http404("Script does not exist")
    






def run_script_by_name(request, script_name):
    
    script = models.Scripts.objects.get(name=script_name)
    if script:
        if 'only_content' in request.GET:
            return HttpResponseRedirect("/schsimplescripts/table/Scripts/%d/action/run/?childwin=1&only_content=1" % script.id)
        else:
            return HttpResponseRedirect("/schsimplescripts/table/Scripts/%d/action/run/?childwin=1" % script.id)
    else:
        raise Http404("Script does not exist")
    






def run_script(request, **argv):
    
    if 'script' in request.POST:
        code = request.POST['script']
        request.session['script_code'] = code
        x = decode_script("code", code)
        if x:    
            form_class=form_from_str(x[0])
            return render(request, 'schsimplescripts/script_form.html',  {'form': form_class()})
    else:
        if request.method == 'POST':
            if 'script_code' in request.session:
                code = request.session['script_code']
                x = decode_script("code", code)
                if x:                
                    form_class=form_from_str(x[0])
                    form=form_class(request.POST)
    
                    if form.is_valid():
                        argv = form.cleaned_data
                        exec(x[1])
                        v = locals().get('scripts_code', None)
                        if v:
                            parms = v(request, form.cleaned_data)
                            parms['form'] = form
                            script = SCRIPT_TEMPLATE % x[2]
                            template = Template(script)
                            context = RequestContext(request, parms)
                            ret_str = template.render(context)
                            return HttpResponse(ret_str)
                            
    return HttpResponse("Error")
    
    


 
