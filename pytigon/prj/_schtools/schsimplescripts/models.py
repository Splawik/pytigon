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


import datetime
from pytigon_lib.schdjangoext.django_ihtml import ihtml_to_html
from schsimplescripts.script_tools import decode_script


class Scripts(models.Model):
    class Meta:
        verbose_name = _("Scripts")
        verbose_name_plural = _("Scripts")
        default_permissions = ("add", "change", "delete", "list")
        app_label = "schsimplescripts"

        ordering = ["id"]

    name = models.CharField(
        "Name", null=False, blank=False, editable=True, max_length=64
    )
    title = models.CharField(
        "Title", null=True, blank=True, editable=True, max_length=64
    )
    code = models.TextField(
        "Code",
        null=True,
        blank=True,
        editable=False,
    )
    category = models.CharField(
        "Category", null=True, blank=True, editable=True, max_length=64
    )
    rights_group = models.CharField(
        "Rights group", null=True, blank=True, editable=True, max_length=64
    )
    menu = models.CharField("Menu", null=True, blank=True, editable=True, max_length=64)
    doc = models.TextField(
        "Doc",
        null=True,
        blank=True,
        editable=False,
    )
    _form = models.TextField(
        "_form",
        null=True,
        blank=True,
        editable=True,
    )
    _view = models.TextField(
        "_view",
        null=True,
        blank=True,
        editable=True,
    )
    _template = models.TextField(
        "_template",
        null=True,
        blank=True,
        editable=True,
    )

    def save(self, *args, **kwargs):
        code = self.code
        if code:
            x = decode_script(self.name, code)
            if x:
                self._form = x[0]
                self._view = x[1]
                self._template = x[2]
            else:
                code = ""

        if not code:
            self._form = ""
            self._view = ""
            self._template = ""

        super(Scripts, self).save(*args, **kwargs)


admin.site.register(Scripts)
