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



def get_reports():
    ret = []
    for rap in Raporty.objects.all():
        ret.append([rap.name, rap.description])
    return ret




RodzajHandlowyChoices = (
    ("o1","like 'PRODUKT'"),
    ("o2","not like 'PRODUKT'"),
    ("o3","like '%'"),
    
    )

WiekowanieTypChoices = (
    ("1","Pełny"),
    ("2","Bez cech"),
    ("3","Bez cech i magazynu"),
    ("4","Tylko przewiezione"),
    
    )

RokChoices = (
    ("2014","2014"),
    ("2015","2015"),
    ("2016","2016"),
    ("2017","2017"),
    ("2018","2018"),
    ("2019","2019"),
    
    )

MiesiacChoices = (
    ("1","styczeń"),
    ("2","luty"),
    ("3","marzec"),
    ("4","kwiecień"),
    ("5","maj"),
    ("6","czerwiec"),
    ("7","lipiec"),
    ("8","sierpień"),
    ("9","wrzesień"),
    ("10","październik"),
    ("11","listopad"),
    ("12","grudzień"),
    
    )

TypMagChoices = (
    ("o1","%"),
    ("o2","MWG"),
    ("o3","MSUR"),
    ("o4","PROD"),
    ("o5","PALIWA"),
    ("o6","DEPOZYT"),
    
    )

RapOkresChoice = (
    ("1","Dzienny"),
    ("2","Tygodniowy"),
    ("3","Miesięczny"),
    ("4","Kwartalny"),
    ("5","Półroczny"),
    ("6","Roczny"),
    ("0","Nigdy"),
    ("7","Co godzinę roboczą"),
    ("8","Co godzinę"),
    ("9","Co pół godziny"),
    ("T","Test"),
    
    )

RapTypChoice = (
    ("pdf","pdf"),
    ("odf","dokument odf"),
    ("mail","treść maila"),
    ("html","html"),
    ("xlsx","arkusz xlsx"),
    
    )




class Raporty( models.Model):
    
    class Meta:
        verbose_name = _("Raporty")
        verbose_name_plural = _("Raporty")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'raporty'


        ordering = ['id']
        
        
    

    name = models.CharField('Nazwa', null=False, blank=False, editable=True, max_length=64)
    description = models.CharField('Opis', null=True, blank=True, editable=True, max_length=128)
    simple = models.BooleanField('Jako załącznik', null=False, blank=False, editable=True, default=True,)
    select = models.TextField('Select', null=False, blank=False, editable=True, )
    columns = models.CharField('Kolumny', null=False, blank=False, editable=True, max_length=1024)
    header = models.CharField('Header', null=True, blank=True, editable=True, max_length=1024)
    footer = models.CharField('Footer', null=True, blank=True, editable=True, max_length=1024)
    okres = models.CharField('Okres powtarzania', null=False, blank=False, editable=True, choices=RapOkresChoice,max_length=1)
    narast = ext_models.NullBooleanField('Narastająco', null=True, blank=True, editable=True, )
    mail = models.TextField('Mali do', null=True, blank=True, editable=True, )
    typ = models.CharField('Typ raportu', null=True, blank=True, editable=True, choices=RapTypChoice,max_length=16)
    group = models.CharField('Grupa', null=True, blank=True, editable=True, max_length=64)
    rigth_group = models.CharField('Grupa uprawnień', null=True, blank=True, editable=True, max_length=64)
    

    
admin.site.register(Raporty)


class Kwerendy( models.Model):
    
    class Meta:
        verbose_name = _("Kwerendy")
        verbose_name_plural = _("Kwerendy")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'raporty'


        ordering = ['id']
        
        
    

    name = models.CharField('Name', null=False, blank=False, editable=True, max_length=64)
    description = models.CharField('Description', null=False, blank=False, editable=True, max_length=256)
    columns = models.CharField('Kolumny', null=True, blank=True, editable=True, max_length=1024)
    select = models.TextField('Select', null=True, blank=True, editable=True, )
    

    
admin.site.register(Kwerendy)




