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


from tables_demo.models import *


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
        default_permissions = ("add", "change", "delete", "list")
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
        "Description", null=False, blank=False, editable=True, max_length=128
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
    def filter(cls, value):
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


admin.site.register(Album)


class AlbumProxy(Album):
    class Meta:
        verbose_name = _("Album")
        verbose_name_plural = _("Albums")
        default_permissions = ("add", "change", "delete", "list")
        app_label = "tables_adv_demo"

        ordering = ["id"]

        proxy = True


admin.site.register(AlbumProxy)


class UserGroup(models.Model):
    class Meta:
        verbose_name = _("User group")
        verbose_name_plural = _("User groups")
        default_permissions = ("add", "change", "delete", "list")
        app_label = "tables_adv_demo"

        ordering = ["id"]


admin.site.register(UserGroup)


class Track(models.Model):
    class Meta:
        verbose_name = _("Track")
        verbose_name_plural = _("Tracks")
        default_permissions = ("add", "change", "delete", "list")
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
        Example4Parameter,
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
        Example4Parameter,
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
