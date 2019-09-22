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








class CastoramaKli( models.Model):
    
    class Meta:
        verbose_name = _("Oddzial Castoramy")
        verbose_name_plural = _("Oddzialy Castoramy")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'sprzedaz'


        ordering = ['id']
        
        
    

    numer = models.CharField('Numer', null=False, blank=False, editable=True, max_length=32)
    nazwa = models.CharField('Nazwa', null=True, blank=True, editable=True, max_length=64)
    adres = models.CharField('Adres', null=True, blank=True, editable=True, max_length=64)
    mag = models.CharField('Magazyn', null=True, blank=True, editable=True, max_length=16)
    logo = models.CharField('Logo w Softlabie', null=False, blank=False, editable=True, max_length=32)
    auto = models.BooleanField('Automatyczne generowanie zamówienia', null=False, blank=False, editable=True, default=True,)
    

    
admin.site.register(CastoramaKli)


class CastoramaKar( models.Model):
    
    class Meta:
        verbose_name = _("Kartoteka Castoramy")
        verbose_name_plural = _("Kartoteki Castoramy")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'sprzedaz'


        ordering = ['id']
        
        
    

    id_castorama = models.CharField('Id w Castoramie', null=False, blank=False, editable=True, max_length=64)
    id_softlab = models.CharField('Id w Softlabie', null=False, blank=False, editable=True, max_length=64)
    nazwa_kar = models.CharField('Nazwa kartoteki', null=False, blank=False, editable=True, max_length=64)
    

    
admin.site.register(CastoramaKar)


class CastoramaLog( models.Model):
    
    class Meta:
        verbose_name = _("Castorama - log")
        verbose_name_plural = _("Castorama - log")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'sprzedaz'


        ordering = ['id']
        
        
    

    hd_id = models.CharField('Helpdesk id', null=False, blank=False, editable=True, max_length=32)
    status = models.IntegerField('Status', null=False, blank=False, editable=True, default=0,)
    description = models.CharField('Description', null=False, blank=False, editable=True, max_length=64)
    

    
admin.site.register(CastoramaLog)


class Nag( models.Model):
    
    class Meta:
        verbose_name = _("Naglowek")
        verbose_name_plural = _("Naglowki")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'sprzedaz'


        ordering = ['id']
        
        
    

    nr_zam = models.CharField('Numer zamówienia', null=False, blank=False, editable=True, max_length=64)
    data_dok = models.DateField('Data dokumentu', null=True, blank=True, editable=True, )
    lokalizacja = models.CharField('Lokalizacja', null=True, blank=True, editable=True, max_length=64)
    adres = models.CharField('Adres', null=True, blank=True, editable=True, max_length=64)
    data_dost = models.DateField('Data dostawy', null=True, blank=True, editable=True, )
    komentarz = models.CharField('Komentarz', null=True, blank=True, editable=True, max_length=256)
    nr_lok_dost = models.CharField('Numer lokalizacji dostawy', null=True, blank=True, editable=True, max_length=64)
    logo = models.CharField('Logo klienta w Softlabie', null=True, blank=True, editable=True, max_length=64)
    mag = models.CharField('Magazyn', null=False, blank=False, editable=True, max_length=16)
    status = models.CharField('Status', null=True, blank=True, editable=True, max_length=16)
    pdf_link = models.CharField('Link do pdf', null=True, blank=True, editable=True, max_length=128)
    

    
admin.site.register(Nag)


class Lin( models.Model):
    
    class Meta:
        verbose_name = _("Linijki")
        verbose_name_plural = _("Linijki")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'sprzedaz'


        ordering = ['id']
        
        
    

    parent = ext_models.ForeignKey(Nag, on_delete=models.CASCADE, null=False, blank=False, editable=True, verbose_name='Parent', )
    lp = models.IntegerField('LP', null=False, blank=False, editable=True, )
    castorama_kar = models.CharField('Nr kartoteki w Castoramie', null=True, blank=True, editable=True, max_length=64)
    symkar = models.CharField('Symbol kartoteki w Softlabie', null=True, blank=True, editable=True, max_length=64)
    opis = models.CharField('Opis', null=True, blank=True, editable=True, max_length=64)
    ilosc = models.DecimalField('Ilość', null=True, blank=True, editable=True, decimal_places=2, max_digits=11)
    cena = models.DecimalField('Cena netto', null=True, blank=True, editable=True, decimal_places=2, max_digits=11)
    jz = models.CharField('JZ', null=True, blank=True, editable=True, max_length=16)
    netto = models.DecimalField('Netto', null=True, blank=True, editable=True, decimal_places=2, max_digits=11)
    

    
admin.site.register(Lin)


class SprzedazParameter(Parameter):
    
    class Meta:
        verbose_name = _("Paremeter")
        verbose_name_plural = _("Parameters")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'sprzedaz'


        ordering = ['id']
        
        proxy=True
    
admin.site.register(SprzedazParameter)


class CastoramaRegion( models.Model):
    
    class Meta:
        verbose_name = _("Region Castoramy")
        verbose_name_plural = _("Regiony Castoramy")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'sprzedaz'


        ordering = ['id']
        
        
    

    name = models.CharField('Name', null=False, blank=False, editable=True, max_length=64)
    

    
admin.site.register(CastoramaRegion)


class CastoramaStanMag( models.Model):
    
    class Meta:
        verbose_name = _("Stan mag. Castoramy")
        verbose_name_plural = _("Stany mag. Castoramy")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'sprzedaz'


        ordering = ['id']
        
        
    

    store_id = models.IntegerField('Store id', null=False, blank=False, editable=True, )
    store_code = models.CharField('Store code', null=False, blank=False, editable=True, max_length=64)
    nazwa = models.CharField('Nazwa', null=False, blank=False, editable=True, max_length=64)
    ulica = models.CharField('Ulica', null=False, blank=False, editable=True, max_length=64)
    telefon = models.CharField('Telefon', null=False, blank=False, editable=True, max_length=32)
    qty = models.FloatField('qty', null=False, blank=False, editable=True, )
    region = models.CharField('Region', null=False, blank=False, editable=True, max_length=64)
    mag = models.CharField('Mag', null=False, blank=False, editable=True, max_length=32)
    logo = models.CharField('Logo', null=False, blank=False, editable=True, max_length=32)
    symkar = models.CharField('SymKar', null=False, blank=False, editable=True, max_length=32)
    nazwa_kar = models.CharField('Nazwa kartoteki', null=False, blank=False, editable=True, max_length=32)
    

    
admin.site.register(CastoramaStanMag)




