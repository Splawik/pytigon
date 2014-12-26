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

from django.db import models
from django.utils.translation import ugettext_lazy as _
from schlib.schmodels.fields import ForeignKeyExt
from django.contrib.auth.models import User, Group
from django.utils.encoding import python_2_unicode_compatible

person_type_choice = (('O', 'Operator'), ('E', 'Employee'), ('C', 'Customer'
                      ), ('F', 'Firm'))


@python_2_unicode_compatible
class Person(models.Model):


    class Meta:

        verbose_name = _('Person')
        verbose_name_plural = _('Person')


    class Admin:

        pass


    user = models.ForeignKey(User, unique=True)
    identifier = models.CharField(max_length=16)
    name = models.CharField(max_length=64)
    type = models.CharField(max_length=1, choices=person_type_choice,
                            editable=True)

    def __unicode__(self):
        return self.name


class Parameter(models.Model):


    class Meta:

        verbose_name = _('Parameter')
        verbose_name_plural = _('Parameter')


    class Admin:

        pass


    key = models.CharField(max_length=32)
    value = models.CharField(max_length=256)


class Autocomplete(models.Model):

    type = models.CharField(max_length=64)
    label = models.CharField(max_length=64)
    value = models.TextField(blank=True)


class ProxyUser(User):


    class Meta:

        proxy = True


class ProxyGroup(Group):


    class Meta:

        proxy = True


