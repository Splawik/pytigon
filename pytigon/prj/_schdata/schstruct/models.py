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


from pytigon_lib.schtools.schjson import json_dumps, json_loads
from django.db.models import Max, Min

from schelements.models import *


class CommonGroupDef(schelements.models.BaseObject):

    class Meta:
        verbose_name = _("Common group definition")
        verbose_name_plural = _("Common groups definition")
        default_permissions = ("add", "change", "delete", "view", "list", "administer")
        app_label = "schstruct"

        ordering = ["id"]

        permissions = [
            ("admin_commongroupdef", "Can administer common group definitions"),
        ]

    on_new_elem_event = models.TextField(
        "On new elemetn event",
        null=True,
        blank=True,
        editable=False,
    )
    allowed_new_fields = models.TextField(
        "Allowed new fields",
        null=True,
        blank=True,
        editable=False,
    )
    main_group = models.BooleanField(
        "Main group",
        null=True,
        blank=True,
        editable=True,
    )

    def __str__(self):
        return self.name


admin.site.register(CommonGroupDef)


class CommonGroup(JSONModel):

    class Meta:
        verbose_name = _("Common group")
        verbose_name_plural = _("Common groups")
        default_permissions = ("add", "change", "delete", "view", "list", "administer")
        app_label = "schstruct"

        ordering = ["id"]

        permissions = [
            ("admin_commongroup", "Can administer common groups"),
        ]

    parent = ext_models.PtigTreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        editable=True,
        verbose_name="Parent",
    )
    gparent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        editable=True,
        verbose_name="Grand parent",
        related_name="gparentrel",
    )
    title = models.CharField(
        "Title", null=True, blank=True, editable=True, max_length=64
    )
    group_def_name = models.CharField(
        "Group definition name", null=False, blank=False, editable=True, max_length=64
    )
    gp_group_def_name = models.CharField(
        "Grand parent group definition name",
        null=False,
        blank=False,
        editable=True,
        max_length=64,
    )
    tag_name = models.CharField(
        "Tag name", null=True, blank=True, editable=True, max_length=64
    )
    key1 = models.CharField(
        "Key 1", null=True, blank=True, editable=True, db_index=True, max_length=64
    )
    key2 = models.CharField(
        "Key 2", null=True, blank=True, editable=True, db_index=True, max_length=64
    )
    key3 = models.CharField(
        "Key 3", null=True, blank=True, editable=True, db_index=True, max_length=64
    )

    def code(self):
        return self.title

    def get_def(self):
        x = CommonGroupDef.objects.filter(name=self.group_def_name)
        if len(x) > 0:
            return x[0]
        else:
            return None

    def to_str(self):
        def_obj = self.get_def()
        if def_obj:
            return def_obj.to_str(self)
        else:
            return None

    def __str__(self):
        return f"{self.title} [{self.group_def_name}]"

    @staticmethod
    def get_group_types(parent_pk):
        if not parent_pk:
            groupdef_list = CommonGroupDef.objects.filter(main_group=True)
            return [pos for pos in groupdef_list]
        else:
            group = CommonGroup.objects.get(id=int(parent_pk))
            groupdef = CommonGroupDef.objects.filter(name=group.group_def_name)
            ret = []
            if len(groupdef) > 0:
                allowed_new_fields = groupdef[0].allowed_new_fields
                if allowed_new_fields:
                    for pos in allowed_new_fields.replace(",", ";").split(";"):
                        if pos:
                            objs = CommonGroupDef.objects.filter(name=pos)
                            if len(objs) > 0:
                                ret.append(objs[0])
            return ret

    @classmethod
    def filter(cls, value, view=None, request=None):
        if value:
            if "__" in value:
                id, grp = value.split("__")
                if grp == "pk" or not id:
                    return cls.objects.filter(pk=id)
            else:
                return cls.objects.filter(group_def_name=value)

        return cls.objects.all()

    def on_delete(self, request, view):
        gdef = self.get_def()
        if gdef:
            return gdef.on_delete(self, request, view)

    def action(self, action_name, argv):
        gdef = self.get_def()
        if gdef:
            return gdef.action(self, action_name, argv)


admin.site.register(CommonGroup)
