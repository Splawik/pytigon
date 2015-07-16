#!/usr/bin/python

# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.template import Context, Template
from django.template import RequestContext
from django.conf import settings
from django.views.generic import TemplateView

from schlib.schviews.form_fun import form_with_perms
from schlib.schviews.viewtools import dict_to_template, dict_to_odf, dict_to_pdf, dict_to_json, dict_to_xml

from django.utils.translation import ugettext_lazy as _

from . import models
import os
import sys
import datetime

from .models import Page

template_start_wiki = """
{# -*- coding: utf-8 -*- #}

{% extends "wiki/wiki_view.html" %}

{% load exfiltry %}
{% load exsyntax %}

"""

template_start = """
{# -*- coding: utf-8 -*- #}

{%% extends "wiki/%s" %%}

{%% load exfiltry %%}
{%% load exsyntax %%}
"""
 










def view_page(request, subject, page_name):
    
    page = None
    try:
        page = Page.objects.get(name=page_name, subject=subject)
        content = page.content
    except Page.DoesNotExist:
        content = None
    c = RequestContext(request, {'page_name': page_name, 'subject': subject, 'content': content,
                       'title': '?: ' + page_name})
    if page:
        if page.page_type != 'W':
            if page.base_template:
                base_template = page.base_template
            else:
                base_template = "view.html"
            content2 = ( template_start % base_template ) + page.content
            t = Template(content2)
            return HttpResponse(t.render(c))
    
    t = Template(template_start_wiki)
    return HttpResponse(t.render(c))
    






def edit_page(request, subject, page_name):
    
    print('edit page:', subject, page_name)
    try:
        page = Page.objects.get(name=page_name, subject=subject)
    except Page.DoesNotExist:
        page = Page(name=page_name, subject=subject)
        page.page_type = 'W'
        page.save()
    
    redir = "/wiki/table/Page/%d/edit/?childwin=1" % page.id
    
    return HttpResponseRedirect(redir)
    


 
