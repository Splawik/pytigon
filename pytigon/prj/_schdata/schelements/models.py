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


import copy
from pytigon_lib.schdjangoext.django_ihtml import ihtml_to_html
from django.template.loader import select_template
import datetime
from django.db import transaction
from django.contrib.contenttypes.models import ContentType
from pytigon_lib.schtools.tools import content_to_function
from django.db.models import Q, Sum
from django.apps import apps


def get_element_queryset():
    return None


GET_ELEMENT_QUERYSET = OverwritableCallable(get_element_queryset)


class ElementManager(models.Manager):
    def get_queryset(self):
        q = GET_ELEMENT_QUERYSET()
        if q:
            return super().get_queryset().filter(q)
        else:
            return super().get_queryset()


account_type_choice_2 = [
    ("B", "Balance"),
    ("O", "Off-balance"),
    ("N", "Non-financial"),
    ("V", "Inventory"),
    ("I", "Inventory income"),
    ("D", "Disposal"),
]

account_type_choice_1 = [
    ("S", "Synthetic"),
    ("A", "Analytical"),
]

element_type_choice = [
    ("O-GRP", "Owner/Group"),
    ("O-COM", "Owner/Company"),
    ("O-DIV", "Owner/Division"),
    ("O-DEP", "Owner/Department"),
    ("O-POS", "Owner/Position"),
    ("O-EMP", "Owner/Employee"),
    ("O-LOC", "Owner/Location"),
    ("O-PER", "Owner/Person"),
    ("O-CUS", "Owner/Customer"),
    ("O-SUP", "Owner/Supplier"),
    ("O-DEV", "Owner/Device"),
    ("O-OTH", "Owner/Other"),
    ("O-ALI", "Owner/Alias"),
    ("I-GRP", "Item/Group"),
    ("I-SRV", "Item/Service"),
    ("I-INT", "Item/Intellectual value"),
    ("I-CUR", "Item/Currency"),
    ("I-MAT", "Item/Material"),
    ("I-RAW", "Item/Raw material"),
    ("I-PRD", "Item/Product"),
    ("I-IPR", "Item/Intermediate product"),
    ("I-MER", "Item/Merchandise"),
    ("I-DEV", "Item/Device"),
    ("I-PMA", "Item/Production machine"),
    ("I-VEH", "Item/Vehicle"),
    ("I-OTH", "Item/Other"),
    ("I-ALI", "Item/Alias"),
    ("C-SYS", "Config/System"),
    ("C-UNT", "Config/Unit of measure"),
    ("C-DIC", "Config/Dictionary"),
    ("C-OTH", "Config/Other"),
    ("C-ALI", "Config/Alias"),
]

doctype_status = [
    ("0", "Disabled"),
    ("1", "Activ"),
]


