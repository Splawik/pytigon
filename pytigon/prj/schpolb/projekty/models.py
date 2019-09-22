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



from django.core.mail import send_mail
from django.contrib.auth.models import User, Permission, Group
from django.db.models import Q
from datetime import datetime

def limit_users_q(group_name):
    try:
        perm = Permission.objects.filter(codename=group_name)
        if len(perm)>0:
            id = len(perm) -1
            return Q(groups__permissions=perm[id])
        else:
            return Q()
    except Exception as e:
        print("Error:", e)
        return Q()

def limit_users_change_etapprojektuinw():
    return limit_users_q('change_etapprojektuinw')

def limit_users_change_projektinw():
    return limit_users_q('change_projektinw')

def limit_users_change_projektnawierzchni():
    return limit_users_q('change_projektnawierzchni')


def lista_projektant():
    ret =[ ['Wszystkie', 'Wszystkie' ], ['Tylko moje', 'Tylko moje'] ] 
    groups = Group.objects.filter(name='projektant')
    if len(groups)>0:
        users = groups[0].user_set.all()    
        for pos in users:
            ret.append([pos.username, pos.username])
    return ret
    



StatusProjektu = (
    ("0","Nierozpoczęty"),
    ("1","W trakcie projektowania"),
    ("2","Realizacja inwestycji"),
    ("5","Zamknięty - sukces"),
    ("9","Zamknięty - klapa"),
    
    )

StatusEtapu = (
    ("0","Nierozpoczęty"),
    ("1","W trakcie"),
    ("2","Zakończony"),
    ("3","Zatwierdzony, zamknięty"),
    
    )

TypAkcji = (
    ("K","Kontakt z klientem"),
    ("P","Przekazanie próbek"),
    ("Z","Zakończenie etapu"),
    ("0","Utworzenie wstępnej wersji projetku"),
    ("1","Utworzenie projektu"),
    ("I","Inne "),
    
    )

TypProjektu = (
    ("B","Projekt ułożenia kostki brukowej"),
    
    )

TypZdarzenia = (
    ("1","Umówione spotkanie"),
    ("2","Projektowanie zakończone"),
    ("3","Korekta"),
    ("4","Akceptacja"),
    ("5","Wysyłka"),
    ("6","Ralizacja"),
    ("7","Zlecenie zwrotu kaucji"),
    ("8","Zakup materiałów"),
    ("0","Inicjowanie"),
    
    )

TypProjektuNawierzchni = (
    ("e","e-koncept"),
    ("2","2d"),
    ("3","3d"),
    
    )

TypObiektu = (
    ("1","jednorodzinny"),
    ("K","komercyjny"),
    ("O","ogród wystawowy"),
    
    )

Region = (
    ("PN","PN"),
    ("CN","CN"),
    ("PD","PD"),
    ("ZD","ZD"),
    
    )

Asortyment = (
    ("1","1"),
    ("2","2"),
    
    )

StatusProjektuNaw = (
    ("0","Nierozpoczęty"),
    ("1","W trakcie projektowania"),
    ("2","Projektowanie zakończone"),
    ("5","Zamknięty - sukces"),
    ("9","Zamknięty - klapa"),
    ("8","Anulowany"),
    
    )

TypRaportu = (
    ("proj_naw_sumy","Projekty nawierzchni - podsumowanie"),
    
    )




class User(django.contrib.auth.models.User):
    
    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'projekty'


        ordering = ['id']
        
        proxy=True
    
admin.site.register(User)


class Asortyment( models.Model):
    
    class Meta:
        verbose_name = _("Asortyment")
        verbose_name_plural = _("Asortyment")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'projekty'


        ordering = ['id']
        
        
    

    name = models.CharField('Nazwa', null=False, blank=False, editable=True, unique=True,max_length=64)
    

    def __str__(self):
        return self.name
    
admin.site.register(Asortyment)


class BiuroProjekt( models.Model):
    
    class Meta:
        verbose_name = _("Biuro projektowe")
        verbose_name_plural = _("Biura projektowe")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'projekty'


        ordering = ['id']
        
        
    

    nazwa = models.CharField('Nazwa', null=False, blank=False, editable=True, max_length=64)
    adres = models.CharField('Adres', null=True, blank=True, editable=True, max_length=64)
    telefon = models.CharField('Nr telefonu', null=False, blank=False, editable=True, max_length=64)
    email = models.EmailField('Email', null=False, blank=False, editable=True, )
    umowa = models.CharField('Umowa projektowa', null=False, blank=False, editable=True, max_length=64)
    projektant = ext_models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, editable=True, verbose_name='Projektant', limit_choices_to=limit_users_change_etapprojektuinw,related_name='b_projekt')
    uwagi = models.CharField('Uwagi', null=False, blank=False, editable=True, max_length=64)
    

    def __str__(self):
        return self.nazwa
    
