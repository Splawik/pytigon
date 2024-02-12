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


from datetime import datetime


class Log(AssociatedModel):

    class Meta:
        verbose_name = _("Log")
        verbose_name_plural = _("Logi")
        default_permissions = ("add", "change", "delete", "view", "list", "administer")
        app_label = "schlog"

        ordering = ["id"]

        permissions = [
            ("admin_log", "Can administer logs"),
        ]

    date = models.DateTimeField(
        "Date",
        null=True,
        blank=True,
        editable=False,
        default=timezone.now,
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
    def filter(cls, value, view=None, request=None):
        if value:
            app, tbl, id, grp = value.split("__")
            return cls.objects.filter(
                application=app, table=tbl, parent_id=id, group=grp
            )
        else:
            return cls.objects.all()

    def init_new(self, request, view, value=None):
        if value:
            app, tbl, id, grp = value.split("__")
            return {"application": app, "table": tbl, "parent_id": id, "group": grp}
        else:
            return {
                "application": "default",
                "table": "default",
                "parent_id": 0,
                "group": "default",
            }


admin.site.register(Log)
