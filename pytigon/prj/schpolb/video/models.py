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








class Video( models.Model):
    
    class Meta:
        verbose_name = _("Video")
        verbose_name_plural = _("Video")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'video'


        ordering = ['id']
        
        
    

    data = models.DateField('Data publikacji', null=False, blank=False, editable=True, default=datetime.datetime.now,)
    name = models.CharField('Nazwa', null=False, blank=False, editable=True, max_length=64)
    plik = models.FileField('Plik', null=True, blank=True, editable=True, )
    

    
admin.site.register(Video)




