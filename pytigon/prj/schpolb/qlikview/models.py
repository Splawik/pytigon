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








class qlik_klient( models.Model):
    
    class Meta:
        verbose_name = _("qlik_klient")
        verbose_name_plural = _("qlik_klient")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'qlikview'


        ordering = ['id']
        
        
    

    FIRMA_ID = models.CharField('FIRMA_ID', null=False, blank=False, editable=False, max_length=16)
    LogoP = models.CharField('LogoP', null=True, blank=True, editable=True, max_length=16)
    NazwaP = models.CharField('NazwaP', null=True, blank=True, editable=True, max_length=128)
    Logo = models.CharField('Logo', null=False, blank=False, editable=False, max_length=16)
    Nazwa = models.CharField('Nazwa', null=False, blank=False, editable=False, max_length=128)
    Segment = models.CharField('Segment', null=True, blank=True, editable=False, max_length=64)
    Segment_2 = models.CharField('Segment_2', null=True, blank=True, editable=False, max_length=64)
    KlasABC = models.CharField('KlasABC', null=True, blank=True, editable=False, max_length=64)
    OsFizyczna = ext_models.NullBooleanField('OsFizyczna', null=True, blank=True, editable=True, )
    KodP = models.CharField('KodP', null=True, blank=True, editable=True, max_length=16)
    Miasto = models.CharField('Miasto', null=True, blank=True, editable=True, max_length=128)
    Powiat = models.CharField('Powiat', null=True, blank=True, editable=True, max_length=64)
    

    
admin.site.register(qlik_klient)


class qlik_kar( models.Model):
    
    class Meta:
        verbose_name = _("qlik_kar")
        verbose_name_plural = _("qlik_kar")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'qlikview'


        ordering = ['id']
        
        
    

    FIRMA_ID = models.CharField('FIRMA_ID', null=False, blank=False, editable=True, max_length=16)
    SymKar = models.CharField('SymKar', null=False, blank=False, editable=True, max_length=32)
    SymKar2 = models.CharField('SymKar2', null=False, blank=False, editable=True, max_length=32)
    Cecha = models.CharField('Cecha', null=True, blank=True, editable=True, max_length=32)
    Firma = models.CharField('Firma', null=False, blank=False, editable=True, max_length=32)
    FirmaLokalizacja = models.CharField('FirmaLokalizacja', null=True, blank=True, editable=True, max_length=64)
    GrupaCen = models.CharField('GrupaCen', null=False, blank=False, editable=True, max_length=32)
    NazwaProdukt = models.CharField('NazwaProdukt', null=False, blank=False, editable=True, max_length=128)
    NazwaProdukt2 = models.CharField('NazwaProdukt2', null=True, blank=True, editable=True, max_length=128)
    Gatunek = models.CharField('Gatunek', null=False, blank=False, editable=True, max_length=32)
    GrupaCenNazwa = models.CharField('GrupaCenNazwa', null=True, blank=True, editable=True, max_length=128)
    GrupaAsortymentuNazwa = models.CharField('GrupaAsortymentuNazwa', null=True, blank=True, editable=True, max_length=64)
    RodzajHandlowy = models.CharField('RodzajHandlowy', null=True, blank=True, editable=True, max_length=32)
    TypProduktu = models.CharField('TypProduktu', null=False, blank=False, editable=True, max_length=32)
    TypProduktuOpis = models.CharField('TypProduktuOpis', null=True, blank=True, editable=True, max_length=64)
    pd_S1 = models.CharField('pd_S1', null=True, blank=True, editable=True, max_length=128)
    pd_S2 = models.CharField('pd_S2', null=True, blank=True, editable=True, max_length=128)
    pd_S3 = models.CharField('pd_S3', null=True, blank=True, editable=True, max_length=128)
    pd_S4 = models.CharField('pd_S4', null=True, blank=True, editable=True, max_length=128)
    pd_S5 = models.CharField('pd_S5', null=True, blank=True, editable=True, max_length=128)
    pd_S6 = models.CharField('pd_S6', null=True, blank=True, editable=True, max_length=128)
    pd_S7 = models.CharField('pd_S7', null=True, blank=True, editable=True, max_length=128)
    pd_S8 = models.CharField('pd_S8', null=True, blank=True, editable=True, max_length=128)
    pd_S9 = models.CharField('pd_S9', null=True, blank=True, editable=True, max_length=128)
    pd_S10 = models.CharField('pd_S10', null=True, blank=True, editable=True, max_length=128)
    CenaDetal = models.DecimalField('CenaDetal', null=True, blank=True, editable=True, max_digits=11, decimal_places=2)
    TKW_SUR = models.DecimalField('TKW_SUR', null=True, blank=True, editable=True, max_digits=11, decimal_places=2)
    TKW_ROB = models.DecimalField('TKW_ROB', null=True, blank=True, editable=True, max_digits=11, decimal_places=2)
    TKW_ADM = models.DecimalField('TKW_ADM', null=True, blank=True, editable=True, max_digits=11, decimal_places=2)
    TKW_ZMIEN = models.DecimalField('TKW_ZMIEN', null=True, blank=True, editable=True, max_digits=11, decimal_places=2)
    TKW_AMOR = models.DecimalField('TKW_AMOR', null=True, blank=True, editable=True, max_digits=11, decimal_places=2)
    TKW_DOS = models.DecimalField('TKW_DOS', null=True, blank=True, editable=True, max_digits=11, decimal_places=2)
    Kolor = models.CharField('Kolor', null=True, blank=True, editable=True, max_length=32)
    

    
