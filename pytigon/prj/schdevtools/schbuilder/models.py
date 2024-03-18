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


import os.path
from pytigon_lib.schhtml.htmltools import superstrip
import inspect
from pytigon_lib.schfs.vfstools import norm_path
from django.template import engines
import pytigon
from django.conf import settings
import django.db.models.fields as fields
import django.db.models.fields.related as related
from django.template.loader import render_to_string
from django.forms import fields as form_fields
from django.forms import models as form_model_fields
from pytigon_lib.schdjangoext import formfields as ext_form_fields

import traceback

field_default = {
    "null": False,
    "blank": False,
    "editable": True,
}
field_defaults = {
    "AutoField": {},
    "BooleanField": {"default": False},
    "CharField": {
        "param": "max_length=64",
        "unique": False,
    },
    "CommaSeparatedIntegerField": {},
    "DateField": {},
    "DateTimeField": {},
    "DecimalField": {},
    "EmailField": {},
    "FileField": {
        "param": "upload_to='upload/'",
    },
    "FilePathField": {},
    "FloatField": {},
    "ImageField": {},
    "IntegerField": {},
    "GenericIPAddressField": {},
    "NullBooleanField": {},
    "PositiveIntegerField": {},
    "PositiveSmallIntegerField": {},
    "SlugField": {},
    "SmallIntegerField": {},
    "TextField": {
        "editable": False,
    },
    "TimeField": {},
    "URLField": {},
    "XMLField": {},
    "ForeignKey": {"name": "parent", "description": "Parent"},
    "OneToOneField": {"name": "parent", "description": "Parent"},
    "ManyToManyField": {},
    "HiddenForeignKey": {"name": "parent", "description": "Parent"},
    "GForeignKey": {"name": "parent", "description": "Parent"},
    "GManyToManyField": {},
    "GHiddenForeignKey": {
        "name": "parent",
        "description": "Parent",
    },
}

formfield_default = {
    "required": True,
}


formfield_defaults = {
    "BooleanField": {"initial": "False"},
    "CharField": {
        "param": "max_length=None, min_length=None",
    },
    "ChoiceField": {
        "param": "choices=models.[[choice_name]]",
    },
    "MultipleChoiceField": {
        "param": "choices=models.[[choice_name]]",
    },
    "TypedChoiceField": {
        "param": "coerce=int,empty_value=''",
    },
    "TypedMultipleChoiceField": {
        "param": "coerce=int,empty_value=''",
    },
    "DateField": {"param": "auto_now=False, auto_now_add=True"},
    "DateTimeField": {"param": "auto_now=False, auto_now_add=True"},
    "TimeField": {"param": "auto_now=False, auto_now_add=True"},
    "DecimalField": {
        "param": "max_value=None, min_value=None, max_digits=None, decimal_places=None",
    },
    "FilePathField": {
        "param": "path='[[path]]', match=None, recursive=False, allow_files=True, allow_folders=False",
    },
    "FloatField": {
        "param": "max_value=None, min_value=None",
    },
    "IntegerField": {
        "param": "max_value=None, min_value=None",
    },
    "GenericIPAddressField": {
        "param": "protocol='both', unpack_ipv4=False",
    },
    "MultipleChoiceField": {
        "param": "choices=models.[[choice_name]]",
    },
    "TypedMultipleChoiceField": {
        "param": "coerce=,empty_value=''",
    },
    "RegexField": {
        "param": "regex='[[regex]]', max_length=None, min_length=None",
    },
    "URLField": {},
    "ComboField": {
        "param": "fields=[[fields]]",
    },
    "ImageField": {
        "param": "upload_to=None",
    },
    "FileField": {
        "param": "upload_to=None",
    },
    "GenericIPAddressField": {},
    "RegexField": {"param": r"""regex='^\d{11}$', max_length=None, min_length=None"""},
    "SlugField": {},
    "UUIDField": {},
    "UserField": {"param": "user_field=forms.CharField(max_length=100)"},
}

widgets = [
    "ok_cancel",
    "button '[[url]]' '[[description]]' '[[name]]' '[[target]]'"
    "action_table '[[action]]' '[[description]]' '[[name]]' '[[target]]'",
    "print_table '[[description]]' '[[target]]'",
    "new_row '[[description]]' '[[target]]'",
    "edit_row '[[description]]' '[[target]]'",
    "view_row '[[description]]' '[[dx]]' '[[dy]]' , '[[target]]'",
    "print_row '[[description]]' '[[target]]'",
    "action_row '[[action]]' '[[description]]' '[[name]]' '[[target]]'",
    "delete_row '[[description]]' '[[target]]'",
    "list_field '[[field]]' '[[name]]' '[[description]]' '[[target]]'"
    "edit_field '[[field]]' '[[name]]' '[[description]]' '[[target]]'"
    "action_field '[[field]]' '[[action]]' '[[description]]' '[[name]]' '[[target]]'",
    "jscript_link '[[href]]'",
    "css_link '[[href]]'",
]


FormField_CHOICES = list(
    [
        (f, f)
        for f in dir(form_fields)
        if f.endswith("Field") and f not in ["BaseTemporalField", "Field", "BoundField"]
    ]
)
for f in dir(form_model_fields) + dir(ext_form_fields):
    if f.endswith("Field") and f != "Field":
        if not (f, f) in FormField_CHOICES:
            FormField_CHOICES.append((f, f))
FormField_CHOICES.append(("UserField", "UserField"))


def apppack():
    ret = []
    for ff in os.listdir(settings.PRJ_PATH):
        if os.path.isdir(os.path.join(settings.PRJ_PATH, ff)):
            if not ff.startswith("_"):
                ret.append([ff, ff])
    return ret


def get_field_choices():
    global Field_CHOICES
    return Field_CHOICES


Field_CHOICES = [
    ("PtigForeignKey", "PtigForeignKey!"),
    ("PtigManyToManyField", "PtigManyToManyField!"),
    ("PtigHiddenForeignKey", "PtigHiddenForeignKey!"),
    ("PtigForeignKeyWithIcon", "PtigForeignKeyWithIcon!"),
    ("PtigManyToManyFieldWithIcon", "PtigManyToManyFieldWithIcon!"),
    ("PtigTreeForeignKey", "PtigTreeForeignKey!"),
    ("UserField", "UserField"),
]

Gui_CHOICES = [
    ("standard", "standard"),
    ("modern", "modern"),
    ("tree", "tree"),
    ("tray", "tray"),
    ("dialog", "dialog"),
    ("one_form", "one_form"),
]

IconSize_CHOICES = [
    ("0", "small"),
    ("1", "medium"),
    ("2", "large"),
]

View_CHOICES = [
    ("t", "Table action"),
    ("r", "Row action"),
    ("u", "View"),
]

Url_CHOICES = [
    ("-", "default"),
    ("desktop", "desktop only"),
    ("panel", "desktop panel"),
    ("header", "desktop header"),
    ("footer", "desktop footer"),
    ("script", "javascript"),
    ("pscript", "python script"),
    ("browser", "browser only"),
    ("browser_panel", "prowser_panel"),
    ("browser_header", "browser_header"),
    ("browser_footer", "browser_footer"),
]

ViewRetType_CHOICES = [
    ("T", "Template"),
    ("O", "Odf format (default .ods)"),
    ("P", "Pdf"),
    ("J", "Json"),
    ("X", "Xml"),
    ("U", "User defined"),
    ("S", "OOXML (default .xlsx)"),
    ("t", "Txt"),
    ("H", "Html to docx template (.hdoc)"),
]

