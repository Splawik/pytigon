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


from schwiki.models import *

from schtasks.models import *

from schcommander.models import *

from schreports.models import *








class demo_tbl( models.Model):
    
    class Meta:
        verbose_name = _("Grid table")
        verbose_name_plural = _("Grid table")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'schtabledemo'


        ordering = ['id']
        
        
    

    boolean_field = models.BooleanField('Boolean field', null=False, blank=False, editable=True, default=False,)
    char_field = models.CharField('Char field', null=True, blank=True, editable=True, max_length=64)
    date_field = models.DateField('Data field', null=True, blank=True, editable=True, )
    

    
admin.site.register(demo_tbl)