class Element(TreeModel):
    class Meta:
        verbose_name = _("Element")
        verbose_name_plural = _("Elements")
        default_permissions = ("add", "change", "delete", "list")
        app_label = "schelements"

        ordering = ["id"]

    parent = ext_models.PtigTreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        editable=True,
        verbose_name="Parent",
    )
    first_ancestor = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        editable=True,
        verbose_name="First ancestor",
        related_name="first_ancestors",
    )
    type = models.CharField(
        "Element type",
        null=False,
        blank=False,
        editable=True,
        choices=element_type_choice,
        max_length=8,
    )
    code = models.CharField(
        "Code", null=True, blank=True, editable=True, db_index=True, max_length=16
    )
    path = models.CharField(
        "Path", null=True, blank=True, editable=True, db_index=True, max_length=1024
    )
    name = models.CharField(
        "Name", null=False, blank=False, editable=True, max_length=64
    )
    grand_parent1 = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        editable=True,
        verbose_name="Grand parent 1",
        related_name="grandparent1",
    )
    grand_parent2 = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        editable=True,
        verbose_name="Grand parent 2",
        related_name="grandparent2",
    )
    grand_parent3 = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        editable=True,
        verbose_name="Grand parent 3",
        related_name="grandparent3",
    )
    grand_parent4 = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        editable=True,
        verbose_name="Grand parent 4",
        related_name="grandparent4",
    )
    key = models.ForeignKey(
        "auth.Group",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    key_path = models.CharField(
        "Key path", null=True, blank=True, editable=False, db_index=True, max_length=256
    )
    description = models.CharField(
        "Description", null=True, blank=True, editable=True, max_length=256
    )

    def init_new(self, request, view, param=None):
        defaults = {"type": param}
        return defaults

    def save(self, *argi, **argv):
        if not self.code:
            object_list = Element.objects.filter(
                type=self.type, code__startswith=self.type
            ).order_by("-id")
            if len(object_list) > 0:
                x = object_list[0].code.split("-")[-1]
                try:
                    i = int(x) + 1
                except:
                    i = 1
                self.code = self.type + "-" + str(i)
            else:
                self.code = self.type + "-1"

        path = self.code
        if self.key:
            key_path = self.key.name
        else:
            key_path = ""

        tab = self.parents()
        for pos in tab:
            path = pos.code + "/" + path
            if pos.key:
                if key_path:
                    key_path = pos.key.name + "/" + key_path
                else:
                    key_path = pos.key.name

        self.path = path
        self.key_path = key_path

        if len(tab) > 0:
            self.first_ancestor = tab[-1]
            super().save(*argi, **argv)
        else:
            super().save(*argi, **argv)
            self.first_ancestor = self
            super().save(*argi, **argv)

    def get_name(self):
        return self.name

    def _get_parent_elem(element_type):
        tab = self.parents()
        for pos in tab:
            if pos.type == element_type:
                return pos
        return None

    def company(self):
        return self._get_parent_elem("O-COM")

    def division(self):
        return self._get_parent_elem("O-DIV")

    def departament(self):
        return self._get_parent_elem("O-DEP")

    def position(self):
        return self._get_parent_elem("O-POS")

    def location(self):
        return self._get_parent_elem("O-LOC")

    def owner_group(self):
        return self._get_parent_elem("O-GRP")

    def owner_grand_group(self):
        grp = self._get_parent_elem("O-GRP")
        if grp:
            return grp._get_parent_elem("O-GRP")
        else:
            return None

    def item_group(self):
        return self._get_parent_elem("I-GRP")

    def item_grand_group(self):
        grp = self._get_parent_elem("I-GRP")
        if grp:
            return grp._get_parent_elem("I-GRP")
        else:
            return None

    def related(self):
        ret = ""
        for obj in (
            self.grand_parent1,
            self.grand_parent2,
            self.grand_parent3,
            self.grand_parent4,
        ):
            if obj:
                if ret == "":
                    ret = obj.name
                else:
                    ret = ret + "; " + obj.name
        return ret

    def parents(self):
        p = []
        parent = self.parent
        while parent:
            p.append(parent)
            if parent == parent.parent:
                break
            parent = parent.parent
        return p

    def del_get_children(self, child_type):
        ret = []
        object_list = Element.objects.filter(parent=self)
        for child in object_list:
            if child.type == child_type:
                ret.append(child)
            else:
                x = child.get_children(child_type)
                if x:
                    ret.extend(list(x))
        return ret

    def q_for_children(self, child_type):
        ret = []
        ret.append(Q(parent=self))
        object_list = list(Element.objects.filter(parent=self).exclude(type=child_type))
        if len(object_list) > 0:
            for child in object_list:
                x = child.get_children(child_type)
                if x:
                    ret.extend(list(x))
        return ret

    def get_children(self, child_type):
        qq = self.q_for_children(child_type)
        return Element.objects.filter(*qq)

    @staticmethod
    def get_children_for_element(parent_code, child_type):
        object_list = Element.objects.filter(code=parent_code)
        if len(object_list) > 0:
            return object_list[0].get_children(child_type)
        return []

    @staticmethod
    def limit_choices(parent_code, child_type):
        ids = []
        objects = Element.get_children_for_element(parent_code, child_type)
        for obj in objects:
            ids.append(obj.id)
        return Q(id__in=ids)

    def href_path(self):
        p = self.parents()
        n = ""
        for parent in p:
            href = "<a target='_refresh_data' href='../../%s/form/tree'>" % parent.id
            if parent.code and parent.code != "":
                n = href + parent.code + "</a>/" + n
            else:
                n = href + "?</a>/" + n
        return (
            "<a target='_refresh_data' href='../../0/form/tree'>/</a>" + n + self.code
        )

    def href_path_list(self):
        p = self.parents()
        n = []
        for parent in p:
            href = "<a target='_refresh_data' href='../../%s/form/tree'>" % parent.id
            if parent.code and parent.code != "":
                n.append(href + parent.code + "</a>")
            else:
                n.append(href + "?</a>")
        n.append("<a target='_refresh_data' href='../../0/form/tree'>/</a>")
        return n

    def __str__(self):
        p = self.parents()
        if self.code and self.code != "":
            n = self.code + ":" + self.name
        else:
            n = self.name
        for parent in p:
            if parent.code and parent.code != "":
                n = parent.code + "/" + n
            else:
                n = "?/" + n
        return n

    @staticmethod
    def gen_url(value):
        if value:
            id = int(value)
        else:
            id = -1
        return "/schsys/treedialog/schelements/Element/%s/" % id

    def get_derived_object(self, param=None):
        t = None
        if type(self) == Element:
            if hasattr(self, "get_structure"):
                s = self.get_structure()
                if param and "view" in param and "add_param" in param["view"].kwargs:
                    t = param["view"].kwargs["add_param"]
                    if t == "-":
                        return self
                    if t in s:
                        model = apps.get_model(s[t]["app"], s[t]["table"])
                        obj2 = copy.copy(self)
                        obj2.__class__ = model
                        return obj2
                else:
                    t = self.type
                    if t in s:
                        if hasattr(self, s[t]["table"].lower()):
                            return getattr(self, s[t]["table"].lower())
                        else:
                            model = apps.get_model(s[t]["app"], s[t]["table"])
                            obj2 = copy.copy(self)
                            obj2.__class__ = model
                            return obj2
        return self

    def template_for_object(self, view, context, doc_type):
        if self.id and doc_type in ("html", "json"):
            if hasattr(self, "get_structure"):
                s = self.get_structure()
                t = self.type
                if t in s:
                    names = [
                        s[t]["app"].lower() + "/" + s[t]["table"].lower() + ".html",
                    ]
                    return names
        return None

    @staticmethod
    def _get_new_buttons(elem_type="ROOT"):
        buttons = []

        if hasattr(Element, "get_structure"):
            s = Element.get_structure()
            if elem_type in s:
                if "next" in s[elem_type]:
                    for item in s[elem_type]["next"]:
                        if item in s:
                            button = {}
                            button["type"] = item
                            if "title" in s[item]:
                                button["title"] = s[item]["title"]
                            else:
                                button["title"] = item
                            if "app" in s[item]:
                                button["app"] = s[item]["app"]
                            else:
                                button["app"] = ""
                            if "table" in s[item]:
                                button["table"] = s[item]["table"]
                            else:
                                button["table"] = ""

                            buttons.append(button)
        return buttons

    @staticmethod
    def get_root_new_buttons():
        return Element._get_new_buttons("ROOT")

    def get_new_buttons(self):
        if self.type in ("O-GRP", "I-GRP"):
            obj = self
            while obj and obj.type in ("O-GRP", "I-GRP"):
                obj = obj.parent
            if obj:
                buttons = self._get_new_buttons(obj.type)
            else:
                buttons = self._get_new_buttons("ROOT")
            if self.description and "(" in self.description and ")" in self.description:
                item = self.description.split("(")[1].split(")")[0]
                if not "," in item and not ";" in item:
                    s = Element.get_structure()
                    if item in s:
                        button = {}
                        button["type"] = item
                        if "title" in s[item]:
                            button["title"] = s[item]["title"]
                        else:
                            button["title"] = item
                        if "app" in s[item]:
                            button["app"] = s[item]["app"]
                        else:
                            button["app"] = ""
                        if "table" in s[item]:
                            button["table"] = s[item]["table"]
                        else:
                            button["table"] = ""
                        if not button in buttons:
                            buttons.append(button)
                ret = []
                for button in buttons:
                    if button["type"] in self.description:
                        ret.append(button)
                return ret
            else:
                return buttons

        else:
            return self._get_new_buttons(self.type)

    objects = ElementManager()


admin.site.register(Element)


class DocReg(models.Model):
    class Meta:
        verbose_name = _("Document register")
        verbose_name_plural = _("Document registers")
        default_permissions = ("add", "change", "delete", "list")
        app_label = "schelements"

        ordering = ["id"]

    app = models.CharField(
        "Application",
        null=False,
        blank=False,
        editable=True,
        db_index=True,
        max_length=16,
    )
    name = models.CharField(
        "Name", null=False, blank=False, editable=True, db_index=True, max_length=32
    )
    group = models.CharField(
        "Group", null=True, blank=True, editable=True, db_index=True, max_length=64
    )
    description = models.CharField(
        "Description", null=False, blank=False, editable=True, max_length=64
    )
    head_form = models.TextField(
        "Head form",
        null=True,
        blank=True,
        editable=False,
    )
    head_template = models.TextField(
        "Head template",
        null=True,
        blank=True,
        editable=False,
    )
    item_form = models.TextField(
        "Item form",
        null=True,
        blank=True,
        editable=False,
    )
    item_template = models.TextField(
        "Item template",
        null=True,
        blank=True,
        editable=False,
    )
    save_head_fun = models.TextField(
        "Save head function",
        null=True,
        blank=True,
        editable=False,
    )
    save_item_fun = models.TextField(
        "Save item function",
        null=True,
        blank=True,
        editable=False,
    )
    access_fun = models.TextField(
        "Access function",
        null=True,
        blank=True,
        editable=False,
    )
    update_time = models.DateTimeField(
        "Time of the last update",
        null=False,
        blank=False,
        editable=True,
        auto_now_add=True,
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.update_time = datetime.datetime.now()
        super().save(*args, **kwargs)

    def get_parent(self):
        if "/" in self.name:
            x = self.name.rsplit("/", 1)
            objs = DocReg.objects.filter(name=x[0])
            if len(objs) == 1:
                return objs[0]
        return None

    def get_last_subname(self):
        if "/" in self.name:
            return self.name.rsplit("/", 1)[1]
        else:
            return self.name


admin.site.register(DocReg)


class DocType(models.Model):
    class Meta:
        verbose_name = _("Type of document")
        verbose_name_plural = _("Types of documents")
        default_permissions = ("add", "change", "delete", "list")
        app_label = "schelements"

        ordering = ["id"]

    parent = ext_models.PtigHiddenForeignKey(
        DocReg,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        editable=True,
        verbose_name="Parent",
        db_index=True,
    )
    name = models.CharField(
        "Name", null=False, blank=False, editable=True, db_index=True, max_length=16
    )
    description = models.CharField(
        "Description", null=False, blank=False, editable=True, max_length=64
    )
    correction = models.BooleanField(
        "Correction",
        null=True,
        blank=True,
        editable=True,
        db_index=True,
    )
    head_form = models.TextField(
        "Head form",
        null=True,
        blank=True,
        editable=False,
    )
    head_template = models.TextField(
        "Head template",
        null=True,
        blank=True,
        editable=False,
    )
    item_form = models.TextField(
        "Item form",
        null=True,
        blank=True,
        editable=False,
    )
    item_template = models.TextField(
        "Item template",
        null=True,
        blank=True,
        editable=False,
    )
    save_head_fun = models.TextField(
        "Save head function",
        null=True,
        blank=True,
        editable=False,
    )
    save_item_fun = models.TextField(
        "Save item function",
        null=True,
        blank=True,
        editable=False,
    )
    doctype_status = models.CharField(
        "Status of document type",
        null=True,
        blank=True,
        editable=True,
        choices=doctype_status,
        db_index=True,
        max_length=1,
    )
    update_time = models.DateTimeField(
        "Time of the last update",
        null=False,
        blank=False,
        editable=True,
        auto_now_add=True,
    )

    def __str__(self):
        return self.name


admin.site.register(DocType)


class DocHead(JSONModel):
    class Meta:
        verbose_name = _("Document header")
        verbose_name_plural = _("Document headers")
        default_permissions = ("add", "change", "delete", "list")
        app_label = "schelements"

        ordering = ["id"]

    parents = models.ManyToManyField(
        "self",
        null=False,
        blank=False,
        editable=False,
        verbose_name="Parents",
        db_index=True,
    )
    doc_type_parent = ext_models.PtigHiddenForeignKey(
        DocType,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        editable=False,
        verbose_name="Document type parent",
        db_index=True,
    )
    parent_element = ext_models.PtigHiddenForeignKey(
        Element,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        editable=False,
        verbose_name="Parent element",
        db_index=True,
    )
    number = models.CharField(
        "Document number",
        null=True,
        blank=True,
        editable=True,
        db_index=True,
        max_length=32,
    )
    date_c = models.DateTimeField(
        "Creation date",
        null=False,
        blank=False,
        editable=False,
        default=datetime.datetime.now,
    )
    date = models.DateField(
        "Date",
        null=True,
        blank=True,
        editable=True,
        default=datetime.date.today,
        db_index=True,
    )
    description = models.CharField(
        "Description", null=True, blank=True, editable=True, max_length=128
    )
    comments = models.CharField(
        "Comments", null=True, blank=True, editable=True, max_length=256
    )
    status = models.CharField(
        "Status", null=True, blank=True, editable=False, db_index=True, max_length=16
    )
    operator = models.CharField(
        "Operator", null=True, blank=True, editable=False, max_length=32
    )
    param1 = models.CharField(
        "Parameter 1",
        null=True,
        blank=True,
        editable=True,
        db_index=True,
        max_length=16,
    )
    param2 = models.CharField(
        "Parameter 2",
        null=True,
        blank=True,
        editable=True,
        db_index=True,
        max_length=16,
    )
    param3 = models.CharField(
        "Parameter 3",
        null=True,
        blank=True,
        editable=True,
        db_index=True,
        max_length=16,
    )

    def __str__(self):
        return self.doc_type_parent.name + ":" + self.number

    @classmethod
    def get_documents_for_reg(cls, value):
        reg = DocReg.objects.filter(name=value.replace("_", "/"))
        ret = []
        if len(reg) == 1:
            docs = DocType.objects.filter(parent=reg[0])
            for doc in docs:
                ret.append(doc)
        return ret

    @classmethod
    def filter(cls, value):
        if value and value.startswith("_code_"):
            code = value.replace("_code_", "")
            return cls.objects.filter(parent_element__code=code)
        elif value and value.startswith("_pk_"):
            i = value.replace("_pk_", "")
            x = cls.objects.filter(parent_element__pk=int(i))
            return x
        elif value:
            rej = value.replace("_", "/")
            return cls.objects.filter(doc_type_parent__parent__name=rej)
        else:
            return cls.objects.all()

    def init_new(self, request, view, add_param=None):
        if add_param:
            docs = DocType.objects.filter(name=add_param)
            if len(docs) == 1:
                self.doc_type_parent = docs[0]
                self.date = datetime.datetime.now()
                self.status = "draft"
                self.operator = request.user.username

        return None

    @staticmethod
    def template_for_list(view, model, context, doc_type):
        if doc_type in ("html", "json") and "filter" in context:
            tmp = DocReg.objects.filter(name=context["filter"].replace("_", "/"))
            reg = tmp.first()
            if len(tmp) == 1:
                names = []
                if reg and reg.head_template:
                    names.append("db/DocReg-%d-head_template.html" % reg.id)

                x = tmp[0]
                while x:
                    names.append(
                        (
                            x.app
                            + "/"
                            + x.name.replace("/", "_")
                            + "_dochead_list.html"
                        ).lower()
                    )
                    x = x.get_parent()

                if "target" in view.kwargs and "calendar" in view.kwargs["target"]:
                    names2 = []
                    for name in names:
                        names2.append(
                            name.replace(".html", "_" + view.kwargs["target"] + ".html")
                        )
                    names = names2

                # template = select_template(names)
                names.append(view.template_name)
                return names
                # if template:
                #    return template

        return None

    def template_for_object(self, view, context, doc_type):
        if doc_type in ("html", "json"):
            try:
                if "add_param" in view.kwargs:
                    objects = DocType.objects.filter(name=view.kwargs["add_param"])
                    doc_type = objects[0]
                    reg = doc_type.parent
                    obj = None
                else:
                    obj = DocHead.objects.get(pk=self.id)
                    reg = obj.doc_type_parent.parent
                names = []

                if reg.head_template:
                    names.append("db/DocReg-%d-head_template.html" % reg.id)

                names.append(
                    "%s/%s" % (self._meta.app_label, self._meta.model.__name__)
                )
                if obj:
                    names.append(
                        (
                            reg.app
                            + "/"
                            + obj.doc_type_parent.name
                            + "_dochead_edit.html"
                        ).lower()
                    )
                else:
                    names.append(
                        (reg.app + "/" + doc_type.name + "_dochead_edit.html").lower()
                    )
                names.append(
                    (
                        reg.app
                        + "/"
                        + reg.name.replace("/", "_")
                        + "_dochead_edit.html"
                    ).lower()
                )
                x = reg.get_parent()
                while x:
                    names.append(
                        (
                            x.app
                            + "/"
                            + x.name.replace("/", "_")
                            + "_dochead_edit.html"
                        ).lower()
                    )
                    x = x.get_parent()
                names.append(context["view"].template_name)
                return names
                # template = select_template(names)
                # if template:
                #    return template
            except:
                return None
        return None

    def get_form_source(self):
        if self.id:
            obj = DocHead.objects.get(pk=self.id)
            if obj.doc_type_parent.head_form:
                return obj.doc_type_parent.head_form

            x = obj.doc_type_parent.parent
            while x:
                if x.head_form:
                    return x.head_form
                x = x.get_parent()

        return None

    def save(self, *args, **kwargs):
        if self.id:
            obj = DocHead.objects.get(pk=self.id)
            save_fun_src = None
            if obj.doc_type_parent.save_head_fun:
                save_fun_src = obj.doc_type_parent.save_head_fun
            else:
                x = obj.doc_type_parent.parent
                while x:
                    if x.save_head_fun:
                        save_fun_src = x.save_head_fun
                        break
                    x = x.get_parent()
            if save_fun_src:
                content_to_function(save_fun_src, "object")(self)

        if not self.pk:
            self.date_c = datetime.datetime.now()

            y = "%04d" % datetime.date.today().year
            t = self.doc_type_parent.name
            objects = DocHead.objects.filter(
                doc_type_parent=self.doc_type_parent, number__startswith=t + "/" + y
            ).order_by("-number")
            if len(objects) > 0:
                tmp = objects[0].number

                try:
                    max_num = int(tmp.split("/")[-1]) + 1
                except:
                    max_num = 1
            else:
                max_num = 1
            self.number = "%s/%s/%06d" % (t, y, max_num)

        super().save(*args, **kwargs)

    def get_visible_statuses(self, request=None):
        if self.id:
            obj = self
            reg = obj.doc_type_parent.parent
            parent_reg = reg
            if hasattr(reg, "cached_statuses"):
                statuses_to_cache = reg.cached_statuses
            else:
                statuses_to_cache = []
                while reg:
                    statuses = reg.docregstatus_set.all().order_by("order")
                    if len(statuses) > 0:
                        statuses_to_cache += list(statuses)
                    reg = reg.get_parent()
                setattr(parent_reg, "cached_statuses", statuses_to_cache)
            ret = []
            for status in statuses_to_cache:
                if status.can_set_proc:
                    data = content_to_function(
                        status.can_set_proc, "request, doc_head"
                    )(request, self)
                    if data:
                        ret.append(status)
                else:
                    ret.append(status)
            return ret
        return []

    def status_can_be_undo(self, request=None):
        if self.id:
            obj = DocHead.objects.get(pk=self.id)
            reg = obj.doc_type_parent.parent
            statuses = reg.docregstatus_set.filter(name=obj.status)
            if len(statuses) == 1:
                status = statuses[0]
                if status.can_undo_proc:
                    data = content_to_function(
                        status.can_undo_proc, "request, doc_head"
                    )(request, self)
                    if data:
                        return True
                    else:
                        return False
            if obj.status == "" or obj.status == "edit":
                return False
            else:
                return True

        return False

    def get_reg_status(self):
        reg = self.doc_type_parent.parent
        if hasattr(reg, "cached_statuses"):
            statuses = reg.cached_statuses
            for status in statuses:
                if status.name == self.status:
                    return status
        else:
            statuses = reg.docregstatus_set.filter(name=self.status)
            if len(statuses) > 0:
                return statuses[0]
        return None

    def get_undo_target(self):
        reg = self.doc_type_parent.parent
        statuses = reg.docregstatus_set.filter(name=self.status)
        if len(statuses) > 0:
            status = statuses[0]
            return status.get_undo_target()
        return "refresh_frame"

    def get_derived_object(self, param=None):
        t = None
        if type(self) == DocHead:
            if param and "view" in param and "add_param" in param["view"].kwargs:
                t = param["view"].kwargs["add_param"]
                if t == "-":
                    return self
                object_list = DocType.objects.filter(name=t)
                if len(object_list):
                    t = object_list[0].parent.name
                return ContentType.objects.get(
                    model=t.lower() + "dochead"
                ).model_class()()
            else:
                t = self.doc_type_parent.parent.name
                name = t.lower() + "dochead"
                if hasattr(self, name):
                    return getattr(self, name)
        return self

    @classmethod
    def table_action(cls, list_view, request, data):
        return standard_table_action(
            cls, list_view, request, data, ["copy", "paste", "delete"]
        )

    @staticmethod
    def filter_by_permissions(view, queryset_or_obj, request):
        q = None
        doc_regs = None

        if hasattr(request, "user") and request.user.is_superuser:
            return queryset_or_obj

        if hasattr(request, "user") and hasattr(request.user, "profile"):
            profile = request.user.profile
            if profile.doc_regs:
                doc_regs = list(
                    [
                        item.strip()
                        for item in profile.doc_regs.replace(",", ";").split(";")
                        if item.strip()
                    ]
                )
        else:
            profile = None

        def append_reg_filter(reg):
            nonlocal q, profile
            q2 = Q(doc_type_parent__parent__name=reg.name)
            if reg.access_fun:
                exec(reg.access_fun)
                if "q_for_list" in locals():
                    q2 = locals()["q_for_list"](request, request.user, profile)
            if q2:
                if q:
                    q = q | q2
                else:
                    q = q2

        if queryset_or_obj != None:
            if "filter" in view.kwargs and not view.kwargs["filter"].startswith("_"):
                reg_name = view.kwargs["filter"].replace("_", "/")
                if doc_regs:
                    if not reg_name in doc_regs:
                        return queryset_or_obj.filter(pk=0)
                reg = DocReg.objects.get(name=reg_name)
                append_reg_filter(reg)
            else:
                regs = DocReg.objects.all()
                for reg in regs:
                    if not doc_regs or (doc_regs and reg in doc_regs):
                        append_reg_filter(reg)
            if q:
                return queryset_or_obj.filter(q)
            else:
                return queryset_or_obj
        else:
            return queryset_or_obj

    def _check_perm(self, user, perm):
        # perm: add, change, delete, view
        reg = self.doc_type_parent.parent
        if reg.access_fun:
            exec(reg.access_fun)
            if "check_user_perm" in locals():
                return locals()["check_user_perm"](
                    self, user, perm, self.doc_type_parent.name
                )
            else:
                return True

    def can_change(self, user):
        return self._check_perm(user, "change")

    def can_delete(self, user):
        return self._check_perm(user, "delete")

    def can_view(self, user):
        return self._check_perm(user, "view")

    @staticmethod
    def can_add(doc_type_name, user):
        doc_type = DocType.objects.get(name=doc_type_name)
        reg = doc_type.parent
        if reg.access_fun:
            exec(reg.access_fun)
            if "check_user_perm" in locals():
                check = locals()["check_user_perm"](None, user, "add", doc_type_name)
                return check
            else:
                return True


admin.site.register(DocHead)


class DocItem(JSONModel):
    class Meta:
        verbose_name = _("Document item")
        verbose_name_plural = _("Document items")
        default_permissions = ("add", "change", "delete", "list")
        app_label = "schelements"

        ordering = ["id"]

    parent = ext_models.PtigHiddenForeignKey(
        DocHead,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        editable=False,
        verbose_name="Parent",
        db_index=True,
    )
    parent_item = ext_models.PtigHiddenForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        editable=False,
        verbose_name="Parent item",
        db_index=True,
    )
    owner = ext_models.PtigForeignKey(
        Element,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        editable=True,
        verbose_name="Owner",
        db_index=True,
        related_name="owners",
    )
    order = models.IntegerField(
        "Order",
        null=False,
        blank=False,
        editable=False,
        default=1,
    )
    item = ext_models.PtigForeignKey(
        Element,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        editable=True,
        verbose_name="Item",
        db_index=True,
    )
    amount = models.DecimalField(
        "Amount", null=True, blank=True, editable=True, max_digits=16, decimal_places=2
    )
    alt_amount = models.DecimalField(
        "Amount", null=True, blank=True, editable=True, max_digits=16, decimal_places=2
    )
    alt_unit = models.CharField(
        "Alternate unit", null=True, blank=True, editable=True, max_length=32
    )
    description = models.CharField(
        "Description", null=True, blank=True, editable=True, max_length=255
    )
    level = models.IntegerField(
        "Level",
        null=False,
        blank=False,
        editable=False,
        default=0,
    )
    active = models.BooleanField(
        "Active item",
        null=False,
        blank=False,
        editable=True,
        default=True,
        db_index=True,
    )
    param1 = models.CharField(
        "Parameter 1",
        null=True,
        blank=True,
        editable=False,
        db_index=True,
        max_length=16,
    )
    param2 = models.CharField(
        "Parameter 2",
        null=True,
        blank=True,
        editable=False,
        db_index=True,
        max_length=16,
    )
    param3 = models.CharField(
        "Parameter 3",
        null=True,
        blank=True,
        editable=False,
        db_index=True,
        max_length=16,
    )

    @staticmethod
    def template_for_list(view, model, context, doc_type):
        if doc_type in ("html", "json"):
            if "parent_pk" in context["view"].kwargs:
                parent_pk = int(context["view"].kwargs["parent_pk"])
                dochead = DocHead.objects.get(pk=parent_pk)
                reg = dochead.doc_type_parent.parent
                names = []
                if reg.item_template:
                    names.append("db/DocReg-%d-item_template.html" % reg.id)
                names.append(
                    (
                        reg.app
                        + "/"
                        + dochead.doc_type_parent.name
                        + "_docitem_list.html"
                    ).lower()
                )
                names.append(
                    (
                        reg.app
                        + "/"
                        + reg.name.replace("/", "_")
                        + "_docitem_list.html"
                    ).lower()
                )

                x = reg.get_parent()
                while x:
                    names.append(
                        x.app + "/" + x.name.replace("/", "_") + "_docitem_list.html"
                    )
                    x = x.get_parent()
                names.append(view.template_name)
                return names

        return None

    def template_for_object(self, view, context, doc_type):
        if doc_type in ("html", "json"):
            try:
                obj = DocItem.objects.get(pk=self.id)
                dochead = obj.parent
            except:
                dochead = context["view"].object.parent

            reg = dochead.doc_type_parent.parent
            names = []
            if reg.item_template:
                names.append("db/DocReg-%d-item_template.html" % reg.id)
            names.append(
                (
                    reg.app
                    + "/"
                    + dochead.doc_type_parent.parent.name
                    + "_docitem_edit.html"
                ).lower()
            )
            names.append(
                (
                    reg.app + "/" + reg.name.replace("/", "_") + "_docitem_edit.html"
                ).lower()
            )
            x = reg.get_parent()
            while x:
                names.append(
                    x.app + "/" + x.name.replace("/", "_") + "_docitem_edit.html"
                )
                x = x.get_parent()

            names.append(
                context["view"].template_name.replace(reg.app + "/", "schelements/")
            )
            return names
        return None

    def get_form_source(self):
        obj = self
        if obj.parent.doc_type_parent.item_form:
            return obj.parent.doc_type_parent.item_form

        x = obj.parent.doc_type_parent.parent
        while x:
            if x.item_form:
                return x.item_form
            x = x.get_parent()

        return None

    def init_new(self, request, view, param=None):
        if "parent_pk" in view.kwargs:
            parent_pk = view.kwargs["parent_pk"]
            parent = DocHead.objects.get(pk=parent_pk)
            items = DocItem.objects.filter(parent=parent).order_by("-order")
            if len(items) > 0:
                max_nr = int(items[0].order) + 1
            else:
                max_nr = 1

            if request.POST:
                return {
                    "parent": str(parent.id),
                    "order": max_nr,
                    "date_c": datetime.datetime.now(),
                    "level": 0,
                }

        return None

    def save(self, *args, **kwargs):
        if self.id:
            obj = DocItem.objects.get(pk=self.id).parent
            save_fun_src = None
            if obj.doc_type_parent.save_head_fun:
                save_fun_src = obj.doc_type_parent.save_item_fun
            else:
                x = obj.doc_type_parent.parent
                while x:
                    if x.save_head_fun:
                        save_fun_src = x.save_item_fun
                        break
                    x = x.get_parent()
            if save_fun_src:
                exec(save_fun_src)

        super().save(*args, **kwargs)

    def get_derived_object(self, param=None):
        t = None
        if type(self) == DocItem:
            if param and "view" in param and "add_param" in param["view"].kwargs:
                t = param["view"].kwargs["add_param"]
                if t == "-":
                    return self
                return ContentType.objects.get(
                    model=t.lower() + "docitem"
                ).model_class()()
            else:
                t = self.parent.doc_type_parent.parent.name
                name = t.lower() + "docitem"
                if hasattr(self, name):
                    return getattr(self, name)
                else:
                    obj2 = copy.copy(self)
                    obj2.__class__ = ContentType.objects.get(model=name).model_class()
                    return obj2
        return self

    def get_period(self):
        return "%04d-%02d" % (self.parent.date.year, self.parent.date.month)

    def new_account_operation(
        self,
        target,
        account_name,
        description,
        sign,
        amount,
        element,
        classifier1value=None,
        classifier2value=None,
        classifier3value=None,
        subcode=None,
        payment=None,
        save=True,
    ):
        if subcode == "*":
            account = Account.objects.get(name=account_name)
            object_list = AccountState.get_account_state(
                target,
                account,
                element,
                classifier1valu,
                classifier2value,
                classifier3value,
                "*",
                None,
            )
            subcode_sum = (
                object_list.values("subcode")
                .annotate(csum=Sum("credit"), dsum=sum("debit"))
                .order_by("subcode")
            )
            a = amount
            ret = []
            for s in subcode_sum:
                subcode2 = s["subcode"]
                c = s["credit"]
                d = s["debit"]
                b = d - s
                if b > a:
                    a2 = a
                    a = 0
                else:
                    a2 = b
                    a -= b
                x = self.new_account_operation(
                    target,
                    account_name,
                    description,
                    sign,
                    a2,
                    element,
                    classifier1value,
                    classifier2value,
                    classifier3value,
                    subcode2,
                    payment,
                    save,
                )
                ret.append(x)
                if a == 0:
                    return ret
        else:
            account = Account.objects.get(name=account_name)
            period = self.get_period()
            object_list = AccountState.objects.filter(
                parent=account,
                element=element,
                target=target,
                classifier1value=classifier1value,
                classifier2value=classifier2value,
                classifier3value=classifier3value,
                period=period,
            )
            if object_list.count() > 0:
                object = object_list[0]
            else:
                object = AccountState()
                object.parent = account
                object.element = element
                object.target = target
                object.classifier1value = classifier1value
                object.classifier2value = classifier2value
                object.classifier3value = classifier3value
                object.period = period
                object.debit = 0
                object.credit = 0
                object.agregate = False
                object.save()
            account_operation = AccountOperation()
            account_operation.parent = self
            account_operation.description = description
            account_operation.payment = payment
            account_operation.account_state = object
            account_operation.sign = sign
            account_operation.amount = amount
            account_operation.enabled = False
            if save:
                account_operation.save()
            return [
                account_operation,
            ]


admin.site.register(DocItem)


class DocRegStatus(models.Model):
    class Meta:
        verbose_name = _("Document status")
        verbose_name_plural = _("Document status")
        default_permissions = ("add", "change", "delete", "list")
        app_label = "schelements"

        ordering = ["id"]

    parent = ext_models.PtigHiddenForeignKey(
        DocReg,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        editable=True,
        verbose_name="Parent",
        db_index=True,
    )
    order = models.IntegerField(
        "Order",
        null=False,
        blank=False,
        editable=True,
    )
    name = models.CharField(
        "Name", null=False, blank=False, editable=True, max_length=16
    )
    description = models.CharField(
        "Description", null=True, blank=True, editable=True, max_length=64
    )
    icon = models.CharField("Icon", null=True, blank=True, editable=True, max_length=64)
    accept_proc = models.TextField(
        "Accept status procedure",
        null=True,
        blank=True,
        editable=False,
    )
    undo_proc = models.TextField(
        "Undo status procedure",
        null=True,
        blank=True,
        editable=False,
    )
    can_set_proc = models.TextField(
        "Check if status can be set",
        null=True,
        blank=True,
        editable=False,
    )
    can_undo_proc = models.TextField(
        "Check if status can be removed",
        null=True,
        blank=True,
        editable=False,
    )
    accept_form = models.TextField(
        "Form for accept",
        null=True,
        blank=True,
        editable=False,
    )
    undo_form = models.TextField(
        "Form for undo",
        null=True,
        blank=True,
        editable=False,
    )

    def __str__(self):
        return self.name

    def get_editor_header(self, field_name):
        if field_name == "can_set_proc":
            return "def can_set_proc(request, doc_head):"
        elif field_name == "can_undo_proc":
            return "def can_undo_proc(request, doc_head):"
        elif field_name == "accept_proc":
            return "def accept_proc(request, doc_head, reg_status, doc_type, doc_reg, form):"
        elif field_name == "undo_proc":
            return (
                "def undo_proc(request, doc_head, reg_status, doc_type, doc_reg, form):"
            )

    def get_accept_target(self):
        if self.accept_form:
            return "popup_edit"
        else:
            return "refresh_frame"

    def get_undo_target(self):
        if self.undo_form:
            return "popup_edit"
        else:
            return "refresh_frame"


admin.site.register(DocRegStatus)


class DocHeadStatus(JSONModel):
    class Meta:
        verbose_name = _("Document head status")
        verbose_name_plural = _("Documents head status")
        default_permissions = ("add", "change", "delete", "list")
        app_label = "schelements"

        ordering = ["id"]

    parent = ext_models.PtigHiddenForeignKey(
        DocHead,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        editable=True,
        verbose_name="Parent",
        db_index=True,
    )
    date = models.DateTimeField(
        "Date",
        null=False,
        blank=False,
        editable=True,
        db_index=True,
    )
    name = models.CharField(
        "Name", null=False, blank=False, editable=True, max_length=16
    )
    description = models.CharField(
        "Description", null=True, blank=True, editable=False, max_length=64
    )
    operator = models.CharField(
        "Operator", null=True, blank=True, editable=True, max_length=32
    )

    def __str__(self):
        return self.name


admin.site.register(DocHeadStatus)


class Account(TreeModel):
    class Meta:
        verbose_name = _("Account")
        verbose_name_plural = _("Account")
        default_permissions = ("add", "change", "delete", "list")
        app_label = "schelements"

        ordering = ["id"]

    parent = ext_models.PtigTreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        editable=True,
        verbose_name="Parent",
        db_index=True,
    )
    type1 = models.CharField(
        "Type 1",
        null=True,
        blank=True,
        editable=False,
        choices=account_type_choice_1,
        max_length=1,
    )
    type2 = models.CharField(
        "Type 2",
        null=True,
        blank=True,
        editable=True,
        choices=account_type_choice_2,
        db_index=True,
        max_length=1,
    )
    name = models.CharField(
        "Name", null=False, blank=False, editable=True, db_index=True, max_length=32
    )
    description = models.CharField(
        "Description", null=False, blank=False, editable=True, max_length=256
    )
    correctness_rule = models.CharField(
        "Correctness rule", null=True, blank=True, editable=True, max_length=256
    )
    root_classifier1 = ext_models.PtigForeignKey(
        Element,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        editable=True,
        verbose_name="Root classifier 1",
        related_name="baseaccount_rc1_set",
    )
    root_classifier2 = ext_models.PtigForeignKey(
        Element,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        editable=True,
        verbose_name="Root classifier 2",
        related_name="baseaccount_rc2_set",
    )
    root_classifier3 = ext_models.PtigForeignKey(
        Element,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        editable=True,
        verbose_name="Root classifier 3",
        related_name="baseaccount_rc3_set",
    )
    enabled = models.BooleanField(
        "Enabled",
        null=True,
        blank=False,
        editable=True,
        default=True,
        db_index=True,
    )

    def save(self, *args, **kwargs):
        if self.parent:
            self.parent.type1 = "S"
            self.parent.save()
            self.type2 = self.parent.type2
        self.type1 = "A"
        super().save(*args, **kwargs)

    def __str__(self):
        x = self
        ret = self.name
        while x.parent:
            x = x.parent
            ret = x.name + "/" + ret
        ret += ": "
        ret += self.description
        return ret