HtmlGui_CHOICES = [
    ("auto", "auto"),
    ("desktop_standard", "desktop_standard"),
    ("desktop_modern", "desktop_modern"),
    ("tablet_standard", "tablet_standard"),
    ("tablet_modern", "tablet_modern"),
    ("smartfon_standard", "smartfon_standard"),
    ("smartfon_modern", "smartfon_modern"),
]

ContentType_CHOICES = [
    ("pythonjs", "pythonjs"),
    ("react_pjsx", "react_pjsx"),
    ("css", "css"),
    ("js", "js"),
]

Static_CHOICES = [
    ("C", "css (included in desktop.html)"),
    ("J", "javascript (included in desktop.html)"),
    ("P", "python to javascript (included in desktop.html)"),
    ("R", "component (included in desktop.html)"),
    ("I", "sass to css (included in desktop.html)"),
    ("U", "custom file (embeded translation for .pyj, .webc, .sass)"),
    ("O", "Other project file"),
]

FileType_CHOICES = [
    ("f", "TemplateFilters"),
    ("t", "TemplateTags"),
    ("c", "Custom file"),
    ("m", "Management command"),
    ("p", "Plugin code"),
    ("i", "Plugin template"),
    ("l", "Library code"),
    ("s", "GraphQL schema"),
    ("r", "Rest api"),
    ("j", "Frontend view"),
    ("T", "Frontend template"),
]

Consumer_CHOICES = [
    ("WebsocketConsumer", "WebsocketConsumer"),
    ("AsyncWebsocketConsumer", "AsyncWebsocketConsumer"),
    ("JsonWebsocketConsumer", "JsonWebsocketConsumer"),
    ("AsyncJsonWebsocketConsumer", "AsyncJsonWebsocketConsumer"),
    ("AsyncHttpConsumer", "AsyncHttpConsumer"),
    ("AsyncConsumer", "AsyncConsumer"),
    ("SyncConsumer", "SyncConsumer"),
]

GuiElements_CHOICES = [
    ("toolbar(file(open,exit),clipboard)", "toolbar(file(open,exit),clipboard)"),
    (
        "toolbar(file(open,save,save_as,exit),clipboard)",
        "toolbar(file(open,save,save_as,exit),clipboard)",
    ),
    ("toolbar(browse)", "toolbar(browse)"),
]


class SChAppSet(JSONModel):

    class Meta:
        verbose_name = _("Application package")
        verbose_name_plural = _("Application packages")
        default_permissions = ("add", "change", "delete", "view", "list", "administer")
        app_label = "schbuilder"

        ordering = ["id"]

    name = models.CharField(
        "Name", null=False, blank=False, editable=True, max_length=64
    )
    title = models.CharField(
        "Title", null=False, blank=False, editable=True, max_length=255
    )
    version = models.CharField(
        "Version", null=True, blank=True, editable=True, default="latest", max_length=16
    )
    main_view = models.BooleanField(
        "Show in main view",
        null=True,
        blank=True,
        editable=True,
        default=True,
    )
    ext_apps = models.CharField(
        "Extern applications", null=True, blank=True, editable=True, max_length=4096
    )
    plugins = models.CharField(
        "Plugins", null=True, blank=True, editable=True, max_length=4096
    )
    gui_type = models.CharField(
        "Gui type",
        null=False,
        blank=False,
        editable=True,
        choices=Gui_CHOICES,
        max_length=32,
    )
    gui_elements = models.CharField(
        "Gui elements",
        null=True,
        blank=True,
        editable=True,
        choices=GuiElements_CHOICES,
        max_length=1024,
    )
    login_required = models.BooleanField(
        "Login required",
        null=True,
        blank=True,
        editable=True,
        default=False,
    )
    public = models.BooleanField(
        "Public",
        null=True,
        blank=True,
        editable=True,
        default=False,
    )
    main = models.BooleanField(
        "Main project",
        null=True,
        blank=True,
        editable=True,
        default=False,
    )
    start_page = models.CharField(
        "Start page", null=True, blank=True, editable=True, max_length=255
    )
    user_app_template = models.TextField(
        "Patches",
        null=True,
        blank=True,
        editable=False,
    )
    app_main = models.TextField(
        "Main application entrypoint",
        null=True,
        blank=True,
        editable=False,
    )
    doc = models.TextField(
        "Doc",
        null=True,
        blank=True,
        editable=False,
    )
    desktop_gui_type = models.CharField(
        "Gui type for pc web browser",
        null=False,
        blank=False,
        editable=True,
        default="auto",
        choices=HtmlGui_CHOICES,
        max_length=32,
    )
    smartfon_gui_type = models.CharField(
        "Gui type for smartfon",
        null=False,
        blank=False,
        editable=True,
        default="auto",
        choices=HtmlGui_CHOICES,
        max_length=32,
    )
    tablet_gui_type = models.CharField(
        "Gui type for tablet",
        null=False,
        blank=False,
        editable=True,
        default="auto",
        choices=HtmlGui_CHOICES,
        max_length=32,
    )
    additional_settings = models.TextField(
        "Additional settings",
        null=True,
        blank=True,
        editable=True,
    )
    custom_tags = models.TextField(
        "Custom tags",
        null=True,
        blank=True,
        editable=True,
    )
    readme_file = models.TextField(
        "README.md",
        null=True,
        blank=True,
        editable=False,
    )
    license_file = models.TextField(
        "LICENSE",
        null=True,
        blank=True,
        editable=False,
    )
    install_file = models.TextField(
        "install.ini",
        null=True,
        blank=True,
        editable=False,
    )
    encoded_zip = models.TextField(
        "Encoded zip file",
        null=True,
        blank=True,
        editable=False,
    )
    icon = models.CharField(
        "Icon", null=True, blank=True, editable=True, max_length=256
    )
    icon_size = models.CharField(
        "Icon size",
        null=False,
        blank=False,
        editable=True,
        default="1",
        choices=IconSize_CHOICES,
        max_length=1,
    )
    icon_code = models.TextField(
        "Icon code (svg)",
        null=True,
        blank=True,
        editable=False,
    )
    git_repository = models.CharField(
        "Git repository", null=True, blank=True, editable=True, max_length=255
    )
    autor_name = models.CharField(
        "Autor name", null=True, blank=True, editable=True, max_length=255
    )
    autor_email = models.CharField(
        "Autor email", null=True, blank=True, editable=True, max_length=256
    )
    autor_www = models.CharField(
        "Autor www page", null=True, blank=True, editable=True, max_length=256
    )
    components_initial_state = models.CharField(
        "The initial state of the components",
        null=True,
        blank=True,
        editable=True,
        max_length=1024,
    )
    template_desktop = models.TextField(
        "Template for desktop",
        null=True,
        blank=True,
        editable=False,
    )
    template_smartfon = models.TextField(
        "Template for smartfon",
        null=True,
        blank=True,
        editable=False,
    )
    template_tablet = models.TextField(
        "Template for tablet",
        null=True,
        blank=True,
        editable=False,
    )
    template_schweb = models.TextField(
        "Template for schweb (native app)",
        null=True,
        blank=True,
        editable=False,
    )
    template_theme = models.TextField(
        "Base template",
        null=True,
        blank=True,
        editable=False,
    )

    filter_fields = {
        "name": ["exact", "icontains", "istartswith"],
    }

    def get_ext_pytigon_apps(self, tab=None):
        if tab:
            ret = tab
        else:
            ret = []
        if self.ext_apps:
            # if self.ext_apps == '*':
            #    appset_list = SChAppSet.objects.all()
            #    for pos in appset_list:
            #        if pos.name == self.name or not pos.public:
            #            continue
            #        app_list = pos.schapp_set.all()
            #        for pos2 in app_list:
            #            name = pos.name+"."+pos2.name
            #            if not name in ret:
            #                ret.append(name)
            #    return ret
            # else:
            l = self.ext_apps.replace("\n", ",").replace(";", ",").split(",")
        else:
            return ret
        for a in l:
            if a != "" and not a.startswith("@"):
                if not a in ret:
                    ret.append(a)
        return ret

    def get_ext_apps(self, tab=None):
        if tab:
            ret = tab
        else:
            ret = []
        if self.ext_apps:
            l = self.ext_apps.replace("\n", ",").replace(";", ",").split(",")
        else:
            return ret
        for a in l:
            if a.startswith("@"):
                a = a[1:]
                if a != "":
                    if not a in ret:
                        ret.append(a)
        return ret

    def get_ext_apps_without_pack(self):
        ret = []
        if self.ext_apps:
            l = self.ext_apps.replace("\n", ",").replace(";", ",").split(",")
            for a in l:
                if a != "" and not a.startswith("@"):
                    if "." in a:
                        ret.append(a.split(".")[1])
                    else:
                        ret.append(a)
        return ret

    def get_ext_modules(self):
        ret = []
        if self.ext_apps:
            l = self.ext_apps.replace("\n", ",").replace(";", ",").split(",")
            for a in l:
                if not a.startswith("@"):
                    elms = a.split(".")
                    if len(elms) > 1:
                        module = elms[-2]
                        ret.append(module)
        return ret

    def icon_exists(self):
        return self.icon or self.icon_code

    def get_icon(self):
        if self.icon_code:
            return "data:image/svg+xml;utf8," + self.icon_code
        else:
            return self.icon

    def __str__(self):
        return self.name

    @classmethod
    def table_action(cls, list_view, request, data):
        return standard_table_action(cls, list_view, request, data, ["copy", "paste"])

    @classmethod
    def filter(cls, value, view=None, request=None):
        if value == "main_view":
            return SChAppSet.objects.filter(main_view=True)
        elif value == "not_main_view":
            return SChAppSet.objects.filter(main_view=False)
        else:
            return SChAppSet.objects.all()

    def get_form_class(self, view, request, create):
        base_form = view.get_form_class()

        class form_class(base_form):
            class Meta(base_form.Meta):
                widgets = {
                    "ext_apps": form_fields.Textarea(attrs={"cols": 80, "rows": 10}),
                    "custom_tags": form_fields.Textarea(attrs={"cols": 80, "rows": 10}),
                    "additional_settings": form_fields.Textarea(
                        attrs={"cols": 80, "rows": 20}
                    ),
                }

        return form_class


