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



import datetime






typ_zmian = (
    ("U","Utworzenie"),
    ("P","Poprawa"),
    ("K","Kasowanie"),
    ("W","Wnioskowanie"),
    ("Z","Zatwierdzenie"),
    
    )




class LogZmian( models.Model):
    
    class Meta:
        verbose_name = _("Log zmian uprawnien")
        verbose_name_plural = _("Log zmian uprawnien")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'prawa'


        ordering = ['id']
        
        
    

    kto = models.CharField('Autor zmiany', null=False, blank=False, editable=True, max_length=64)
    kiedy = models.DateTimeField('Kiedy', null=False, blank=False, editable=True, )
    opis = models.CharField('Opis', null=True, blank=True, editable=True, max_length=1024)
    

    
admin.site.register(LogZmian)


class Lokalizacja( models.Model):
    
    class Meta:
        verbose_name = _("Lokalizacja")
        verbose_name_plural = _("Lokalizacje")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'prawa'


        ordering = ['opis', 'nazwa']
        
        
    

    nazwa = models.CharField('Nazwa', null=False, blank=False, editable=True, max_length=64)
    opis = models.CharField('Opis', null=False, blank=False, editable=True, max_length=128)
    

    def __str__(self):
        return "%s (%s)" % (self.opis, self.nazwa)
        
    
admin.site.register(Lokalizacja)


class Dzial( models.Model):
    
    class Meta:
        verbose_name = _("Dzial")
        verbose_name_plural = _("Dzialy")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'prawa'


        ordering = ['nazwa', 'opis']
        
        
    

    nazwa = models.CharField('Nazwa', null=False, blank=False, editable=True, max_length=64)
    opis = models.CharField('Opis', null=False, blank=False, editable=True, max_length=128)
    profil = models.CharField('Profil', null=True, blank=True, editable=True, max_length=64)
    

    def __str__(self):
        return "%s: %s" % (self.nazwa, self.opis)
        
    
admin.site.register(Dzial)


class GrupaPraw( models.Model):
    
    class Meta:
        verbose_name = _("Grupa praw")
        verbose_name_plural = _("Grupy praw")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'prawa'


        ordering = ['nazwa', 'opis']
        
        
    

    nazwa = models.CharField('Nazwa', null=False, blank=False, editable=True, max_length=64)
    opis = models.CharField('Opis', null=False, blank=False, editable=True, max_length=128)
    zakaz = models.ManyToManyField('self', null=True, blank=True, editable=True, verbose_name='Grupy zakazane', )
    

    def __str__(self):
        return self.nazwa + ' (' + self.opis + ')'
    
admin.site.register(GrupaPraw)


class Operator( models.Model):
    
    class Meta:
        verbose_name = _("Operator")
        verbose_name_plural = _("Operatorzy")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'prawa'


        ordering = ['nazwisko', 'imie']
        
        
    

    login = models.CharField('Login', null=False, blank=False, editable=True, max_length=64)
    imie = models.CharField('Imię', null=False, blank=False, editable=True, max_length=64)
    nazwisko = models.CharField('Nazwisko', null=False, blank=False, editable=True, max_length=64)
    lokalizacja = models.ForeignKey(Lokalizacja, on_delete=models.CASCADE, null=True, blank=True, editable=True, verbose_name='Lokalizacja', )
    dzial = models.ForeignKey(Dzial, on_delete=models.CASCADE, null=True, blank=True, editable=True, verbose_name='Dział', )
    przelozony = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, editable=True, verbose_name='Przełożony', )
    aktywny = models.BooleanField('Aktywny', null=False, blank=False, editable=True, default=True,)
    grupy = ext_models.ManyToManyFieldWidthIcon(GrupaPraw, null=True, blank=True, editable=True, verbose_name='Grupy praw', )
    

    def __str__(self):
        return "%s %s (%s)" % (self.nazwisko, self.imie, self.login)
    
    def has_attachements(self):
        x = Attachements.objects.filter(application='prawa', table='Operator', parent_id=self.id, group='potwierdzenia')
        if len(x)>0:
            return True
        else:
            return False
    