admin.site.register(Account)


class AccountState(models.Model):
    class Meta:
        verbose_name = _("State of account")
        verbose_name_plural = _("States of account")
        default_permissions = ("add", "change", "delete", "list")
        app_label = "schelements"

        ordering = ["id"]

    parent = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        editable=True,
        verbose_name="Parent",
        db_index=True,
    )
    target = models.ForeignKey(
        Element,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        editable=True,
        verbose_name="Target",
        db_index=True,
        related_name="state_targets",
    )
    classifier1value = models.ForeignKey(
        Element,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        editable=True,
        verbose_name="Classifier 1 value",
        db_index=True,
        related_name="account_c1_set",
    )
    classifier2value = models.ForeignKey(
        Element,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        editable=True,
        verbose_name="Classifier 2 value",
        db_index=True,
        related_name="account_c2_set",
    )
    classifier3value = models.ForeignKey(
        Element,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        editable=True,
        verbose_name="Classifier 3 value",
        db_index=True,
        related_name="account_c3_set",
    )
    period = models.CharField(
        "Period", null=True, blank=True, editable=True, db_index=True, max_length=10
    )
    subcode = models.CharField(
        "Subcode", null=True, blank=True, editable=True, db_index=True, max_length=16
    )
    element = models.ForeignKey(
        Element,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        editable=True,
        verbose_name="Element",
        db_index=True,
    )
    debit = models.DecimalField(
        "Debit", null=False, blank=False, editable=True, max_digits=16, decimal_places=2
    )
    credit = models.DecimalField(
        "Credit",
        null=False,
        blank=False,
        editable=True,
        max_digits=16,
        decimal_places=2,
    )
    zero_balance = models.BooleanField(
        "None",
        null=True,
        blank=True,
        editable=True,
        default=True,
        db_index=True,
    )
    aggregate = models.BooleanField(
        "Aggregate",
        null=True,
        blank=False,
        editable=True,
        default=False,
    )
    date_c = models.DateTimeField(
        "Creation date",
        null=False,
        blank=False,
        editable=True,
        default=datetime.datetime.now,
    )

    def __str__(self):
        s = self.target.name + "/" + self.parent.name
        if self.classifier1value:
            s += "/" + classifier1value
        if self.classifier2value:
            s += "/" + classifier2value
        if self.classifier3value:
            s += "/" + classifier3value
        if self.subcode:
            s += self.subcode
        s += "(" + self.element.name + ")"
        return s

    @staticmethod
    def get_account_state(
        target=None,
        account=None,
        element=None,
        classifier1value=None,
        classifier2value=None,
        classifier3value=None,
        subcode=None,
        period=None,
        q=None,
    ):
        object_list = AccountState.objects.all()
        if target != None:
            if isinstance(target, int):
                object_list = object_list.filter(target__id=target)
            elif isinstance(target, Element):
                object_list = object_list.filter(target=target)
            elif isinstance(target, str):
                object_list = object_list.filter(target__code=target)
            else:
                return None
        else:
            object_list = object_list.filter(target__isnull=True)

        if account != None:
            if isinstance(target, int):
                object_list = object_list.filter(parent__id=account)
            elif isinstance(target, Account):
                object_list = object_list.filter(parent=account)
            elif isinstance(target, str):
                object_list = object_list.filter(parent__name=account)
            else:
                return None

        if elementt != None:
            if isinstance(element, int):
                object_list = object_list.filter(element__id=element)
            elif isinstance(element, Element):
                object_list = object_list.filter(element=element)
            elif isinstance(target, str):
                object_list = object_list.filter(element__code=element)
            else:
                return None
        else:
            object_list = object_list.filter(element__isnull=True)

        if classifier1value != None:
            if isinstance(classifier1value, int):
                object_list = object_list.filter(classifier1value__id=classifier1value)
            elif isinstance(classifier, Element):
                object_list = object_list.filter(classifier1value=classifier1value)
            elif isinstance(classifier, str):
                object_list = object_list.filter(
                    classifier1value__code=classifier1value
                )
            else:
                return None
        else:
            object_list = object_list.filter(classifier1value__isnull=True)

        if classifier2value != None:
            if isinstance(classifier2value, int):
                object_list = object_list.filter(classifier2value__id=classifier2value)
            elif isinstance(classifier, Element):
                object_list = object_list.filter(classifier2value=classifier2value)
            elif isinstance(classifier, str):
                object_list = object_list.filter(
                    classifier2value__code=classifier2value
                )
            else:
                return None
        else:
            object_list = object_list.filter(classifier2value__isnull=True)

        if classifier3value != None:
            if isinstance(classifier3value, int):
                object_list = object_list.filter(classifier3value__id=classifier3value)
            elif isinstance(classifier, Element):
                object_list = object_list.filter(classifier3value=classifier3value)
            elif isinstance(classifier, str):
                object_list = object_list.filter(
                    classifier3value__code=classifier3value
                )
            else:
                return None
        else:
            object_list = object_list.filter(classifier3value__isnull=True)

        if subcode:
            object_list = object_list.filter(subcode=subcode)
        else:
            object_list = object_list.filter(
                Q(subcode__isnull=True) | Q(subcode__exact="")
            )

        if period:
            object_list = object_list.filter(period=period)
        else:
            object_list = object_list.filter(
                Q(period__isnull=True) | Q(period__exact="")
            )

        if q:
            object_list = object_list.filter(q)

        return object_list

    @staticmethod
    def get_balance(
        target=None,
        account=None,
        element=None,
        classifier1value=None,
        classifier2value=None,
        classifier3value=None,
        subcode=None,
        period=None,
        q=None,
    ):
        ret = AccountState.get_account_state(
            target,
            account,
            element,
            classifier1value,
            classifier2value,
            classifier3value,
            subcode,
            period,
            q,
        )
        result = ret.aggregate(Sum("credit"), Sum("debit"))
        result["balance__sum"] = result["debit__sum"] - result["credit__sum"]
        return result

    def save(self, *args, **kwargs):
        if self.parent.correctness_rule:
            x = self.parent.correctness_rule.split(":")
            if len(x) > 1:
                expression = x[0]
                error_txt = x[1]
            else:
                expression = x[0]
                error_txt = (
                    "The validation rule is not ensured: "
                    + self.parent.correctness_rule
                )

            s = expression.replace("DEBIT", str(self.debit)).replace(
                "CREDIT", str(self.credit)
            )
            if self.period:
                s = s.replace("PERIOD", self.period)
            ret = eval(s)
            if not ret:
                raise ValueError(error_txt)
        if self.debit == self.credit:
            self.zero_balance = True
        else:
            self.zero_balance = False
        super().save(*args, **kwargs)


