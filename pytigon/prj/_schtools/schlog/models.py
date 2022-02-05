import django
from django.db import models

from pytigon_lib.schdjangoext.fields import *
from pytigon_lib.schdjangoext.models import *
import pytigon_lib.schdjangoext.fields as ext_models
from pytigon_lib.schtools import schjson

from django.utils.translation import gettext_lazy as _
from django.contrib import admin

import os, os.path
import sys
from pytigon_lib.schhtml.htmltools import superstrip


from datetime import datetime


class Log(models.Model):
    class Meta:
        verbose_name = _("Log")
        verbose_name_plural = _("Logi")
        default_permissions = ("add", "change", "delete", "list")
        app_label = "schlog"

        ordering = ["id"]

    application = models.CharField(
        "Application", null=False, blank=False, editable=False, max_length=64
    )
    table = models.CharField(
        "Table",
        null=False,
        blank=False,
        editable=False,
        default="default",
        max_length=64,
    )
    group = models.CharField(
        "Group", null=True, blank=True, editable=False, default="default", max_length=64
    )
    parent_id = models.IntegerField(
        "Parent id",
        null=True,
        blank=True,
        editable=False,
    )
    date = models.DateTimeField(
        "Date",
        null=True,
        blank=True,
        editable=False,
        default=datetime.now,
    )
    description = models.CharField(
        "Description", null=True, blank=True, editable=False, max_length=256
    )
    operator = models.CharField(
        "Operator", null=True, blank=True, editable=True, max_length=64
    )
    operator_id = models.IntegerField(
        "Operator id",
        null=True,
        blank=True,
        editable=True,
    )

    @classmethod
    def filter(cls, value):
        if value:
            app, tbl, id, grp = value.split("__")
            return cls.objects.filter(
                application=app, table=tbl, parent_id=id, group=grp
            )
        else:
            return cls.objects.all()


admin.site.register(Log)
