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

from .models import Page
from pytigon_lib.schdjangoext.fastform import form_from_str
from django.template.loader import select_template
from pytigon_lib.schviews import make_path
from pytigon_lib.schtools.schjson import json_loads, json_dumps
from base64 import b32decode, b32encode

template_start_wiki = """
{# -*- coding: utf-8 -*- #}

{% extends "schwiki/wiki_view.html" %}

{% load exfiltry %}
{% load exsyntax %}

"""

template_start = """
{# -*- coding: utf-8 -*- #}

{%% extends "schwiki/%s" %%}

{%% load exfiltry %%}
{%% load exsyntax %%}
"""

template_simple = """
{# -*- coding: utf-8 -*- #}

{% load exfiltry %}
{% load exsyntax %}
"""
 










def view_page(request, app_or_subject, page_path):
    
    desc = request.GET.get('desc','')
    path, sep, page_name = page_path.rpartition('+')
    if page_name:
        page_name = page_name[0].upper()+page_name[1:]
        
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
    
    path_list2 = []
    if path_list:
        for pos in path_list:
            try:
                #p = Page.objects.get(name=pos, subject=app_or_subject)
                p = Page.get_page(request, app_or_subject, name)
                if p.description:
                    path_list2.append(p.description)
                else:
                    path_list2.append(pos)
            except:
                path_list2.append(pos)
    
    page = Page.get_page(request, app_or_subject, page_name)
    if page:
        id = page.id
        content = page.content
        try: 
            t = Template(template_simple + content)
            c = RequestContext(request, {'object': page, 'wiki_path': path, })        
            #c = Context({'object': page, 'wiki_path': path, 'request': request })    
            content=t.render(c)
        except:
            content = page.content
    else:
        page = Page()
        page.name = page_name
        page.description=desc
        page.subject = app_or_subject
        page.update_time = datetime.datetime.now()
        page.operator = request.user.username
        page.save()
        id = page.id
        content = None
    
    
    conf = None
    if page:
        conf_list = models.WikiConf.objects.filter(subject=page.subject)
        if len(conf_list)>0:
            conf = conf_list[0]
        
    c = {'page_name': page_name, 'subject': app_or_subject, 'content': content, 'wiki_path': path, 
         'wiki_path_list': path_list, 'wiki_path_desc': path_list2, 'title': '?: ' + page_name, 'object': page,
         'description': desc if desc else page_name, 'only_content': True, 'conf': conf,
    }
    
    
    if page and page.base_template:
        base_template = page.base_template
    else:
        base_template = "schwiki/wiki_view.html"
    
    c['content'] = content
    
    
    return render(request, base_template, context=c)
    






def edit_page(request, app_or_subject, page_name):
    
    page = Page.get_page(request, subject=app_or_subject, name=page_name)    
    #page = Page.objects.get(name=page_name, subject=app_or_subject)
    if not page:
        page = Page(app=app, name=page_name, subject=app_or_subject)
        page.save()
    
    redir = make_href("/schwiki/table/Page/%d/edit/?childwin=1" % page.id)
    
    return HttpResponseRedirect(redir)
    




@dict_to_json

def insert_object_to_editor(request, pk):
    
    page_id = request.GET.get('page_id', 0)
    page=models.Page.objects.get(pk=page_id)
    
    if pk:
        object = models.PageObjectsConf.objects.get(pk=pk)        
        if object.edit_form:
            edit_form = "True"
        else:
            edit_form = "False"
        object_name = object.name
        object_inline_editing = object.inline_editing
    else:
        object = None
        edit_form = "True"
        object_name = None
        object_inline_editing = None
    
    return { 'pk': pk, 'object_name': object_name, 'object_inline_editing': object_inline_editing, 'object': object, 'page_id': page_id, 'page': page, 'edit_form': edit_form }
    






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
            
            context = {'conf': obj, 'page': page, 'request': request}
            
            if request.POST or request.FILES:    
                if request.method == 'POST':
                    if form_class:
                        form = form_class(request.POST, request.FILES)
                        if form.is_valid():
                            if obj.save_fun:
                                try:
                                    context['old_data'] = page.get_json_data()[name]
                                except:
                                    pass
                                exec(obj.save_fun)
                                data = locals()['save'](form, context)
                            else:
                                data = form.cleaned_data
                            page._data = { name: data } 
                            page._data['json_update'] = True
                            page.operator = request.user.username
                            page.update_time = datetime.datetime.now()
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
                        data_form = locals()['load'](data, context)
                    else:
                        if name in data:
                            data_form = data[name]
                        else:
                            data_form = {}
                    form = form_class(initial=data_form)
            
        
            template_name1 = (obj.app + "/" + obj.name).lower()+"_wikiobj_edit.html"
            template_name2 = "schwiki/wikiobj_edit.html"
            
            t = select_template([template_name1,template_name2,])
            c = { 'form': form, 'object': obj, 'page': page}
            
            return HttpResponse(t.render(c, request))
        
    url = make_path('ok')
    return HttpResponseRedirect(url)
    

@dict_to_template('schwiki/v_publish.html')




def publish(request, pk):
    
    conf = models.WikiConf.objects.get(pk = pk)
    object_list = []
    
    pages = models.Page.objects.filter(subject=conf.subject, latest=True, published=False, operator=request.user.username)
    if len(pages)>0:
        for page in pages:
            page.published = True
            page.save()
            if conf.publish_fun:
                exec(conf.publish_fun)
                info = locals()['publish_fun'](page, conf)
                object_list.append([page, info])
            else:
                object_list.append([page, ""])
    
    pages = models.Page.objects.filter(subject=conf.subject, latest=False, published=True, operator=request.user.username).update(published=False)
    
    return { "OK": True, 'object_list': object_list }
    

@dict_to_template('schwiki/v_search.html')




def search(request, q):
    
    search_txt = b32decode(q).decode('utf-8')
    object_list = Page.objects.filter(content__iregex=search_txt)
    
    return { "object_list": object_list, 'q': search_txt }
    


 
