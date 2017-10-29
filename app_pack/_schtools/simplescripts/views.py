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
from schlib.schdjangoext.tools import make_href

from django.utils.translation import ugettext_lazy as _

from . import models
import os
import sys
import datetime

from django.http import Http404

template_template = """
{%% extends 'simplescripts/script_form.html' %%}

{%% load exfiltry %%}
{%% load exsyntax %%}

%s

"""
 










def run(request, pk):
    
    script = models.Scripts.objects.get(pk=pk)
    form = None
    if script:
        exec(script._form)
        form_class=locals().get('ScriptsForm'+script.name, None)
        if form_class:
            if request.method == 'POST':
                form=form_class(request.POST)
                if form.is_valid():
                    exec(script._view)
                    v = locals().get('scripts_'+script.name, None)
                    if v:
                        parms = v(request, form.cleaned_data)
                        parms['form'] = form
                        script = template_template % script._template
    
                        template = Template(script)
                        context = RequestContext(request, parms)
                        ret_str = template.render(context)
                        return HttpResponse(ret_str)
            else:
                form = form_class()
        return render_to_response('simplescripts/script_form.html',  {'form': form}, request=request)
    raise Http404("Script does not exist")
    






def run_script_by_name(request, script_name):
    
    script = models.Scripts.objects.get(name=script_name)
    if script:
        if 'only_content' in request.GET:
            return HttpResponseRedirect("/simplescripts/table/Scripts/%d/action/run?childwin=1&only_content=1" % script.id)
        else:
            return HttpResponseRedirect("/simplescripts/table/Scripts/%d/action/run?childwin=1" % script.id)
    else:
        raise Http404("Script does not exist")
    


 