admin.site.register(BiuroProjekt)


class ProjektInw( models.Model):
    
    class Meta:
        verbose_name = _("Projekt inwestycyjny")
        verbose_name_plural = _("Projekty inwestycyjne")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'projekty'


        ordering = ['id']
        
        
    

    numer = models.CharField('Numer', null=False, blank=False, editable=True, max_length=64)
    data_start = models.DateField('Data', null=False, blank=False, editable=True, )
    gl_projektant = ext_models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, editable=True, verbose_name='Główny projektant', limit_choices_to = limit_users_change_projektinw,related_name='gl_projektant')
    projektant = ext_models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, editable=True, verbose_name='Projektant', limit_choices_to=limit_users_change_etapprojektuinw,related_name='projektant')
    szef = ext_models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, editable=True, verbose_name='Szef regionu', limit_choices_to = limit_users_change_projektinw, related_name='szef')
    opis_projektu = models.CharField('Opis projektu', null=False, blank=False, editable=True, max_length=64)
    lokalizacja = models.CharField('Lokalizacja projektu', null=False, blank=False, editable=True, max_length=64)
    biuro_proj = ext_models.ForeignKey(BiuroProjekt, on_delete=models.CASCADE, null=False, blank=False, editable=True, verbose_name='Biuro projektowe', search_fields=['nazwa__icontains',])
    inwestor = models.CharField('Inwestor', null=False, blank=False, editable=True, max_length=64)
    wykonawca = models.CharField('Generalny wykonawca', null=True, blank=True, editable=True, max_length=64)
    podwykonawca = models.CharField('Podwykonawca', null=False, blank=False, editable=True, max_length=64)
    uwagi = models.TextField('Uwagi', null=False, blank=False, editable=True, )
    nr_umowy_prow = models.CharField('Nr umowy prowizyjnej', null=False, blank=False, editable=True, max_length=64)
    material = models.CharField('Materiał', null=False, blank=False, editable=True, max_length=64)
    status = models.CharField('Status projektu', null=False, blank=False, editable=True, choices=StatusProjektu,max_length=64)
    typ_projektu = models.CharField('Typ projektu', null=False, blank=False, editable=True, choices=TypProjektu,max_length=64)
    

    def transform_form(self, request, form, is_new_form=False):
        if is_new_form:
            form.initial['gl_projektant']=request.user
        
    def save(self, *args, **kwargs):
        ret = super().save(*args, **kwargs)
        #send_mail('Subject', 'Here is the message.', 'slawomir.cholaj@crhem.pl',  ['slawomir.cholaj@gmail.com'], fail_silently=False)
        return ret
    
admin.site.register(ProjektInw)


class EtapProjektuInw( models.Model):
    
    class Meta:
        verbose_name = _("Etap ")
        verbose_name_plural = _("Etapy projektu")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'projekty'


        ordering = ['id']
        
        
    

    parent = ext_models.HiddenForeignKey(ProjektInw, on_delete=models.CASCADE, null=False, blank=False, editable=True, verbose_name='Parent', )
    projektant = ext_models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, editable=True, verbose_name='Projektant', limit_choices_to = limit_users_change_etapprojektuinw)
    opis = models.CharField('Opis', null=False, blank=False, editable=True, max_length=64)
    status = models.CharField('Status', null=False, blank=False, editable=True, default='0',choices=StatusEtapu,max_length=64)
    data_od = models.DateField('Od', null=False, blank=False, editable=True, default=datetime.now,)
    data_do = models.DateField('Do', null=False, blank=False, editable=True, default=datetime.now,)
    

    def transform_form(self, request, form, is_new_form=False):
        if is_new_form:
            form.initial['projektant']=self.parent.projektant
            
    
admin.site.register(EtapProjektuInw)


class Hurtownia( models.Model):
    
    class Meta:
        verbose_name = _("Hurtownia")
        verbose_name_plural = _("Hurtownie")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'projekty'


        ordering = ['id']
        
        
    

    nazwa = models.CharField('Nazwa', null=False, blank=False, editable=True, max_length=64)
    softlab_id = models.CharField('ID w Softlabie', null=True, blank=True, editable=True, max_length=16)
    adres = models.CharField('Adres', null=False, blank=False, editable=True, max_length=64)
    telefon = models.CharField('Telefon', null=False, blank=False, editable=True, max_length=64)
    email = models.EmailField('Email', null=True, blank=True, editable=True, )
    uwagi = models.CharField('Uwagi', null=True, blank=True, editable=True, max_length=64)
    

    def __str__(self):
        return self.nazwa
    