admin.site.register(SChAppSet)


class SChApp(JSONModel):

    class Meta:
        verbose_name = _("SChApp")
        verbose_name_plural = _("SChApp")
        default_permissions = ("add", "change", "delete", "view", "list", "administer")
        app_label = "schbuilder"

        ordering = ["id"]

    parent = ext_models.PtigForeignKey(
        SChAppSet,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        editable=True,
        verbose_name="Parent",
    )
    name = models.CharField(
        "Name", null=False, blank=False, editable=True, max_length=64
    )
    title = models.CharField(
        "Title", null=True, blank=True, editable=True, max_length=255
    )
    module_name = models.CharField(
        "Module name", null=False, blank=False, editable=True, max_length=64
    )
    module_title = models.CharField(
        "Module title", null=True, blank=True, editable=True, max_length=255
    )
    perms = models.BooleanField(
        "Perms",
        null=False,
        blank=False,
        editable=True,
        default=False,
    )
    index = models.CharField(
        "Index", null=True, blank=True, editable=True, max_length=255
    )
    model_code = models.TextField(
        "Model code",
        null=True,
        blank=True,
        editable=False,
    )
    view_code = models.TextField(
        "View code",
        null=True,
        blank=True,
        editable=False,
    )
    urls_code = models.TextField(
        "Urls code",
        null=True,
        blank=True,
        editable=False,
    )
    tasks_code = models.TextField(
        "Tasks code",
        null=True,
        blank=True,
        editable=True,
    )
    consumer_code = models.TextField(
        "Consumer code",
        null=True,
        blank=True,
        editable=True,
    )
    doc = models.TextField(
        "Doc",
        null=True,
        blank=True,
        editable=False,
    )
    user_param = models.TextField(
        "Urser parameter",
        null=True,
        blank=True,
        editable=True,
    )
    icon = models.CharField(
        "Icon", null=True, blank=True, editable=True, max_length=256
    )
    icon_size = models.CharField(
        "Icon size",
        null=False,
        blank=False,
        editable=True,
        default="1",
        choices=IconSize_CHOICES,
        max_length=1,
    )
    icon_code = models.TextField(
        "Icon code",
        null=True,
        blank=True,
        editable=False,
    )

    filter_fields = {
        "name": ["exact", "icontains", "istartswith"],
    }

    def get_models(self):
        ret = [
            "'self'",
        ]
        tmp = set()
        for app in self.parent.schapp_set.all():
            for tab in app.schtable_set.all():
                if app.name == self.name:
                    ret.append(tab.name)
                else:
                    tmp.add(app.name + "." + tab.name)
        if self.parent.ext_apps:
            ext_apps = self.parent.ext_apps.replace("\n", ",").split(",")
        else:
            ext_apps = []

        if len(ext_apps) > 0:
            for ext_app in ext_apps:
                if "schserw." in ext_app:
                    try:
                        module = __import__(ext_app + ".models")
                        app = getattr(module, ext_app.split(".")[1])
                        models = getattr(app, "models")
                        for name in dir(models):
                            obj = getattr(models, name)
                            if inspect.isclass(obj):
                                tmp.add(ext_app + "." + name)
                    except:
                        pass
            for ext_app in ext_apps:
                if not "schserw." in ext_app:
                    try:
                        appset = ext_app.split(".")[0].strip()
                        appname = ext_app.split(".")[1].strip()
                        prj_path = os.path.join(settings.PRJ_PATH, appset)
                        if not os.path.exists(prj_path):
                            prj_path = os.path.join(settings.PRJ_PATH_ALT, appset)
                            if not os.path.exists(prj_path):
                                continue
                        model_path = os.path.join(prj_path, appname, "models.py")
                        if os.path.exists(model_path):
                            line1 = ""
                            line2 = ""
                            line3 = ""
                            with open(model_path, "rt") as f:
                                txt = f.read()
                                for line in txt.split("\n"):
                                    if "class Meta:" in line:
                                        x = None
                                        if line1.startswith("class "):
                                            x = line1
                                        elif line2.startswith("class "):
                                            x = line2
                                        elif line3.startswith("class "):
                                            x = line3
                                        if x:
                                            name = x[6:].split("(")[0].strip()
                                            tmp.add(appname + "." + name)
                                    line3 = line2
                                    line2 = line1
                                    line1 = line
                    except:
                        traceback.print_exception(*sys.exc_info())
            if tmp:
                ret += sorted(tmp)
        return ret

    def get_urls(self, main=False):
        ret = []
        for table in self.schtable_set.all():
            if table.generic:
                ret.append("table/" + table.name + "/-/form/list/")
            for field in table.schfield_set.all():
                if field.is_rel():
                    if field.type[0] == "G":
                        if field.name == "parent" and field.rel_to == "'self'":
                            ret.append("table/" + table.name + "/0/form/tree/")
        for view in self.schview_set.all():
            if view.url and view.url != "":
                if not main:
                    if view.view_type == "r":
                        url = "table/" + view.url + "/<<pk>>/action/" + view.name + "/"
                        ret.append(url)
                if view.view_type == "t":
                    url = "table/" + view.url + "/action/" + view.name + "/"
                    ret.append(url)
                if view.view_type == "u":
                    if not (main and "?P" in view.url):
                        ret.append(view.url)
        for template in self.schtemplate_set.all():
            if template.direct_to_template:
                ret.append(template.get_url_name())
        # for wiki in Page.objects.all():
        #   url = 'schwiki/{{%s}}/{{%s}}/view/' % (wiki.subject, wiki.name)
        #   ret.append(url)
        for form in self.schform_set.all():
            if not form.name.startswith("_"):
                ret.append("form/" + form.name + "/")

        for form in self.schform_set.all():
            if not form.name.startswith("_"):
                ret.append("form/" + form.name + "/")

        for f in self.schfiles_set.all():
            if f.file_type == "j":
                ret.append("../static/" + self.name + "/views/" + f.name + ".fview")

        if "_schdata.schelements" in self.parent.ext_apps:
            ret.append(
                "../schelements/table/DocHead/[[docreg_name/form/docheadlist/?view_in=desktop"
            )
            ret.append(
                "../schelements/table/DocHead/[[docreg_name]]/[[target]]/docheadlist/?view_in=desktop"
            )
            ret.append(
                "../schelements/view_elements/[[element_code]]/[[element_type]]/-/?view_in=desktop"
            )
            ret.append(
                "../schelements/view_elements/[[element_code or -]]/[[element_type or -]]/[[app_name]]__[[target_name]]/"
            )
            ret.append(
                "../schelements/view_elements_as_tree/[[element_code or -]]/[[element_type or -]]/-/?view_in=desktop"
            )
            ret.append(
                "../schelements/view_elements_as_tree/[[element_code or -]]/[[element_type or -]]/[[app_name]]__[[target_name]]/?view_in=desktop"
            )
            ret.append(
                "../schelements/view_elements_of_type/[[element_type or -]]/-/?view_in=desktop"
            )
            ret.append(
                "../schelements/view_elements_of_type/[[element_type or -]]/[[app_name]]__[[target_name]]/?view_in=desktop"
            )
            ret.append(
                "../schstruct/list_group_by_tag/[[tag]]/[[app_name]]__[[target_name]]/?view_in=desktop"
            )

        if "_schdata.schstruct" in self.parent.ext_apps:
            ret.append(
                "../schstruct/list_group_by_tag/[[element_type]]/[[app_name]]__[[target_name]]/?view_in=desktop"
            )

        if "_schtools.schworkflow" in self.parent.ext_apps:
            ret.append(
                "../schworkflow/table/WorkflowItem//[app_name]__[[taable_name]]__0__[[filter]]/form__[[target]]/sublist/?fragment=page"
            )

        return ret

    def model_code_start(self):
        if self.model_code:
            return self.model_code.split("[[[GEN]]]")[0]
        else:
            return ""

    def model_code_end(self):
        if self.model_code:
            x = self.model_code.split("[[[GEN]]]")
            if len(x) > 1:
                return x[1]
        return ""

    def icon_exists(self):
        return self.icon or self.icon_code

    def get_icon(self):
        if self.icon_code:
            return "data:image/svg+xml;utf8," + self.icon_code
        else:
            return self.icon

    def get_models_to_import(self):
        tab = []
        for table in self.schtable_set.all():
            if table.base_table and "." in table.base_table:
                x = table.base_table.split(".")
                if x[-2] != "models":
                    if not x[-2] in tab:
                        tab.append(x[-2])
            for field in table.schfield_set.all():
                if field.is_rel():
                    if field.rel_to and "." in field.rel_to:
                        x = field.rel_to.split(".")
                        if not x[-2] in tab:
                            tab.append(x[-2])
        return tab

    def __str__(self):
        return self.name


