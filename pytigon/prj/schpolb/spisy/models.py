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







TypRaportu = (
    ("1","są w Softlabie brak w AD"),
    ("2","są w AD brak w Softlabie"),
    ("3","brak kart uprawnień"),
    ("4","są w AD bez komputera"),
    ("5","są w AD, nie są pracownikami"),
    
    )




class UserAD( models.Model):
    
    class Meta:
        verbose_name = _("AD user")
        verbose_name_plural = _("AD users")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'spisy'


        ordering = ['id']
        
        
    

    loginname = models.CharField('Login name', null=False, blank=False, editable=True, max_length=64)
    employee_id = models.CharField('Employee ID', null=True, blank=True, editable=True, max_length=64)
    nazwisko_imie = models.CharField('Nazwisko i imię', null=False, blank=False, editable=True, max_length=64)
    dzial = models.CharField('Dział', null=True, blank=True, editable=True, max_length=64)
    lokalizacja = models.CharField('Lokalizacja', null=True, blank=True, editable=True, max_length=64)
    mail = models.CharField('Mail', null=True, blank=True, editable=True, max_length=64)
    szef = models.CharField('Szef', null=True, blank=True, editable=True, max_length=64)
    adres = models.CharField('Adres', null=True, blank=True, editable=True, max_length=64)
    tel = models.CharField('Telefon', null=True, blank=True, editable=True, max_length=32)
    tytul = models.CharField('Tytuł', null=True, blank=True, editable=True, max_length=64)
    data_start = models.DateField('Data założenia', null=True, blank=True, editable=True, )
    aktywny = models.BooleanField('Aktywny', null=False, blank=False, editable=True, default=False,)
    

    def __str__(self):
        return self.nazwisko_imie
    
    def dzial_softlab(self):
        objects = UserSoftlab.objects.filter(loginname = self.loginname)
        if len(objects)==1:
            return objects[0].dzial
        else:
            return ""
        
    def grupa(self):
        objects = UserSoftlab.objects.filter(loginname = self.loginname)
        if len(objects)==1:
            return objects[0].grupa
        else:
            return ""
    
    def oddzial(self):
        objects = UserSoftlab.objects.filter(loginname = self.loginname)
        if len(objects)==1:
            return objects[0].oddzial
        else:
            return ""
    
admin.site.register(UserAD)


class UserSoftlab( models.Model):
    
    class Meta:
        verbose_name = _("Softlab user")
        verbose_name_plural = _("Softab users")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'spisy'


        ordering = ['id']
        
        
    

    oldloginname = models.CharField('Stary login name', null=False, blank=False, editable=True, max_length=64)
    loginname = models.CharField('Login name', null=False, blank=False, editable=True, max_length=64)
    nazwisko_imie = models.CharField('Nazwisko i imię', null=False, blank=False, editable=True, max_length=64)
    domena = models.CharField('Domena', null=False, blank=False, editable=True, max_length=64)
    ostatnie_logowanie = models.DateField('Ostatnie logowanie', null=False, blank=False, editable=True, )
    ostatni_komputer = models.CharField('Ostatni komputer', null=False, blank=False, editable=True, max_length=64)
    aktywny = models.BooleanField('Aktywny', null=False, blank=False, editable=True, default=False,)
    dzial = models.CharField('Dział', null=True, blank=True, editable=True, max_length=64)
    grupa = models.CharField('Grupa', null=True, blank=True, editable=True, max_length=64)
    oddzial = models.CharField('Oddział', null=True, blank=True, editable=True, max_length=64)
    

    def __str__(self):
        return self.nazwisko_imie
        
    
admin.site.register(UserSoftlab)


class TypKomputera( models.Model):
    
    class Meta:
        verbose_name = _("Computer type")
        verbose_name_plural = _("Computer types")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'spisy'


        ordering = ['id']
        
        
    

    nazwa = models.CharField('Nazwa', null=False, blank=False, editable=True, max_length=64)
    opis = models.TextField('Opis', null=False, blank=False, editable=True, )
    

    def __str__(self):
        return self.nazwa
    
admin.site.register(TypKomputera)


