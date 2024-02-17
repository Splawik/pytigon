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

import schelements.models
import schstruct.models


class LabelType(models.Model):

    class Meta:
        verbose_name = _("Label type")
        verbose_name_plural = _("Label types")
        default_permissions = ("add", "change", "delete", "view", "list", "administer")
        app_label = "schlabels"

        ordering = ["id"]

    name = models.CharField(
        "Name", null=False, blank=False, editable=True, max_length=256
    )
    title = models.CharField(
        "Title", null=True, blank=True, editable=True, max_length=256
    )


admin.site.register(LabelType)


class ElementLabel(models.Model):

    class Meta:
        verbose_name = _("Element label")
        verbose_name_plural = _("Element labels")
        default_permissions = ("add", "change", "delete", "view", "list", "administer")
        app_label = "schlabels"

        ordering = ["id"]

    parent = ext_models.PtigForeignKey(
        schelements.models.Element,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        editable=False,
        verbose_name="Parent",
        db_index=True,
    )
    type = ext_models.PtigForeignKey(
        LabelType,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        editable=False,
        verbose_name="Type",
        db_index=True,
    )

    @staticmethod
    def set_label(element, label_type_name):
        label_type = LabelType.objects.filter(name=label_type_name).first()
        if label_type:
            if not ElementLabel.objects.filter(
                parent=element, type=label_type
            ).exists():
                obj = ElementLabel()
                obj.parent = element
                obj.type = label_type
                obj.save()

    @staticmethod
    def remove_label(element, label_type_name):
        ElementLabel.objects.filter(parent=element, type__name=label_type_name).delete()

    @staticmethod
    def has_label(element, label_type_name):
        return element.elementlabel_set.filter(type__name=label_type_name).exists()

    @staticmethod
    def objects_with_label(label_type_name):
        return schelements.models.Element.objects.filter(
            elementlabel_set__type__name=label_type_name
        )


admin.site.register(ElementLabel)


class CommonGroupLabel(models.Model):

    class Meta:
        verbose_name = _("Common group label")
        verbose_name_plural = _("Common groups labels")
        default_permissions = ("add", "change", "delete", "view", "list", "administer")
        app_label = "schlabels"

        ordering = ["id"]

    parent = ext_models.PtigForeignKey(
        schstruct.models.CommonGroup,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        editable=False,
        verbose_name="Group",
        db_index=True,
    )
    type = ext_models.PtigForeignKey(
        LabelType,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        editable=False,
        verbose_name="Type",
        db_index=True,
    )

    @staticmethod
    def set_label(group, label_type_name):
        label_type = LabelType.objects.filter(name=label_type_name).first()
        if not CommonGroupLabel.objects.filter(parent=group, type=label_type).exists():
            obj = CommonGroupLabel()
            obj.parent = group
            obj.type = label_type
            obj.save()

    @staticmethod
    def remove_label(group, label_type_name):
        CommonGroupLabel.objects.filter(
            parent=group, type__name=label_type_name
        ).delete()

    @staticmethod
    def has_label(group, label_type_name):
        return group.commongrouplabel_set.filter(type__name=label_type_name).exists()

    @staticmethod
    def objects_with_label(label_type_name):
        return schstruct.models.CommonGroup.objects.filter(
            commongrouplabel_set__type__name=label_type_name
        )


admin.site.register(CommonGroupLabel)


class Label(AssociatedModel):

    class Meta:
        verbose_name = _("Label")
        verbose_name_plural = _("Labels")
        default_permissions = ("add", "change", "delete", "view", "list", "administer")
        app_label = "schlabels"

        ordering = ["id"]

    type = ext_models.PtigForeignKey(
        LabelType,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        editable=False,
        verbose_name="Type",
        db_index=True,
    )

    @staticmethod
    def set_label(application, table, group, id, label_type_name):
        label_type = LabelType.objects.filter(name=label_type_name).first()
        if label_type:
            if not Label.objects.filter(
                application=application,
                table=table,
                group=group,
                parent_id=id,
                type=label_type,
            ).exists():
                obj = Label()
                obj.application = application
                obj.table = table
                obj.group = group
                obj.parent_id = id
                obj.type = label_type
                obj.save()

    @staticmethod
    def remove_label(application, table, group, id, label_type_name):
        Label.objects.filter(
            application=application,
            table=table,
            group=group,
            parent_id=id,
            type__name=label_type_name,
        ).delete()

    @staticmethod
    def has_label(application, table, group, id, label_type_name):
        return Label.objects.filter(
            application=application,
            table=table,
            group=group,
            parent_id=id,
            type__name=label_type_name,
        ).exists()

    @staticmethod
    def objects_with_label(application, table, group, label_type_name):
        object_list = Label.objects.filter(
            application=application,
            table=table,
            group=group,
            type__name=label_type_name,
        )
        return (obj.parent_id for obj in object_list)


admin.site.register(Label)
