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


from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from schelements.models import Element
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from pytigon_lib.schtools.tools import get_request
from pytigon_lib.schdjangoext.tools import from_migrations


def limit_owner():
    return {}


def limit_config():
    return {}


LIMIT_OWNER = OverwritableCallable(limit_owner)
LIMIT_CONFIG = OverwritableCallable(limit_config)

User = get_user_model()


class Profile(models.Model):

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")
        default_permissions = ("add", "change", "delete", "view", "list", "administer")
        app_label = "schprofile"

        ordering = ["id"]

        permissions = [
            ("admin_profile", "Can administer profiles"),
        ]

    owner = ext_models.PtigForeignKey(
        schelements.models.Element,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        editable=True,
        verbose_name="Owner",
        related_name="profile_owners",
        limit_choices_to=LIMIT_OWNER,
    )
    config = ext_models.PtigForeignKey(
        schelements.models.Element,
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
    variants = models.TextField(
        "Variants",
        null=True,
        blank=True,
        editable=True,
    )

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)

    def set_active_variant(self, value):
        if self.variants:
            request = get_request()
            tab = self.variants.split("\n")
            for row in tab:
                if row.startswith(value):
                    request.session["active_variant"] = row.strip()
                    return True
        return False

    def get_active_variant(self):
        request = get_request()
        ret = request.session.get("active_variant", None)
        if ret != None:
            v = {}
            for x in ret.split(",", 1):
                if x and "=" in x:
                    xx = x.split("=", 1)
                    v[xx[0].strip()] = xx[1].strip()
            return v
        else:
            if self.variants:
                x = self.variants.split("\n")[0].split(":", 1)[1]
                if x:
                    request.session["active_variant"] = x
                    return self.get_active_variant()
            return None

    def get_active_variant_description(self):
        request = get_request()
        ret = request.session.get("active_variant", None)
        if ret != None:
            if ":" in ret:
                return ret.split(":", 1)[0].strip()
            return None
        else:
            if self.variants:
                x = self.variants.split("\n")[0]
                if x:
                    request.session["active_variant"] = x
                    return self.get_active_variant_description()
            return None

    def get_all_variants(self):
        if self.variants:
            return [item.split(":")[0] for item in self.variants.split("\n") if item]
        else:
            return None

    def get_variant_count(self):
        if self.variants:
            return len([item for item in self.variants.split("\n") if item])
        else:
            return None


admin.site.register(Profile)


class UserProxy(User):

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        default_permissions = ("add", "change", "delete", "view", "list", "administer")
        app_label = "schprofile"

        ordering = ["id"]

        proxy = True


admin.site.register(UserProxy)


USER_PROFILES = False


def init_user_profiles():
    global USER_PROFILES

    if not USER_PROFILES and not from_migrations():
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
