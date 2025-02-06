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

import tables_demo.models


from tables_demo.models import *
from django.forms import fields as form_fields


GenreChoices = [
    ("r", "Rock"),
    ("p", "Pop"),
    ("j", "Jazz"),
    ("h", "Heavy Metal"),
    ("e", "Elekctonic"),
    ("c", "Classical"),
    ("o", "Other"),
]


class Album(models.Model):

    class Meta:
        verbose_name = _("Album")
        verbose_name_plural = _("Albums")
        default_permissions = ("add", "change", "delete", "view", "list", "administer")
        app_label = "tables_adv_demo"

        ordering = ["id"]

    release_date = models.DateField(
        "Release date",
        null=True,
        blank=True,
        editable=True,
    )
    artist = models.CharField(
        "Artist", null=True, blank=True, editable=True, max_length=64
    )
    description = models.CharField(
        "Description", null=False, blank=False, editable=True, max_length=256
    )
    genre = models.CharField(
        "Genre",
        null=False,
        blank=False,
        editable=True,
        choices=GenreChoices,
        max_length=2,
    )

    @classmethod
    def filter(cls, value, view=None, request=None):
        if value:
            return cls.objects.filter(genre=value)
        else:
            return cls.objects.all()

    def init_new(self, request, view, value=None):
        if value:
            return {
                "genre": value,
            }
        else:
            return {}

    def sort(queryset, sort, order):
        if sort:
            if order == "asc":
                queryset = queryset.order_by(sort)
            else:
                queryset = queryset.order_by("-" + sort)
        return queryset

    def get_form_class(self, view, request, create):
        base_form = view.get_form_class()

        class form_class(base_form):
            class Meta(base_form.Meta):
                widgets = {
                    "description": form_fields.Textarea(attrs={"cols": 80, "rows": 3}),
                }

        return form_class


admin.site.register(Album)


class AlbumProxy(Album):

    class Meta:
        verbose_name = _("Album")
        verbose_name_plural = _("Albums")
        default_permissions = ("add", "change", "delete", "view", "list", "administer")
        app_label = "tables_adv_demo"

        ordering = ["id"]

        proxy = True


admin.site.register(AlbumProxy)


class UserGroup(models.Model):

    class Meta:
        verbose_name = _("User group")
        verbose_name_plural = _("User groups")
        default_permissions = ("add", "change", "delete", "view", "list", "administer")
        app_label = "tables_adv_demo"

        ordering = ["id"]


admin.site.register(UserGroup)


class Track(models.Model):

    class Meta:
        verbose_name = _("Track")
        verbose_name_plural = _("Tracks")
        default_permissions = ("add", "change", "delete", "view", "list", "administer")
        app_label = "tables_adv_demo"

        ordering = ["id"]

    parent = ext_models.PtigForeignKey(
        Album,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        editable=True,
        verbose_name="Parent",
    )
    name = models.CharField(
        "Name", null=False, blank=False, editable=True, max_length=64
    )
    param = ext_models.PtigForeignKey(
        tables_demo.models.Example4Parameter,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        editable=True,
        verbose_name="Param",
        search_fields=[
            "key__icontains",
        ],
        can_add=False,
    )
    params = ext_models.PtigManyToManyField(
        tables_demo.models.Example4Parameter,
        null=False,
        blank=False,
        editable=True,
        verbose_name="Parameters",
        search_fields=[
            "key__icontains",
        ],
        related_name="track_parameters",
    )


admin.site.register(Track)
