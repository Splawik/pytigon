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
from django.template.loader import select_template


template_content = """
{# -*- coding: utf-8 -*- #}
{%% load exfiltry %%}
{%% load exsyntax %%}
%s
"""




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
    edit_form = models.TextField('Edit form', null=True, blank=True, editable=False, )
    load_fun = models.TextField('Load function', null=True, blank=True, editable=False, )
    save_fun = models.TextField('Save function', null=True, blank=True, editable=False, )
    view_dict = models.TextField('Get view dict function', null=True, blank=True, editable=False, )
    doc = models.TextField('Documentaction', null=True, blank=True, editable=False, )
    

    def save(self, *args, **kwargs):
        if self.content_src:
            
            def get_wiki_object(buf, name):
                name0 = name.split('_')[0]
                x=PageObjectsConf.objects.filter(name=name0)
                if len(x)>0:
                    conf = x[0]
                    d = self.get_json_data()
                    if name in d:
                        content = d[name]
                    else:
                        content = ""
                    
                    inline_content = buf
                
                context = { 'content': content, 'inline_content': inline_content }    
                if conf.view_dict:
                    exec(conf.view_dict)
                    content = locals()['get_view_dict'](context)
                        
                template_name1 = (self.app + "/" + self.name).lower()+"_wikiobj_view.html"
                template_name2 = "wiki/wikiobj_view.html"
            
                t = select_template([template_name1,template_name2,])
                c = RequestContext(request, { 'form': form, 'object': obj, 'page': page })
            
                return t.render(c)
                
            def get_markdown_object(buf):
                return markdown.markdown("\n".join(buf), extras=['tables', 'codehilite'])
                
            blocks = []
            buf = []
            level = 0
            in_wiki_object = False
            name = ""
    
            lines = self.content_src.replace('\r','').split('\n')
            for line in lines:
                if in_wiki_object:
                    if line.startswith(' ') or not line:
                        buf.append(line)
                        continue
                    else:
                        x = get_wiki_object(buf,name)
                        blocks.append(x)
                        buf = []
                        in_wiki_object = False
                        
                if line.startswith('@'):
                    if buf:
                        x = get_markdown_object(buf)
                        blocks.append(x)
                    buf = []
                    in_wiki_object = True
                    name = line.split(':')[0][1:].strip()
                else:
                    buf.append(line)
                    
            if buf:
                if in_wiki_object:
                    x = get_wiki_object(buf,name)
                else:
                    x = get_markdown_object(buf)
                blocks.append(x)
                
            content = "\n".join(blocks)
        else:
            content = ""
        t = Template(template_content % content)
        c = Context({})
        self.content=t.render(c)
    
        super(Page, self).save(*args, **kwargs) 
    
    def transform_template_name(self, request, template_name):
        return "wiki/edit_wiki_content.html"
    
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
    

    def save(self, *args, **kwargs):
        if self.content_src:
            
            def get_wiki_object(buf, name):
                name0 = name.split('_')[0]
                conf = None
                x=PageObjectsConf.objects.filter(name=name0)
                if len(x)>0:
                    conf = x[0]
                    d = self.get_json_data()
                    if name in d:
                        content = d[name]
                    else:
                        content = ""
                    
                    inline_content = buf
                
                context = { 'content': content, 'inline_content': inline_content, 'object': conf, 'page': self }    
                if conf.view_dict:
                    exec(conf.view_dict)
                    content = locals()['get_view_dict'](context)
                        
                template_name1 = (conf.app + "/" + conf.name).lower()+"_wikiobj_view.html"
                template_name2 = "wiki/wikiobj_view.html"
            
                t = select_template([template_name1,template_name2,])
            
                return t.render(context)
                
            def get_markdown_object(buf):
                return markdown.markdown("\n".join(buf), extras=['tables', 'codehilite'])
                
            blocks = []
            buf = []
            level = 0
            in_wiki_object = False
            name = ""
    
            lines = self.content_src.replace('\r','').split('\n')
            for line in lines:
                if in_wiki_object:
                    if line.startswith(' ') or not line:
                        buf.append(line)
                        continue
                    else:
                        x = get_wiki_object(buf,name)
                        blocks.append(x)
                        buf = []
                        in_wiki_object = False
                        
                if line.startswith('@'):
                    if buf:
                        x = get_markdown_object(buf)
                        blocks.append(x)
                    buf = []
                    in_wiki_object = True
                    name = line.split(':')[0][1:].strip()
                else:
                    buf.append(line)
                    
            if buf:
                if in_wiki_object:
                    x = get_wiki_object(buf,name)
                else:
                    x = get_markdown_object(buf)
                blocks.append(x)
                
            content = "\n".join(blocks)
        else:
            content = ""
        t = Template(template_content % content)
        c = Context({})
        self.content=t.render(c)
    
        super(Page, self).save(*args, **kwargs) 
    
    def transform_template_name(self, request, template_name):
        return "wiki/edit_wiki_content.html"
    
admin.site.register(Page)




