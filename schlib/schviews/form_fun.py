#!/usr/bin/python
# -*- coding: utf-8 -*-
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation; either version 3, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.

#Pytigon - wxpython and django application framework

#author: "Sławomir Chołaj (slawomir.cholaj@gmail.com)"
#copyright: "Copyright (C) ????/2012 Sławomir Chołaj"
#license: "LGPL 3.0"
#version: "0.1a"

# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template import loader
from .perms import make_perms_url_test_fun
from .viewtools import render_to_response_ext

def form(request, form_class, template_name, object_id=None, form_end=False, param=None, mimetype=None):
    template_name2 = template_name
    if request.POST:
        f = form_class(request.POST, request.FILES)
        if hasattr(f, "init"):
            f.init(request)
        if f.is_valid():
            if param:
                user_dict = f.process(request, param)
            else:
                user_dict = f.process(request)
            user_dict.update({'form': f})
            if object_id:
                user_dict.update({'object_id': object_id})

            c = RequestContext(request, user_dict)
            if hasattr(f, "render_to_response"):
                return f.render_to_response(request, template_name2, c)
            else:
                if 'doc_type' in user_dict:
                    doc_type = user_dict['doc_type']
                else:
                    doc_type = 'html'
                return render_to_response_ext(request, template_name2, context=user_dict, doc_type=doc_type)
                #if doc_type= 'html':
                #    return render_to_response(template_name2, context_instance=c)
                #elif doc_type= 'pdf':

        else:
            c = RequestContext(request, {'form': f})
            return render_to_response(template_name2, context_instance=c)
    else:
        f = form_class()
        if hasattr(f, "init"):
            f.init(request)
        if object_id:
            f.object_id = object_id
    
        if hasattr(f, "process_empty"):
            if param:
                user_dict = f.process_empty(request, param)
            else:
                user_dict = f.process_empty(request)
            c = RequestContext(request, {'form': f})
            c.update(user_dict)
        else:
            user_dict = {'form': f}
            if object_id:
                user_dict.update({'object_id': object_id})
            c = RequestContext(request, user_dict)
            if param:
                c.update(param)
        return render_to_response(template_name2, context_instance=c)

def form_with_perms(app):
    return make_perms_url_test_fun(app, form)

def list_and_form(
    request,
    queryset,
    form_class,
    template_name,
    table_always=True,
    paginate_by=None,
    page=None,
    allow_empty=True,
    extra_context=None,
    context_processors=None,
    template_object_name='obj',
    mimetype=None,
    param=None,
    ):

    queryset2 = queryset
    if request.POST:
        new_data = request.POST.copy()
        f = form_class(new_data)
        if f.is_valid():
            if param:
                queryset2 = f.Process(request, queryset, param)
            else:
                queryset2 = f.Process(request, queryset)
            if extra_context:
                extra_context.update({'form': f})
            else:
                extra_context = {'form': f}
            return list(
                request=request,
                queryset=queryset2,
                paginate_by=paginate_by,
                page=page,
                allow_empty=allow_empty,
                template_loader=loader,
                template_name=template_name,
                extra_context=extra_context,
                context_processors=context_processors,
                template_object_name=template_object_name,
                mimetype=mimetype,
                )
    else:
        f = form_class()
        if table_always:
            if extra_context:
                extra_context.update({'form': f})
            else:
                extra_context = {'form': f}

            if hasattr(f, "ProcessEmpty"):
                if param:
                    queryset2 = f.ProcessEmpty(request, queryset, param)
                else:
                    queryset2 = f.ProcessEmpty(request, queryset)

            return list(
                request=request,
                queryset=queryset2,
                paginate_by=paginate_by,
                page=page,
                allow_empty=allow_empty,
                template_loader=loader,
                template_name=template_name,
                extra_context=extra_context,
                context_processors=context_processors,
                template_object_name=template_object_name,
                mimetype=mimetype,
                )

    c = RequestContext(request, {'form': f})
    return render_to_response(template_name, context_instance=c)


def direct_to_template(request, template, extra_context=None, mimetype=None, **kwargs):
    """
    Render a given template with any extra URL parameters in the context as
    ``{{ params }}``.
    """
    if extra_context is None: extra_context = {}
    dictionary = {'params': kwargs}
    for key, value in extra_context.items():
        if callable(value):
            dictionary[key] = value()
        else:
            dictionary[key] = value
    c = RequestContext(request, dictionary)
    t = loader.get_template(template)
    s = t.render(c)
    return HttpResponse(s, mimetype=mimetype)

