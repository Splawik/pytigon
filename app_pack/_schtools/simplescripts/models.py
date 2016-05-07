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




import datetime
from schlib.schdjangoext.django_ihtml import ihtml_to_html





@python_2_unicode_compatible
class Scripts( models.Model):
    
    class Meta:
        verbose_name = _("Scripts")
        verbose_name_plural = _("Scripts")
        default_permissions = ('add', 'change', 'delete', 'list')
        
        ordering = ['id']
        
        
    

    name = models.CharField('Name', null=False, blank=False, editable=True, max_length=64)
    title = models.CharField('Title', null=True, blank=True, editable=True, max_length=64)
    code = models.TextField('Code', null=True, blank=True, editable=False, )
    category = models.CharField('Category', null=True, blank=True, editable=True, max_length=64)
    rights_group = models.CharField('Rights group', null=True, blank=True, editable=True, max_length=64)
    menu = models.CharField('Menu', null=True, blank=True, editable=True, max_length=64)
    doc = models.TextField('Doc', null=True, blank=True, editable=False, )
    _form = models.TextField('_form', null=True, blank=True, editable=True, )
    _view = models.TextField('_view', null=True, blank=True, editable=True, )
    _template = models.TextField('_template', null=True, blank=True, editable=True, )
    

    def _get_form_line(self, elem_type, id, title):
        if elem_type[0]=='*':
            required='True'
            elem_type = elem_type[1:]
        else:
            required='False'
            
        if elem_type[0]=='"':
            if len(elem_type==10) and elem_type[4]=='-' and elem_type[7]=='-':
                if elem_type[0]=='9':
                    return "%s=forms.DateField(label='%s', required=%s, initial=datetime.date.today)" % (id, title, required)
                else:
                    return "%s=forms.DateField(label='%s', required=%s, initial=datetime.date.today)" % (id, title, required)
            else:
                if len(elem_type)>2:
                    return "%s=forms.CharField(label='%s', required=%s, initial=%s, max_length=64)" % (id, title, required, elem_type)
                else:
                    return "%s=forms.CharField(label='%s', required=%s, max_length=64)" % (id, title, required)
                
        elif elem_type[0]>='0' and elem_type[0]<='9':
                if '.' in elem_type[0]:
                    if elem_type[0]=='0':
                        return "%s=forms.FloatField(label='%s', required=%s)" % (id, title, required)
                    else:
                        return "%s=forms.FloatField(label='%s', required=%s, initial=%s)" % (id, title, required, elem_type)
                else:
                    if elem_type[0]=='0':
                        return "%s=forms.IntegerField(label='%s', required=%s)" % (id, title, required)
                    else:
                        return "%s=forms.IntegerField(label='%s', required=%s, initial=%s)" % (id, title, required, elem_type)
        elif elem_type[0]=='|':
            return "%s=forms.ChoiceField(label='%s', required=%s, choices= [ (y, y) for y in ['%s'] ])" % (id, title, required, elem_type[1:].replace("|", "','"))
        elif elem_type[0]=='?':
            return "%s=forms.BooleanField(label='%s',required=False)" % (id, title)
        return None
    
    
    def _transform_form(self, txt):
        form = "class ScriptsForm%s(forms.Form):\n" % self.name
        for line in txt.split('\n'):
            elements = line.split(',,,')
            if len(elements)>=3:
                title=elements[0]
                id=elements[1]
                elem_type=elements[2]
                form_line = self._get_form_line(elem_type, id, title)
                if form_line:
                    form+="    "+form_line+"\n"
        return form
        
        
    def _transform_view(self, txt1, txt2):
        fun = ""
        for row in txt2.split('\n'):
            fun = fun + "    "+row+"\n"
    
        x2 = """def scripts_%s(request, argv):
    %s
    """ % (self.name, fun)
    
        return txt1+"\n"+x2
    
        
    def _transform_template(self, txt):
        return ihtml_to_html(None, txt)
        
    def save(self, *args, **kwargs):
        code = self.code
        if code:
            elements = code.split('===')
            if len(elements)>=4:
                self._form = self._transform_form(elements[0])
                self._view = self._transform_view(elements[1], elements[2])
                self._template = self._transform_template(elements[3])
            else:
                code = ""
            
        if not code:
            self._form = ""
            self._view = ""
            self._template = ""
        
        super(Scripts, self).save(*args, **kwargs) 
    
admin.site.register(Scripts)




