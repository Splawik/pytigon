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







CompanyChoice = (
    ("polbruk","Polbruk S.A."),
    
    )




class Employee( models.Model):
    
    class Meta:
        verbose_name = _("Employee")
        verbose_name_plural = _("Employees")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'config'


        ordering = ['id']
        
        
    

    surname = models.CharField('Surname', null=False, blank=False, editable=True, max_length=64)
    name = models.CharField('Name', null=False, blank=False, editable=True, max_length=64)
    email = models.EmailField('Email', null=False, blank=False, editable=True, )
    company = models.CharField('Company', null=True, blank=True, editable=True, choices=CompanyChoice,max_length=64)
    department = models.CharField('Department', null=True, blank=True, editable=True, max_length=64)
    location = models.CharField('Location', null=True, blank=True, editable=True, max_length=64)
    title = models.CharField('Title', null=True, blank=True, editable=True, max_length=64)
    external_id = models.CharField('External id', null=True, blank=True, editable=True, max_length=64)
    postalCode = models.CharField('Postal code', null=True, blank=True, editable=True, max_length=16)
    city = models.CharField('City', null=True, blank=True, editable=True, max_length=64)
    street = models.CharField('Street', null=True, blank=True, editable=True, max_length=64)
    telephoneNumber = models.CharField('Telephone number', null=True, blank=True, editable=True, max_length=32)
    mobile = models.CharField('Mobile telephone number', null=True, blank=True, editable=True, max_length=32)
    manager_name = models.CharField('Manager name', null=True, blank=True, editable=True, max_length=64)
    active = ext_models.NullBooleanField('Active', null=False, blank=False, editable=True, )
    

    
admin.site.register(Employee)




