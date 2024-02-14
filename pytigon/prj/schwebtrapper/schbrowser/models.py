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


class bookmarks(models.Model):

    class Meta:
        verbose_name = _("Bookmarks")
        verbose_name_plural = _("Bookmarks")
        default_permissions = ("add", "change", "delete", "view", "list", "administer")
        app_label = "schbrowser"

        ordering = ["id"]

    parent = ext_models.PtigHiddenForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        editable=True,
        verbose_name="Parent",
    )
    name = models.CharField(
        "Name", null=False, blank=False, editable=True, max_length=64
    )
    url = models.CharField("url", null=True, blank=True, editable=True, max_length=256)


admin.site.register(bookmarks)


class history(models.Model):

    class Meta:
        verbose_name = _("History")
        verbose_name_plural = _("History")
        default_permissions = ("add", "change", "delete", "view", "list", "administer")
        app_label = "schbrowser"

        ordering = ["id"]

    date = models.DateTimeField(
        "Date", null=True, blank=True, editable=True, auto_now=True
    )
    url = models.CharField(
        "url", null=False, blank=False, editable=True, max_length=256
    )


admin.site.register(history)