admin.site.register(Hurtownia)


class Akcja( models.Model):
    
    class Meta:
        verbose_name = _("Akcja")
        verbose_name_plural = _("Akcje")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'projekty'


        ordering = ['id']
        
        
    

    parent = ext_models.HiddenForeignKey(EtapProjektuInw, on_delete=models.CASCADE, null=False, blank=False, editable=True, verbose_name='Parent', )
    typ_akcji = models.CharField('Typ akcji', null=False, blank=False, editable=True, choices=TypAkcji,max_length=64)
    opis = models.CharField('Opis', null=False, blank=False, editable=True, max_length=64)
    data = models.DateField('Data', null=False, blank=False, editable=True, default=datetime.now,)
    alert = models.BooleanField('Czy przypomnieć?', null=False, blank=False, editable=True, default=False,)
    

    
admin.site.register(Akcja)


class ProjektNawierzchni( models.Model):
    
    class Meta:
        verbose_name = _("Projekt nawierzchni")
        verbose_name_plural = _("Projekty nawierzchni")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'projekty'


        ordering = ['id']
        
        
    

    numer = models.CharField('Numer projektu', null=False, blank=False, editable=True, max_length=64)
    data_prz = models.DateField('Data przyjęcia', null=False, blank=False, editable=True, )
    klient_nazwa = models.CharField('Nazwa klienta (Nazwisko i imię)', null=False, blank=False, editable=True, max_length=64)
    klient_adres = models.CharField('Adres inwestycji', null=False, blank=False, editable=True, max_length=64)
    klient_tel = models.CharField('Nr tel. klienta', null=False, blank=False, editable=True, max_length=64)
    klient_email = models.EmailField('Email klienta', null=False, blank=False, editable=True, )
    klient_uwagi = models.CharField('Dodatkowe uwagi dotyczące klienta', null=True, blank=True, editable=True, max_length=64)
    hurtownia = ext_models.ForeignKey(Hurtownia, on_delete=models.CASCADE, null=True, blank=True, editable=True, verbose_name='Hurtownia', )
    powierzchnia = models.DecimalField('Powierzchnia', null=False, blank=False, editable=True, max_digits=12, decimal_places=2)
    typ_projektu = models.CharField('Typ projektu', null=False, blank=False, editable=True, choices=TypProjektuNawierzchni,max_length=1)
    typ_obiektu = models.CharField('Typ obiektu', null=False, blank=False, editable=True, choices=TypObiektu,max_length=1)
    region = models.CharField('Region', null=False, blank=False, editable=True, choices=Region,max_length=2)
    asortymenty = models.ManyToManyField(Asortyment, null=True, blank=True, editable=True, verbose_name='Asortyment', )
    status = models.CharField('Status', null=False, blank=False, editable=True, default='0',choices=StatusProjektuNaw,max_length=1)
    projektant = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, editable=True, verbose_name='Projektant', limit_choices_to=limit_users_change_projektnawierzchni)
    

    def transform_form(self, request, form, is_new_form=False):
            if is_new_form:
                form.initial['projektant']=request.user
    
    def post(self, request):
        id = self.id
        
        self.save()
        
        x=Log()
        x.application = 'projekty'
        x.table = 'ProjektNawierzchni'
        x.group = 'default'
        x.parent_id = self.id
        x.date = datetime.now()
        if id:
            x.description = "Zmiana projektu, status: %s" % self.get_status_display()
        else:
            x.description = "Utworzenie projektu o statusie %s" % self.get_status_display()
        x.operator = request.user.username
        x.operator_id = request.user.id
        x.save()
        
        return True
    
admin.site.register(ProjektNawierzchni)


class Zdarzenie( models.Model):
    
    class Meta:
        verbose_name = _("Zdarzenie")
        verbose_name_plural = _("Zdarzenia")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'projekty'


        ordering = ['id']
        
        
    

    typ_zdarzenia = models.CharField('Typ zdarzenia', null=False, blank=False, editable=True, choices=TypZdarzenia,max_length=64)
    data = models.DateField('Data', null=False, blank=False, editable=True, )
    uwagi = models.CharField('Uwagi', null=False, blank=False, editable=True, max_length=64)
    

    
admin.site.register(Zdarzenie)




