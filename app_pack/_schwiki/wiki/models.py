# -*- coding: utf-8 -*-

import django
from django.db import models
from schlib.schdjangoext.fields import ForeignKey, HiddenForeignKey

from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.utils.encoding import python_2_unicode_compatible

import os, os.path
import sys
from schlib.schhtml.htmltools import superstrip




from django.template import RequestContext,Context, Template
import markdown
from schlib.schdjangoext.django_ihtml import ihtml_to_html
from schlib.schtools.wiki import wikify

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




@python_2_unicode_compatible
class Page( models.Model):
    
    class Meta:
        verbose_name = _("Page")
        verbose_name_plural = _("Page")
        default_permissions = ('add', 'change', 'delete', 'list')
        
        ordering = ['id']
        
        

    

    name = models.CharField('name', null=False, blank=False, editable=True, max_length=64)
    subject = models.CharField('subject', null=False, blank=False, editable=True, max_length=64)
    description = models.CharField('description', null=True, blank=True, editable=True, max_length=64)
    page_type = models.CharField('page_type', null=False, blank=False, editable=True, choices=page_type_choices,max_length=1)
    content_src = models.TextField('content_src', null=True, blank=True, editable=True, )
    content = models.TextField('content', null=True, blank=True, editable=True, )
    base_template = models.CharField('base_template', null=True, blank=True, editable=True, max_length=64)
    rights_group = models.CharField('rights_group', null=True, blank=True, editable=True, max_length=64)
    menu = models.CharField('Menu', null=True, blank=True, editable=True, max_length=64)
    

    def save(self, *args, **kwargs):
        if self.page_type == 'W':
            if self.content_src:
                #content = wikify(markdown.markdown(self.content_src, extensions=['tables', 'codehilite']))
                content = markdown.markdown(self.content_src, extensions=['tables', 'codehilite'])
            else:
                content = ""
            t = Template(template_content % content)
            c = Context({})
            self.content=t.render(c)
        elif self.page_type == 'I':
            #self.content = wikify(ihtml_to_html(None, self.content_src))
            self.content = ihtml_to_html(None, self.content_src)
        elif self.page_type == 'H':
            #self.content = wikify(self.content_src)
            self.content = self.content_src
    
        super(Page, self).save(*args, **kwargs) 
    
admin.site.register(Page)




