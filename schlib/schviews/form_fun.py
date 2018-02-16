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

"""Module contains views for form processing

"""


from django.http import HttpResponse
from django.template import RequestContext
from django.template import loader
from django.conf import settings

from schlib.schviews.viewtools import render_to_response

from .perms import make_perms_url_test_fun
from .viewtools import render_to_response_ext


def form(request, app_name, form_class, template_name, object_id=None, form_end=False, param=None, mimetype=None):
    """Function make new form views

    Args:
        request
        app_name
        form_class
        template_name
        object_id
        form_end
        param
        mimetype
    """
    template_name2 = template_name
    app_pack = ""
    for app in settings.APPS:
        if '.' in app and app_name in app:
            _app = app.split('.')[0]
            if not _app.startswith('_'):
                app_pack = app.split('.')[0]
            break

    if request.POST or request.FILES:
        f = form_class(request.POST, request.FILES)
    else:
        f = form_class()

    if hasattr(f, "preprocess_request"):
        post = f.preprocess_request(request)
    else:
        post = request.POST

    if post:
        if hasattr(f, "init"):
            f.init(request)
        if f.is_valid():
            if param:
                user_dict = f.process(request, param)
            else:
                user_dict = f.process(request)
            if not issubclass(type(user_dict), dict):
                return user_dict
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
        else:
            if hasattr(f, "process_invalid"):
                if param:
                    user_dict = f.process(request, param)
                else:
                    user_dict = f.process(request)
                user_dict.update({'form': f})
                if not issubclass(type(user_dict), dict):
                    return user_dict
                if object_id:
                    user_dict.update({'object_id': object_id})
                return render_to_response(template_name2, context=user_dict, request=request)
            else:
                return render_to_response(template_name2, context={'form': f}, request=request)
    else:
        if hasattr(f, "init"):
            f.init(request)
        if object_id:
            f.object_id = object_id
    
        if hasattr(f, "process_empty"):
            if param:
                user_dict = f.process_empty(request, param)
            else:
                user_dict = f.process_empty(request)
            user_dict['form'] = f
            user_dict['app_pack'] = app_pack
        else:
            user_dict = {'form': f,  'app_pack': app_pack}
            if object_id:
                user_dict.update({'object_id': object_id})
            if param:
                user_dict.update(param)
        return render_to_response(template_name2, context=user_dict, request=request)

def form_with_perms(app):
    return make_perms_url_test_fun(app, form)

def list_and_form(request, queryset, form_class, template_name, table_always=True, paginate_by=None, page=None,
        allow_empty=True, extra_context=None, context_processors=None, template_object_name='obj',
        mimetype=None, param=None):
    """List form

    Args:
        request
        queryset
        form_class
        template_name
        table_always
        paginate_by
        page
        allow_empty
        extra_context
        context_processors
        template_object_name
        mimetype
        param
    """

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
            return list(request=request, queryset=queryset2, paginate_by=paginate_by, page=page,
                    allow_empty=allow_empty, template_loader=loader, template_name=template_name,
                    extra_context=extra_context, context_processors=context_processors,
                    template_object_name=template_object_name, mimetype=mimetype,)
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

            return list(request=request, queryset=queryset2, paginate_by=paginate_by, page=page,
                    allow_empty=allow_empty, template_loader=loader, template_name=template_name,
                    extra_context=extra_context, context_processors=context_processors,
                    template_object_name=template_object_name, mimetype=mimetype,)

    return render_to_response(template_name, context={'form': f}, request=request)


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

