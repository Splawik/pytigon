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


from django.core.mail import send_mail
from datetime import datetime
from django.conf import settings
from os.path import join


def upload_path_fun(obj, filename):
    return (
        "attachements/"
        + obj.application
        + "_"
        + obj.table
        + "_"
        + str(obj.parent_id)
        + "_"
        + obj.group
        + "_"
        + filename
    )


class Attachements(models.Model):
    class Meta:
        verbose_name = _("Attachements")
        verbose_name_plural = _("Attachements")
        default_permissions = ("add", "change", "delete", "list")
        app_label = "schattachements"

        ordering = ["id"]

    name = models.CharField("Name", null=True, blank=True, editable=True, max_length=64)
    ext = models.CharField(
        "Extension", null=True, blank=True, editable=False, max_length=64
    )
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
    thumb = models.TextField(
        "thumbnail",
        null=True,
        blank=True,
        editable=False,
    )
    upload_date = models.DateTimeField(
        "Upload date",
        null=False,
        blank=False,
        editable=False,
        default=datetime.now,
    )
    file = models.FileField(
        "Select file", null=False, blank=False, editable=True, upload_to=upload_path_fun
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

    def save(self, *args, **kwargs):
        self.ext = self.file.url.split(".")[-1].upper()
        if not self.name:
            self.name = str(self.file)
        super(Attachements, self).save(*args, **kwargs)


admin.site.register(Attachements)
