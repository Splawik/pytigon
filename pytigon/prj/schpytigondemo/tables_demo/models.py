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


from django.db.models.signals import post_save
from django.dispatch import receiver
from schattachements.models import Attachement
from pytigon_lib.schdjangoext.tools import from_migrations

if not from_migrations():

    @receiver(post_save, sender=Attachement)
    def attachement_created(sender, instance, created, **kwargs):
        if created:
            WorkflowType.new_workflow_item("demo", instance)


tag_CHOICE = [
    ("0", "Standard"),
    ("1", "Important"),
]


class Example1User(models.Model):

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        default_permissions = ("add", "change", "delete", "view", "list", "administer")
        app_label = "tables_demo"

        ordering = ["id"]

    username = models.CharField(
        "User name", null=False, blank=False, editable=True, max_length=64
    )
    email = models.EmailField(
        "Email",
        null=True,
        blank=True,
        editable=True,
    )


admin.site.register(Example1User)


class Example1Computer(models.Model):

    class Meta:
        verbose_name = _("Computer")
        verbose_name_plural = _("Computers")
        default_permissions = ("add", "change", "delete", "view", "list", "administer")
        app_label = "tables_demo"

        ordering = ["id"]

    sn = models.CharField(
        "Serial number", null=False, blank=False, editable=True, max_length=64
    )
    description = models.CharField(
        "Description", null=False, blank=False, editable=True, max_length=64
    )
    ip = models.GenericIPAddressField(
        "IP",
        null=True,
        blank=True,
        editable=True,
    )
    active = models.BooleanField(
        "Active",
        null=False,
        blank=False,
        editable=True,
        default=False,
    )


admin.site.register(Example1Computer)


class Example2Peripheral(models.Model):

    class Meta:
        verbose_name = _("Peripheral")
        verbose_name_plural = _("Peripherals")
        default_permissions = ("add", "change", "delete", "view", "list", "administer")
        app_label = "tables_demo"

        ordering = ["id"]

    parent = ext_models.PtigForeignKey(
        Example1Computer,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        editable=True,
        verbose_name="Parent",
    )
    description = models.CharField(
        "Description", null=False, blank=False, editable=True, max_length=64
    )


admin.site.register(Example2Peripheral)


class Example3Tag(models.Model):

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")
        default_permissions = ("add", "change", "delete", "view", "list", "administer")
        app_label = "tables_demo"

        ordering = ["id"]

    tag = models.CharField(
        "Tag", null=False, blank=False, editable=True, choices=tag_CHOICE, max_length=64
    )
    description = models.CharField(
        "Description", null=True, blank=True, editable=True, max_length=64
    )
    app = models.CharField(
        "Application", null=False, blank=False, editable=True, max_length=64
    )
    table = models.CharField(
        "Table", null=True, blank=True, editable=True, max_length=64
    )
    parent_id = models.IntegerField(
        "Parent id",
        null=True,
        blank=True,
        editable=True,
    )

    def init_new(self, request, view, value=None):
        if value:
            app, tbl, id = value.split("__")
            return {"app": app, "table": tbl, "parent_id": id}
        else:
            return {"app": "default", "table": "default", "parent_id": 0}

    @classmethod
    def filter(cls, value, view=None, request=None):
        if value:
            app, tbl, id = value.split("__")
            return cls.objects.filter(app=app, table=tbl, parent_id=id)
        else:
            return cls.objects.all()


admin.site.register(Example3Tag)


class Example4Parameter(JSONModel):

    class Meta:
        verbose_name = _("Parameter")
        verbose_name_plural = _("Parameters")
        default_permissions = ("add", "change", "delete", "view", "list", "administer")
        app_label = "tables_demo"

        ordering = ["id"]

    key = models.CharField("Key", null=False, blank=False, editable=True, max_length=32)

    def get_form_class(self, view, request, create):
        base_form = view.get_form_class()
        data = self.get_json_data()

        class form_class(base_form):
            def __init__(self, *args, **kwargs):
                nonlocal data
                super().__init__(*args, **kwargs)
                if data:
                    for key, value in data.items():
                        self.fields["json_%s" % key] = forms.CharField(
                            label=key, initial=value
                        )
                else:
                    self.fields["json_test1"] = forms.CharField(
                        label="test1", initial="value_test1"
                    )
                    self.fields["json_test2"] = forms.CharField(
                        label="test2", initial="value_test2"
                    )

        return form_class

    def post_form(self, view, form, request):
        data = form.cleaned_data
        if "json_test1" in data:
            self.json_test1 = data["json_test1"]
        if "json_test2" in data:
            self.json_test2 = data["json_test2"]
        return True

    def __str__(self):
        return self.key


admin.site.register(Example4Parameter)


class Example5ParamGroup(TreeModel):

    class Meta:
        verbose_name = _("Group of parameters")
        verbose_name_plural = _("Groups of parameters")
        default_permissions = ("add", "change", "delete", "view", "list", "administer")
        app_label = "tables_demo"

        ordering = ["id"]

    parent = ext_models.PtigTreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        editable=True,
        verbose_name="Parent",
    )
    main_parameter = ext_models.PtigForeignKey(
        Example4Parameter,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        editable=True,
        verbose_name="Main parameter",
    )
    second_parameter = ext_models.PtigForeignKey(
        Example4Parameter,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        editable=True,
        verbose_name="Second parameter",
        related_name="second_parameters",
        search_fields=[
            "key__startswith",
        ],
    )
    parameters = ext_models.PtigManyToManyField(
        Example4Parameter,
        null=False,
        blank=False,
        editable=True,
        verbose_name="Parameters",
        related_name="group_parameters",
    )


admin.site.register(Example5ParamGroup)


class Example6ComputerFromExample1(Example1Computer):

    class Meta:
        verbose_name = _("Proxy to computer")
        verbose_name_plural = _("Proxy to computers")
        default_permissions = ("add", "change", "delete", "view", "list", "administer")
        app_label = "tables_demo"

        ordering = ["id"]

        proxy = True


admin.site.register(Example6ComputerFromExample1)


class Example7ComputerFromExample1(Example1Computer):

    class Meta:
        verbose_name = _("Proxy to computer")
        verbose_name_plural = _("Proxy to computers")
        default_permissions = ("add", "change", "delete", "view", "list", "administer")
        app_label = "tables_demo"

        ordering = ["id"]

        proxy = True

    @classmethod
    def table_action(cls, list_view, request, data):
        if "action" in data:
            if data["action"] == "insert_rows":
                table = data["table"]
                return actions.refresh(request)
        return standard_table_action(
            cls, list_view, request, data, ["copy", "paste", "delete"]
        )


admin.site.register(Example7ComputerFromExample1)