admin.site.register(SChApp)


class SChChoice(models.Model):

    class Meta:
        verbose_name = _("SChChoice")
        verbose_name_plural = _("SChChoice")
        default_permissions = ("add", "change", "delete", "view", "list", "administer")
        app_label = "schbuilder"

        ordering = ["id"]

    parent = ext_models.PtigHiddenForeignKey(
        SChApp,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        editable=True,
        verbose_name="Parent",
    )
    name = models.CharField(
        "Name", null=False, blank=False, editable=True, max_length=255
    )
    verbose_name = models.CharField(
        "Verbose name", null=False, blank=False, editable=True, max_length=255
    )

    def __str__(self):
        return self.name


admin.site.register(SChChoice)


class SChChoiceItem(models.Model):

    class Meta:
        verbose_name = _("SChChoiceItem")
        verbose_name_plural = _("SChChoiceItem")
        default_permissions = ("add", "change", "delete", "view", "list", "administer")
        app_label = "schbuilder"

        ordering = ["id"]

    parent = ext_models.PtigHiddenForeignKey(
        SChChoice,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        editable=True,
        verbose_name="Parent",
    )
    name = models.CharField(
        "Key name", null=False, blank=False, editable=True, max_length=255
    )
    value = models.CharField(
        "Verbose name", null=False, blank=False, editable=True, max_length=255
    )

    def __str__(self):
        return self.name


admin.site.register(SChChoiceItem)


class SChTable(models.Model):

    class Meta:
        verbose_name = _("SChTable")
        verbose_name_plural = _("SChTable")
        default_permissions = ("add", "change", "delete", "view", "list", "administer")
        app_label = "schbuilder"

        ordering = ["id"]

    parent = ext_models.PtigHiddenForeignKey(
        SChApp,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        editable=True,
        verbose_name="Parent",
    )
    base_table = models.CharField(
        "Base table", null=True, blank=True, editable=True, max_length=255
    )
    name = models.CharField(
        "Name", null=False, blank=False, editable=True, max_length=255
    )
    verbose_name = models.CharField(
        "Verbose name", null=False, blank=False, editable=True, max_length=255
    )
    verbose_name_plural = models.CharField(
        "Verbose name plural", null=False, blank=False, editable=True, max_length=255
    )
    metaclass_code = models.TextField(
        "Metaclass code",
        null=True,
        blank=True,
        editable=False,
    )
    table_code = models.TextField(
        "Table code",
        null=True,
        blank=True,
        editable=False,
    )
    ordering = models.CharField(
        "Ordering",
        null=True,
        blank=True,
        editable=True,
        default="['id']",
        max_length=255,
    )
    doc = models.TextField(
        "Doc",
        null=True,
        blank=True,
        editable=False,
    )
    generic = models.BooleanField(
        "Generic",
        null=False,
        blank=False,
        editable=True,
        default=False,
    )
    url_params = models.CharField(
        "Url params", null=True, blank=True, editable=True, max_length=255
    )
    proxy_model = models.CharField(
        "Proxy model", null=True, blank=True, editable=True, max_length=255
    )

    def get_models(self):
        return self.parent.get_models()

    def get_base_table(self):
        l = self.base_table.split(".")
        if len(l) > 1 and l[-2] != "models":
            return l[-2] + ".models." + l[-1]
        else:
            return self.base_table

    def fields_have_parent(self):
        return self.schfield_set.filter(name="parent").count() > 0

    def template_for_object(self, view, context, doc_type):
        if "field_name" in context and context["field_name"] in ("table_code",):
            return "schbuilder/db_field_edt_table.html"
        return None

    def __str__(self):
        return self.name


