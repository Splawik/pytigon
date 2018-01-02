# -*- coding: utf-8 -*-

import django
from django.db import models

from schlib.schdjangoext.fields import *
from schlib.schdjangoext.models import *

import schlib.schdjangoext.fields as ext_models

from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

import os, os.path
import sys
from schlib.schhtml.htmltools import superstrip




from django.template import RequestContext,Context, Template
import markdown2 as markdown
from schlib.schdjangoext.django_ihtml import ihtml_to_html
from schlib.schtools.wiki import wikify
from schlib.schtools.tools import norm_indent
from django.template.loader import select_template
from datetime import datetime

template_content = """
{# -*- coding: utf-8 -*- #}
{%% load exfiltry %%}
{%% load exsyntax %%}
%s
"""

def _get_wiki_object(page, buf, name):
    name0 = name.split('_')[0]
    conf = None
    x = PageObjectsConf.objects.filter(name=name0)
    if len(x) > 0:
        conf = x[0]
        d = page.get_json_data()
        if name in d:
            c = d[name]
        else:
            c = ""

        inline_content = norm_indent(buf)
        if conf.inline_wiki:
            inline_content = html_from_wiki(page, inline_content)

        context = {'param': c, 'inline_content': inline_content, 'object': conf, 'page': page}
        if conf.view_dict:
            exec(conf.view_dict)
            context = locals()['get_view_dict'](context)

        template_name1 = (conf.app + "/" + conf.name).lower() + "_wikiobj_view.html"
        template_name2 = "wiki/wikiobj_view.html"

        t = select_template([template_name1, template_name2, ])

        return t.render(context).replace('[[', '{{').replace(']]', '}}').replace('[%', '{%').replace('%]',
                                                                                                     '%}')
    else:
        return ""


def _get_markdown_object(buf):
    return markdown.markdown("\n".join(buf), extras=['tables', 'codehilite'])


def html_from_wiki(page, wiki_str):
    document = []
    paragraf = []
    buf = []
    in_wiki_object = False
    name = ""

    paragraf_prefix = None
    paragraf_suffix = None
    section_close_elements = []

    def write_papragraf():
        nonlocal in_wiki_object, buf, paragraf_prefix, paragraf_suffix, document, paragraf

        if in_wiki_object:
            x = _get_wiki_object(page, buf, name)
            document.append(x)
            buf = []
        else:
            if buf:
                paragraf.append((buf, True))
                buf = []

            if paragraf:
                if paragraf_prefix:
                    x = paragraf_prefix
                else:
                    x = ""
                for pos in paragraf:
                    if pos[1]:
                        x += _get_markdown_object(pos[0])
                    else:
                        x += pos[0]

                if paragraf_suffix:
                    x += paragraf_suffix

                document.append(x)

                paragraf = []

    def write_section():
        nonlocal section_close_elements, document
        if section_close_elements:
            document.append("".join(list(reversed(section_close_elements))))
        section_close_elements = []

    lines = wiki_str.replace('\r', '').split('\n')
    for line in lines:
        if in_wiki_object:
            if line.startswith(' ') or line.startswith('\t') or not line:
                buf.append(line)
                continue
            else:
                x = _get_wiki_object(page, buf, name)

                if x.startswith('@@@'):
                    if '|||' in x:
                        y  = x[3:].split('|||')
                        paragraf_prefix = y[0]
                        paragraf_suffix = y[1]
                    else:
                        paragraf_prefix = x[3:]
                        paragraf_suffix = ""
                else:
                    if '|||' in x:
                        y = x.split('|||')
                        paragraf.append((y[0], False))
                        section_close_elements.append(y[1])
                    else:
                        paragraf.append((x, False))

                buf = []
                in_wiki_object = False

        if line.startswith('@'):
            if buf:
                #x = _get_markdown_object(buf)
                paragraf.append((buf, True))
            buf = []
            in_wiki_object = True
            name = line.split(':')[0][1:].strip()
        elif line.startswith('...') or line.startswith('+++'):
            write_papragraf()
            if line.startswith('+++'):
                write_section()
                paragraf_prefix = ""
                paragraf_suffix = ""
        else:
            buf.append(line)

    write_papragraf()
    write_section()

    return "\n".join(document)




page_type_choices = (
    ("W","Wiki"),
    ("I","Indent html"),
    ("H","Html"),
    
    )




class PageObjectsConf( models.Model):
    
    class Meta:
        verbose_name = _("Page objects configurations")
        verbose_name_plural = _("Page objects configurations")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'wiki'


        ordering = ['id']
        
        
    

    app = models.CharField('Application', null=False, blank=False, editable=True, max_length=32)
    name = models.CharField('Name', null=False, blank=False, editable=True, max_length=64)
    description = models.CharField('Description', null=True, blank=True, editable=True, max_length=128)
    inline_editing = models.NullBooleanField('Inline editing', null=False, blank=False, editable=True, default=False,)
    inline_wiki = models.NullBooleanField('Inline wiki', null=False, blank=False, editable=True, default=False,)
    edit_form = models.TextField('Edit form', null=True, blank=True, editable=False, )
    load_fun = models.TextField('Load function', null=True, blank=True, editable=False, )
    save_fun = models.TextField('Save function', null=True, blank=True, editable=False, )
    view_dict = models.TextField('Get view dict function', null=True, blank=True, editable=False, )
    doc = models.TextField('Documentaction', null=True, blank=True, editable=False, )
    

    def __str__(self):
        return self.name
    
admin.site.register(PageObjectsConf)


class Page(JSONModel):
    
    class Meta:
        verbose_name = _("Page")
        verbose_name_plural = _("Page")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'wiki'


        ordering = ['id']
        
        
    

    subject = models.CharField('Subject', null=False, blank=False, editable=True, max_length=64)
    name = models.CharField('Name', null=False, blank=False, editable=True, max_length=64)
    description = models.CharField('Description', null=True, blank=True, editable=True, max_length=64)
    content_src = models.TextField('Content source', null=True, blank=True, editable=False, )
    content = models.TextField('Content', null=True, blank=True, editable=False, )
    base_template = models.CharField('Base template', null=True, blank=True, editable=True, max_length=64)
    rights_group = models.CharField('Rights group', null=True, blank=True, editable=True, max_length=64)
    menu = models.CharField('Menu', null=True, blank=True, editable=True, max_length=64)
    operator = models.CharField('Operator', null=True, blank=True, editable=False, max_length=64)
    update_time = models.DateTimeField('Update time', null=False, blank=False, editable=False, default=datetime.now,)
    

    def save_from_request(self, request, view_type, param):
        self.operator = request.user.username
        self.update_time = datetime.now()
        self.save()
    
    def save(self, *args, **kwargs):
        if self.content_src:
            content = html_from_wiki(self, self.content_src)
        else:
            content = ""
        t = Template(template_content % content)
        c = Context({})
        self.content=t.render(c)
    
        super(Page, self).save(*args, **kwargs) 
    
    def transform_template_name(self, request, template_name):
        return "wiki/edit_wiki_content.html"
    
    def get_form(self, view, request, form_class, adding):
        return None
    
admin.site.register(Page)


class WikiConf(JSONModel):
    
    class Meta:
        verbose_name = _("Wiki config")
        verbose_name_plural = _("Wiki config")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'wiki'


        ordering = ['id']
        
        
    

    operator_or_group = models.CharField('Operator or group', null=False, blank=False, editable=True, max_length=64)
    time = models.DateTimeField('Time of publication', null=False, blank=False, editable=True, )
    copies = models.IntegerField('Number of copies', null=False, blank=False, editable=True, )
    

    
admin.site.register(WikiConf)