admin.site.register(qlik_kar)


class qlik_handlowiec( models.Model):
    
    class Meta:
        verbose_name = _("qlik_handlowiec")
        verbose_name_plural = _("qlik_handlowiec")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'qlikview'


        ordering = ['id']
        
        
    

    FIRMA_ID = models.CharField('FIRMA_ID', null=False, blank=False, editable=True, max_length=16)
    LogoH = models.CharField('LogoH', null=False, blank=False, editable=True, max_length=16)
    NazwaH = models.CharField('NazwaH', null=False, blank=False, editable=True, max_length=32)
    Region = models.CharField('Region', null=True, blank=True, editable=True, max_length=32)
    

    
admin.site.register(qlik_handlowiec)


class qlik_dok( models.Model):
    
    class Meta:
        verbose_name = _("qlik_dok")
        verbose_name_plural = _("qlik_dok")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'qlikview'


        ordering = ['id']
        
        
    

    FIRMA_ID = models.CharField('FIRMA_ID', null=False, blank=False, editable=True, max_length=16)
    NumerDok = models.CharField('NumerDok', null=False, blank=False, editable=True, max_length=32)
    DataPlat = models.DateField('DataPlat', null=True, blank=True, editable=True, )
    DataSprz = models.DateField('DataSprz', null=True, blank=True, editable=True, )
    Logo = models.CharField('Logo', null=False, blank=False, editable=True, max_length=16)
    LogoH = models.CharField('LogoH', null=False, blank=False, editable=True, max_length=16)
    SymKar = models.CharField('SymKar', null=False, blank=False, editable=True, max_length=32)
    JM = models.CharField('JM', null=False, blank=False, editable=True, max_length=16)
    IloscMgPrzel = models.DecimalField('IloscMgPrzel', null=False, blank=False, editable=True, max_digits=11, decimal_places=2)
    Ilosc = models.DecimalField('Ilosc', null=False, blank=False, editable=True, max_digits=11, decimal_places=2)
    Brutto = models.DecimalField('Brutto', null=False, blank=False, editable=True, max_digits=11, decimal_places=2)
    Netto = models.DecimalField('Netto', null=False, blank=False, editable=True, max_digits=11, decimal_places=2)
    WartoscExWorks = models.DecimalField('WartoscExWorks', null=True, blank=True, editable=True, max_digits=11, decimal_places=2)
    TypPlat = models.CharField('TypPlat', null=True, blank=True, editable=True, max_length=16)
    SymRej = models.CharField('SymRej', null=True, blank=True, editable=True, max_length=32)
    SymWl = models.CharField('SymWl', null=True, blank=True, editable=True, max_length=16)
    MagSprz = models.CharField('MagSprz', null=False, blank=False, editable=True, max_length=16)
    MagProd = models.CharField('MagProd', null=True, blank=True, editable=True, max_length=16)
    

    