admin.site.register(SChTable)


class SChField(models.Model):

    class Meta:
        verbose_name = _("SChField")
        verbose_name_plural = _("SChField")
        default_permissions = ("add", "change", "delete", "view", "list", "administer")
        app_label = "schbuilder"

        ordering = ["id"]

    parent = ext_models.PtigHiddenForeignKey(
        SChTable,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        editable=True,
        verbose_name="Parent",
    )
    name = models.CharField(
        "Name", null=True, blank=True, editable=True, max_length=255
    )
    description = models.CharField(
        "Description", null=True, blank=True, editable=True, max_length=255
    )
    type = models.CharField(
        "Type",
        null=False,
        blank=False,
        editable=True,
        choices=get_field_choices,
        max_length=64,
    )
    null = models.BooleanField(
        "Null",
        null=False,
        blank=False,
        editable=True,
        default=False,
    )
    blank = models.BooleanField(
        "Blank",
        null=False,
        blank=False,
        editable=True,
        default=False,
    )
    editable = models.BooleanField(
        "Editable",
        null=False,
        blank=False,
        editable=True,
        default=False,
    )
    unique = models.BooleanField(
        "Unique",
        null=False,
        blank=False,
        editable=True,
        default=False,
    )
    db_index = models.BooleanField(
        "DB index",
        null=False,
        blank=False,
        editable=True,
        default=False,
    )
    default = models.CharField(
        "Default", null=True, blank=True, editable=True, max_length=255
    )
    help_text = models.CharField(
        "Help text", null=True, blank=True, editable=True, max_length=255
    )
    choices = models.CharField(
        "Choices", null=True, blank=True, editable=True, max_length=255
    )
    rel_to = models.CharField(
        "Relation to", null=True, blank=True, editable=True, max_length=255
    )
    param = models.CharField(
        "Param", null=True, blank=True, editable=True, max_length=255
    )
    url_params = models.CharField(
        "Url params", null=True, blank=True, editable=True, max_length=255
    )

    def init_new(self, request, view, param=None):
        if param:
            self.type = param

            defaults = self.get_field_defaults()
            defaults["type"] = param

            for key in defaults:
                value = getattr(self, key)
                if not value:
                    setattr(self, key, defaults[key])
            return defaults
        else:
            return None

    def save(self, force_insert=False, force_update=False):
        super(SChField, self).save(force_insert, force_update)

    def __str__(self):
        return self.name

    def is_rel(self):
        if "Key" in self.type or "Many" in self.type or "OneToOne" in self.type:
            return True
        else:
            return False

    def is_generic_rel(self):
        if self.is_rel() and self.type[0] == "G":
            return True
        else:
            return False

    def has_choices(self):
        if self.type in ("CharField",):
            return True
        else:
            return False

    def get_models(self):
        return self.parent.get_models()

    def as_declaration(self):
        # if 'TreeForeignKey' in self.type:
        #    if not self.parent.base_table in ("", "models.Model"):
        #        return ""

        if self.type == "NullBooleanField":
            self.type = "BooleanField"
            self.null = True

        if self.type == "UserField":
            return self.param
        type_desc = dict(Field_CHOICES)[self.type]
        if type_desc.endswith("!"):
            module = "ext_models."
        else:
            module = "models."
        if self.is_rel():
            # rel_model =self.rel_to.split('.')[-1]
            x = self.rel_to.split(".")
            if len(x) > 1:
                rel_model = x[-2] + ".models." + x[-1]
            else:
                rel_model = self.rel_to
            # if self.type.startswith('Ptig'):
            #    if 'ForeignKey' in self.type:
            #        ret = "%s = %s%s(%s, on_delete=models.CASCADE, null=%s, blank=%s, editable=%s, verbose_name='%s', " % \
            #            (self.name, module, self.type[1:], rel_model, self.null, self.blank, self.editable, self.description)
            #    else:
            #        ret = "%s = %s%s(%s, null=%s, blank=%s, editable=%s, verbose_name='%s', " % \
            #            (self.name, module, self.type[1:], rel_model, self.null, self.blank, self.editable, self.description)
            # else:
            if "ForeignKey" in self.type or "OneToOne" in self.type:
                ret = (
                    "%s = %s%s(%s, on_delete=models.CASCADE, null=%s, blank=%s, editable=%s, verbose_name='%s', "
                    % (
                        self.name,
                        module,
                        self.type,
                        rel_model,
                        self.null,
                        self.blank,
                        self.editable,
                        self.description,
                    )
                )
            else:
                ret = (
                    "%s = %s%s(%s, null=%s, blank=%s, editable=%s, verbose_name='%s', "
                    % (
                        self.name,
                        module,
                        self.type,
                        rel_model,
                        self.null,
                        self.blank,
                        self.editable,
                        self.description,
                    )
                )
        else:
            ret = "%s = %s%s('%s', null=%s, blank=%s, editable=%s, " % (
                self.name,
                module,
                self.type,
                self.description,
                self.null,
                self.blank,
                self.editable,
            )
        if self.unique:
            ret += "unique=%s," % self.unique
        if self.default and len(self.default) > 0:
            ret += "default=%s," % self.default
        if self.help_text and len(self.help_text) > 0:
            ret += "help_text=%s," % self.help_text
        if self.choices:
            ret += "choices=%s," % self.choices
        if self.db_index:
            ret += "db_index=True,"
        if self.param and len(self.param) > 0:
            ret += self.param
            # .replace(':','=')
        ret += ")"
        return ret

    def get_field_defaults(self):
        ret = field_default.copy()
        if self.type in field_defaults:
            for key, value in field_defaults[self.type].items():
                ret[key] = value
        return ret

    def get_rel_to(self):
        if self.rel_to == "'self'":
            return self.parent.name
        else:
            return self.rel_to

    def get_relate_set_name(self):
        if self.param and "related_name" in self.param:
            for pos in self.param.split(","):
                rec = pos.split("=")
                if rec[0].strip() == "related_name":
                    return rec[1].replace("'", "").replace('"', "").strip()
        return self.parent.name.lower() + "_set"

    @classmethod
    def table_action(cls, list_view, request, data):
        return standard_table_action(cls, list_view, request, data, ["copy", "paste"])


admin.site.register(SChField)