admin.site.register(AccountState)


class AccountOperation(models.Model):
    class Meta:
        verbose_name = _("Account operation")
        verbose_name_plural = _("Account operations")
        default_permissions = ("add", "change", "delete", "list")
        app_label = "schelements"

        ordering = ["id"]

    parent = ext_models.PtigHiddenForeignKey(
        DocItem,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        editable=True,
        verbose_name="Parent",
        db_index=True,
    )
    date = models.DateField(
        "Date",
        null=False,
        blank=False,
        editable=True,
        default=datetime.date.today,
    )
    date_c = models.DateTimeField(
        "Creation date",
        null=False,
        blank=False,
        editable=False,
        default=datetime.datetime.now,
    )
    description = models.CharField(
        "Description", null=False, blank=False, editable=True, max_length=255
    )
    payment = models.CharField(
        "Name of payment",
        null=True,
        blank=True,
        editable=True,
        db_index=True,
        max_length=64,
    )
    account_state = ext_models.PtigForeignKey(
        AccountState,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        editable=True,
        verbose_name="Account state",
        db_index=True,
        related_name="accountoper_set",
        search_fields=[
            "parent__name__icontains",
        ],
    )
    sign = models.IntegerField(
        "Sign - debit or credit",
        null=False,
        blank=False,
        editable=True,
    )
    amount = models.DecimalField(
        "Amount",
        null=False,
        blank=False,
        editable=True,
        max_digits=16,
        decimal_places=2,
    )
    enabled = models.BooleanField(
        "Enabled",
        null=True,
        blank=True,
        editable=False,
        default=False,
        db_index=True,
    )

    def __str__(self):
        return self.description

    def get_or_create_account_state(
        self,
        target,
        account,
        element,
        classifier1,
        classifier2,
        classifier3,
        subcode,
        period,
    ):
        objs = AccountState.objects.filter(
            parent=account, element=element, subcode=subcode, period=period
        )
        if target:
            objs = objs.filter(target=target)
        else:
            objs = objs.filter(target__isnull=True)

        if classifier1:
            objs = objs.filter(classifier1value=classifier1)
        else:
            objs = objs.filter(classifier1value__isnull=True)

        if classifier2:
            objs = objs.filter(classifier2value=classifier2)
        else:
            objs = objs.filter(classifier2value__isnull=True)

        if classifier3:
            objs = objs.filter(classifier3value=classifier3)
        else:
            objs = objs.filter(classifier3value__isnull=True)

        if subcode:
            objs = objs.filter(subcode=subcode)
        else:
            objs = objs.filter(Q(subcode__isnull=True) | Q(subcode__exact=""))

        if period:
            objs = objs.filter(period=period)
        else:
            objs = objs.filter(Q(period__isnull=True) | Q(period__exact=""))

        if objs.count() > 0:
            return objs[0]
        else:
            obj = AccountState()
            obj.parent = account
            obj.target = target
            obj.classifier1value = classifier1
            obj.classifier2value = classifier2
            obj.classifier3value = classifier3
            obj.period = period
            obj.subcode = subcode
            obj.element = element
            obj.aggregate = True
            obj.debit = 0
            obj.credit = 0
            obj.save()
            return obj

    def _update_account_state(self, account, state, debit, credit, with_subcode):
        targets = (state.target, None) if state.target else (None,)
        classifier1values = (
            (state.classifier1value, None) if state.classifier1value else (None,)
        )
        classifier2values = (
            (state.classifier2value, None) if state.classifier2value else (None,)
        )
        classifier3values = (
            (state.classifier3value, None) if state.classifier3value else (None,)
        )
        periods = (state.period, None) if state.period else (None,)
        subcodes = (state.subcode, None) if state.subcode and with_subcode else (None,)

        for target in targets:
            for classifier1value in classifier1values:
                for classifier2value in classifier2values:
                    for classifier3value in classifier3values:
                        for period in periods:
                            for subcode in subcodes:
                                state = self.get_or_create_account_state(
                                    target,
                                    account,
                                    state.element,
                                    classifier1value,
                                    classifier2value,
                                    classifier3value,
                                    subcode,
                                    period,
                                )
                                state.debit += debit
                                state.credit += credit
                                state.save()

    def update_accounts_state(self, debit, credit):
        state = self.account_state
        account = state.parent
        self._update_account_state(account, state, debit, credit, True)
        account = account.parent
        while account:
            self._update_account_state(account, state, debit, credit, False)
            account = account.parent

    def confirm(self):
        ret = False
        self.refresh_from_db()
        if not self.enabled:
            self.enabled = True
            if self.sign > 0:
                self.update_accounts_state(0, self.amount)
            else:
                self.update_accounts_state(self.amount, 0)
            self.save()
            ret = True
        return ret

    def atomic_confirm(self):
        ret = False
        with transaction.atomic():
            ret = self.confirm()
        return ret

    def cancel_confirmation(self):
        ret = False
        self.refresh_from_db()
        if self.enabled:
            self.enabled = False
            if self.sign > 0:
                self.update_accounts_state(0, -1 * self.amount)
            else:
                self.update_accounts_state(-1 * self.amount, 0)
            self.save()
            ret = True
        return ret

    def atomic_cancel_confirmation(self):
        ret = False
        with transaction.atomic():
            ret = self.cancel_confirmation()
        return ret


