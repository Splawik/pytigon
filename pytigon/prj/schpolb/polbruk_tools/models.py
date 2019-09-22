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







SrodekLokomocji = (
    ("P","Pieszo"),
    ("R","Samochód prywatny"),
    ("S","Samochód służbowy"),
    ("A","Autobus"),
    ("C","Pociąg"),
    ("L","Samolot"),
    ("T","Taxi"),
    
    )

Status = (
    ("0","W trakcie edycji"),
    ("1","Sporządzona"),
    ("2","Zatwierdzona"),
    ("3","Zaksięgowana"),
    ("9","Zamknięta"),
    
    )




class DelegNag( models.Model):
    
    class Meta:
        verbose_name = _("Delegacja")
        verbose_name_plural = _("Delegacje")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'polbruk_tools'


        ordering = ['id']
        
        
    

    nr = models.CharField('Numer', null=True, blank=True, editable=True, max_length=64)
    operator = models.CharField('Operator', null=True, blank=True, editable=True, max_length=64)
    stanowisko = models.CharField('Stanowisko', null=False, blank=False, editable=True, max_length=64)
    przelozony = models.CharField('Przełożony', null=False, blank=False, editable=True, max_length=64)
    dokad = models.CharField('Dokąd', null=False, blank=False, editable=True, max_length=64)
    data = models.DateTimeField('Data', null=True, blank=True, editable=True, )
    data_od = models.DateTimeField('Data od', null=True, blank=True, editable=True, )
    data_do = models.DateTimeField('Data do', null=True, blank=True, editable=True, )
    opis = models.CharField('Opis', null=False, blank=False, editable=True, max_length=256)
    koszt_pkp = models.FloatField('Koszt PKP', null=True, blank=True, editable=True, )
    koszt_log = models.FloatField('Koszt lot', null=True, blank=True, editable=True, )
    koszt_inne = models.FloatField('Koszty inne', null=True, blank=True, editable=True, )
    ryczalt_ilosc_dni = models.IntegerField('Ryczałt - ilość dni', null=False, blank=False, editable=True, )
    ryczalt_stawka = models.FloatField('Ryczałt - stawka', null=True, blank=True, editable=True, )
    kilometry_ilość = models.IntegerField('Kilometrówka - ilość', null=False, blank=False, editable=True, )
    kilometr_stawka = models.FloatField('Kilometrówka - stawka', null=True, blank=True, editable=True, )
    dieta_ilosc_dni = models.IntegerField('Dieta - ilość dni', null=False, blank=False, editable=True, )
    dieta_stawka = models.FloatField('Dieta - stawka', null=True, blank=True, editable=True, )
    wyzywienie_rach = models.FloatField('Wyżywienie wg rachunków', null=True, blank=True, editable=True, )
    noclegi_rach = models.FloatField('Noclegi wg rachunków', null=True, blank=True, editable=True, )
    noclegi_ryczalt = models.FloatField('Noclegi wg ryczałtu', null=True, blank=True, editable=True, )
    inne_wydatki = models.FloatField('Inne wydatki', null=True, blank=True, editable=True, )
    noclegi_ryczalt = models.FloatField('Noclegi wg ryczałtu', null=True, blank=True, editable=True, )
    zaliczka = models.FloatField('Zaliczka', null=True, blank=True, editable=True, )
    status = models.CharField('Status', null=False, blank=False, editable=True, choices=Status,max_length=2)
    

    
admin.site.register(DelegNag)


class DelegLin( models.Model):
    
    class Meta:
        verbose_name = _("Linijka delegacji")
        verbose_name_plural = _("Linijki delegacji")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'polbruk_tools'


        ordering = ['id']
        
        
    

    skad = models.CharField('Skąd', null=False, blank=False, editable=True, max_length=64)
    dokad = models.CharField('Dokąd', null=False, blank=False, editable=True, max_length=64)
    data_od = models.DateTimeField('Data od', null=False, blank=False, editable=True, )
    data_do = models.DateTimeField('Data do', null=False, blank=False, editable=True, )
    srodek_lokomocji = models.CharField('Środek lokomocji', null=False, blank=False, editable=True, choices=SrodekLokomocji,max_length=64)
    

    
admin.site.register(DelegLin)