class SChView(models.Model):

    class Meta:
        verbose_name = _("SChView")
        verbose_name_plural = _("SChView")
        default_permissions = ("add", "change", "delete", "view", "list", "administer")
        app_label = "schbuilder"

        ordering = ["id"]

    parent = ext_models.PtigHiddenForeignKey(
        SChApp,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        editable=True,
        verbose_name="Parent",
    )
    name = models.CharField(
        "Name", null=False, blank=False, editable=True, max_length=255
    )
    view_type = models.CharField(
        "View type",
        null=False,
        blank=False,
        editable=True,
        choices=View_CHOICES,
        max_length=1,
    )
    param = models.CharField(
        "Param", null=True, blank=True, editable=True, max_length=255
    )
    url = models.CharField("Url", null=True, blank=True, editable=True, max_length=255)
    view_code = models.TextField(
        "View code",
        null=True,
        blank=True,
        editable=False,
    )
    url_params = models.CharField(
        "Url params", null=True, blank=True, editable=True, max_length=255
    )
    ret_type = models.CharField(
        "Return value type",
        null=False,
        blank=False,
        editable=True,
        default="U",
        choices=ViewRetType_CHOICES,
        max_length=1,
    )
    asynchronous = models.BooleanField(
        "Async",
        null=True,
        blank=True,
        editable=True,
        default=False,
    )
    extra_code = models.TextField(
        "Extra code",
        null=True,
        blank=True,
        editable=False,
    )
    doc = models.TextField(
        "Doc",
        null=True,
        blank=True,
        editable=False,
    )

    def init_new(self, request, view, param=None):
        if param:
            self.view_type = param
            defaults = {}
            defaults["view_type"] = param
            if param == "r":
                self.param = "pk"
                defaults["param"] = self.param
            if param == "t":
                pass
            if param == "u":
                defaults["param"] = "**argv"
                defaults["url_params"] = "{}"
                defaults["url"] = (
                    "fun/<str:str_param>/<slug:slug_param>/<int:int_param>/"
                )
            return defaults
        else:
            return None

    def get_name(self):
        if "/" in self.name:
            return self.name.split("/")[-1]
        elif "#" in self.name:
            return self.name.split("#")[0]
        else:
            return self.name

    def get_url(self):
        name = self.get_name()
        if self.view_type == "u":
            if "(?P" in self.url:
                if self.url_params and self.url_params != "":
                    return "re_path(r'%s', views.%s, %s, name='%s')" % (
                        self.url,
                        name,
                        self.url_params,
                        self.parent.name + "_" + name,
                    )
                else:
                    return "re_path(r'%s', views.%s, name='%s')" % (
                        self.url,
                        name,
                        self.parent.name + "_" + name,
                    )
            else:
                if self.url_params and self.url_params != "":
                    return "path('%s', views.%s, %s, name='%s')" % (
                        self.url,
                        name,
                        self.url_params,
                        self.parent.name + "_" + name,
                    )
                else:
                    return "path('%s', views.%s, name='%s')" % (
                        self.url,
                        name,
                        self.parent.name + "_" + name,
                    )
        else:
            if self.view_type == "r":
                bname = "gen_row_action"
            else:
                bname = "gen_tab_action"

            if self.url_params and self.url_params != "":
                if "#" in self.name:
                    x = self.name.split("#")
                    return "%s('%s', '%s', views.%s, %s)" % (
                        bname,
                        self.url,
                        x[0],
                        x[1],
                        self.url_params,
                    )
                else:
                    return "%s('%s', '%s', views.%s, %s)" % (
                        bname,
                        self.url,
                        self.name,
                        name,
                        self.url_params,
                    )
            else:
                if "#" in self.name:
                    x = self.name.split("#")
                    return "%s('%s', '%s', views.%s)" % (bname, self.url, x[0], x[1])
                else:
                    return "%s('%s', '%s', views.%s)" % (
                        bname,
                        self.url,
                        self.name,
                        name,
                    )

    def __str__(self):
        return self.name

    def template_for_object(self, view, context, doc_type):
        if "field_name" in context and context["field_name"] in ("view_code",):
            return "schbuilder/db_field_edt_mod.html"
        return None

    def get_models(self):
        return self.parent.get_models()

    def clean_url(self):
        return self.url.replace("$", "")

    def view_code_start(self):
        if self.extra_code:
            return self.extra_code.split("[[[GEN]]]")[0]
        else:
            return ""

    def view_code_end(self):
        if self.extra_code:
            x = self.extra_code.split("[[[GEN]]]")
            if len(x) > 1:
                return x[1]
        return ""


admin.site.register(SChView)


class SChStatic(models.Model):

    class Meta:
        verbose_name = _("Static file")
        verbose_name_plural = _("Static files")
        default_permissions = ("add", "change", "delete", "view", "list", "administer")
        app_label = "schbuilder"

        ordering = ["id"]

    parent = ext_models.PtigHiddenForeignKey(
        SChAppSet,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        editable=True,
        verbose_name="Parent",
    )
    type = models.CharField(
        "Type",
        null=False,
        blank=False,
        editable=True,
        choices=Static_CHOICES,
        max_length=1,
    )
    name = models.CharField(
        "Name", null=False, blank=False, editable=True, max_length=64
    )
    code = models.TextField(
        "Code",
        null=True,
        blank=True,
        editable=False,
    )
    doc = models.TextField(
        "Doc",
        null=True,
        blank=True,
        editable=False,
    )

    def __str__(self):
        return self.get_type_display() + "/" + self.name

    def __lt__(self, other):
        return (self.name < other.name) and (self.name < other.name)


admin.site.register(SChStatic)


