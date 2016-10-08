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


from commander.models import *








@python_2_unicode_compatible
class Parameter( models.Model):
    
    class Meta:
        verbose_name = _("Parameter")
        verbose_name_plural = _("Parameter")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'tools'


        ordering = ['id']
        
        
    

    key = models.CharField('Key', null=False, blank=False, editable=True, max_length=64)
    value = models.CharField('Value', null=False, blank=False, editable=True, max_length=64)
    

    
admin.site.register(Parameter)


@python_2_unicode_compatible
class Autocomplete( models.Model):
    
    class Meta:
        verbose_name = _("Autocomplete")
        verbose_name_plural = _("Autocomplete")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'tools'


        ordering = ['id']
        
        
    

    type = models.CharField('Type', null=False, blank=False, editable=True, max_length=64)
    label = models.CharField('Label', null=False, blank=False, editable=True, max_length=64)
    value = models.TextField('Value', null=False, blank=False, editable=True, )
    

    
admin.site.register(Autocomplete)




