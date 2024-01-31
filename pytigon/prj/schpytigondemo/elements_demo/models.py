from django.db import models

from pytigon_lib.schdjangoext.fields import *
from pytigon_lib.schdjangoext.models import *
from pytigon_lib.schtools import schjson

from django.utils.translation import gettext_lazy as _
from django.contrib import admin


import schelements.models


from schelements import models as schelements_models
from schprofile import models as schprofile_models
from schprofile.models import init_user_profiles
from django.db.models import Q
from pytigon_lib.schtools.tools import get_request
import datetime


def limit_owner():
    print("get_owner")
    return {"type": "O-CUS"}


def limit_config():
    return {"type": "C-DIC"}


schprofile_models.LIMIT_OWNER.set_function(limit_owner)
schprofile_models.LIMIT_CONFIG.set_function(limit_config)

init_user_profiles()


class DemoElement:
    def save(self, *argi, **argv):
        super().save(*argi, **argv)

    @staticmethod
    def filter_by_permissions(view, queryset_or_obj, request):
        if queryset_or_obj != None:
            print(queryset_or_obj.model)
            if queryset_or_obj.model == DemoElement:
                return schelements_models.Element.objects.filter(
                    type__in=schelements_models.Element.get_structure().keys()
                )
        return queryset_or_obj

    @classmethod
    def filter(cls, value, view=None, request=None):
        if value and value != "-":
            try:
                i = int(value)
                if i >= 0:
                    if i == 0:
                        return schelements_models.Element.objects.filter(parent=None)
                    else:
                        return schelements_models.Element.objects.filter(parent=i)
                else:
                    return schelements_models.Element.objects.filter(parent__id=i * -1)
            except:
                return schelements_models.Element.objects.filter(type=value)
        else:
            return schelements_models.Element.objects.all()

    @staticmethod
    def has_the_right(perm, kwargs, request):
        return True

    @staticmethod
    def get_structure():
        ret = {
            "ROOT": {"next": ["O-COM", "I-GRP"]},
            "O-COM": {
                "next": [
                    "O-LOC",
                ],
                "title": "Company",
            },
            "O-LOC": {
                "next": [
                    "O-EMP",
                ],
                "title": "Location",
            },
            "O-EMP": {
                "title": "Employee",
                "table": "Administrator",
            },
            "I-GRP": {
                "title": "Group of items",
                "table": "IGroup",
                "next": [
                    "I-PRD",
                ],
            },
            "I-PRD": {
                "title": "Products",
                "table": "Product",
            },
        }
        for pos in ret:
            ret[pos]["app"] = "elements_demo"
        return ret


extend_class(schelements_models.Element, DemoElement)


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
    return Q(pk=0)


schelements_models.GET_ELEMENT_QUERYSET.set_function(get_element_queryset)


priority_CHOICE = [
    ("1", "low"),
    ("9", "high"),
]


