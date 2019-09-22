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







Rok_CHOICES = (
    ("2015","2015"),
    ("2016","2016"),
    ("2017","2017"),
    ("2018","2018"),
    
    )

Miesiac_CHOICES = (
    ("01","01"),
    ("02","02"),
    ("03","03"),
    ("04","04"),
    ("05","05"),
    ("06","06"),
    ("07","07"),
    ("08","08"),
    ("09","09"),
    ("10","10"),
    ("11","11"),
    ("12","12"),
    
    )

PhotoType_CHOICES = (
    ("1","Wjazd"),
    ("0","Wyjazd"),
    
    )

PhotoStatus_CHOICES = (
    ("0","Nierozpoznany"),
    ("1","OK"),
    
    )

LoadTruckStatus_CHOICES = (
    ("1","OK"),
    ("0","Błąd rozpoznania"),
    ("2","Rozpoznanie niepewne"),
    
    )




class Config( models.Model):
    
    class Meta:
        verbose_name = _("Config")
        verbose_name_plural = _("Config")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'produkcja'


        ordering = ['id']
        
        
    

    nr_oddz = models.IntegerField('Numer oddziału', null=False, blank=False, editable=True, )
    nazwa = models.CharField('Nazwa oddziału', null=False, blank=False, editable=True, max_length=64)
    email_to = models.EmailField('Email to', null=False, blank=False, editable=True, )
    gniazda = models.CharField('Gniazda', null=False, blank=False, editable=True, max_length=64)
    p1 = models.CharField('Pożądane g netto t / rbh', null=True, blank=True, editable=True, max_length=16)
    p2 = models.CharField('Pożądana ilość niepierwszego gat', null=False, blank=False, editable=True, max_length=16)
    p3 = models.CharField('Premia przy wykonaniu 100% założeń', null=False, blank=False, editable=True, max_length=16)
    p4 = models.CharField('Korekta premii za 1% wyrobienia', null=False, blank=False, editable=True, max_length=16)
    p5 = models.CharField('Korekta premii za 1% niepierwszgo gat', null=False, blank=False, editable=True, max_length=16)
    p6 = models.CharField('Premia remontowa', null=False, blank=False, editable=True, max_length=16)
    p7 = models.CharField('Wyrobienie od którego zwiększa się stawka premii', null=False, blank=False, editable=True, max_length=16)
    p8 = models.CharField('Średnia ilość godzin netto teoretycznych/ mc', null=False, blank=False, editable=True, max_length=16)
    

    
admin.site.register(Config)


class TruckPhotos( models.Model):
    
    class Meta:
        verbose_name = _("Fotografia ciezarowki")
        verbose_name_plural = _("Fotografie ciezarowek")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'produkcja'


        ordering = ['id']
        
        
    

    location_id = models.CharField('Numer oddziału', null=True, blank=True, editable=True, max_length=16)
    pfoto_type = models.CharField('Typ fotografii', null=True, blank=True, editable=True, choices=PhotoType_CHOICES,max_length=64)
    camera_name = models.CharField('Nazwa kamery', null=True, blank=True, editable=True, max_length=32)
    date = models.DateTimeField('Data', null=True, blank=True, editable=True, )
    registration_no = models.CharField('Nr rejestracji', null=True, blank=False, editable=True, max_length=16)
    photo_path = models.CharField('Folder fotografii na ftp', null=True, blank=True, editable=True, max_length=256)
    photo_status = models.CharField('Status fotografii', null=True, blank=True, editable=True, choices=PhotoStatus_CHOICES,max_length=64)
    

    
admin.site.register(TruckPhotos)


class TimeLoadTruck( models.Model):
    
    class Meta:
        verbose_name = _("Czas zaladunku ciezarowki")
        verbose_name_plural = _("Czasy zaladunku ciezarowek")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'produkcja'


        ordering = ['id']
        
        
    

    location_id = models.CharField('Numer oddziału', null=True, blank=True, editable=True, max_length=16)
    date_in = models.DateTimeField('Data wjazdu', null=True, blank=True, editable=True, )
    date_out = models.DateTimeField('Data wyjazdu', null=True, blank=True, editable=True, )
    registration_no = models.CharField('Nr rejestracyjny', null=True, blank=True, editable=True, max_length=16)
    wz = models.CharField('Numer WZ', null=True, blank=False, editable=True, max_length=64)
    load_truck_status = models.CharField('Status załadunku', null=True, blank=True, editable=True, choices=LoadTruckStatus_CHOICES,max_length=64)
    

    
admin.site.register(TimeLoadTruck)


class TruckConfig( models.Model):
    
    class Meta:
        verbose_name = _("Konfiguracja monitorowania ciezarowek")
        verbose_name_plural = _("Konfiguracja monitorowania ciezarowek")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'produkcja'


        ordering = ['id']
        
        
    

    name = models.CharField('Nazwa oddziału', null=False, blank=False, editable=True, max_length=64)
    location_id = models.CharField('Nr oddziału', null=False, blank=False, editable=True, max_length=16)
    ftp_sever = models.CharField('Ftp serwer', null=True, blank=True, editable=True, max_length=64)
    ftp_user = models.CharField('Ftp user', null=True, blank=True, editable=True, max_length=64)
    ftp_password = models.CharField('Ftp hasło', null=True, blank=True, editable=True, max_length=64)
    pfoto_type = models.CharField('Typ fotografii', null=True, blank=True, editable=True, choices=PhotoType_CHOICES,max_length=2)
    

    
admin.site.register(TruckConfig)




