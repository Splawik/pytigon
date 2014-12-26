#!/usr/bin/python
# -*- coding: utf-8 -*-
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation; either version 3, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.

#Pytigon - wxpython and django application framework

#author: "Slawomir Cholaj (slawomir.cholaj@gmail.com)"
#copyright: "Copyright (C) ????/2012 Slawomir Cholaj"
#license: "LGPL 3.0"
#version: "0.1a"

from datetime import date, timedelta
from django import forms
from django.db import models
from django.utils.translation import ugettext_lazy as _
import django.contrib.auth.models as auth


#class Prawa(models.Model):
#
#
#    class Meta:
#
#        permissions = ((u'OgladaniePraw',
#                       u'Prawa do ogl\xc4\x85dania praw dost\xc4\x99p\xc3\xb3w'
#                       ), (u'SporzadzaniePraw',
#                       u'Prawa do sporz\xc4\x85dzania praw dost\xc4\x99p\xc3\xb3w'
#                       ), (u'ZatwierdzaniePraw',
#                       u'Prawa do zatwierdzania praw dost\xc4\x99p\xc3\xb3w'),
#                       (u'AdministrowaniePrawami',
#                       u'Prawa do administrowania prawami dost\xc4\x99p\xc3\xb3w'
#                       ))


class FileManager(models.Model):


    class Meta:

        verbose_name = _('File manager')
        verbose_name_plural = _('File manager')


