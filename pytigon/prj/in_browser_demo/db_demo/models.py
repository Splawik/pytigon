import os, os.path
import sys

import django
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib import admin

from pytigon_lib.schdjangoext.fields import *
import pytigon_lib.schdjangoext.fields as ext_models
from pytigon_lib.schdjangoext.models import *
from pytigon_lib.schtools import schjson
from pytigon_lib.schhtml.htmltools import superstrip


class Teest(models.Model):

    class Meta:
        verbose_name = _("Test")
        verbose_name_plural = _("Tests")
        default_permissions = ("add", "change", "delete", "view", "list", "administer")
        app_label = "db_demo"

        ordering = ["id"]

    description = models.CharField(
        "Description", null=False, blank=False, editable=True, max_length=256
    )


admin_register(Teest)
