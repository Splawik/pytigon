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


from schtools.models import *


from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from schelements.models import Element
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from pytigon_lib.schtools.tools import get_request


def limit_owner():
    return {}


def limit_config():
    return {}


LIMIT_OWNER = OverwritableCallable(limit_owner)
LIMIT_CONFIG = OverwritableCallable(limit_config)


def set_active_variant(user, value):
    pass


def get_active_variant(user):
    return None


def get_active_variant_description(user):
    return None


def get_all_variants(user):
    return []


SET_ACTIVE_VARIANT = OverwritableCallable(set_active_variant)
GET_ACTIVE_VARIANT = OverwritableCallable(get_active_variant)
GET_ACTIVE_VARIANT_DESCRIPTION = OverwritableCallable(get_active_variant_description)
GET_ALL_VARIANTS = OverwritableCallable(get_all_variants)


class Profile(models.Model):
    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")
        default_permissions = ("add", "change", "delete", "list")
        app_label = "schprofile"

        ordering = ["id"]

    owner = ext_models.PtigForeignKey(
        Element,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        editable=True,
        verbose_name="Owner",
        related_name="profile_owners",
        limit_choices_to=LIMIT_OWNER,
    )
    config = ext_models.PtigForeignKey(
        Element,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        editable=True,
        verbose_name="Config",
        related_name="profile_configs",
        limit_choices_to=LIMIT_CONFIG,
    )
    user_type = models.CharField(
        "User type", null=True, blank=True, editable=True, max_length=32
    )
    doc_regs = models.CharField(
        "Allowed document registers",
        null=True,
        blank=True,
        editable=True,
        max_length=256,
    )
    doc_types = models.CharField(
        "Allowed document types", null=True, blank=True, editable=True, max_length=256
    )
    accounts = models.CharField(
        "Allowed accounts", null=True, blank=True, editable=True, max_length=256
    )
    aliases = models.CharField(
        "Aliases", null=True, blank=True, editable=True, max_length=256
    )

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)

    def set_active_variant(self, value):
        request = get_request()
        session["active_variant"] = value
        if request and request.user:
            return SET_ACTIVE_VARIANT(request.user, value)
        else:
            return None

    def get_active_variant(self):
        request = get_request()
        ret = session.get("active_variant", None)
        if ret != None:
            return ret
        else:
            if request and request.user:
                return GET_ACTIVE_VARIANT(request.user)
            else:
                return None

    def get_active_variant_description(self):
        request = get_request()
        if request and request.user:
            return GET_ACTIVE_VARIANT_DESCRIPTION(request.user)
        else:
            return None

    def get_all_variants(self):
        request = get_request()
        if request and request.user:
            return GET_ALL_VARIANTS(request.user)
        else:
            return None


admin.site.register(Profile)


USER_PROFILES = False


def init_user_profiles():
    global USER_PROFILES

    if not USER_PROFILES:
        USER_PROFILES = True

        @receiver(post_save, sender=get_user_model())
        def create_user_profile(sender, instance, created, **kwargs):
            if created:
                Profile.objects.create(user=instance)

            if hasattr(instance, "profile"):
                instance.profile.save()
            else:
                if not created:
                    Profile.objects.create(user=instance)

        class UserWithProfileInline(admin.StackedInline):
            model = Profile
            can_delete = False
            verbose_name_plural = "Profile"

        class UserAdmin(BaseUserAdmin):
            inlines = (UserWithProfileInline,)

            def get_inline_instances(self, request, obj=None):
                if not obj:
                    return list()
                return super(UserAdmin, self).get_inline_instances(request, obj)

        admin.site.unregister(get_user_model())
        admin.site.register(get_user_model(), UserAdmin)
