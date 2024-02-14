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


import copy
from pytigon_lib.schdjangoext.django_ihtml import ihtml_to_html
from django.template.loader import select_template
import datetime
from django.db import transaction
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q, Sum
from django.apps import apps
from django.dispatch import receiver
from django.db.models.signals import post_delete
from django.conf import settings
from django.template import Template, Context

from pytigon_lib.schviews.actions import new_row_ok, update_row_ok
from pytigon_lib.schdjangoext.import_from_db import run_code_from_db_field, ModuleStruct
from pytigon_lib.schdjangoext.fastform import form_from_str, FAST_FORM_EXAMPLE

from pytigon_lib.schdjangoext.django_ihtml import ihtml_to_html
from pytigon_lib.schdjangoext.import_from_db import (
    run_code_from_db_field,
    get_fun_from_db_field,
    ModuleStruct,
)
from pytigon_lib.schtools.tools import is_in_cancan_rules

from pytigon_lib.schviews import actions


def get_element_queryset():
    return None


GET_ELEMENT_QUERYSET = OverwritableCallable(get_element_queryset)


class ElementManager(models.Manager):
    def get_queryset(self):
        q = GET_ELEMENT_QUERYSET()
        if q:
            q2 = super().get_queryset().filter(q)
        else:
            q2 = super().get_queryset()
        return q2.prefetch_related(
            "parent",
            "grand_parent1",
            "grand_parent2",
            "grand_parent3",
            "grand_parent4",
            "first_ancestor",
        )


GROUP_FOR_TYPE = None

STRUCTURE = {
    "ROOT": {"next": ["I-GRP", "O-GRP", "C-GRP"]},
    "O-GRP": {"title": "Group of owners", "table": "Element", "app": "schelements"},
    "O-COM": {"title": "Companies", "table": "Element", "app": "schelements"},
    "O-DIV": {"title": "Divisions", "table": "Element", "app": "schelements"},
    "O-DEP": {"title": "Departaments", "table": "Element", "app": "schelements"},
    "O-POS": {"title": "Positions", "table": "Element", "app": "schelements"},
    "O-EMP": {"title": "Employees", "table": "Element", "app": "schelements"},
    "O-LOC": {"title": "Locations", "table": "Element", "app": "schelements"},
    "O-PER": {"title": "Persons", "table": "Element", "app": "schelements"},
    "O-CUS": {"title": "Customers", "table": "Element", "app": "schelements"},
    "O-SUP": {"title": "Suppliers", "table": "Element", "app": "schelements"},
    "O-DEV": {"title": "Devices", "table": "Element", "app": "schelements"},
    "O-OTH": {"title": "Other owners", "table": "Element", "app": "schelements"},
    "O-ALI": {"title": "Aliases", "table": "Element", "app": "schelements"},
    "I-GRP": {"title": "Group of items", "table": "Element", "app": "schelements"},
    "I-SRV": {"title": "Services", "table": "Element", "app": "schelements"},
    "I-INT": {"title": "Intellectual values", "table": "Element", "app": "schelements"},
    "I-CUR": {"title": "Currency", "table": "Element", "app": "schelements"},
    "I-MAT": {"title": "Materials", "table": "Element", "app": "schelements"},
    "I-RAW": {"title": "Raw materials", "table": "Element", "app": "schelements"},
    "I-PRD": {"title": "Products", "table": "Element", "app": "schelements"},
    "I-IPR": {
        "title": "Intermediate products",
        "table": "Element",
        "app": "schelements",
    },
    "I-MER": {"title": "Merchandises", "table": "Element", "app": "schelements"},
    "I-DEV": {"title": "Devices", "table": "Element", "app": "schelements"},
    "I-PMA": {"title": "Production machines", "table": "Element", "app": "schelements"},
    "I-VEH": {"title": "Vehicles", "table": "Element", "app": "schelements"},
    "I-OTH": {"title": "Other items", "table": "Element", "app": "schelements"},
    "I-ALI": {"title": "Item aliases", "table": "Element", "app": "schelements"},
    "C-SYS": {"title": "Config - system", "table": "Element", "app": "schelements"},
    "C-UNT": {"title": "Units of measure", "table": "Element", "app": "schelements"},
    "C-DIC": {"title": "Dictionaries", "table": "Element", "app": "schelements"},
    "C-OTH": {"title": "Config - others", "table": "Element", "app": "schelements"},
    "C-ALI": {"title": "Config aliases", "table": "Element", "app": "schelements"},
    "C-FLD": {"title": "Config folders", "table": "Element", "app": "schelements"},
    "C-GRP": {"title": "Group of config", "table": "Element", "app": "schelements"},
}

ACCESS_FUN = """#import datetime
#
#def q_for_list(request, user, profile):
#    pass
#
#def check_user_perm(dochead, user, perm, doc_type_name):
#    pass 
    
"""

SAVE_ITEM = """#import datetime
#
#def save(docitem, view, form, request):
#    return True #True if you want to save the object else False
    
"""

SAVE_HEAD = """#import datetime
#
#def save(dochead, view, form, request):
#    return True #True if you want to save the object else False
    
"""


TO_STR = """#Example: 
#import datetime
#
#def to_str(obj):
#    pass

"""

LOAD_BASE_OBJ = """#Example: 
#import datetime
#
#def load(data):
#    return data
    
"""

SAVE_BASE_OBJ = """#Example: 
#import datetime
#
#def save(form, obj):
#    return form.cleaned_data
    
"""

ACCEPT_PROC = """#Example: 
#import datetime
#
#def accept(request, doc_head, reg_status, doc_type, doc_reg, doc_status, form):
#    pass

"""

UNDO_PROC = """#Example: 
#import datetime
#
#def undo(request, doc_head, reg_status, doc_type, doc_reg, doc_status, form):
#    pass

"""

CAN_SET = """#Example: 
#import datetime
#
#def can_set(request, doc_head):
#    pass

"""

CAN_UNDO = """#Example: 
#import datetime
#
#def can_undo(request, doc_head):
#    pass

"""

HEAD_TEMPLATE = """#Example:
#% extends "schelements/dochead.html"
#
#% load exfiltry
#% load exsyntax

"""


ITEM_TEMPLATE = """#Example:
#% extends "schelements/docitem.html"
#
#% load exfiltry
#% load exsyntax

"""

TEMPLATE_SRC = """#Example:
% extends "forms/edit_form.html"

% load exfiltry
% load exsyntax
% load subreport

%% row_edit_form
    % form:

"""

ACTION_TEMPLATE = """#Example
#% load exfiltry
#% load exsyntax
"""

INFO_TEMPLATE = """#Example
#% load exfiltry
#% load exsyntax
"""


TO_STR = """#Example
#import datetime
#
#def to_str(obj):
#    return obj.name
"""

ON_DELETE = """#Example
#import datetime
#
#def on_delete(obj, request, view):
#    pass
"""

ACTION = """#Example
#import datetime
#
#def action(obj, action_name argv):
#    pass
"""

TO_HTML_REC = """#header
#
#body
#    {{ object.opis }}
#
#footer
#

"""

