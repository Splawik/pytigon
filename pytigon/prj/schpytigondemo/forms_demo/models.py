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


from schwiki.models import *

from schsimplescripts.models import *

from schlog.models import *

from schcommander.models import *

from schtools.models import *

from schreports.models import *

from schelements.models import *

from standard_components.models import *

from schprofile.models import *

from schadmin.models import *


test_choice = [
    ("1", "Test 1"),
    ("2", "Test 2"),
    ("3", "Test 3"),
    ("4", "Test 4"),
    ("5", "Test 5"),
    ("6", "Test 6"),
    ("7", "Test 7"),
    ("8", "Test 8"),
]


class Select2Example(models.Model):
    class Meta:
        verbose_name = _("Select2 example")
        verbose_name_plural = _("Select2 examples")
        default_permissions = ("add", "change", "delete", "list")
        app_label = "forms_demo"

        ordering = ["id"]

    name = models.CharField(
        "Name", null=False, blank=False, editable=True, max_length=64
    )

    def __str__(self):
        return self.name


admin.site.register(Select2Example)
