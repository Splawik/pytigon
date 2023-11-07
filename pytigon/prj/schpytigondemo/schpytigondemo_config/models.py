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


from django import forms
from pytigon_lib.schdjangoext.formfields import Select2Field
from pytigon_lib.schviews import actions
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from schprofile.models import init_user_profiles, Profile
from django.db.models import Q
from django.core.management.utils import get_random_secret_key
from pytigon_lib.schtools.tools import get_request
from pytigon_lib.schdjangoext.email import send_message
from mailer.models import Message as MailMessage
from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from allauth.account.forms import EmailAwarePasswordResetTokenGenerator
from allauth.account.utils import url_str_to_user_pk, user_pk_to_url_str
from allauth.utils import build_absolute_uri
import datetime
import dateutil.parser
from django.utils.timezone import make_aware

import schelements.models
import schprofile.models
import school.models


from schtools.models import Parameter

# Module customization: _schdata.schelements - Element

STRUCTURE = {
    "ROOT": {"next": ["O-COM", "I-GRP", "I-GRP-D", "C-GRP"]},
}

for pos in STRUCTURE:
    if not "app" in STRUCTURE[pos]:
        STRUCTURE[pos]["app"] = "schpytigondemo"
    if "next" in STRUCTURE[pos]:
        STRUCTURE[pos]["next"].append("O-GRP")

for pos in schelements.models.STANDARD_STRUCTURE:
    if not pos in STRUCTURE:
        STRUCTURE[pos] = schelements.models.STANDARD_STRUCTURE[pos]


class DemoElement:
    def save(self, *argi, **argv):
        super().save(*argi, **argv)

    @staticmethod
    def filter_by_permissions(view, queryset_or_obj, request):
        # if queryset_or_obj != None:
        #    print(queryset_or_obj.model)
        #    if queryset_or_obj.model == SchoolElement:
        #        return schelements.models.Element.objects.filter(
        #            type__in=schelements.models.Element.get_structure().keys()
        #        )
        return queryset_or_obj

    @classmethod
    def filter(cls, value, view=None, request=None):
        ret = None
        if value and value != "-":
            try:
                i = int(value)
                if i >= 0:
                    if i == 0:
                        ret = schelements.models.Element.objects.filter(parent=None)
                    else:
                        ret = schelements.models.Element.objects.filter(parent=i)
                else:
                    ret = schelements.models.Element.objects.filter(parent__id=i * -1)
            except:
                ret = schelements.models.Element.objects.filter(type=value)
        else:
            ret = schelements.models.Element.objects.all()

        x = view.kwargs["target"].split("__")
        if len(x) == 3:
            if x[-1] == "all_devices":
                ret = ret.filter(
                    Q(type__startswith="I-DEV")
                    | Q(
                        type__in=(
                            "I-GRP",
                            "I-GRP-D",
                            "O-COM",
                            "O-LOC",
                        )
                    )
                    | Q(type="O-GRP", parent__type__in=("O-GRP", "O-COM", "O-LOC"))
                )

        return ret

    @staticmethod
    def has_the_right(perm, kwargs, request):
        return True

    @staticmethod
    def get_structure():
        global STRUCTURE
        return STRUCTURE


extend_class(schelements.models.Element, DemoElement)

schelements.models.Element.add_type("O-CUS-S", "Owner/Customer/Student")
schelements.models.Element.add_type("O-SUP-T", "Owner/Supplier/Teacher")

schelements.models.Element.add_type("I-DEV-C", "Item/Device/Computer")
schelements.models.Element.add_type("I-DEV-M", "Item/Device/Monitor")
schelements.models.Element.add_type("I-DEV-P", "Item/Device/Printer")
schelements.models.Element.add_type("I-DEV-H", "Item/Device/Phone")
schelements.models.Element.add_type("I-DEV-O", "Item/Device/Other")

schelements.models.Element.add_type("I-GRP-D", "Item/Group/Device")


def get_element_queryset():
    request = get_request()
    if request:
        if request.user.is_superuser:
            return None
        elif (
            hasattr(request.user, "profile")
            and request.user.profile
            and request.user.profile.owner
        ):
            return Q(first_ancestor=request.user.profile.owner.first_ancestor)
    else:
        return None
    return Q(pk=0)


schelements.models.GET_ELEMENT_QUERYSET.set_function(get_element_queryset)


# Module customization: _schdata.schelements - DocHead, DocItem


class DemoDocHead:
    def save(self, *argi, **argv):
        super().save(*argi, **argv)

    @staticmethod
    def filter_by_permissions(view, queryset_or_obj, request):
        return queryset_or_obj

    @staticmethod
    def has_the_right(perm, kwargs, request):
        return True


extend_class(schelements.models.DocHead, SchoolDocHead)


class DemoDocItem:
    def save(self, *argi, **argv):
        super().save(*argi, **argv)

    @staticmethod
    def filter_by_permissions(view, queryset_or_obj, request):
        return queryset_or_obj

    @staticmethod
    def has_the_right(perm, kwargs, request):
        return True


extend_class(schelements.models.DocItem, SchoolDocItem)


# Module customization: _schdata.schprofile


def limit_owner():
    return {"type__in": ("O-CUS", "O-CUS-S")}


def limit_config():
    return {"type": "C-DIC"}


schprofile.models.LIMIT_OWNER.set_function(limit_owner)
schprofile.models.LIMIT_CONFIG.set_function(limit_config)

init_user_profiles()


def add_user_to_group(user, group_name):
    groups = Group.objects.filter(name=group_name)
    if len(groups) < 1:
        g = Group()
        g.name = group_name
        g.save()
    else:
        g = groups[0]
    g.user_set.add(user)


def context_for_password_reset(user):
    request = get_request()
    if request:
        current_site = get_current_site(request)
        email = user.email
        token_generator = EmailAwarePasswordResetTokenGenerator()
        temp_key = token_generator.make_token(user)
        path = reverse(
            "account_reset_password_from_key",
            kwargs=dict(uidb36=user_pk_to_url_str(user), key=temp_key),
        )
        url = build_absolute_uri(request, path)
        context = {
            "current_site": current_site,
            "user": user,
            "password_reset_url": url,
            "request": request,
        }
        return context
    return None


def add_user(user_obj, surname, name, email, user_type):
    user_model = get_user_model()
    user_objects = user_model.objects.filter(email=email)
    if not len(user_objects) > 0:
        user = user_model()
        user.username = email
        user.first_name = name
        user.last_name = surname
        user.email = email
        user.is_staff = False
        user.is_active = True
        user.is_superuser = False
        user.set_password(get_random_secret_key())
        user.save()

        user.profile.owner = user_obj
        user.profile.user_type = user_type
        user.profile.save()
    else:
        user = user_objects[0]
    context = context_for_password_reset(user)
    if context:
        context["user"] = user
    elif user_type in ("ADMINISTRATOR", "O-EMP"):
        add_user_to_group(user, "admins")
        send_message(
            "Welcome to the program " + settings.PRJ_TITLE,
            "school/message_initial_admin.html",
            settings.DEFAULT_FROM_EMAIL,
            (email,),
            None,
            context,
        )


def define_access_rules(user, rules):
    rules.allow("view", schelements.models.Element)
    rules.allow("change", schelements.models.Element, code="DEMO")

    if not user.is_authenticated:
        return

    if user.is_superuser:
        # Superuser gets unlimited access to all articles
        rules.allow("change", schelements.models.Element)