HEAD_FORM = "\n".join(("#" + item for item in FAST_FORM_EXAMPLE.split("\n")))
ITEM_FORM = HEAD_FORM
DECLARATION = ITEM_FORM
ACCEPT_FORM = ITEM_FORM
UNDO_FORM = ITEM_FORM


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
    ("C-FLD", "Config/Folder"),
    ("C-GRP", "Config/Group"),
]

doctype_status = [
    ("0", "Disabled"),
    ("1", "Activ"),
]


class Element(TreeModel):

    class Meta:
        verbose_name = _("Element")
        verbose_name_plural = _("Elements")
        default_permissions = ("add", "change", "delete", "view", "list", "administer")
        app_label = "schelements"

        ordering = ["id"]

        permissions = [
            ("admin_element", "Can administer elements"),
        ]

    parent = ext_models.PtigTreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        editable=True,
        verbose_name="Parent",
    )
    type = models.CharField(
        "Element type",
        null=False,
        blank=False,
        editable=True,
        choices=element_type_choice,
        max_length=8,
    )
    subtype = models.CharField(
        "Element subtype", null=True, blank=True, editable=False, max_length=16
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
    description = models.CharField(
        "Description", null=True, blank=True, editable=True, max_length=256
    )
    grand_parent1 = ext_models.PtigForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        editable=True,
        verbose_name="Grand parent 1",
        related_name="grandparent1",
    )
    grand_parent2 = ext_models.PtigForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        editable=True,
        verbose_name="Grand parent 2",
        related_name="grandparent2",
        search_fields=[
            "name__icontains",
        ],
    )
    grand_parent3 = ext_models.PtigForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        editable=True,
        verbose_name="Grand parent 3",
        related_name="grandparent3",
        search_fields=[
            "name__icontains",
        ],
    )
    grand_parent4 = ext_models.PtigForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        editable=True,
        verbose_name="Grand parent 4",
        related_name="grandparent4",
        search_fields=[
            "name__icontains",
        ],
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
    can_have_children = models.BooleanField(
        "Can have children",
        null=True,
        blank=True,
        editable=False,
        default=True,
    )
    has_children = models.BooleanField(
        "Element has children",
        null=True,
        blank=True,
        editable=False,
        default=False,
    )
    can_view_permission = models.ForeignKey(
        "auth.Permission",
        related_name="permission_set_perm_view",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    can_add_permission = models.ForeignKey(
        "auth.Permission",
        related_name="permission_set_perm_add",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    can_change_permission = models.ForeignKey(
        "auth.Permission",
        related_name="permission_set_perm_change",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    can_delete_permission = models.ForeignKey(
        "auth.Permission",
        related_name="permission_set_perm_delete",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    @staticmethod
    def get_structure():
        return STRUCTURE

    def init_new(self, request, view, param=None):
        defaults = {"type": param}
        return defaults

    def save(self, *argi, **argv):
        if not self.parent:
            global GROUP_FOR_TYPE
            if GROUP_FOR_TYPE == None:
                GROUP_FOR_TYPE = {}
                object_list = Element.objects.filter(Q(type="I-GRP") | Q(type="O-GRP"))
                for obj in object_list:
                    if obj.code:
                        if "(" in obj.description and ")" in obj.description:
                            types = (
                                obj.description.split("(")[1]
                                .split(")")[0]
                                .replace(",", ";")
                                .split(";")
                            )
                            for t in types:
                                t2 = t.strip()
                                if t2:
                                    GROUP_FOR_TYPE[t2] = obj
            if self.type in GROUP_FOR_TYPE:
                self.parent = GROUP_FOR_TYPE[self.type]

        if not self.code:
            self.code = self.gen_code()

        path = self.code if self.code else ""

        tab = self.parents()
        for pos in tab:
            if pos.code:
                path = pos.code + "/" + path

        self.path = path

        if len(tab) > 0:
            self.first_ancestor = tab[-1]
            super().save(*argi, **argv)
        else:
            super().save(*argi, **argv)
            self.first_ancestor = self
            super().save(*argi, **argv)

        if self.parent:
            if not self.parent.has_children:
                self.parent.has_children = True
                self.parent.save()

    def get_name(self):
        return self.name

    def _get_parent_elem(self, element_type):
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

    def number_of_children(self):
        return Element.objects.filter(parent=self).count()

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

    @staticmethod
    def add_type(type_code, type_name, title, table, app):
        global element_type_choice
        element_type_choice.append((type_code, type_name))
        s = Element.get_structure()
        if not type_code in s:
            s[type_code] = {"title": title, "table": table, "app": app}

    def get_derived_object(self, param=None):
        t = None
        if type(self) == Element:
            s = Element.get_structure()
            if s:
                if param and "view" in param and "add_param" in param["view"].kwargs:
                    t = param["view"].kwargs["add_param"]
                    if t == "-":
                        return self
                    if s[t]["app"] == "schelements" and s[t]["table"] == "Element":
                        return self
                    if t in s:
                        model = apps.get_model(s[t]["app"], s[t]["table"])
                        return model.objects.get(pk=self.id)
                else:
                    t = self.type
                    if t in s:
                        if hasattr(self, s[t]["table"].lower()):
                            return getattr(self, s[t]["table"].lower())
                        else:
                            if (
                                s[t]["app"] == "schelements"
                                and s[t]["table"] == "Element"
                            ):
                                return self
                            model = apps.get_model(s[t]["app"], s[t]["table"])
                            try:
                                ret = model.objects.get(pk=self.id)
                            except:
                                print(
                                    "Object of type %s[%d] does'nt exists!"
                                    % (model.__name__, self.id)
                                )
                                ret = self
                            return ret

        return self

    def template_for_object(self, view, context, doc_type):
        if self.id and doc_type in ("html", "json"):
            s = Element.get_structure()
            if s:
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

        s = Element.get_structure()
        if s:
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
        if self.type in ("O-GRP", "I-GRP", "C-GRP") and Element.get_structure():
            obj = self
            while obj and obj.type in ("O-GRP", "I-GRP", "C-GRP"):
                obj = obj.parent
            if obj:
                buttons = self._get_new_buttons(obj.type)
            else:
                buttons = self._get_new_buttons("ROOT")

            buttons2 = self._get_new_buttons(self.type)

            for b in buttons2:
                if not b in buttons:
                    buttons.append(b)

            if self.description and "(" in self.description and ")" in self.description:
                items = self.description.split("(")[1].split(")")[0]
                s = Element.get_structure()
                for item in items.replace(",", ";").split(";"):
                    if s:
                        if item and item in s:
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

    @classmethod
    def filter(cls, value, view=None, request=None):
        if (
            hasattr(settings, "CANCAN")
            and settings.CANCAN
            and request
            and is_in_cancan_rules(cls, request.ability.access_rules.rules)
        ):
            if value and value != "-":
                return request.ability.queryset_for("view", cls).filter(type=value)
            else:
                return request.ability.queryset_for("view", cls)
        else:
            if value and value != "-":
                return cls.objects.filter(type=value)
            else:
                return cls.objects.all()

    def gen_standard_code(self):
        code = ""
        if self.parent and self.type in ("I-MAT", "I-RAW", "I-PRD", "I-IPR", "I-MER"):
            if self.parent.type in ("I-GRP",):
                code = self.parent.code
            if self.parent.parent and self.parent.parent.type in ("I-GRP",):
                code = self.parent.parent.code + "-" + code
            if code:
                code += "-"
            obj = (
                Element.objects.filter(type=self.type, code__startswith=code)
                .order_by("-code")
                .first()
            )
            if obj:
                try:
                    n = int(obj.code[len(code) :])
                    n += 1
                    code += str(n)
                except:
                    code = code + "0"
            else:
                code = code + "1"
            return code
        return None

    def gen_code(self):
        code = ""
        try:
            code = super().gen_code()
        except:
            code = self.gen_standard_code()
        return code

    def can_view(self, user, check_parents=True):
        if self.can_view_permission:
            ret = user.has_perm(self.can_view_permission.name)
        else:
            ret = user.has_perm("schelements.view_element")
        if check_parents:
            if ret and self.parent:
                ret = self.parent.can_view(user)
            if ret and self.grand_parent1:
                ret = self.grand_parent1.can_view(user, False)
            if ret and self.grand_parent2:
                ret = self.grand_parent2.can_view(user, False)
            if ret and self.grand_parent3:
                ret = self.grand_parent3.can_view(user, False)
        return ret

    def can_change(self, user):
        if self.can_change_permission:
            ret = user.has_perm(self.can_change_permission.name)
        else:
            ret = user.has_perm("schelements.change_element")
        if ret:
            ret = self.can_view(user)
        return ret

    def can_delete(self, user):
        if self.can_delete_permission:
            ret = user.has_perm(self.can_delete_permission.name)
        else:
            ret = user.has_perm("schelements.delete_element")
        if ret:
            ret = self.can_view(user)
        return ret

    def can_add(self, user, child_type):
        if self.can_add_permission:
            ret = user.has_perm(self.can_add_permission.name)
        else:
            ret = user.has_perm("schelements.add_element")
        if ret:
            ret = self.can_view(user)
        return ret

    @classmethod
    def table_action(cls, list_view, request, data):
        return standard_table_action(
            cls, list_view, request, data, ["copy", "paste", "delete"]
        )

    objects = ElementManager()


admin.site.register(Element)


class DocReg(models.Model):

    class Meta:
        verbose_name = _("Document register")
        verbose_name_plural = _("Document registers")
        default_permissions = ("add", "change", "delete", "view", "list", "administer")
        app_label = "schelements"

        ordering = ["id"]

        permissions = [
            ("admin_docreg", "Can administer document registers"),
        ]

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
        self.update_time = timezone.now()
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

    def get_save_head_fun_if_empty(
        self, request, template_name, ext, extra_context, target
    ):
        return SAVE_HEAD

    def get_save_item_fun_if_empty(
        self, request, template_name, ext, extra_context, target
    ):
        return SAVE_ITEM

    def get_head_form_if_empty(
        self, request, template_name, ext, extra_context, target
    ):
        return HEAD_FORM

    def get_item_form_if_empty(
        self, request, template_name, ext, extra_context, target
    ):
        return ITEM_FORM

    def get_head_template_if_empty(
        self, request, template_name, ext, extra_context, target
    ):
        return HEAD_TEMPLATE

    def get_item_template_if_empty(
        self, request, template_name, ext, extra_context, target
    ):
        return ITEM_TEMPLATE

    def get_access_fun_if_empty(
        self, request, template_name, ext, extra_context, target
    ):
        return ACCESS_FUN

    def copy_to_clipboard(self):
        object_list = self.docregstatus_set.all()
        return {
            "action": "paste_from_clipboard",
            "table": "DocReg",
            "objects": [
                {
                    "app": self.app,
                    "name": self.name,
                    "group": self.group,
                    "description": self.description,
                    "head_form": self.head_form,
                    "head_template": self.head_template,
                    "item_form": self.item_form,
                    "item_template": self.item_template,
                    "save_head_fun": self.save_head_fun,
                    "save_item_fun": self.save_item_fun,
                    "access_fun": self.access_fun,
                    "statuses": [obj.copy_to_clipboard() for obj in object_list],
                },
            ],
        }

    @classmethod
    def table_action(cls, list_view, request, data):
        if (
            "action" in data
            and data["action"] == "paste_from_clipboard"
            and "table" in data
            and data["table"] == "DocReg"
        ):

            class _LV:
                pass

            obj = None
            object_list = data["objects"]
            for obj_param in object_list:
                obj = DocReg()
                obj.app = obj_param["app"]
                obj.name = "COPY: " + obj_param["name"]
                obj.group = obj_param["group"]
                obj.description = obj_param["description"]
                obj.head_form = obj_param["head_form"]
                obj.head_template = obj_param["head_template"]
                obj.item_form = obj_param["item_form"]
                obj.item_template = obj_param["item_template"]
                obj.save_head_fun = obj_param["save_head_fun"]
                obj.save_item_fun = obj_param["save_item_fun"]
                obj.access_fun = obj_param["access_fun"]
                obj.save()

                lv = _LV()
                lv.kwargs = {"parent_pk": obj.id}
                for status in obj_param["statuses"]:
                    DocRegStatus.table_action(lv, request, status)

            if obj:
                return new_row_ok(request, int(obj.id), str(obj))
            return True

        return standard_table_action(
            cls, list_view, request, data, ["copy", "paste", "delete"]
        )


admin.site.register(DocReg)


class DocType(models.Model):

    class Meta:
        verbose_name = _("Type of document")
        verbose_name_plural = _("Types of documents")
        default_permissions = ("add", "change", "delete", "view", "list", "administer")
        app_label = "schelements"

        ordering = ["id"]

        permissions = [
            ("admin_doctype", "Can administer document types"),
        ]

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
        default=False,
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
    correction_name = models.CharField(
        "Correction name", null=True, blank=True, editable=True, max_length=16
    )

    def __str__(self):
        return self.name

    def get_save_head_fun_if_empty(
        self, request, template_name, ext, extra_context, target
    ):
        return SAVE_HEAD

    def get_save_item_fun_if_empty(
        self, request, template_name, ext, extra_context, target
    ):
        return SAVE_ITEM

    def get_head_form_if_empty(
        self, request, template_name, ext, extra_context, target
    ):
        return HEAD_FORM

    def get_item_form_if_empty(
        self, request, template_name, ext, extra_context, target
    ):
        return ITEM_FORM

    def get_head_template_if_empty(
        self, request, template_name, ext, extra_context, target
    ):
        return HEAD_TEMPLATE

    def get_item_template_if_empty(
        self, request, template_name, ext, extra_context, target
    ):
        return ITEM_TEMPLATE

    def get_access_fun_if_empty(
        self, request, template_name, ext, extra_context, target
    ):
        return ACCESS_FUN


admin.site.register(DocType)


class DocHead(JSONModel):

    class Meta:
        verbose_name = _("Document header")
        verbose_name_plural = _("Document headers")
        default_permissions = ("add", "change", "delete", "view", "list", "administer")
        app_label = "schelements"

        ordering = ["id"]

        permissions = [
            ("admin_dochead", "Can administer document headers"),
        ]

    parents = models.ManyToManyField(
        "self",
        null=False,
        blank=False,
        editable=False,
        verbose_name="Parents",
        db_index=True,
        symmetrical=False,
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
        select2=True,
    )
    number = models.CharField(
        "Document number",
        null=True,
        blank=True,
        editable=True,
        db_index=True,
        max_length=64,
    )
    date_c = models.DateTimeField(
        "Creation date",
        null=False,
        blank=False,
        editable=False,
        default=timezone.now,
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
        "Status",
        null=True,
        blank=True,
        editable=False,
        default="draft",
        db_index=True,
        max_length=16,
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
    corrected = models.BooleanField(
        "Corrected",
        null=False,
        blank=False,
        editable=False,
        default=False,
    )
    corrected_dochead = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        editable=True,
        verbose_name="Corrected dochead",
        db_index=True,
        related_name="correction",
    )

    def __str__(self):
        if self.number:
            return self.doc_type_parent.name + ":" + self.number
        else:
            return self.doc_type_parent.name + ":"

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
    def filter(cls, value, view=None, request=None):
        if value and value.startswith("_code_"):
            code = value.replace("_code_", "")
            return cls.objects.filter(parent_element__code=code)
        elif value and value.startswith("_pk_"):
            i = value.replace("_pk_", "")
            x = cls.objects.filter(parent_element__pk=int(i))
            return x
        elif value and value.startswith("_children_"):
            i = value.replace("_children_", "")
            x = cls.objects.filter(parents__pk=int(i))
            return x
        elif value and value.startswith("_parents_"):
            i = value.replace("_parents_", "")
            obj = cls.objects.get(pk=int(i))
            return obj.parents.all()
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
                self.date = timezone.now()
                self.status = "draft"
                self.operator = request.user.username

        return None

    @staticmethod
    def template_for_list(view, model, context, doc_type):
        if doc_type in ("html", "json") and "filter" in context:
            reg = DocReg.objects.filter(
                name=context["filter"].replace("_", "/")
            ).first()
            if reg:
                names = []
                if "version" in context and context["version"]:
                    v = context["version"]
                    if "__" in v:
                        app, version = v.split("__", 1)
                    else:
                        app = reg.app
                        version = v
                    if version:
                        names.append(
                            (
                                app
                                + "/"
                                + reg.name.replace("/", "_")
                                + "_dochead_list_"
                                + version
                                + ".html"
                            ).lower()
                        )
                    else:
                        names.append(
                            (
                                app
                                + "/"
                                + reg.name.replace("/", "_")
                                + "_dochead_list"
                                + ".html"
                            ).lower()
                        )

                    if reg and reg.head_template:
                        names.append("db/DocReg-%d-head_template.html" % reg.id)
                else:
                    if reg and reg.head_template:
                        names.append("db/DocReg-%d-head_template.html" % reg.id)
                    x = reg
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

                names.append(view.template_name)
                return names

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
                if "version" in context and context["version"]:
                    v = context["version"]
                    if "__" in v:
                        app, version = v.split("__", 1)
                    else:
                        app = reg.app
                        version = v
                    names.append(
                        (
                            app
                            + "/"
                            + reg.name.replace("/", "_")
                            + "_dochead_edit_"
                            + version
                            + ".html"
                        ).lower()
                    )
                    if reg.head_template:
                        names.append("db/DocReg-%d-head_template.html" % reg.id)
                else:
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
                            (
                                reg.app + "/" + doc_type.name + "_dochead_edit.html"
                            ).lower()
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
            except:
                return None
        return None

    def old_get_form_source(self):
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

    def get_form_source(self):
        if self.doc_type_parent:
            if self.doc_type_parent.head_form:
                return self.doc_type_parent.head_form
            x = self.doc_type_parent.parent
            while x:
                if x.head_form:
                    return x.head_form
                x = x.get_parent()

        return None

    def post_form(self, view, form, request):
        obj = self
        save_fun_src_obj = None
        if obj.doc_type_parent.save_head_fun:
            save_fun_src_obj = obj.doc_type_parent
        else:
            x = obj.doc_type_parent.parent
            while x:
                if x.save_head_fun:
                    save_fun_src_obj = x
                    break
                x = x.get_parent()
        if save_fun_src_obj:
            ret = run_code_from_db_field(
                f"dochead__save_{save_fun_src_obj.pk}.py",
                save_fun_src_obj,
                "save_head_fun",
                "save",
                dochead=self,
                view=view,
                form=form,
                request=request,
            )
            return ret
        return True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.date_c = timezone.now()

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

        if self.corrected_dochead:
            if self.status in ("draft", ""):
                if self.corrected_dochead.corrected:
                    self.corrected_dochead.corrected = False
                    self.corrected_dochead.save()
            else:
                if not self.corrected_dochead.corrected:
                    self.corrected_dochead.corrected = True
                    self.corrected_dochead.save()

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
                data = run_code_from_db_field(
                    f"docregstatus__can_set_proc_{status.pk}.py",
                    status,
                    "can_set_proc",
                    "can_set",
                    request=request,
                    doc_head=self,
                )
                if data == None or data:
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
                data = run_code_from_db_field(
                    f"docregstatus__can_undo_proc_{status.pk}.py",
                    status,
                    "can_undo_proc",
                    "can_undo",
                    request=request,
                    doc_head=self,
                )
                if data:
                    return True
                elif data != None:
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

                c = ContentType.objects.filter(model=t.lower() + "dochead").first()
                if c:
                    return c.model_class()()
                else:
                    return DocHead()

            else:
                t = self.doc_type_parent.parent.name
                name = t.lower() + "dochead"
                if hasattr(self, name):
                    return getattr(self, name)
                else:
                    c = ContentType.objects.filter(model=name).first()
                    if c:
                        obj2 = copy.copy(self)
                        obj2.__class__ = c.model_class()
                        return obj2
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
            qq = run_code_from_db_field(
                f"dochead__q_for_list_{reg.pk}.py",
                reg,
                "access_fun",
                "q_for_list",
                request=request,
                user=request.user,
                profile=profile,
            )
            if qq:
                q2 = qq
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
        check = run_code_from_db_field(
            f"dochead__check_user_perm_{reg.pk}.py",
            reg,
            "access_fun",
            "check_user_perm",
            dochead=self,
            user=user,
            perm=perm,
            doc_type_name=self.doc_type_parent.name,
        )
        if check != None:
            return check
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
        check = run_code_from_db_field(
            f"dochead__check_user_perm_{reg.pk}.py",
            reg,
            "access_fun",
            "check_user_perm",
            dochead=None,
            user=user,
            perm="add",
            doc_type_name=doc_type_name,
        )
        if check != None:
            return check
        return True

    def log(self, log_class, request, description, save=True):
        obj = log_class()
        obj.application = "schelements"
        obj.table = "DocHead"
        obj.group = "default"
        obj.parent_id = self.id
        obj.description = description
        obj.operator_id = request.user.id
        obj.operator = request.user.username
        if save:
            obj.save()
        return obj

    def change_status(
        self,
        action_name,
        action="accept",
        data=None,
        request=None,
        operator=None,
        batch_mode=False,
    ):
        doc_type = self.doc_type_parent
        doc_reg = doc_type.parent
        reg_status_list = DocRegStatus.objects.filter(parent=doc_reg, name=action_name)
        if len(reg_status_list) == 1:
            reg_status = reg_status_list[0]
        else:
            reg_status = None
        form = None

        if reg_status:
            if action == "accept":
                form_txt = reg_status.accept_form
                fun = get_fun_from_db_field(
                    f"regstatus__accept_proc_{reg_status.pk}.py",
                    reg_status,
                    "accept_proc",
                    "accept",
                )
            else:
                form_txt = reg_status.undo_form
                fun = get_fun_from_db_field(
                    f"regstatus__undo_proc_{reg_status.pk}.py",
                    reg_status,
                    "undo_proc",
                    "undo",
                )

            params = {
                "request": request,
                "doc_head": self,
                "doc_type": doc_type,
                "doc_reg": doc_reg,
            }
            if form_txt:
                form_class = form_from_str(form_txt, params)
            else:
                form_class = None

            if (not form_class) or data != None:
                if form_class:
                    form = form_class(data)
                else:
                    form = None

                if (not form) or form.is_valid():
                    doc_status = DocHeadStatus()
                    doc_status.parent = self
                    callback = None
                    new_status = None

                    try:
                        if fun:
                            with transaction.atomic():
                                ret = fun(
                                    request,
                                    self,
                                    reg_status,
                                    doc_type,
                                    doc_reg,
                                    doc_status,
                                    form,
                                )
                                if type(ret) == dict and "errors" in ret:
                                    errors = ret["errors"]
                                    if "callback" in ret:
                                        callback = ret["callback"]
                                    if "status" in ret:
                                        new_status = ret["status"]
                                else:
                                    errors = ret
                        else:
                            errors = None

                    except ValueError as err:
                        errors = err.args

                    if not errors:
                        if new_status:
                            self.status = action_name
                            self.save()
                        elif (
                            action_name
                            and action_name[:1] != "_"
                            and action_name != self.status
                        ):
                            self.status = action_name
                            self.save()

                        if action != "accept":
                            DocItem.objects.filter(
                                parent=self,
                                level__gt=(
                                    reg_status.order if reg_status.order >= 0 else 0
                                ),
                            ).delete()

                        doc_status.date = timezone.now()
                        if operator:
                            doc_status.operator = operator
                        elif not batch_mode:
                            doc_status.operator = request.user.username
                        doc_status.save()
                        if callback:
                            if batch_mode:
                                return callback
                            else:
                                return callback()
                        else:
                            if batch_mode:
                                return {
                                    "errors": None,
                                    "id": self.id,
                                    "description": str(self),
                                }
                            else:
                                return actions.update_row_ok(
                                    request, int(self.id), str(self)
                                )
                    else:
                        return {
                            "errors": errors,
                            "form": form,
                            "doc_head": self,
                            "doctype": doc_type,
                            "doc_reg": doc_reg,
                            "reg_status": reg_status,
                            "action_name": action_name,
                        }
            if not form:
                if form_class:
                    form = form_class()
                else:
                    form = None
                return {
                    "error": False,
                    "form": form,
                    "doc_head": self,
                    "doctype": doc_type,
                    "doc_reg": doc_reg,
                    "reg_status": reg_status,
                    "action_name": action_name,
                }
        else:
            return {"error": "Status %s doesn't exists" % action_name}

    def copy_to(
        self,
        doc_head_dest,
        doc_head_callback=None,
        doc_item_callback=None,
        without_items=False,
    ):
        doc_head_dest.doc_type_parent = self.doc_type_parent
        doc_head_dest.parent_element = self.parent_element
        doc_head_dest.description = self.description
        doc_head_dest.param1 = self.param1
        doc_head_dest.param2 = self.param2
        doc_head_dest.param3 = self.param3
        doc_head_dest.date_c = timezone.now()
        doc_head_dest.date = datetime.date.today()
        doc_head_dest.status = "draft"
        if doc_head_callback:
            doc_head_callback(self, doc_head_dest)
        else:
            doc_head_dest.save()
        if not without_items:
            for _item in docitem_set.all():
                item = _item.get_derived_object()
                item2 = type(item)()
                item.copy_to(item2)
                if doc_item_callback:
                    doc_item_callback(item, item2)
                else:
                    item2.save()

    def gen_correction(self, request):
        if not self.doc_type_parent.correction_name:
            return

        new_obj = type(self)()

        def dochead_callback(dochead_src, dochead_dest):
            dochead_dest.doc_type_parent = DocType.objects.get(
                name=self.doc_type_parent.correction_name
            )
            dochead_dest.corrected_dochead = self
            dochead_dest.operator = request.user.username
            dochead_dest.save()
            dochead_dest.parents.add(self)

        def docitem_callback(docitem_src, docitem_dest):
            docitem_dest.parent = new_obj
            docitem_dest.parent_item = docitem_src
            docitem_dest.save()

        self.copy_to(new_obj, dochead_callback, docitem_callback)

        return new_obj


admin.site.register(DocHead)


class DocItem(JSONModel):

    class Meta:
        verbose_name = _("Document item")
        verbose_name_plural = _("Document items")
        default_permissions = ("add", "change", "delete", "view", "list", "administer")
        app_label = "schelements"

        ordering = ["id"]

        permissions = [
            ("admin_docitem", "Can administer document items"),
        ]

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
    qty = models.DecimalField(
        "Quantity",
        null=True,
        blank=True,
        editable=True,
        max_digits=16,
        decimal_places=2,
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
    corrected = models.BooleanField(
        "Corrected",
        null=False,
        blank=False,
        editable=False,
        default=False,
        db_index=True,
    )

    @staticmethod
    def template_for_list(view, model, context, doc_type):
        if doc_type in ("html", "json"):
            if "parent_pk" in context["view"].kwargs:
                parent_pk = int(context["view"].kwargs["parent_pk"])
                dochead = DocHead.objects.get(pk=parent_pk)
                reg = dochead.doc_type_parent.parent
                names = []
                if "version" in context and context["version"]:
                    v = context["version"]
                    if "__" in v:
                        app, version = v.split("__", 1)
                    else:
                        app = reg.app
                        version = v
                    names.append(
                        (
                            app
                            + "/"
                            + dochead.doc_type_parent.name
                            + "_docitem_list_"
                            + version
                            + ".html"
                        ).lower()
                    )
                    names.append(
                        (
                            app
                            + "/"
                            + dochead.doc_type_parent.parent.name
                            + "_docitem_list_"
                            + version
                            + ".html"
                        ).lower()
                    )
                    if reg.item_template:
                        names.append("db/DocReg-%d-item_template.html" % reg.id)
                else:
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
                            x.app
                            + "/"
                            + x.name.replace("/", "_")
                            + "_docitem_list.html"
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
            doc = dochead.doc_type_parent
            names = []

            if "version" in context and context["version"]:
                v = context["version"]
                if "__" in v:
                    app, version = v.split("__", 1)
                else:
                    app = reg.app
                    version = v

                names.append(
                    (
                        app
                        + "/"
                        + doc.name.replace("/", "_")
                        + "_docitem_edit_"
                        + version
                        + ".html"
                    ).lower()
                )
                names.append(
                    (
                        app
                        + "/"
                        + reg.name.replace("/", "_")
                        + "_docitem_edit_"
                        + version
                        + ".html"
                    ).lower()
                )
                if reg.item_template:
                    names.append("db/DocReg-%d-item_template.html" % reg.id)
            else:
                if reg.item_template:
                    names.append("db/DocReg-%d-item_template.html" % reg.id)

                names.append(
                    (
                        reg.app
                        + "/"
                        + doc.name.replace("/", "_")
                        + "_docitem_edit.html"
                    ).lower()
                )
                names.append(
                    (
                        reg.app
                        + "/"
                        + reg.name.replace("/", "_")
                        + "_docitem_edit.html"
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
                    "date_c": timezone.now(),
                    "level": 0,
                }

        return None

    def post_form(self, view, form, request):
        obj = self.parent
        save_fun_src_obj = None
        if obj.doc_type_parent.save_item_fun:
            save_fun_src_obj = obj.doc_type_parent
        else:
            x = obj.doc_type_parent.parent
            while x:
                if x.save_item_fun:
                    save_fun_src_obj = x
                    break
                x = x.get_parent()
        if save_fun_src_obj:
            ret = check = run_code_from_db_field(
                f"docitem__save_{save_fun_src_obj.pk}.py",
                save_fun_src_obj,
                "save_item_fun",
                "save",
                docitem=self,
                view=view,
                form=form,
                request=request,
            )
            return ret
        return True

    def save(self, *args, **kwargs):
        if self.parent.correction and self.parent_item:
            if self.active:
                if not self.parent_item.corrected:
                    self.parent_item.corrected = True
                    self.parent_item.save()
            else:
                if self.parent_item.corrected:
                    self.parent_item.corrected = False
                    self.parent_item.save()
        super().save(*args, **kwargs)

    def get_qty(self):
        if self.parent.correction and self.parent_item:
            return self.qty - self.parent_item.qty
        else:
            return self.qty

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
                    c = ContentType.objects.filter(model=name).first()
                    if c:
                        obj2 = copy.copy(self)
                        obj2.__class__ = c.model_class()
                        return obj2
        return self

    def get_period(self):
        return "%04d-%02d" % (self.parent.date.year, self.parent.date.month)

    def new_account_operations(
        self,
        account_states_and_qty,
        description,
        sign,
        payment=None,
        save=True,
        transfer=False,
    ):
        account_operations = []
        for account_state, qty in account_states_and_qty:
            account_operation = AccountOperation()
            account_operation.parent = self
            account_operation.description = description
            account_operation.payment = payment
            account_operation.account_state = account_state
            account_operation.sign = sign
            account_operation.qty = qty
            account_operation.enabled = transfer

            account_operations.append(account_operation)

            if save:
                account_operation.save()

        return account_operations

    def new_account_operation(
        self,
        target,
        account_name,
        description,
        sign,
        qty,
        element,
        classifier1value=None,
        classifier2value=None,
        classifier3value=None,
        subcode="",
        payment=None,
        save=True,
    ):
        account_state = AccountState.get_or_create_account_state(
            account_name,
            subcode,
            target,
            classifier1value=classifier1value,
            classifier2value=classifier2value,
            classifier3value=classifier3value,
            period="",
            element=element,
            aggregate=False,
        )
        return self.new_account_operations(
            ((account_state, qty),), description, sign, payment, save
        )

    def move_account_operation(
        self,
        docitem_src,
        account_name,
        description=None,
        payment=None,
        percent=100,
        update_docitem=False,
        update_docitem_src=False,
        update_account_states=False,
    ):
        sum = 0
        account_operations = []
        for account_operation in docitem_src.accountoperation_set.filter(
            account_state__parent__name=account_name, enabled=True
        ):
            qty = account_operation.qty * percent / 100
            sum += qty
            account_operation.qty -= qty
            if update_account_states:
                account_operation2 = self.accountoperation_set.filter(
                    account_state=account_operation.account_state, enabled=True
                ).first()
                if account_operation2:
                    account_operation2.qty += qty
                    account_operation2.save()
                    account_operations.append(account_operation2)
            else:
                account_operations.extend(
                    self.new_account_operations(
                        ((account_operation.account_state, qty),),
                        description if description else account_operation.description,
                        account_operation.sign,
                        payment,
                        transfer=True,
                    )
                )
            account_operation.save()

        if update_docitem_src:
            docitem_src.qty -= sum
            docitem_src.save()
        if update_docitem:
            self.qty += sum
            self.save()

        return account_operations

    def copy_to(self, doc_item_dest):
        doc_item_dest.owner = self.owner
        doc_item_dest.order = self.order
        doc_item_dest.item = self.item
        doc_item_dest.qty = self.qty
        doc_item_dest.description = self.description
        doc_item_dest.level = self.level
        doc_item_dest.param1 = self.param1
        doc_item_dest.param2 = self.param2
        doc_item_dest.param3 = self.param3


admin.site.register(DocItem)


class DocRegStatus(models.Model):

    class Meta:
        verbose_name = _("Document status")
        verbose_name_plural = _("Document status")
        default_permissions = ("add", "change", "delete", "view", "list", "administer")
        app_label = "schelements"

        ordering = ["id"]

        permissions = [
            ("admin_docregstatus", "Can administer document register statuses"),
        ]

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
    for_accept_template = models.TextField(
        "Template for accept",
        null=True,
        blank=True,
        editable=False,
    )
    for_undo_template = models.TextField(
        "Template for undo",
        null=True,
        blank=True,
        editable=False,
    )

    def __str__(self):
        return self.name

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

    def get_accept_proc_if_empty(
        self, request, template_name, ext, extra_context, target
    ):
        return ACCEPT_PROC

    def get_undo_proc_if_empty(
        self, request, template_name, ext, extra_context, target
    ):
        return UNDO_PROC

    def get_can_set_proc_if_empty(
        self, request, template_name, ext, extra_context, target
    ):
        return CAN_SET

    def get_can_undo_proc_if_empty(
        self, request, template_name, ext, extra_context, target
    ):
        return CAN_UNDO

    def get_accept_form_if_empty(
        self, request, template_name, ext, extra_context, target
    ):
        return ACCEPT_FORM

    def get_undo_form_if_empty(
        self, request, template_name, ext, extra_context, target
    ):
        return UNDO_FORM

    def copy_to_clipboard(self):
        return {
            "action": "paste_from_clipboard",
            "table": "DocRegStatus",
            "objects": [
                {
                    "order": self.order,
                    "name": self.name,
                    "description": self.description,
                    "icon": self.icon,
                    "accept_proc": self.accept_proc,
                    "undo_proc": self.undo_proc,
                    "can_set_proc": self.can_set_proc,
                    "can_undo_proc": self.can_undo_proc,
                    "accept_form": self.accept_form,
                    "undo_form": self.undo_form,
                    "for_accept_template": self.for_accept_template,
                    "for_undo_template": self.for_undo_template,
                },
            ],
        }

    @classmethod
    def table_action(cls, list_view, request, data):
        print("TABLE_ACTION", data)
        if (
            "action" in data
            and data["action"] == "paste_from_clipboard"
            and "table" in data
            and data["table"] == "DocRegStatus"
        ):
            print("X1: ", data)
            try:
                parent_pk = int(list_view.kwargs["parent_pk"])
            except:
                parent_pk = -1
            if parent_pk >= 0:
                obj = None
                object_list = data["objects"]
                for obj_param in object_list:
                    obj = DocRegStatus()
                    obj.parent_id = parent_pk
                    obj.order = obj_param["order"]
                    obj.name = "COPY: " + obj_param["name"]
                    obj.description = obj_param["description"]
                    obj.icon = obj_param["icon"]
                    obj.accept_proc = obj_param["accept_proc"]
                    obj.undo_proc = obj_param["undo_proc"]
                    obj.can_set_proc = obj_param["can_set_proc"]
                    obj.can_undo_proc = obj_param["can_undo_proc"]
                    obj.accept_form = obj_param["accept_form"]
                    obj.undo_form = obj_param["undo_form"]
                    obj.for_accept_template = obj_param["for_accept_template"]
                    obj.for_undo_template = obj_param["for_undo_template"]

                    obj.save()
                if obj:
                    return new_row_ok(request, int(obj.id), str(obj))
                # print("PASTE: ", data)
            return True
        return standard_table_action(
            cls, list_view, request, data, ["copy", "paste", "delete"]
        )


admin.site.register(DocRegStatus)


class DocHeadStatus(JSONModel):

    class Meta:
        verbose_name = _("Document head status")
        verbose_name_plural = _("Documents head status")
        default_permissions = ("add", "change", "delete", "view", "list", "administer")
        app_label = "schelements"

        ordering = ["id"]

        permissions = [
            ("admin_docheadstatus", "Can administer document header statuses"),
        ]

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
        default_permissions = ("add", "change", "delete", "view", "list", "administer")
        app_label = "schelements"

        ordering = ["id"]

        permissions = [
            ("admin_account", "Can administer accounts"),
        ]
        ordering = [
            "name",
        ]

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
        return self.name + ": " + self.description

    @staticmethod
    def get(account_name):
        return Account.objects.get(name=account_name)


admin.site.register(Account)


class AccountState(models.Model):

    class Meta:
        verbose_name = _("State of account")
        verbose_name_plural = _("States of account")
        default_permissions = ("add", "change", "delete", "view", "list", "administer")
        app_label = "schelements"

        ordering = ["id"]

        permissions = [
            ("admin_accountstatus", "Can administer account statuses"),
        ]
        ordering = [
            "parent__name",
            "subcode",
            "period",
            "target__name",
            "element__name",
        ]

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
        "Balance is zero",
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
        default=timezone.now,
    )

    def __str__(self):
        s = self.parent.name

        if self.subcode:
            s += "-" + self.subcode

        if (
            self.target
            or self.classifier1value
            or self.classifier2value
            or self.classifier3value
        ):
            s += "/"
        else:
            s += " [" + self.element.name + "]"
            return s

        if self.target and self.parent:
            s += self.target.name

        if self.classifier1value or self.classifier2value or self.classifier3value:
            if self.classifier1value:
                s += ":" + self.classifier1value.name
            else:
                s += ":"
            if self.classifier2value:
                s += ":" + self.classifier2value.name
            else:
                s += ":"
            if self.classifier3value:
                s += ":" + self.classifier3value.name
            else:
                s += ":"
        s += " [" + self.element.name + "]"
        return s

    @staticmethod
    def get_account_states(
        account,
        subcode="",
        target=None,
        classifier1value=None,
        classifier2value=None,
        classifier3value=None,
        period="",
        element=None,
        aggregate=False,
        q=None,
    ):
        if type(account) == str:
            account = Account.objects.get(name=account)

        objs = AccountState.objects.filter(
            parent=account,
            subcode=subcode,
            element=element,
            classifier1value=classifier1value,
            classifier2value=classifier2value,
            classifier3value=classifier3value,
            period=period,
            aggregate=aggregate,
        )

        if target:
            objs = objs.filter(target=target)
        else:
            objs = objs.filter(target__isnull=True)

        if element:
            objs = objs.filter(element=element)

        if q:
            objs = objs.filter(q)

        return objs

    @staticmethod
    def completing(
        quantity,
        account,
        subcode="",
        target=None,
        classifier1value=None,
        classifier2value=None,
        classifier3value=None,
        element=None,
        q=None,
        only_all=True,
        raise_error=False,
    ):
        sum = 0
        ret_tab = []
        object_list = (
            AccountState.get_account_states(
                account,
                subcode,
                target,
                classifier1value,
                classifier2value,
                classifier3value,
                "",
                element,
                False,
                q,
            )
            .order_by("date_c")
            .exclude(zero_balance=True)
        )
        for obj in object_list:
            if sum + obj.credit - obj.debit < quantity:
                ret_tab.append((obj, obj.credit - obj.debit))
                sum += obj.credit - obj.debit
            else:
                ret_tab.append((obj, quantity - sum))
                return ret_tab
        if only_all:
            if raise_error:
                raise ValueError("Not enough quantity in stock!")
            else:
                return None
        else:
            return ret_tab

    @staticmethod
    def get_or_create_account_state(
        account,
        subcode="",
        target=None,
        classifier1value=None,
        classifier2value=None,
        classifier3value=None,
        period="",
        element=None,
        aggregate=False,
    ):
        if type(account) == str:
            account = Account.objects.get(name=account)

        objs = AccountState.get_account_states(
            account,
            subcode,
            target,
            classifier1value,
            classifier2value,
            classifier3value,
            period,
            element,
            aggregate,
        )

        if objs.count() > 0:
            return objs[0]
        else:
            obj = AccountState()
            obj.parent = account
            obj.target = target
            obj.classifier1value = classifier1value
            obj.classifier2value = classifier2value
            obj.classifier3value = classifier3value
            obj.period = period
            obj.subcode = subcode
            obj.element = element
            obj.debit = 0
            obj.credit = 0
            obj.zero_balance = True
            obj.aggregate = aggregate
            obj.date_c = timezone.now()
            obj.save()
            return obj

    @staticmethod
    def get_balance(
        account,
        subcode="",
        target=None,
        classifier1value=None,
        classifier2value=None,
        classifier3value=None,
        period=None,
        element=None,
        aggregate=False,
        q=None,
    ):
        ret = AccountState.get_account_states(
            account,
            subcode,
            target,
            classifier1value,
            classifier2value,
            classifier3value,
            period,
            element,
            aggregate,
            q,
        )
        result = ret.aggregate(Sum("credit"), Sum("debit"))
        result["balance__sum"] = result["debit__sum"] - result["credit__sum"]
        return result

    def update_state(self, debit, credit, period):
        self.debit += debit
        self.credit += credit

        if self.target:
            targets = [self.target, None]
        else:
            targets = [
                None,
            ]

        classifier1values = [
            self.classifier1value,
        ]
        if self.classifier1value:
            classifier1values.append(None)
        classifier2values = [
            self.classifier2value,
        ]
        if self.classifier2value:
            classifier2values.append(None)
        classifier3values = [
            self.classifier3value,
        ]
        if self.classifier3value:
            classifier3values.append(None)
        periods = (None, period)

        tab = []
        parent = self.parent
        while parent:
            if len(tab) == 0:
                if self.subcode:
                    tab.append((parent, self.subcode))
                    tab.append((parent, None))
                else:
                    tab.append((parent, None))
            else:
                tab.append((parent, None))
            parent = parent.parent

        first = True
        for account, subcode in tab:
            for target in targets:
                for classifier1value in classifier1values:
                    for classifier2value in classifier2values:
                        for classifier3value in classifier3values:
                            for period in periods:
                                state = self.get_or_create_account_state(
                                    account,
                                    subcode,
                                    target,
                                    classifier1value,
                                    classifier2value,
                                    classifier3value,
                                    period,
                                    self.element,
                                    True,
                                )
                                state.debit += debit
                                state.credit += credit
                                state.save()
                                first = False
        self.save()

    def twin_state(self, account, target=0):
        object_list = AccountState.objects.filter(
            classifier1value=self.classifier1value,
            classifier2value=self.classifier2value,
            classifier3value=self.classifier3value,
            subcode=self.subcode,
            aggregate=self.aggregate,
        )
        if account:
            if type(account) == str:
                account = Account.objects.get(name=account)
            object_list = object_list.filter(parent=account)
        if target != 0:
            object_list = object_list.filter(target=target)
        return object_list.first()

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

        elif self.parent.type2 == "V":
            if self.credit - self.debit < 0:
                raise ValueError(
                    "The balance of the account with the number '%s' cannot be less than zero"
                    % self.parent.name
                )
        elif self.parent.type2 == "I":
            if self.credit - self.debit > 0:
                raise ValueError(
                    "The balance of the account with the number '%s' cannot be greater than zero"
                    % self.parent.name
                )
        elif self.parent.type2 == "D":
            if self.credit - self.debit < 0:
                raise ValueError(
                    "The balance of the account with the number '%s' cannot be less than zero"
                    % self.parent.name
                )
        if self.debit == self.credit:
            self.zero_balance = True
        else:
            self.zero_balance = False

        # self.aggregate = True
        # if self.parent.type1 == "A" and self.classifier1value != '*' and self.classifier2value != '*' and self.classifier2value != '*' and self.subcode != '*' and  not self.period:
        #    self.aggregate = False

        super().save(*args, **kwargs)


admin.site.register(AccountState)


class AccountOperation(models.Model):

    class Meta:
        verbose_name = _("Account operation")
        verbose_name_plural = _("Account operations")
        default_permissions = ("add", "change", "delete", "view", "list", "administer")
        app_label = "schelements"

        ordering = ["id"]

        permissions = [
            ("admin_accountoperation", "Can administer account operations"),
        ]

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
        default=timezone.now,
    )
    description = models.CharField(
        "Description", null=True, blank=True, editable=True, max_length=255
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
    qty = models.DecimalField(
        "Quantity",
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
        if self.description:
            return self.description
        else:
            return "Operation id: %d" % self.id

    def update_accounts_state(self, debit, credit):
        self.account_state.update_state(debit, credit, self.parent.get_period())

    def confirm(self):
        ret = False
        self.refresh_from_db()
        if not self.enabled:
            self.enabled = True
            if self.sign > 0:
                self.update_accounts_state(0, self.qty)
            else:
                self.update_accounts_state(self.qty, 0)
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
                self.update_accounts_state(0, -1 * self.qty)
            else:
                self.update_accounts_state(-1 * self.qty, 0)
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
        default_permissions = ("add", "change", "delete", "view", "list", "administer")
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
    info_template = models.TextField(
        "Info template",
        null=True,
        blank=True,
        editable=False,
    )
    on_delete_fun = models.TextField(
        "Fnction called when deleting an object",
        null=True,
        blank=True,
        editable=False,
    )
    action_fun = models.TextField(
        "Additional actions",
        null=True,
        blank=True,
        editable=False,
    )

    def save(self, *argi, **argv):
        if self.template_src:
            self.template = ihtml_to_html(None, self.template_src)
        super().save(*argi, **argv)

    def to_str(self, obj):
        ret = run_code_from_db_field(
            f"baseobject__to_str_fun_{self.pk}.py",
            self,
            "to_str_fun",
            "to_str",
            obj=obj,
        )
        if ret != None:
            return ret
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

    def get_info_template(self):
        if self.info_template:
            return ihtml_to_html(None, self.info_template)
        else:
            return None

    def on_delete(self, obj, request, view):
        run_code_from_db_field(
            f"baseobject__on_delete_{self.pk}.py",
            self,
            "on_delete_fun",
            "on_delete",
            obj=obj,
            request=request,
            view=view,
        )

    def action(self, obj, action_name, argv):
        return run_code_from_db_field(
            f"baseobject__action_{self.pk}.py",
            self,
            "action_fun",
            "action",
            obj=obj,
            action_name=action_name,
            argv=argv,
        )

    def get_declaration_if_empty(
        self, request, template_name, ext, extra_context, target
    ):
        return DECLARATION

    def get_to_str_fun_if_empty(
        self, request, template_name, ext, extra_context, target
    ):
        return TO_STR

    def get_to_html_rec_if_empty(
        self, request, template_name, ext, extra_context, target
    ):
        return TO_HTML_REC

    def get_template_src_if_empty(
        self, request, template_name, ext, extra_context, target
    ):
        return TEMPLATE_SRC

    def get_load_fun_if_empty(self, request, template_name, ext, extra_context, target):
        return LOAD_BASE_OBJ

    def get_save_fun_if_empty(self, request, template_name, ext, extra_context, target):
        return SAVE_BASE_OBJ

    def get_action_template_if_empty(
        self, request, template_name, ext, extra_context, target
    ):
        return ACTION_TEMPLATE

    def get_on_delete_fun_if_empty(
        self, request, template_name, ext, extra_context, target
    ):
        return ON_DELETE

    def get_action_fun_if_empty(
        self, request, template_name, ext, extra_context, target
    ):
        return ACTION


@receiver(post_delete, sender=Element)
def delete_profile(sender, instance, *args, **kwargs):
    if instance.parent:
        n = instance.parent.number_of_children()
        if n < 2:
            instance.parent.has_children = False
