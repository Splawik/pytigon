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

#author: "Slawomir Cholaj (slawomir.cholaj@gmail.com)"
#copyright: "Copyright (C) ????/2012 Slawomir Cholaj"
#license: "LGPL 3.0"
#version: "0.1a"
#from django.db import models

from django.apps import apps
from django.db.models import Max, Min
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.response import TemplateResponse
from django.template import loader, RequestContext, Context
from django.views import generic
from django.core import serializers

import os
import os.path
from schlib.schhtml.htmlviewer import stream_from_html
from schlib.schdjangoext.odf_render import render_odf
from schlib.schtools import schjson
from schlib.schhttptools.htmltab import SimpleTabParserBase
from django.utils import six
import io


def transform_template_name(obj, request, template_name):
    if hasattr(obj, 'transform_template_name'):
        return obj.transform_template_name(request, template_name)
    else:
        return template_name


def change_pos(
    request,
    app,
    tab,
    pk,
    forward=True,
    field=None,
    callback_fun=None
    ):
    model = apps.get_model(app, tab)
    #obj = lookup_object(model, pk, None, None)
    obj = model.objects.get(id=pk)
    if field:
        query = model.objects.extra(where=[field + '_id=%s'],
                                    params=[getattr(obj, field).pk])
    else:
        query = model.objects
    if forward:
        agr = query.filter(id__gt=int(pk)).aggregate(Min('id'))
        if 'id__min' in agr:
            object_id_2 = agr['id__min']
        else:
            HttpResponse('NO')
    else:
        agr = query.filter(id__lt=int(pk)).aggregate(Max('id'))
        if 'id__max' in agr:
            object_id_2 = agr['id__max']
        else:
            HttpResponse('NO')
    if object_id_2 == None:
        return HttpResponse('NO')
    #obj2 = lookup_object(model, object_id_2, None, None)
    obj2 = model.objects.get(id=object_id_2)
    tmp_id = obj.id
    obj.id = obj2.id
    obj2.id = tmp_id
    if callback_fun:
        callback_fun(obj, obj2)
    obj.save()
    obj2.save()
    return HttpResponse('YES')


def duplicate_row(
    request,
    app,
    tab,
    pk,
    field=None,
    ):
    model = apps.get_model(app, tab)
    obj = model.objects.get(id=pk)
    if obj:
        obj.id = None
        obj.save()
        return HttpResponse('YES')
    return HttpResponse('NO')



class LocalizationTemplateResponse(TemplateResponse):
    def resolve_template(self, template):
        lang=self._request.LANGUAGE_CODE[:2].lower()
        if lang!='en':
            if isinstance(template, (list, tuple)):
                templates = []
                for pos in template:
                    templates.append(pos.replace('.html','_'+lang+'.html'))
                    templates.append(pos)
                return loader.select_template(templates)
            elif isinstance(template, six.string_types):
                return TemplateResponse.resolve_template(self, [template.replace('.html','_'+lang+'.html'), template])
            else:
                return template
        else:
            return TemplateResponse.resolve_template(self, template)