admin.site.register(qlik_dok)


class qlik_mm( models.Model):
    
    class Meta:
        verbose_name = _("qlik_mm")
        verbose_name_plural = _("qlik_mm")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'qlikview'


        ordering = ['id']
        
        
    

    FIRMA_ID = models.CharField('FIRMA_ID', null=False, blank=False, editable=True, max_length=16)
    MagProd = models.CharField('MagProd', null=False, blank=False, editable=True, max_length=16)
    MagSprz = models.CharField('MagSprz', null=False, blank=False, editable=True, max_length=16)
    Odleglosc = models.FloatField('Odległość', null=False, blank=False, editable=True, )
    SymKar2 = models.CharField('SymKar2', null=False, blank=False, editable=True, max_length=32)
    KosztMM = models.DecimalField('Koszt MM', null=False, blank=False, editable=True, max_digits=11, decimal_places=6)
    IloscMGPrzel = models.DecimalField('IloscMGPrzel', null=False, blank=False, editable=True, max_digits=11, decimal_places=6)
    

    
admin.site.register(qlik_mm)


class qlik_lokalizacje( models.Model):
    
    class Meta:
        verbose_name = _("qlik_lokalizacje")
        verbose_name_plural = _("qlik_lokalizacje")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'qlikview'


        ordering = ['id']
        
        
    

    FIRMA_ID = models.CharField('FIRMA_ID', null=False, blank=False, editable=True, max_length=16)
    MagSprz = models.CharField('MagSprz', null=False, blank=False, editable=True, max_length=16)
    Opis = models.CharField('Opis', null=False, blank=False, editable=True, max_length=64)
    Region = models.CharField('Region', null=False, blank=False, editable=True, max_length=32)
    

    
admin.site.register(qlik_lokalizacje)


class qlik_segmentacja( models.Model):
    
    class Meta:
        verbose_name = _("qlik_segmentacja")
        verbose_name_plural = _("qlik_segmentacja")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'qlikview'


        ordering = ['id']
        
        
    

    LogoP = models.CharField('LogoP', null=False, blank=False, editable=True, max_length=16)
    FIRMA_ID = models.CharField('FIRMA_ID', null=False, blank=False, editable=True, max_length=16)
    Klastrowanie_BEH_FD = models.CharField('Klastrowanie_BEH_FD', null=True, blank=True, editable=True, max_length=64)
    Klastrowanie_VAL_FD = models.CharField('Klastrowanie_VAL_FD', null=True, blank=True, editable=True, max_length=64)
    Klastrowanie_BEH_Hurtownie = models.CharField('Klastrowanie_BEH_Hurtownie', null=True, blank=True, editable=True, max_length=64)
    Klastrowanie_VAL_Hurtownie = models.CharField('Klastrowanie_VAL_Hurtownie', null=True, blank=True, editable=True, max_length=64)
    Segment_2 = models.CharField('Segment_2', null=False, blank=False, editable=True, max_length=64)
    

    
admin.site.register(qlik_segmentacja)


class qlik_grupa_asortyment( models.Model):
    
    class Meta:
        verbose_name = _("qlik_grupa_asortyment")
        verbose_name_plural = _("qlik_grupa_asortyment")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'qlikview'


        ordering = ['id']
        
        
    

    FIRMA_ID = models.CharField('FIRMA_ID', null=False, blank=False, editable=True, max_length=16)
    GrupaAsortymentuNazwa = models.CharField('GrupaAsortymentuNazwa', null=False, blank=False, editable=True, max_length=64)
    GrupaAsortymentuNazwa2 = models.CharField('GrupaAsortymentuNazwa2', null=False, blank=False, editable=True, max_length=64)
    

    
admin.site.register(qlik_grupa_asortyment)


class qlik_firmy( models.Model):
    
    class Meta:
        verbose_name = _("qlik_firmy")
        verbose_name_plural = _("qlik_firmy")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'qlikview'


        ordering = ['id']
        
        
    

    FIRMA_ID = models.CharField('FIRMA_ID', null=False, blank=False, editable=True, max_length=16)
    Opis = models.CharField('Opis', null=False, blank=False, editable=True, max_length=64)
    

    
admin.site.register(qlik_firmy)