admin.site.register(Operator)


class DokPrzydzielenia( models.Model):
    
    class Meta:
        verbose_name = _("Dokument przydzielenia praw")
        verbose_name_plural = _("Dokumenty przydzielenia praw")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'prawa'


        ordering = ['id']
        
        
    

    parent = models.ForeignKey(Operator, on_delete=models.CASCADE, null=False, blank=False, editable=True, verbose_name='Operator', )
    data = models.DateField('Data', null=True, blank=True, editable=True, )
    data_przydzial = models.DateField('Data przydziału uprawnień', null=False, blank=False, editable=True, )
    grupy = models.ManyToManyField(GrupaPraw, null=True, blank=True, editable=True, verbose_name='Grupy', )
    uwagi = models.CharField('Uwagi', null=True, blank=True, editable=True, max_length=256)
    sporzadzil = models.CharField('Sporządził', null=True, blank=True, editable=True, max_length=64)
    zatwierdzil = models.CharField('Zatwierdził', null=True, blank=True, editable=True, max_length=64)
    

    def post(self, request):
        u = django.contrib.auth.get_user(request)
        uname = u.email.split('@')[0]
        oprs = Operator.objects.filter(login=uname)
        if len(oprs)==1:
            sporzadzil = oprs[0]
        else:
            sporzadzil = None
    
        if not self.sporzadzil:
            if sporzadzil:
                self.sporzadzil = sporzadzil.nazwisko + " " + sporzadzil.imie
        
        self.data = datetime.date.today()
            
        log = LogZmian()
        log.opis = "Zmiana obiektu DokPrzydzielenia: " + self.parent.nazwisko + " " + self.parent.imie + " /"+str(self.data_przydzial)    
        if self.sporzadzil:
            log.kto = sporzadzil.nazwisko + " " + sporzadzil.imie    
        log.kiedy = datetime.date.today()
        
        log.save()
        
        return True
    
            
    @staticmethod    
    def filter(f):
        if f=='niezatwierdzone':
            return DokPrzydzielenia.objects.filter(zatwierdzil='')
        else:
            tabid = f.split(',')
            tabid = map(int,tabid)
            return DokPrzydzielenia.objects.filter(id__in=tabid)
            
    def has_attachements(self):
        x = Attachements.objects.filter(application='prawa', table='DokPrzydzielenia', parent_id=self.id, group='default')
        if len(x)>0:
            return True
        else:
            return False
    
    @staticmethod
    def is_form_valid(form):
        if form.is_valid():
            x = form.cleaned_data['grupy']
            grupy = []
            zakazane = []
            for pos in x.all():
                grupy.append(pos.nazwa)
                for pos2 in pos.zakaz.all():
                    zakazane.append(pos2.nazwa)
            if any(i in zakazane for i in grupy):
                form.add_error(None, 'Zakazany zestaw grup') 
                return False
            else:
                return True
        else:
            return False
    
admin.site.register(DokPrzydzielenia)


class DokOdebrania( models.Model):
    
    class Meta:
        verbose_name = _("Dokument odebrania praw")
        verbose_name_plural = _("Dokumenty odebrania praw")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'prawa'


        ordering = ['id']
        
        
    

    parent = models.ForeignKey(Operator, on_delete=models.CASCADE, null=False, blank=False, editable=True, verbose_name='Operator', )
    data = models.DateField('Data', null=True, blank=True, editable=True, )
    data_odebrania = models.DateField('Data odebrania uprawnień', null=True, blank=True, editable=True, )
    sporzadzil = models.CharField('Sporządził', null=True, blank=True, editable=True, max_length=64)
    zatwierdzil = models.CharField('Zatwierdził', null=True, blank=True, editable=True, max_length=64)
    uwagi = models.CharField('Uwagi', null=True, blank=True, editable=True, max_length=64)
    

    def has_attachements(self):
        x = Attachements.objects.filter(application='prawa', table='DokOdebrania', parent_id=self.id, group='default')
        if len(x)>0:
            return True
        else:
            return False
    
admin.site.register(DokOdebrania)