class DemoDocHead(schelements.models.DocHead):
    class Meta:
        verbose_name = _("Demo document head")
        verbose_name_plural = _("Demo document heads")
        default_permissions = ("add", "change", "delete", "list")
        app_label = "elements_demo"

        ordering = ["id"]

    date_from = models.DateTimeField(
        "Date from",
        null=True,
        blank=True,
        editable=True,
    )
    date_to = models.DateTimeField(
        "Date to",
        null=True,
        blank=True,
        editable=True,
    )
    test = models.CharField("Test", null=True, blank=True, editable=True, max_length=64)

    @classmethod
    def table_action(cls, list_view, request, data):
        if "action" in data:
            if data["action"] == "calendar_events":

                def all_day(date1, date2):
                    if (
                        date1
                        == datetime.datetime.combine(date1.date(), datetime.time.min)
                        and date1 + datetime.timedelta(1) == date2
                    ):
                        return True
                    else:
                        return False

                queryset = list_view.get_queryset()
                if "date" in data:
                    queryset = queryset.filter(
                        date=datetime.datetime.fromisoformat(data["date"])
                    )
                else:
                    if "start" in data:
                        queryset = queryset.filter(
                            date_from__gte=datetime.datetime.fromisoformat(
                                data["start"]
                            )
                        )
                    if "end" in data:
                        queryset = queryset.filter(
                            date_to__lte=datetime.datetime.fromisoformat(data["end"])
                        )
                return schjson.json_dumps(
                    [
                        {
                            "resourceId": 1,
                            "color": "#FE6B64",
                            "id": obj.pk,
                            "title": obj.description,
                            "start": obj.date_from.isoformat(),
                            "end": obj.date_to.isoformat(),
                            "allDay": all_day(obj.date_from, obj.date_to),
                        }
                        for obj in queryset
                    ]
                )
            if data["action"] == "calendar_change_event":
                pk = data["id"]
                date_from = data["start"]
                date_to = data["end"]
                tab = list_view.get_queryset().filter(pk=pk)
                if len(tab) > 0:
                    obj = tab[0]
                    if date_from:
                        obj.date_from = datetime.datetime.fromisoformat(date_from)
                    if date_to:
                        obj.date_to = datetime.datetime.fromisoformat(date_to)
                    obj.save()
                    return {"OK": True}
        return None


admin.site.register(DemoDocHead)


class DemoDocItem(schelements.models.DocItem):
    class Meta:
        verbose_name = _("Demo document item")
        verbose_name_plural = _("Demo document items")
        default_permissions = ("add", "change", "delete", "list")
        app_label = "elements_demo"

        ordering = ["id"]

    priority = models.CharField(
        "Priority",
        null=False,
        blank=False,
        editable=True,
        default="1",
        choices=priority_CHOICE,
        max_length=1,
    )
    date_from = models.DateTimeField(
        "Date from",
        null=True,
        blank=True,
        editable=True,
    )
    date_to = models.DateTimeField(
        "Date to",
        null=True,
        blank=True,
        editable=True,
    )

    @classmethod
    def table_action(cls, list_view, request, data):
        if "action" in data:
            if data["action"] == "calendar_events":

                def all_day(date1, date2):
                    if (
                        date1
                        == datetime.datetime.combine(date1.date(), datetime.time.min)
                        and date1 + datetime.timedelta(1) == date2
                    ):
                        return True
                    else:
                        return False

                queryset = DemoDocItem.objects.filter(
                    parent=list_view.kwargs["parent_pk"]
                )

                if "date" in data:
                    queryset = queryset.filter(
                        date=datetime.datetime.fromisoformat(data["date"])
                    )
                else:
                    if "start" in data:
                        queryset = queryset.filter(
                            date_from__gte=datetime.datetime.fromisoformat(
                                data["start"]
                            )
                        )
                    if "end" in data:
                        queryset = queryset.filter(
                            date_to__lte=datetime.datetime.fromisoformat(data["end"])
                        )
                return schjson.json_dumps(
                    [
                        {
                            "resourceId": 1,
                            "color": "#FE6B64",
                            "id": obj.pk,
                            "title": obj.description,
                            "start": obj.date_from.isoformat(),
                            "end": obj.date_to.isoformat(),
                            "allDay": all_day(obj.date_from, obj.date_to),
                        }
                        for obj in queryset
                    ]
                )
            if data["action"] == "calendar_change_event":
                pk = data["id"]
                date_from = data["start"]
                date_to = data["end"]
                tab = DemoDocItem.objects.filter(pk=pk)
                if len(tab) > 0:
                    obj = tab[0]
                    if date_from:
                        obj.date_from = datetime.datetime.fromisoformat(date_from)
                    if date_to:
                        obj.date_to = datetime.datetime.fromisoformat(date_to)
                    obj.save()
                    return {"OK": True}
        return None


admin.site.register(DemoDocItem)