class NowyKomputer( models.Model):
    
    class Meta:
        verbose_name = _("New computer")
        verbose_name_plural = _("New computers")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'spisy'


        ordering = ['id']
        
        
    

    hostname = models.CharField('Hostname', null=False, blank=False, editable=True, max_length=64)
    typ_komputera = ext_models.ForeignKey(TypKomputera, on_delete=models.CASCADE, null=False, blank=False, editable=True, verbose_name='Typ komputera', )
    uwagi = models.TextField('Uwagi', null=True, blank=True, editable=True, )
    operator = ext_models.ForeignKey(UserAD, on_delete=models.CASCADE, null=True, blank=True, editable=True, verbose_name='Operator', )
    aktywny = models.BooleanField('Aktywny', null=False, blank=False, editable=True, default=False,)
    

    def __str__(self):
        return self.hostname+"/"+self.operator.loginname
    
admin.site.register(NowyKomputer)


class StarySprzet( models.Model):
    
    class Meta:
        verbose_name = _("Old equipment")
        verbose_name_plural = _("Old equipments")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'spisy'


        ordering = ['id']
        
        
    

    nazwa = models.CharField('Nazwa', null=False, blank=False, editable=True, max_length=64)
    opis = models.TextField('Opis', null=True, blank=True, editable=True, )
    do_sprzedania = models.BooleanField('Do sprzedania', null=False, blank=False, editable=True, default=False,)
    zafakturowany = models.BooleanField('Zafakturowany', null=False, blank=False, editable=True, default=False,)
    zgoda_na_sprzedaz = models.BooleanField('Zgodna na sprzedaż', null=False, blank=False, editable=True, default=False,)
    operator = ext_models.ForeignKey(UserAD, on_delete=models.CASCADE, null=True, blank=True, editable=True, verbose_name='Operator', related_name='operator_staregosprzetu')
    

    
admin.site.register(StarySprzet)


class Lokalizacja( models.Model):
    
    class Meta:
        verbose_name = _("Location")
        verbose_name_plural = _("Locations")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'spisy'


        ordering = ['id']
        
        
    

    

    
admin.site.register(Lokalizacja)


class Switch( models.Model):
    
    class Meta:
        verbose_name = _("Switch")
        verbose_name_plural = _("Switches")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'spisy'


        ordering = ['id']
        
        
    

    

    
admin.site.register(Switch)


class WAN( models.Model):
    
    class Meta:
        verbose_name = _("WAN")
        verbose_name_plural = _("WAN")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'spisy'


        ordering = ['id']
        
        
    

    

    
admin.site.register(WAN)


class WiFi( models.Model):
    
    class Meta:
        verbose_name = _("WiFi")
        verbose_name_plural = _("WiFi")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'spisy'


        ordering = ['id']
        
        
    

    

    
admin.site.register(WiFi)


class CentralaTel( models.Model):
    
    class Meta:
        verbose_name = _("Telephone exchange")
        verbose_name_plural = _("Telephone exchanges")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'spisy'


        ordering = ['id']
        
        
    

    

    
admin.site.register(CentralaTel)


class NowaDrukarka( models.Model):
    
    class Meta:
        verbose_name = _("New printer")
        verbose_name_plural = _("New printers")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'spisy'


        ordering = ['id']
        
        
    

    

    
admin.site.register(NowaDrukarka)


class UserPolbruk( models.Model):
    
    class Meta:
        verbose_name = _("UserPolbruk")
        verbose_name_plural = _("UserPolbruk")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'spisy'


        ordering = ['id']
        
        
    

    loginname = models.CharField('Login name', null=False, blank=False, editable=True, unique=True,max_length=64)
    imie = models.CharField('Imię', null=False, blank=False, editable=True, max_length=64)
    nazwisko = models.CharField('Nazwisko', null=False, blank=False, editable=True, max_length=64)
    oddz = models.CharField('Oddział', null=True, blank=True, editable=True, max_length=64)
    dzial = models.CharField('Dział', null=True, blank=True, editable=True, max_length=64)
    

    
admin.site.register(UserPolbruk)




