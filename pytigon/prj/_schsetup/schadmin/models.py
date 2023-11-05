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


from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


class SChSetup(models.Model):
    class Meta:
        verbose_name = _("SChSetup")
        verbose_name_plural = _("SChSetups")
        default_permissions = ("can_administer", "add", "change", "delete", "list")
        app_label = "schadmin"

    # name = models.CharField(
    #    "Name", null=False, blank=False, editable=True, max_length=255
    # )


# content_type = ContentType.objects.get_for_model(SChSetup)

# permission = Permission.objects.create(
#    codename='can_administer',
#    name='Can administer',
#    content_type = content_type
# )
