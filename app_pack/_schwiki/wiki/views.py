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

from .models import Page
from schlib.schdjangoext.fastform import form_from_str
from django.template.loader import select_template
from schlib.schviews import make_path

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
 










def view_page(request, app_or_subject, page_name):
    
    path, sep, page_name = page_name.rpartition('+')
    id = -1
    if path:
        path_list = path.split('+')
        if page_name in path_list:
            path_list = path_list[:path_list.index(page_name)]
        if len(path_list) > 10:
            path_list = path_list[1:]    
        path = '+'.join(path_list+[page_name,]) 
    else:
        path_list = None
        path = page_name
    page = None
    try:
        page = Page.objects.get(name=page_name, subject=app_or_subject)
        id = page.id
        content = page.content
    except Page.DoesNotExist:
        content = None
        
    c = {'page_name': page_name, 'subject': app_or_subject, 'content': content, 'wiki_path': path, 'wiki_path_list': path_list, 'title': '?: ' + page_name, 'object': page }
    #if page:
        #if page.page_type != 'W':
    
    if page.base_template:
        base_template = page.base_template
    else:
        base_template = "wiki/wiki_view.html"
    
    #content2 = ( template_start % base_template ) + page.content
    c['content'] = content
    
    
    return render(request, base_template, context=c)
    #t = Template(content)
    #return HttpResponse(t.render(c))
    
    #t = Template(template_start_wiki)
    #return HttpResponse(t.render(c))
    






def edit_page(request, app_or_subject, page_name):
    
    #print('edit page:', subject, page_name)
    try:
        page = Page.objects.get(name=page_name, subject=app_or_subject)
    except Page.DoesNotExist:
        page = Page(app=app, name=page_name, subject=app_or_subject)
        #page.page_type = 'W'
        page.save()
    
    redir = make_href("/wiki/table/Page/%d/edit/?childwin=1" % page.id)
    
    return HttpResponseRedirect(redir)
    

@dict_to_template('wiki/v_insert_object_to_editor.html')




def insert_object_to_editor(request, pk):
    
    if pk != '0':
        object = models.PageObjectsConf.objects.get(pk=pk)
        page_id = request.GET.get('page_id', 0)
        page=models.Page.objects.get(pk=page_id)
        return { 'pk': pk, 'object': object, 'page': page }
    else:
        return {}
    






def edit_page_object(request):
    
    name = request.GET.get('name', None)
    if name:
        name = name.replace('\r','').strip()
        name0 = name.split('_')[0]
        object_list = models.PageObjectsConf.objects.filter(name=name0)
        if len(object_list)>0:
            obj = object_list[0]
            pk = request.GET.get('page_id', 0)
            page = models.Page.objects.get(pk=pk)
            
            if obj.edit_form:
                form_class = form_from_str(obj.edit_form)
            else:
                form_class = None
                form = None
                
            if request.POST or request.FILES:    
                if request.method == 'POST':
                    if form_class:
                        form = form_class(request.POST, request.FILES)
                        if form.is_valid():
                            if obj.save_fun:
                                exec(obj.save_fun)
                                data = locals()['save'](form, rep)
                            else:
                                data = form.cleaned_data
                            page._data = { name: data }
                            page._data['json_update'] = True
                            page.save()
                            url = make_path('ok')
                            return HttpResponseRedirect(url)
                    else:
                        url = make_path('ok')
                        return HttpResponseRedirect(url)
                                        
            if not request.POST:
                if form_class:
                    data = page.get_json_data()
                    
                    if obj.load_fun:
                        exec(obj.load_fun)
                        data_form = locals()['load'](data)
                    else:
                        if name in data:
                            data_form = data[name]
                        else:
                            data_form = {}
                    form = form_class(initial=data_form)
            
        
            template_name1 = (obj.app + "/" + obj.name).lower()+"_wikiobj_edit.html"
            template_name2 = "wiki/wikiobj_edit.html"
            
            t = select_template([template_name1,template_name2,])
            c = { 'form': form, 'object': obj, 'page': page}
            
            return HttpResponse(t.render(c, request))
        
    url = make_path('ok')
    return HttpResponseRedirect(url)
    


 