admin.site.register(AccountOperation)


class BaseObject(models.Model):
    class Meta:
        verbose_name = _("Base object")
        verbose_name_plural = _("Base objects")
        default_permissions = ("add", "change", "delete", "list")
        app_label = "schelements"

        ordering = ["id"]

        abstract = True

    app = models.CharField(
        "Application",
        null=False,
        blank=False,
        editable=True,
        db_index=True,
        max_length=16,
    )
    name = models.CharField(
        "Name", null=False, blank=False, editable=True, db_index=True, max_length=64
    )
    description = models.CharField(
        "Description", null=False, blank=False, editable=True, max_length=64
    )
    declaration = models.TextField(
        "Declaration",
        null=True,
        blank=True,
        editable=False,
    )
    template_src = models.TextField(
        "Template source",
        null=True,
        blank=True,
        editable=False,
    )
    template = models.TextField(
        "Template",
        null=True,
        blank=True,
        editable=False,
    )
    to_html_rec = models.TextField(
        "Convert fields to html",
        null=True,
        blank=True,
        editable=False,
    )
    save_fun = models.TextField(
        "Save function",
        null=True,
        blank=True,
        editable=False,
    )
    load_fun = models.TextField(
        "Load function",
        null=True,
        blank=True,
        editable=False,
    )
    to_str_fun = models.TextField(
        "Object to str function",
        null=True,
        blank=True,
        editable=False,
    )
    action_template = models.TextField(
        "Action template",
        null=True,
        blank=True,
        editable=False,
    )

    def to_str(self, obj):
        if self.to_str_fun:
            tmp = "def _to_str(self):\n" + "\n".join(
                ["    " + pos for pos in self.to_str_fun.split("\n")]
            )
            exec(tmp)
            return locals()["_to_str"](obj)
        else:
            if obj.title:
                return obj.title + " [" + self.name + "]"
            else:
                return str(obj) + " [" + self.name + "]"

    def get_action_template(self):
        if self.action_template:
            return ihtml_to_html(None, self.action_template)
        else:
            return None