class ExtTemplateResponse(LocalizationTemplateResponse):
    def __init__(self, request, template, context=None, content_type=None, status=None, mimetype=None,
                 current_app=None, charset=None, using=None):


        if context and 'view' in context and context['view'].doc_type()=='pdf':
            template2 = []
            if 'template_name' in context:
                template2.append(context['template_name']+'.html')
            for pos in template:
                template2.append(pos.replace('.html', '_pdf.html'))
            template2.append("schsys/table_pdf.html")
        elif context and 'view' in context and context['view'].doc_type()=='txt':
            template2 = []
            if 'template_name' in context:
                template2.append(context['template_name']+'.html')
            for pos in template:
                template2.append(pos.replace('.html', '_txt.html'))
        elif context and 'view' in context and context['view'].doc_type()=='odf':
            template2 = []
            if 'template_name' in context:
                template2.append(context['template_name']+'.ods')
            for pos in template:
                template2.append(pos.replace('.html', '.ods'))
            template2.append("schsys/table.ods")
        else:
            template2 = template

        try:
            TemplateResponse.__init__(self, request, template2, context,
                                      content_type, status, current_app, charset=charset, using=using)
        except:
            TemplateResponse.__init__(self, request, template2, context,
                                  content_type, status, current_app)

    def render(self):
        if self.context_data['view'].doc_type()=='odf':
            self['Content-Type'] = 'application/vnd.oasis.opendocument.spreadsheet'
            file_out, file_in = render_odf(self.template_name, None, Context(self.resolve_context(self.context_data)))
            if file_out:
                f = open(file_out,"rb")
                self.content = f.read()
                f.close()
                os.remove(file_out)
                file_in_name = os.path.basename(file_in)
                self['Content-Disposition'] = 'attachment; filename=%s' % file_in_name
            return self
        else:
            ret = TemplateResponse.render(self)
            if self.context_data['view'].doc_type()=='pdf':
                if self._request.META['HTTP_USER_AGENT'].startswith('Py'):
                    self['Content-Type'] = 'application/zip'
                    self['Content-Disposition'] = 'attachment; filename="somefilename.zip"'
                    zip_stream = stream_from_html(self.content, stream_type='zip')
                    self.content = zip_stream.getvalue()
                else:
                    self['Content-Type'] = 'application/pdf'
                    #self['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
                    pdf_stream = stream_from_html(self.content, stream_type='pdf')
                    self.content = pdf_stream.getvalue()
            elif self.context_data['view'].doc_type()=='json':
                self['Content-Type'] = 'application/json'

                mp = SimpleTabParserBase()
                mp.feed(self.content.decode('utf-8'))
                mp.close()

                row_title = mp.tables[-1][0]
                tab = mp.tables[-1][1:]


                if ':' in row_title[0]:
                    x = row_title[0].split(':')
                    title=x[0]
                    per_page, c = x[1].split('/')
                    row_title[0] = title
                else:
                    per_page = 1
                    c = len(tab)-1

                for i in range(len(row_title)):
                    row_title[i] = "%d" % i
                row_title[0] = 'cid'
                row_title[-1] = 'caction'

                tab2 = []
                for row in tab:
                    tab2.append(dict(zip(row_title, row)))

                d = {}
                d['total'] = c
                d['rows'] = tab2

                self.content = schjson.json_dumps(d)

            return ret


class ExtTemplateView(generic.TemplateView):

    response_class = ExtTemplateResponse

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def doc_type(self):
        if self.kwargs['target']=='pdf':
            return "pdf"
        elif self.kwargs['target']=='odf':
            return "odf"
        elif self.kwargs['target']=='txt':
            return "txt"
        else:
            return "html"

def render_to_response_ext(request, template_name, context, doc_type='html'):
    context['target'] = doc_type
    if 'request' in context:
        del context['request']
    return ExtTemplateView.as_view(template_name=template_name)(request, **context)
    


def dict_to_template(template_name):
    def _dict_to_template(func):
        def inner(request, *args, **kwargs):
            v = func(request, *args, **kwargs)
            c=RequestContext(request, v)
            return render_to_response(template_name, context_instance=c)
        return inner
    return _dict_to_template


def dict_to_odf(template_name):
    def _dict_to_template(func):
        def inner(request, *args, **kwargs):
            v = func(request, *args, **kwargs)
            c=RequestContext(request, v)
            return render_to_response_ext(request, template_name, c, doc_type='odf')
        return inner
    return _dict_to_template


def dict_to_pdf(template_name):
    def _dict_to_template(func):
        def inner(request, *args, **kwargs):
            v = func(request, *args, **kwargs)
            c=RequestContext(request, v)
            return render_to_response_ext(request, template_name, c, doc_type='pdf')
        return inner
    return _dict_to_template


def dict_to_json(func):
    def inner(request, *args, **kwargs):
        v = func(request, *args, **kwargs)
        return HttpResponse(schjson.json_dumps(v), content_type="application/json")
    return inner


def dict_to_xml(func):
    def inner(request, *args, **kwargs):
        v = func(request, *args, **kwargs)
        if type(v)=='str':
            return HttpResponse(v, content_type="application/xhtml+xml")
        else:
            return HttpResponse(serializers.serialize("xml", v), content_type="application/xhtml+xml")
    return inner
