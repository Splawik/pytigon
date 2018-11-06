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

from django.template import loader

from schlib.schdjangoext.odf_render import render_odf, render_xlsx
from schlib.schhtml.htmlviewer import stream_from_html
import os

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


    if doc_type in ('odf', 'ods'):
        template2 = []
        if 'template_name' in context:
            template2.append(context['template_name'] + '.ods')
        if ol:
            template2.append("schsys/object_list.ods")
        else:
            template2.append("schsys/object.ods")

        file_out, file_in = render_odf(template2, context)
        if file_out:
            with open(file_out, "rb") as f:
                ret_content = f.read()
            os.remove(file_out)
            ret_attr['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(file_in)
            ret_attr['Content-Type'] = 'application/vnd.oasis.opendocument.spreadsheet'

        return ret_attr, ret_content

    elif doc_type == 'xlsx':
        template2 = []
        if 'template_name' in context:
            template2.append(context['template_name'] + '.xlsx')

        if ol:
            template2.append("schsys/object_list.xlsx")
        else:
            template2.append("schsys/object.xlsx")

        if ol:
            transform_list = list(context['object_list'])
        else:
            transform_list = context['object']

        stream_out = render_xlsx(template2, transform_list)
        ret_content = stream_out.getvalue()
        ret_attr['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(template2[0])
        ret_attr['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        return ret_attr, ret_content

    elif doc_type == 'pdf':
        template2 = []
        if 'template_name' in context:
            template2.append(context['template_name'] + '_pdf.html')
        if ol:
            template2.append("schsys/object_list_pdf.html")
        else:
            template2.append("schsys/object_pdf.html")
        t = loader.select_template(template2)
        content = t.render(context)
        ret_attr['Content-Type'] = 'application/pdf'
        pdf_stream = stream_from_html(content, stream_type='pdf', base_url="file://")
        ret_content = pdf_stream.getvalue()
        return ret_attr, ret_content

    elif doc_type == 'txt':
        template2 = []
        if 'template_name' in context:
            template2.append(context['template_name'] + '_txt.html')
        if ol:
            template2.append("schsys/object_list_txt.html")
        else:
            template2.append("schsys/object_txt.html")
        t = loader.select_template(template2)
        ret_content = t.render(context)
        return ret_attr, ret_content

    else:
        template2 = []
        if 'template_name' in context:
            template2.append(context['template_name'] + '.html')
        if ol:
            template2.append("schsys/object_list.html")
        else:
            template2.append("schsys/object.html")
        t = loader.select_template(template2)
        ret_content = t.render(context)
        return ret_attr, ret_content