class SChTemplate(models.Model):

    class Meta:
        verbose_name = _("SChTemplate")
        verbose_name_plural = _("SChTemplate")
        default_permissions = ("add", "change", "delete", "view", "list", "administer")
        app_label = "schbuilder"

        ordering = ["id"]

    parent = ext_models.PtigHiddenForeignKey(
        SChApp,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        editable=True,
        verbose_name="Parent",
    )
    name = models.CharField(
        "Name", null=False, blank=False, editable=True, max_length=255
    )
    direct_to_template = models.BooleanField(
        "Direct to template",
        null=True,
        blank=True,
        editable=True,
    )
    url = models.CharField("Url", null=True, blank=True, editable=True, max_length=64)
    url_parm = models.CharField(
        "Parameters passed to the template",
        null=True,
        blank=True,
        editable=True,
        max_length=128,
    )
    template_code = models.TextField(
        "Template code",
        null=True,
        blank=True,
        editable=False,
    )
    static_files = models.ManyToManyField(
        SChStatic,
        null=True,
        blank=True,
        editable=True,
        verbose_name="Static files",
    )
    tags_mount = models.CharField(
        "Mount component tags", null=True, blank=True, editable=True, max_length=256
    )
    asynchronous = models.BooleanField(
        "Async",
        null=True,
        blank=True,
        editable=True,
        default=False,
    )

    TAG_LIBS = [
        "cache",
        "i18n",
        "l10n",
        "static",
        "tz",
        "log",
        "catch",
        "collapse",
        "defexfiltry",
        "exfiltry",
        "expr",
        "exsyntax",
        "htmlwidget",
        "mptt_tags",
        "compress",
    ]

    def get_url_name(self):
        if self.url and self.url != "":
            return self.url
        else:
            return self.name

    def get_url(self):
        if self.direct_to_template:
            url_name = self.get_url_name()
            app_name = self.parent.name
            template_name = self.name.lower().replace(" ", "_") + ".html"
            if self.url_parm:
                param = self.url_parm
            else:
                param = ""
            if "(?P" in self.url:
                return (
                    "re_path(r'^%s', TemplateView.as_view(template_name='%s/%s'), {%s})"
                    % (url_name, app_name, template_name, param)
                )
            else:
                return (
                    "path('%s', TemplateView.as_view(template_name='%s/%s'), {%s})"
                    % (url_name, app_name, template_name, param)
                )
        else:
            return None

    def _get_table_fields(self, table):
        ret = []
        if table and hasattr(table, "schfield_set"):
            for pos in table.schfield_set.all():
                ret.append(pos)
            if table.base_table and table.base_table != None:
                tables = SChTable.objects.filter(name=table.base_table)
                if len(tables) > 0:
                    ret2 = self._get_table_fields(
                        SChTable.objects.filter(name=tables[0].base_table)
                    )
                    for pos in ret2:
                        ret.append(pos)
        return ret

    def get_table_fields(self):
        return self._get_table_fields(self.get_rel_table())

    def get_all_table_fields(self):
        return [pos.name for pos in self._get_table_fields(self.get_rel_table())]

    def get_rel_table_fields(self):
        return [pos.name for pos in self._get_table_fields(self.get_rel_table())]

    def get_edit_table_fields(self):
        return list(
            [
                pos.name
                for pos in self._get_table_fields(self.get_rel_table())
                if pos.type == "TextField"
            ]
        )

    def get_rel_table(self):
        tables = self.parent.schtable_set.filter(parent=self.parent).filter(
            name=self.name
        )
        if len(tables) > 0:
            return tables[0]
        else:
            return None

    def get_table_methods(self):
        ret = []
        table = self.get_rel_table()
        if table:
            if table.table_code:
                for line in table.table_code.split("\n"):
                    if line.startswith("def"):
                        buf = line[4:].replace(" ", "")
                        if "(self)" in buf and not buf.startswith("_"):
                            ret.append(buf.split("(")[0])
        return ret

    def get_tables_for_template(self):
        app = self.parent
        app_set = app.parent
        buf = []
        object_list = app_set.schapp_set.all()
        for pos in object_list:
            buf.append(pos)
        ext_apps = app_set.ext_apps
        if ext_apps:
            app_list = ext_apps.replace("\n", ",").replace(";", ",").split(",")
            for pos in app_list:
                if "." in pos:
                    app_set_str, app_str = pos.split(".")
                    object_list = SChApp.objects.filter(
                        parent__name=app_set_str, name=app_str
                    )
                    if len(object_list) > 0:
                        buf.append(object_list[0])
        ret = []
        for pos in buf:
            for table in pos.schtable_set.all():
                ret.append(table)
        return ret

    def get_table_rel_fields(self):
        table = self.get_rel_table()
        ret = []
        if table:
            tables = self.get_tables_for_template()
            for table2 in tables:
                field_list = table2.schfield_set.all()
                for field in field_list:
                    if field.rel_to == table.name:
                        if field.param and "related_name" in field.param:
                            x = (
                                field.param.replace(" ", "")
                                .split("related_name=")[1]
                                .replace('"', "'")
                                .split("'")[1]
                            )
                            ret.append(x)
                        else:
                            ret.append(table2.name.lower() + "_set")
        return ret

    def get_django_filters(self):
        ret = []
        django_engine = engines["django"].engine
        for pos in django_engine.template_builtins:
            for f in pos.filters:
                ret.append(f)
        return ret

    def get_django_tags(self):
        ret = []
        django_engine = engines["django"].engine
        for pos in django_engine.template_builtins:
            for f in pos.tags:
                ret.append(f)
        return ret

    def get_pytigon_filters(self):
        ret = []
        for name, lib in engines["django"].engine.template_libraries.items():
            if name in self.TAG_LIBS:
                for name in lib.filters:
                    ret.append(name)
        return ret

    def get_pytigon_tags(self):
        ret = []
        for name, lib in engines["django"].engine.template_libraries.items():
            if name in self.TAG_LIBS:
                for name in lib.tags:
                    ret.append(name)
        return ret

    def get_blocks(self):
        ret = []
        form_path = os.path.join(
            os.path.dirname(pytigon.__file__), "templates", "base0.html"
        )
        f = open(form_path, "rt")
        buf = f.read()
        f.close()
        for line in buf.split("\n"):
            line2 = line.strip()
            if line2.startswith("{% block"):
                ret.append(line2.split(" ", 3)[2])
        return ret

    def get_template_widgets(self):
        return widgets

    def template_for_object(self, view, context, doc_type):
        if doc_type == "py":
            return "schbuilder/db_field_edt_template.html"
        return None

    def __str__(self):
        return self.name


admin.site.register(SChTemplate)


class SChAppMenu(models.Model):

    class Meta:
        verbose_name = _("SChAppMenu")
        verbose_name_plural = _("SChAppMenu")
        default_permissions = ("add", "change", "delete", "view", "list", "administer")
        app_label = "schbuilder"

        ordering = ["id"]

    parent = ext_models.PtigHiddenForeignKey(
        SChApp,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        editable=True,
        verbose_name="Parent",
    )
    name = models.CharField(
        "Name", null=False, blank=False, editable=True, max_length=255
    )
    url = models.CharField(
        "Url", null=False, blank=False, editable=True, max_length=255
    )
    url_type = models.CharField(
        "Url type",
        null=True,
        blank=True,
        editable=True,
        default="-",
        choices=Url_CHOICES,
        max_length=16,
    )
    perms = models.CharField(
        "Perms", null=True, blank=True, editable=True, max_length=255
    )
    icon = models.CharField(
        "Icon", null=True, blank=True, editable=True, max_length=255
    )
    icon_size = models.CharField(
        "Icon size",
        null=False,
        blank=False,
        editable=True,
        default="1",
        choices=IconSize_CHOICES,
        max_length=1,
    )
    icon_code = models.TextField(
        "Icon code (svg)",
        null=True,
        blank=True,
        editable=False,
    )

    def not_standard_icon_size(self):
        if self.icon_size == "1":
            return False
        else:
            return True

    def icon_exists(self):
        return self.icon or self.icon_code

    def get_icon(self):
        if self.icon_code:
            return "data:image/svg+xml;utf8," + self.icon_code
        else:
            return self.icon

    def get_perms(self):
        if self.perms and self.perms != " ":
            return "'%s'" % self.perms
        else:
            return "None"

    def get_main_urls(self):
        return self.parent.get_urls(main=True)

    def get_urls(self):
        return self.parent.get_urls(main=False)

    def get_url_type_ext(self):
        if self.url_type in [None, "-"]:
            return ""
        else:
            if "?" in self.url:
                return "&view_in=" + self.url_type
            else:
                return "?view_in=" + self.url_type

    def clean_url(self):
        return self.url.replace("$", "")

    def __str__(self):
        return self.name


admin.site.register(SChAppMenu)


class SChForm(models.Model):

    class Meta:
        verbose_name = _("Form")
        verbose_name_plural = _("Form")
        default_permissions = ("add", "change", "delete", "view", "list", "administer")
        app_label = "schbuilder"

        ordering = ["id"]

    parent = ext_models.PtigHiddenForeignKey(
        SChApp,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        editable=True,
        verbose_name="Parent",
    )
    name = models.CharField(
        "Name", null=False, blank=False, editable=True, max_length=64
    )
    module = models.CharField(
        "Module", null=True, blank=True, editable=True, max_length=64
    )
    process_code = models.TextField(
        "Process code",
        null=True,
        blank=True,
        editable=True,
    )
    end_class_code = models.TextField(
        "End class code",
        null=True,
        blank=True,
        editable=True,
    )
    end_code = models.TextField(
        "End code",
        null=True,
        blank=True,
        editable=True,
    )
    asynchronous = models.BooleanField(
        "Async",
        null=True,
        blank=True,
        editable=True,
        default=False,
    )
    doc = models.TextField(
        "Doc",
        null=True,
        blank=True,
        editable=True,
    )

    def template_for_object(self, view, context, doc_type):
        if "field_name" in context and context["field_name"] in (
            "process_code",
            "end_class_code",
            "end_code",
        ):
            return "schbuilder/db_field_edt_form.html"
        return None


admin.site.register(SChForm)


