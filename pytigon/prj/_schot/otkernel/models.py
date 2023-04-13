import django
from django.db import models
from django.utils import timezone

from pytigon_lib.schdjangoext.fields import *
from pytigon_lib.schdjangoext.models import *
import pytigon_lib.schdjangoext.fields as ext_models
from pytigon_lib.schtools import schjson

from django.utils.translation import gettext_lazy as _
from django.contrib import admin

import os, os.path
import sys
from pytigon_lib.schhtml.htmltools import superstrip


from schadmin.models import *

from schcommander.models import *

from schtools.models import *


class Feature(JSONModel):
    class Meta:
        verbose_name = _("Feature")
        verbose_name_plural = _("Features")
        default_permissions = ("add", "change", "delete", "list")
        app_label = "otkernel"

        ordering = ["id"]


admin.site.register(Feature)


class Location(models.Model):
    class Meta:
        verbose_name = _("Location")
        verbose_name_plural = _("Locations")
        default_permissions = ("add", "change", "delete", "list")
        app_label = "otkernel"

        ordering = ["id"]

    name = models.CharField(
        "Name", null=False, blank=False, editable=True, max_length=128
    )
    external_id = models.CharField(
        "External id",
        null=True,
        blank=True,
        editable=True,
        db_index=True,
        max_length=16,
    )


admin.site.register(Location)


class MeasurementPoint(models.Model):
    class Meta:
        verbose_name = _("Measurement point")
        verbose_name_plural = _("Measurement points")
        default_permissions = ("add", "change", "delete", "list")
        app_label = "otkernel"

        ordering = ["id"]

    company = models.CharField(
        "Company", null=False, blank=False, editable=True, max_length=16
    )
    facility = models.CharField(
        "Facility", null=True, blank=True, editable=True, max_length=32
    )
    name = models.CharField(
        "Name", null=False, blank=False, editable=True, max_length=128
    )
    input_proc = models.TextField(
        "Input procedure",
        null=True,
        blank=True,
        editable=False,
    )
    control_proc = models.TextField(
        "Control procedure",
        null=True,
        blank=True,
        editable=False,
    )
    com_proc = models.TextField(
        "Communication procedure",
        null=True,
        blank=True,
        editable=False,
    )
    state_proc = models.TextField(
        "State procedure",
        null=True,
        blank=True,
        editable=False,
    )

    filter_fields = {
        "name": ["exact", "icontains", "istartswith"],
    }

    def save(self, *argi, **argv):
        super().save(*argi, **argv)
        try:
            self.measurementpointstate
        except:
            obj = MeasurementPointState()
            obj.parent = self
            obj.save()
        try:
            self.mpointinputqueuestatus
        except:
            obj = MPointInputQueueStatus()
            obj.mp = self
            obj.save()
        try:
            self.mpointoutputqueuestatus
        except:
            obj = MPointOutputQueueStatus()
            obj.mp = self
            obj.save()
        try:
            self.mpointcontrolqueuestatus
        except:
            obj = MPointControlQueueStatus()
            obj.mp = self
            obj.save()


admin.site.register(MeasurementPoint)


class MeasurementPointState(JSONModel):
    class Meta:
        verbose_name = _("Measurement point state")
        verbose_name_plural = _("Measurement point state")
        default_permissions = ("add", "change", "delete", "list")
        app_label = "otkernel"

        ordering = ["id"]

    parent = models.OneToOneField(
        MeasurementPoint,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        editable=True,
        verbose_name="Parent",
    )
    description = models.CharField(
        "Description", null=True, blank=True, editable=True, max_length=128
    )


admin.site.register(MeasurementPointState)


class Product(models.Model):
    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        default_permissions = ("add", "change", "delete", "list")
        app_label = "otkernel"

        ordering = ["id"]

    external_id = models.CharField(
        "External id",
        null=True,
        blank=True,
        editable=True,
        db_index=True,
        max_length=64,
    )
    name = models.CharField(
        "Name", null=False, blank=False, editable=True, max_length=128
    )
    conversion_factor = models.FloatField(
        "Conversion factor",
        null=True,
        blank=True,
        editable=True,
        default=1,
    )
    active = models.BooleanField(
        "Active",
        null=True,
        blank=True,
        editable=True,
        default=True,
        db_index=True,
    )


admin.site.register(Product)


class RawMaterial(models.Model):
    class Meta:
        verbose_name = _("Raw material")
        verbose_name_plural = _("Raw materials")
        default_permissions = ("add", "change", "delete", "list")
        app_label = "otkernel"

        ordering = ["id"]

    external_id = models.CharField(
        "External id",
        null=True,
        blank=True,
        editable=True,
        db_index=True,
        max_length=64,
    )
    name = models.CharField(
        "Name", null=False, blank=False, editable=True, max_length=128
    )
    active = models.BooleanField(
        "Active",
        null=False,
        blank=False,
        editable=True,
        default=True,
    )


admin.site.register(RawMaterial)


class Operation(JSONModel):
    class Meta:
        verbose_name = _("Operation")
        verbose_name_plural = _("Operations")
        default_permissions = ("add", "change", "delete", "list")
        app_label = "otkernel"

        ordering = ["id"]

    previous_operation = ext_models.PtigForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        editable=True,
        verbose_name="Previous operation",
    )
    time = models.DateTimeField(
        "Time", null=False, blank=False, editable=True, auto_now_add=True
    )


admin.site.register(Operation)


