import django
from django.db import models
from django.utils import timezone

from pytigon_lib.schdjangoext.fields import *
from pytigon_lib.schdjangoext.models import *
import pytigon_lib.schdjangoext.fields as ext_models
from pytigon_lib.schtools import schjson

from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from django.utils import timezone

import os, os.path
import sys
from pytigon_lib.schhtml.htmltools import superstrip


class Parameter(models.Model):

    class Meta:
        verbose_name = _("Parameter")
        verbose_name_plural = _("Parameter")
        default_permissions = ("add", "change", "delete", "view", "list", "administer")
        app_label = "schtools"

        ordering = ["id"]

        permissions = [
            ("admin_parameter", "Can administer parameters"),
        ]

    type = models.CharField(
        "Parameter type",
        null=True,
        blank=True,
        editable=True,
        db_index=True,
        max_length=16,
    )
    subtype = models.CharField(
        "Parameter subtype",
        null=True,
        blank=True,
        editable=True,
        db_index=True,
        max_length=16,
    )
    key = models.CharField(
        "Key", null=False, blank=False, editable=True, db_index=True, max_length=64
    )
    value = models.CharField(
        "Value", null=False, blank=False, editable=True, max_length=64
    )

    @classmethod
    def get_dict(cls, type, subtype):
        d = {}
        object_list = cls.objects.filter(type=type, subtype=subtype)
        for obj in object_list:
            d[obj.key] = obj.value
        return d


admin.site.register(Parameter)


class Autocomplete(models.Model):

    class Meta:
        verbose_name = _("Autocomplete")
        verbose_name_plural = _("Autocomplete")
        default_permissions = ("add", "change", "delete", "view", "list", "administer")
        app_label = "schtools"

        ordering = ["id"]

    type = models.CharField(
        "Type", null=False, blank=False, editable=True, db_index=True, max_length=64
    )
    label = models.CharField(
        "Label", null=False, blank=False, editable=True, db_index=True, max_length=64
    )
    value = models.TextField(
        "Value",
        null=False,
        blank=False,
        editable=True,
    )


admin.site.register(Autocomplete)
