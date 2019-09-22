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



from prawa.models import Operator
from datetime import datetime



RepeatChoice = (
    ("1","Co miesiąc"),
    ("2","Co tydzień"),
    ("3","Codziennie"),
    ("0","Nigdy"),
    
    )

StatusChoices = (
    ("0","Nie rozpoczęte"),
    ("5","Sukces"),
    ("1","Niepowodzenie"),
    ("3","Do obserwacji"),
    
    )




class TypAudytu( models.Model):
    
    class Meta:
        verbose_name = _("Typ audytu")
        verbose_name_plural = _("Typy audytow")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'audyty'


        ordering = ['id']
        
        
    

    nazwa = models.CharField('Nazwa', null=False, blank=False, editable=True, max_length=64)
    powtarzaj = models.CharField('Powtarzaj', null=False, blank=False, editable=True, choices=RepeatChoice,max_length=64)
    ile = models.IntegerField('Ile', null=False, blank=False, editable=True, default=1,)
    sporzadza = ext_models.ForeignKey(Operator, on_delete=models.CASCADE, null=False, blank=False, editable=True, verbose_name='Sporządza', related_name='sporzadzajacy')
    zatwierdza = ext_models.ForeignKey(Operator, on_delete=models.CASCADE, null=False, blank=False, editable=True, verbose_name='Zatwierdza', related_name='zatwierdzajacy')
    template = models.TextField('Templatka', null=True, blank=True, editable=True, )
    dane = models.TextField('Dane', null=True, blank=True, editable=True, )
    opis1title = models.CharField('Tytuł opisu 1', null=True, blank=True, editable=True, max_length=64)
    opis2title = models.CharField('Tytuł opisu 2', null=True, blank=True, editable=True, max_length=64)
    opis3title = models.CharField('Tytuł opisu 3', null=True, blank=True, editable=True, max_length=64)
    copy = models.BooleanField('Czy kopiować opisy', null=False, blank=False, editable=True, default=False,)
    

    
admin.site.register(TypAudytu)


class Audyt( models.Model):
    
    class Meta:
        verbose_name = _("Audyt")
        verbose_name_plural = _("Audyty")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'audyty'


        ordering = ['id']
        
        
    

    parent = ext_models.HiddenForeignKey(TypAudytu, on_delete=models.CASCADE, null=False, blank=False, editable=True, verbose_name='Parent', )
    data = models.DateField('Data', null=False, blank=False, editable=True, )
    data_sporz = models.DateTimeField('Data sporządzenia', null=True, blank=True, editable=True, )
    data_zatw = models.DateTimeField('Data zatwierdzenia', null=True, blank=True, editable=True, )
    status = models.CharField('Staus', null=True, blank=True, editable=True, default='0',choices=StatusChoices,max_length=1)
    opis1 = models.TextField('Opis 1', null=True, blank=True, editable=True, )
    opis2 = models.TextField('Opis 2', null=True, blank=True, editable=True, )
    opis3 = models.TextField('Opis 3', null=True, blank=True, editable=True, )
    

    
admin.site.register(Audyt)


class Change( models.Model):
    
    class Meta:
        verbose_name = _("Change")
        verbose_name_plural = _("Changes")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'audyty'


        ordering = ['id']
        
        
    

    softlab_id = models.CharField('Softabl ID', null=False, blank=False, editable=True, max_length=64)
    asseco_id = models.CharField('Asseco ID', null=False, blank=False, editable=True, max_length=64)
    helpdesk_id = models.CharField('HelpDesk ID', null=False, blank=False, editable=True, max_length=64)
    description = models.CharField('Description', null=False, blank=False, editable=True, max_length=64)
    author = models.CharField('Author', null=False, blank=False, editable=True, max_length=64)
    test_ver = models.CharField('Version of test', null=False, blank=False, editable=True, max_length=64)
    test_exists = ext_models.NullBooleanField('Test exists', null=True, blank=True, editable=True, default=False,)
    tested = ext_models.NullBooleanField('Tested', null=True, blank=True, editable=True, default=False,)
    published = ext_models.NullBooleanField('Published', null=True, blank=True, editable=True, default=False,)
    create_date = models.DateField('Creating date', null=True, blank=True, editable=True, )
    pub_date = models.DateField('Date of publication', null=True, blank=True, editable=True, )
    

    
admin.site.register(Change)


class Test( models.Model):
    
    class Meta:
        verbose_name = _("Test")
        verbose_name_plural = _("Tests")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'audyty'


        ordering = ['id']
        
        
    

    softlab_comment_id = models.CharField('Softlab comment id', null=True, blank=True, editable=True, max_length=64)
    changes = ext_models.ManyToManyField(Change, null=False, blank=False, editable=True, verbose_name='Changes', )
    description = models.CharField('None', null=True, blank=True, editable=True, max_length=64)
    questions = models.TextField('Questions', null=True, blank=True, editable=False, )
    sign_count = models.IntegerField('Sign count', null=True, blank=True, editable=True, )
    finished = ext_models.NullBooleanField('Finished', null=True, blank=True, editable=True, default=False,)
    ok = ext_models.NullBooleanField('OK', null=True, blank=True, editable=True, default=False,)
    closed = ext_models.NullBooleanField('Closed', null=True, blank=True, editable=True, default=False,)
    

    
admin.site.register(Test)


class TestForUser( models.Model):
    
    class Meta:
        verbose_name = _("Test for user")
        verbose_name_plural = _("Tests for user")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'audyty'


        ordering = ['id']
        
        
    

    parent = ext_models.ForeignKey(Test, on_delete=models.CASCADE, null=False, blank=False, editable=True, verbose_name='Parent', )
    username = models.CharField('None', null=False, blank=False, editable=True, max_length=64)
    send_date = models.DateTimeField('Date of sending', null=True, blank=True, editable=True, )
    close_date = models.DateTimeField('Closing date', null=True, blank=True, editable=True, )
    finished = ext_models.NullBooleanField('Finished', null=True, blank=True, editable=True, default=False,)
    ok = ext_models.NullBooleanField('OK', null=True, blank=True, editable=True, default=False,)
    closed = ext_models.NullBooleanField('Closed', null=True, blank=True, editable=True, default=False,)
    

    
admin.site.register(TestForUser)