class SChFormField(models.Model):

    class Meta:
        verbose_name = _("Form field")
        verbose_name_plural = _("Form field")
        default_permissions = ("add", "change", "delete", "view", "list", "administer")
        app_label = "schbuilder"

        ordering = ["id"]

    parent = ext_models.PtigHiddenForeignKey(
        SChForm,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        editable=True,
        verbose_name="Parent",
    )
    name = models.CharField(
        "Name", null=False, blank=False, editable=True, max_length=64
    )
    type = models.CharField(
        "Type",
        null=False,
        blank=False,
        editable=True,
        choices=FormField_CHOICES,
        max_length=64,
    )
    required = models.BooleanField(
        "Required",
        null=False,
        blank=False,
        editable=True,
        default=False,
    )
    label = models.CharField(
        "Label", null=False, blank=False, editable=True, max_length=64
    )
    initial = models.CharField(
        "Initial", null=True, blank=True, editable=True, max_length=256
    )
    widget = models.CharField(
        "Widget", null=True, blank=True, editable=True, max_length=256
    )
    help_text = models.CharField(
        "Help text", null=True, blank=True, editable=True, max_length=256
    )
    error_messages = models.CharField(
        "Error messages", null=True, blank=True, editable=True, max_length=64
    )
    param = models.CharField(
        "Param", null=True, blank=True, editable=True, max_length=1024
    )

    def init_new(self, request, view, param=None):
        if param:
            self.type = param

            defaults = self.get_field_defaults()
            defaults["type"] = param

            for key in defaults:
                setattr(self, key, defaults[key])
            return defaults
        else:
            return None

    def as_declaration(self):
        if self.type == "UserField":
            return self.param
        if hasattr(ext_form_fields, self.type):
            ret = "%s = ext_form_fields.%s(label=_('%s'), required=%s, " % (
                self.name,
                self.type,
                self.label,
                self.required,
            )
        else:
            ret = "%s = forms.%s(label=_('%s'), required=%s, " % (
                self.name,
                self.type,
                self.label,
                self.required,
            )
        if self.initial:
            ret += "initial=%s," % self.initial
        if self.widget and len(self.widget) > 0:
            ret += "widget=%s," % self.widget
        if self.help_text and len(self.help_text) > 0:
            ret += "help_text=%s," % self.help_text
        if self.error_messages:
            ret += "error_messages=%s," % self.error_messages
        if self.param and len(self.param) > 0:
            ret += self.param
        ret += ")"
        return ret

    def get_field_defaults(self):
        ret = formfield_default.copy()
        if self.type in formfield_defaults:
            for key, value in formfield_defaults[self.type].items():
                ret[key] = value
        return ret


admin.site.register(SChFormField)


class SChTask(models.Model):

    class Meta:
        verbose_name = _("SChTask")
        verbose_name_plural = _("SChTask")
        default_permissions = ("add", "change", "delete", "view", "list", "administer")
        app_label = "schbuilder"

        ordering = ["id"]

    parent = ext_models.PtigHiddenForeignKey(
        SChApp,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        editable=True,
        verbose_name="Parent",
    )
    name = models.CharField(
        "Name", null=False, blank=False, editable=True, max_length=255
    )
    code = models.TextField(
        "Code",
        null=True,
        blank=True,
        editable=False,
    )
    doc = models.TextField(
        "Doc",
        null=True,
        blank=True,
        editable=False,
    )
    perms = models.CharField(
        "Perms", null=True, blank=True, editable=True, max_length=255
    )
    publish = models.BooleanField(
        "Publish",
        null=True,
        blank=True,
        editable=True,
    )
    publish_group = models.CharField(
        "Publish group", null=True, blank=True, editable=True, max_length=64
    )

    def template_for_object(self, view, context, doc_type):
        if doc_type == "py":
            return "schbuilder/db_field_edt_task.html"
        return None

    def get_name(self):
        return self.name


admin.site.register(SChTask)


class SChFiles(models.Model):

    class Meta:
        verbose_name = _("SChFiles")
        verbose_name_plural = _("SChFiles")
        default_permissions = ("add", "change", "delete", "view", "list", "administer")
        app_label = "schbuilder"

        ordering = ["id"]

    parent = ext_models.PtigHiddenForeignKey(
        SChApp,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        editable=True,
        verbose_name="Parent",
    )
    file_type = models.CharField(
        "File  type",
        null=False,
        blank=False,
        editable=True,
        choices=FileType_CHOICES,
        max_length=3,
    )
    name = models.CharField(
        "Name", null=False, blank=False, editable=True, max_length=256
    )
    content = models.TextField(
        "Content",
        null=True,
        blank=True,
        editable=False,
    )

    def save(self, *argi, **argv):
        if self.file_type == "r" and not self.content:
            self.content = render_to_string("schbuilder/wzr/rest_api.html", {})
        elif self.file_type == "s" and not self.content:
            self.content = render_to_string("schbuilder/wzr/graphql_api.html", {})
        super().save(*argi, **argv)


admin.site.register(SChFiles)


class SChLocale(models.Model):

    class Meta:
        verbose_name = _("Locale")
        verbose_name_plural = _("Locales")
        default_permissions = ("add", "change", "delete", "view", "list", "administer")
        app_label = "schbuilder"

        ordering = ["id"]

    parent = ext_models.PtigHiddenForeignKey(
        SChAppSet,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        editable=True,
        verbose_name="Parent",
    )
    name = models.CharField(
        "Name", null=False, blank=False, editable=True, max_length=16
    )


admin.site.register(SChLocale)


class SChTranslate(models.Model):

    class Meta:
        verbose_name = _("Translate")
        verbose_name_plural = _("Translate")
        default_permissions = ("add", "change", "delete", "view", "list", "administer")
        app_label = "schbuilder"

        ordering = ["id"]

    parent = ext_models.PtigHiddenForeignKey(
        SChLocale,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        editable=False,
        verbose_name="Parent",
    )
    description = models.CharField(
        "Description", null=False, blank=False, editable=True, max_length=1024
    )
    translation = models.CharField(
        "Translation", null=True, blank=True, editable=True, max_length=1024
    )
    status = models.CharField(
        "Status", null=True, blank=True, editable=False, max_length=16
    )


admin.site.register(SChTranslate)


class SChChannelConsumer(models.Model):

    class Meta:
        verbose_name = _("Channel consumer")
        verbose_name_plural = _("Channel consumers")
        default_permissions = ("add", "change", "delete", "view", "list", "administer")
        app_label = "schbuilder"

        ordering = ["id"]

    parent = ext_models.PtigHiddenForeignKey(
        SChApp,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        editable=True,
        verbose_name="Parent",
    )
    name = models.CharField(
        "Name", null=False, blank=False, editable=True, max_length=255
    )
    consumer_type = models.CharField(
        "Consumer type",
        null=False,
        blank=False,
        editable=True,
        choices=Consumer_CHOICES,
        max_length=64,
    )
    url = models.CharField("Url", null=True, blank=True, editable=True, max_length=255)
    consumer_code = models.TextField(
        "Consumer code",
        null=True,
        blank=True,
        editable=False,
    )
    doc = models.TextField(
        "Doc",
        null=True,
        blank=True,
        editable=False,
    )

    def init_new(self, request, view, param=None):
        if param:
            self.view_type = param
            defaults = {}
            defaults["consumer_type"] = param
            return defaults
        else:
            return None


admin.site.register(SChChannelConsumer)


tmp = [
    pos
    for pos in dir(models)
    if (pos.endswith("Field") and pos != "Field") or pos.endswith("Key")
]
for pos in tmp:
    Field_CHOICES.append((pos, pos))