class Inventory(models.Model):
    class Meta:
        verbose_name = _("Inventory")
        verbose_name_plural = _("Inventories")
        default_permissions = ("add", "change", "delete", "list")
        app_label = "otkernel"

        ordering = ["id"]

    feature = ext_models.PtigForeignKey(
        Feature,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        editable=True,
        verbose_name="Feature",
    )
    product = ext_models.PtigForeignKey(
        Product,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        editable=True,
        verbose_name="Product",
    )
    rfid = models.CharField(
        "RFID", null=True, blank=True, editable=True, db_index=True, max_length=64
    )
    location = ext_models.PtigForeignKey(
        Location,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        editable=True,
        verbose_name="Location",
    )
    place = models.CharField(
        "Place", null=True, blank=True, editable=True, max_length=32
    )
    amount = models.IntegerField(
        "Amount",
        null=False,
        blank=False,
        editable=True,
        default=1,
    )
    last_operation = ext_models.PtigForeignKey(
        Operation,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        editable=True,
        verbose_name="Last operation",
    )


admin.site.register(Inventory)


class Log(models.Model):
    class Meta:
        verbose_name = _("Log")
        verbose_name_plural = _("Logs")
        default_permissions = ("add", "change", "delete", "list")
        app_label = "otkernel"

        ordering = ["id"]

    mp = ext_models.PtigForeignKey(
        MeasurementPoint,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        editable=True,
        verbose_name="Measurement point",
    )
    time = models.DateTimeField(
        "Time", null=False, blank=False, editable=True, db_index=True, auto_now_add=True
    )
    attr = models.CharField(
        "Attribute",
        null=False,
        blank=False,
        editable=True,
        db_index=True,
        max_length=16,
    )
    amount = models.FloatField(
        "Amount",
        null=True,
        blank=True,
        editable=True,
    )


admin.site.register(Log)


class ExtendedLog(JSONModel):
    class Meta:
        verbose_name = _("Extended log")
        verbose_name_plural = _("Extended log")
        default_permissions = ("add", "change", "delete", "list")
        app_label = "otkernel"

        ordering = ["id"]

    mp = ext_models.PtigForeignKey(
        MeasurementPoint,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        editable=True,
        verbose_name="Measurement point",
    )
    time = models.DateTimeField(
        "Time", null=False, blank=False, editable=True, db_index=True, auto_now_add=True
    )
    attr = models.CharField(
        "Attribute",
        null=False,
        blank=False,
        editable=True,
        db_index=True,
        max_length=16,
    )


admin.site.register(ExtendedLog)


class MPointInputQueue(JSONModel):
    class Meta:
        verbose_name = _("Measurement point input queue")
        verbose_name_plural = _("Measurement point input queue")
        default_permissions = ("add", "change", "delete", "list")
        app_label = "otkernel"

        ordering = ["id"]

    mp = ext_models.PtigForeignKey(
        MeasurementPoint,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        editable=True,
        verbose_name="Measurement point",
    )


admin.site.register(MPointInputQueue)


class MPointInputQueueStatus(JSONModel):
    class Meta:
        verbose_name = _("Measurement point input queue status")
        verbose_name_plural = _("Measurement point input queue statuses")
        default_permissions = ("add", "change", "delete", "list")
        app_label = "otkernel"

        ordering = ["id"]

    mp = models.OneToOneField(
        MeasurementPoint,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        editable=True,
        verbose_name="Measurement point",
    )


admin.site.register(MPointInputQueueStatus)


class MPointOutputQueue(JSONModel):
    class Meta:
        verbose_name = _("Measurement point output queue")
        verbose_name_plural = _("Measurement point output queue")
        default_permissions = ("add", "change", "delete", "list")
        app_label = "otkernel"

        ordering = ["id"]

    mp = ext_models.PtigForeignKey(
        MeasurementPoint,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        editable=True,
        verbose_name="Measurement point",
    )


admin.site.register(MPointOutputQueue)


class MPointOutputQueueStatus(JSONModel):
    class Meta:
        verbose_name = _("Measurement point output queue status")
        verbose_name_plural = _("Measurement point output queue status")
        default_permissions = ("add", "change", "delete", "list")
        app_label = "otkernel"

        ordering = ["id"]

    mp = models.OneToOneField(
        MeasurementPoint,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        editable=True,
        verbose_name="Measurement point",
    )


admin.site.register(MPointOutputQueueStatus)


class MPointControlQueue(JSONModel):
    class Meta:
        verbose_name = _("Measurement point control queue")
        verbose_name_plural = _("Measurement point control queue")
        default_permissions = ("add", "change", "delete", "list")
        app_label = "otkernel"

        ordering = ["id"]

    mp = ext_models.PtigForeignKey(
        MeasurementPoint,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        editable=True,
        verbose_name="Measurement point",
    )
    description = models.CharField(
        "Description", null=True, blank=True, editable=True, max_length=128
    )


admin.site.register(MPointControlQueue)


class MPointControlQueueStatus(JSONModel):
    class Meta:
        verbose_name = _("Measurement point control queue status")
        verbose_name_plural = _("Measurement point control queue status")
        default_permissions = ("add", "change", "delete", "list")
        app_label = "otkernel"

        ordering = ["id"]

    mp = models.OneToOneField(
        MeasurementPoint,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        editable=True,
        verbose_name="Measurement point",
    )


admin.site.register(MPointControlQueueStatus)
