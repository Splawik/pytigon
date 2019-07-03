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

from django.template import loader, Context

from schlib.schdjangoext.spreadsheet_render import render_odf, render_xlsx
from schlib.schhtml.htmlviewer import stream_from_html
import os

def get_template_names(context, doc_type):
    ret = []
    templates = []
    if 'template_names' in context:
        t = context['template_names']
        if type(t) in (tuple, list):
            for pos in t:
                templates.append(pos)
        else:
            templates.append(t)        
    if 'object_list' in context:                
        templates.append("schsys/object_list")
    else:
        templates.append("schsys/object")

    for pos in templates:
        dtype = doc_type.replace('odf', 'ods')
        if doc_type in ('html', 'txt', 'pdf'):
            ret.append(f'{pos}_{dtype}.html')
        else:
            ret.append(f'{pos}.{dtype}')
    
    return ret


def render_doc(context):
    ret_attr = {}
    ret_content = None

    if 'doc_type' in context:
        doc_type = context['doc_type']
    else:
        doc_type = 'html'

    if 'object_list' in context:
        ol = True
    else:
        ol = False
        
    templates = get_template_names(context, doc_type)

    if doc_type in ('odf', 'ods'):
        file_out, file_in = render_odf(templates, Context(context))
        if file_out:
            with open(file_out, "rb") as f:
                ret_content = f.read()
            os.remove(file_out)
            ret_attr['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(file_in)
            ret_attr['Content-Type'] = 'application/vnd.oasis.opendocument.spreadsheet'

        return ret_attr, ret_content

    elif doc_type == 'xlsx':
        if ol:
            transform_list = list(context['object_list'])
        else:
            transform_list = context['object']

        stream_out = render_xlsx(templates, transform_list)
        ret_content = stream_out.getvalue()
        ret_attr['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(templates[0])
        ret_attr['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        return ret_attr, ret_content

    elif doc_type == 'pdf':
        t = loader.select_template(templates)
        content = ""+t.render(context)
        ret_attr['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(templates[0]).replace('.html','').replace('_pdf', '.pdf')
        ret_attr['Content-Type'] = 'application/pdf'
        pdf_stream = stream_from_html(content, stream_type='pdf', base_url="file://")
        ret_content = pdf_stream.getvalue()
        return ret_attr, ret_content

    elif doc_type == 'txt':
        ret_attr['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(templates[0]).replace('.html','').replace('_txt', '.txt')
        ret_attr['Content-Type'] = 'text/plain'
        t = loader.select_template(templates)
        ret_content = ""+t.render(context)
        return ret_attr, ret_content

    else:
        ret_attr['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(templates[0]).replace('_html', '')
        ret_attr['Content-Type'] = 'text/html'
        t = loader.select_template(templates)
        ret_content = ""+t.render(context)
        return ret_attr, ret_content
