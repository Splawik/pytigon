# -*- coding: utf-8 -*-

import django
from django.db import models

from pytigon_lib.schdjangoext.fields import *
from pytigon_lib.schdjangoext.models import *

import pytigon_lib.schdjangoext.fields as ext_models

from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

import os, os.path
import sys
from pytigon_lib.schhtml.htmltools import superstrip


from schsimplescripts.models import *

from schwiki.models import *

from schattachements.models import *

from schlog.models import *

from schtools.models import *

from schelements.models import *

from schreports.models import *



from config.models import Employee




class Proces( models.Model):
    
    class Meta:
        verbose_name = _("Proces")
        verbose_name_plural = _("Procesy")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'bhp'


        ordering = ['id']
        
        
    

    

    
admin.site.register(Proces)


class Etap( models.Model):
    
    class Meta:
        verbose_name = _("Etap")
        verbose_name_plural = _("Etapy")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'bhp'


        ordering = ['id']
        
        
    

    

    
admin.site.register(Etap)


class EventType( models.Model):
    
    class Meta:
        verbose_name = _("Event type")
        verbose_name_plural = _("Event types")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'bhp'


        ordering = ['id']
        
        
    

    group = models.CharField('Group', null=False, blank=False, editable=True, max_length=64)
    name = models.CharField('Name', null=False, blank=False, editable=True, max_length=64)
    title = models.CharField('Title', null=False, blank=False, editable=True, max_length=64)
    description = models.TextField('Description', null=False, blank=False, editable=False, )
    external_name = models.CharField('External name', null=False, blank=False, editable=True, max_length=64)
    active = ext_models.NullBooleanField('Active', null=True, blank=True, editable=True, )
    

    
admin.site.register(EventType)


class Event( models.Model):
    
    class Meta:
        verbose_name = _("Event")
        verbose_name_plural = _("Events")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'bhp'


        ordering = ['id']
        
        
    

    parent = ext_models.HiddenForeignKey(EventType, on_delete=models.CASCADE, null=False, blank=False, editable=True, verbose_name='Parent', )
    date = models.DateField('Date', null=False, blank=False, editable=True, )
    time_from = models.DateTimeField('Time from', null=True, blank=True, editable=True, )
    time_to = models.DateTimeField('Time to', null=True, blank=True, editable=True, )
    location = models.CharField('Location', null=False, blank=False, editable=True, max_length=64)
    description = models.TextField('Description', null=False, blank=False, editable=False, )
    status = models.CharField('Status', null=True, blank=True, editable=True, max_length=16)
    

    
admin.site.register(Event)


class EventUser( models.Model):
    
    class Meta:
        verbose_name = _("Event user")
        verbose_name_plural = _("Event users")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'bhp'


        ordering = ['id']
        
        
    

    parent = ext_models.HiddenForeignKey(Event, on_delete=models.CASCADE, null=False, blank=False, editable=True, verbose_name='Parent', )
    employee = ext_models.ForeignKey(Employee, on_delete=models.CASCADE, null=False, blank=False, editable=True, verbose_name='Employee', )
    time_from = models.DateTimeField('None', null=True, blank=True, editable=True, )
    time_to = models.DateTimeField('None', null=True, blank=True, editable=True, )
    result = models.FloatField('Result', null=True, blank=True, editable=True, )
    description = models.TextField('Description', null=True, blank=True, editable=True, )
    status = models.CharField('Status', null=True, blank=True, editable=True, max_length=16)
    

    
admin.site.register(EventUser)




