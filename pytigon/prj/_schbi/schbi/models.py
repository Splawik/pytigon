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


from pytigon_lib.schdjangoext.import_from_db import run_code_from_db_field, ModuleStruct
from django.conf import settings
import datetime
import pyarrow
import pyarrow.parquet
import duckdb
import numpy
import os
import os.path as os_path

PROJECTS_DATA = {}
PROJECTS_DATA_VERSION = {}

REFRESH_DATA = """

"""

FORM = """

"""

VIEW = """

"""

TEMPLATE = """

"""


menu_icon_size_choice = [
    ("0", "small"),
    ("1", "medium"),
    ("2", "large"),
]


class Project(JSONModel):

    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")
        default_permissions = ("add", "change", "delete", "view", "list", "administer")
        app_label = "schbi"

        ordering = ["id"]

    base_prj_name = models.CharField(
        "Base project name", null=True, blank=True, editable=True, max_length=64
    )
    name = models.CharField(
        "Name", null=False, blank=False, editable=True, max_length=64
    )
    description = models.CharField(
        "Description", null=True, blank=True, editable=True, max_length=128
    )
    parquet_files = models.CharField(
        "Parquet files", null=True, blank=True, editable=True, max_length=1024
    )
    refresh_data = models.TextField(
        "Refresh data",
        null=True,
        blank=True,
        editable=False,
    )
    form = models.TextField(
        "Form",
        null=True,
        blank=True,
        editable=False,
    )
    view = models.TextField(
        "View",
        null=True,
        blank=True,
        editable=False,
    )
    template = models.TextField(
        "Template",
        null=True,
        blank=True,
        editable=False,
    )
    rights_group = models.CharField(
        "Rights group", null=True, blank=True, editable=True, max_length=64
    )
    menu = models.CharField(
        "Manu path", null=True, blank=True, editable=True, max_length=64
    )
    menu_position = models.IntegerField(
        "Menu position",
        null=True,
        blank=True,
        editable=True,
        default=0,
    )
    menu_icon = models.CharField(
        "Menu icon", null=True, blank=True, editable=True, max_length=256
    )
    menu_icon_size = models.CharField(
        "Menu icon size",
        null=False,
        blank=False,
        editable=True,
        default="1",
        choices=menu_icon_size_choice,
        max_length=1,
    )

    def load_data(self):
        data_path = os_path.join(settings.DATA_PATH, settings.PRJ_NAME)

        if not self.name in PROJECTS_DATA:
            PROJECTS_DATA[self.name] = {}
        pd = PROJECTS_DATA[self.name]
        if not self.name in PROJECTS_DATA_VERSION:
            PROJECTS_DATA_VERSION[self.name] = None
        data_time = PROJECTS_DATA_VERSION[self.name]

        if data_time and (datetime.datetime.now() - data_time).seconds < 60:
            return

        modify = False
        check_time = datetime.datetime.now()

        files = self.parquet_files.replace(",", ";").replace("\n", ";").split(";")
        cleaned_files = [file_name.rsplit(".", 1)[0].strip() for file_name in files]
        for data_name in cleaned_files:
            t = datetime.datetime.fromtimestamp(
                os_path.getmtime(os_path.join(data_path, data_name + ".parquet"))
            )

            if (not data_time) or data_time < t:
                pd[data_name] = pyarrow.parquet.read_table(
                    os_path.join(data_path, data_name + ".parquet")
                )
                modify = True

        PROJECTS_DATA_VERSION[self.name] = check_time

    def get_data(self):
        return PROJECTS_DATA[self.name]

    def get_refresh_data_if_empty(
        self, request, template_name, ext, extra_context, target
    ):
        return REFRESH_DATA

    def get_form_if_empty(self, request, template_name, ext, extra_context, target):
        return FORM

    def get_view_if_empty(self, request, template_name, ext, extra_context, target):
        return VIEW

    def get_template_if_empty(self, request, template_name, ext, extra_context, target):
        return TEMPLATE


admin.site.register(Project)


class Page(models.Model):

    class Meta:
        verbose_name = _("Page")
        verbose_name_plural = _("Pages")
        default_permissions = ("add", "change", "delete", "view", "list", "administer")
        app_label = "schbi"

        ordering = ["id"]

    parent = ext_models.PtigForeignKey(
        Project,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        editable=True,
        verbose_name="Parent",
    )
    name = models.CharField(
        "Name", null=False, blank=False, editable=True, max_length=64
    )
    title = models.CharField(
        "Title", null=True, blank=True, editable=True, max_length=64
    )
    form = models.TextField(
        "Form",
        null=True,
        blank=True,
        editable=False,
    )
    view = models.TextField(
        "View",
        null=True,
        blank=True,
        editable=False,
    )
    template = models.TextField(
        "Template",
        null=True,
        blank=True,
        editable=False,
    )


admin.site.register(Page)


class Chart(models.Model):

    class Meta:
        verbose_name = _("Chart")
        verbose_name_plural = _("Charts")
        default_permissions = ("add", "change", "delete", "view", "list", "administer")
        app_label = "schbi"

        ordering = ["id"]

    parent = ext_models.PtigForeignKey(
        Page,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        editable=True,
        verbose_name="Parent",
    )
    name = models.CharField(
        "Name", null=False, blank=False, editable=True, max_length=64
    )
    title = models.CharField(
        "Title", null=True, blank=True, editable=True, max_length=64
    )
    form = models.TextField(
        "Form",
        null=True,
        blank=True,
        editable=False,
    )
    view = models.TextField(
        "View",
        null=True,
        blank=True,
        editable=False,
    )
    template = models.TextField(
        "Template",
        null=True,
        blank=True,
        editable=False,
    )

    def get_prj(self):
        return self.parent.parent


admin.site.register(Chart)


def refresh_data(refresh_type):
    """
    refresh_type:
        begin - on the start
        before - before every request
        after - after every request

        bi_sheduler_1 - defined by user, handled by django-q sheduler
        ...
        bi_sheduler_9 - defined by user, handled by django-q sheduler
    """

    try:
        for prj in Project.objects.all():
            run_code_from_db_field(
                f"bi_prj_{prj.name}_refresh_data.py",
                prj,
                "refresh_data",
                "refresh_data",
                module=ModuleStruct(globals(), locals()),
                prj=prj,
                refresh_type=refresh_type,
            )
    except:
        pass
