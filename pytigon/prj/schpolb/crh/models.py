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








class Ad( models.Model):
    
    class Meta:
        verbose_name = _("AD")
        verbose_name_plural = _("AD")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'crh'


        ordering = ['id']
        
        
    

    c = models.CharField('c', null=True, blank=True, editable=True, max_length=64)
    company = models.CharField('company', null=True, blank=True, editable=True, max_length=64)
    co = models.CharField('co', null=True, blank=True, editable=True, max_length=64)
    physicalDeliveryOfficeName = models.CharField('physicalDeliveryOfficeName', null=True, blank=True, editable=True, max_length=64)
    postalCode = models.CharField('postalCode', null=True, blank=True, editable=True, max_length=64)
    l = models.CharField('l', null=True, blank=True, editable=True, max_length=64)
    streetAddress = models.CharField('streetAddress', null=True, blank=True, editable=True, max_length=64)
    employeeID = models.CharField('employeeID', null=True, blank=True, editable=True, max_length=64)
    sAMAccountName = models.CharField('sAMAccountName', null=True, blank=True, editable=True, max_length=64)
    displayName = models.CharField('displayName', null=True, blank=True, editable=True, max_length=64)
    name = models.CharField('name', null=True, blank=True, editable=True, max_length=64)
    cn = models.CharField('cn', null=True, blank=True, editable=True, max_length=64)
    givenName = models.CharField('givenName', null=True, blank=True, editable=True, max_length=64)
    sn = models.CharField('sn', null=True, blank=True, editable=True, max_length=64)
    title = models.CharField('title', null=True, blank=True, editable=True, max_length=64)
    department = models.CharField('department', null=True, blank=True, editable=True, max_length=64)
    distinguishedName = models.CharField('distinguishedName', null=True, blank=True, editable=True, max_length=64)
    userPrincipalName = models.CharField('userPrincipalName', null=True, blank=True, editable=True, max_length=64)
    mail = models.CharField('mail', null=True, blank=True, editable=True, max_length=64)
    telephoneNumber = models.CharField('telephoneNumber', null=True, blank=True, editable=True, max_length=64)
    mobile = models.CharField('mobile', null=True, blank=True, editable=True, max_length=64)
    manager = models.CharField('manager', null=True, blank=True, editable=True, max_length=64)
    userAccountControl = models.CharField('userAccountControl', null=True, blank=True, editable=True, max_length=64)
    whenCreated = models.CharField('whenCreated', null=True, blank=True, editable=True, max_length=64)
    PwdLastSet = models.CharField('PwdLastSet', null=True, blank=True, editable=True, max_length=64)
    manager_name = models.CharField('manager_name', null=True, blank=True, editable=True, max_length=64)
    is_ok = ext_models.NullBooleanField('None', null=True, blank=True, editable=True, )
    disabled = ext_models.NullBooleanField('Disabled', null=True, blank=True, editable=True, )
    errors = models.CharField('Errors', null=True, blank=True, editable=True, max_length=256)
    active = ext_models.NullBooleanField('Active', null=False, blank=False, editable=True, )
    

    
admin.site.register(Ad)


class AgreementDoc( models.Model):
    
    class Meta:
        verbose_name = _("Agreement document")
        verbose_name_plural = _("Agreement documents")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'crh'


        ordering = ['id']
        
        
    

    name = models.CharField('Name', null=False, blank=False, editable=True, max_length=64)
    data = models.TextField('Data', null=True, blank=True, editable=False, )
    obligatory = ext_models.NullBooleanField('Obligatory', null=False, blank=False, editable=True, )
    

    
admin.site.register(AgreementDoc)


class Agreement( models.Model):
    
    class Meta:
        verbose_name = _("Agreement")
        verbose_name_plural = _("Agreements")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'crh'


        ordering = ['id']
        
        
    

    parent = ext_models.ForeignKey(Ad, on_delete=models.CASCADE, null=False, blank=False, editable=True, verbose_name='Parent', )
    doc = ext_models.ForeignKey(AgreementDoc, on_delete=models.CASCADE, null=False, blank=False, editable=True, verbose_name='Doc', )
    date = models.DateField('Date', null=False, blank=False, editable=True, )
    data = models.TextField('Data', null=False, blank=False, editable=False, )
    

    
admin.site.register(Agreement)




