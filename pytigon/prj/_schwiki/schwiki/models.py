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


from django.template import RequestContext, Context, Template
import markdown
from pytigon_lib.schdjangoext.django_ihtml import ihtml_to_html
from pytigon_lib.schtools.wiki import wikify, wiki_from_str, make_href
from pytigon_lib.schtools.tools import norm_indent
from django.template.loader import select_template
from datetime import datetime
from collections import namedtuple
from pytigon_lib.schindent.indent_markdown import (
    IndentMarkdownProcessor,
    REG_OBJ_RENDERER,
)

PUBLISH_FUN = """#Example: 
#import datetime
#
#def publish(page, conf):
#    pass
    
"""


page_type_choices = [
    ("W", "Wiki"),
    ("I", "Indent html"),
    ("H", "Html"),
]

menu_icon_size_choices = [
    ("0", "small"),
    ("1", "medium"),
    ("2", "large"),
]


class Page(JSONModel):

    class Meta:
        verbose_name = _("Page")
        verbose_name_plural = _("Page")
        default_permissions = ("add", "change", "delete", "view", "list", "administer")
        app_label = "schwiki"

        ordering = ["id"]

    subject = models.CharField(
        "Subject", null=False, blank=False, editable=True, db_index=True, max_length=64
    )
    name = models.CharField(
        "Name", null=False, blank=False, editable=True, db_index=True, max_length=64
    )
    description = models.CharField(
        "Description", null=True, blank=True, editable=True, max_length=256
    )
    content_src = models.TextField(
        "Content source",
        null=True,
        blank=True,
        editable=False,
    )
    content = models.TextField(
        "Content",
        null=True,
        blank=True,
        editable=False,
    )
    base_template = models.CharField(
        "Base template", null=True, blank=True, editable=True, max_length=64
    )
    rights_group = models.CharField(
        "Rights group", null=True, blank=True, editable=True, max_length=64
    )
    prj_name = models.CharField(
        "Project name", null=True, blank=True, editable=True, max_length=64
    )
    menu = models.CharField(
        "Menu path", null=True, blank=True, editable=True, max_length=64
    )
    menu_position = models.IntegerField(
        "Menu position",
        null=True,
        blank=True,
        editable=True,
    )
    menu_icon = models.CharField(
        "Icon in menu", null=True, blank=True, editable=True, max_length=256
    )
    menu_icon_size = models.CharField(
        "Icon size",
        null=False,
        blank=False,
        editable=True,
        default="1",
        choices=menu_icon_size_choices,
        max_length=1,
    )
    operator = models.CharField(
        "Operator", null=True, blank=True, editable=False, max_length=64
    )
    update_time = models.DateTimeField(
        "Update time", null=False, blank=False, editable=False, auto_now=True
    )
    published = models.BooleanField(
        "Published",
        null=True,
        blank=False,
        editable=False,
        default=False,
        db_index=True,
    )
    latest = models.BooleanField(
        "Latest",
        null=True,
        blank=False,
        editable=False,
        default=True,
    )

    def save_from_request(self, request, view_type, param):
        if "direct_save" in request.POST:
            self.operator = request.user.username
            super(Page, self).save()
        else:
            conf_list = WikiConf.objects.filter(subject=self.subject)
            conf_exists = False
            if len(conf_list) > 0:
                conf = conf_list[0]
                conf_exists = True
                if conf.backup_copies > 0:
                    pages = Page.objects.filter(
                        subject=self.subject, name=self.name
                    ).update(latest=False)
                    obj_to_save = Page()
                    obj_to_save.subject = self.subject
                    obj_to_save.name = self.name
                    obj_to_save.description = self.description
                    obj_to_save.content_src = self.content_src
                    obj_to_save.content = self.content
                    obj_to_save.base_template = self.base_template
                    obj_to_save.rights_group = self.rights_group
                    obj_to_save.menu = self.menu
                    obj_to_save.operator = self.operator
                    obj_to_save.update_time = self.update_time
                    obj_to_save.jsondata = self.jsondata
                    obj_to_save.published = False
                    obj_to_save.latest = True
                    obj_to_save.update_time = timezone.now()
                    obj_to_save.save()
                    pages = Page.objects.filter(
                        subject=self.subject, name=self.name
                    ).order_by("update_time")
                    if len(pages) > conf.backup_copies:
                        to_delete_count = len(pages) - conf.backup_copies
                        to_delete = []
                        for pos in pages:
                            if not pos.published and not pos.latest:
                                to_delete.append(pos)
                                to_delete_count -= 1
                            if to_delete_count <= 0:
                                break
                        if to_delete:
                            for pos2 in to_delete:
                                pos2.delete()
                    return

            self.operator = request.user.username
            self.update_time = timezone.now()
            self.latest = True
            if not conf_exists:
                self.published = True
            self.save()

    def save(self, *args, **kwargs):
        # if not self.id:
        super(Page, self).save(*args, **kwargs)
        if self.content_src:
            # content = html_from_wiki(self, self.content_src+"\n\n\n&nbsp;")
            conf = WikiConf.objects.filter(subject=self.subject).first()
            header = ""
            footer = ""
            line_number = 0
            if conf:
                if conf.page_header:
                    header = conf.page_header + "\n"
                    line_number -= len(conf.page_header.split("\n"))
                if conf.page_footer:
                    footer = conf.page_footer + "\n"

            x = IndentMarkdownProcessor(output_format="html", line_number=line_number)
            content = x.convert(header + self.content_src + footer)
        else:
            content = ""
        self.content = content
        super(Page, self).save(*args, **kwargs)

    def template_for_object(self, view, context, doc_type):
        if doc_type == "py":
            return "schwiki/edit_wiki_content.html"
        return None

    def get_page_for_wiki(self, wiki_str, user=None):
        wiki_word = wiki_from_str(wiki_str)
        return Page.get_page(user, self.subject, wiki_word)

    def get_href(self, path=None):
        return make_href(
            self.description if self.description else self.name,
            new_win=False,
            section=self.subject,
            path=path,
        )

    @staticmethod
    def get_page(request_or_username, subject, name):
        if type(request_or_username) == str:
            username = request_or_username
        elif request_or_username.user:
            username = request_or_username.user.username
        else:
            username = None
        objs = None
        if username:
            objs = Page.objects.filter(
                subject=subject, name=name, operator=username, latest=True
            )
        if not objs or len(objs) == 0:
            objs = Page.objects.filter(subject=subject, name=name, published=True)
        if not objs or len(objs) == 0:
            objs = Page.objects.filter(subject=subject, name=name)
        if len(objs) > 0:
            return objs[0]
        else:
            return None

    def __str__(self):
        return self.name

    @staticmethod
    def get_wiki_objects():
        global REG_OBJ_RENDERER
        ret = []
        for key, obj in REG_OBJ_RENDERER.items():
            ret.append(obj.get_info())
        return ret

    def get_user_blocks(self):
        conf = WikiConf.objects.filter(subject=self.subject).first()
        if conf:
            if conf.page_header:
                tab = []
                for line in conf.page_header.split("\n"):
                    if line and line.startswith("%") and "name/" in line:
                        tab.append(line.split("/", 1)[1].split(":")[0].strip())
                return tab
        return ""


admin.site.register(Page)


class WikiConf(JSONModel):

    class Meta:
        verbose_name = _("Wiki config")
        verbose_name_plural = _("Wiki config")
        default_permissions = ("add", "change", "delete", "view", "list", "administer")
        app_label = "schwiki"

        ordering = ["id"]

    subject = models.CharField(
        "Wiki subject", null=False, blank=False, editable=True, max_length=64
    )
    group_of_rights_to_view = models.CharField(
        "A group of rights to view wiki",
        null=True,
        blank=True,
        editable=True,
        max_length=64,
    )
    group_of_rights_to_edit = models.CharField(
        "A group of rights to edit wiki",
        null=True,
        blank=True,
        editable=True,
        max_length=64,
    )
    backup_copies = models.IntegerField(
        "Number of backup copies",
        null=False,
        blank=False,
        editable=True,
    )
    publish_fun = models.TextField(
        "Function called after publishing",
        null=True,
        blank=True,
        editable=False,
    )
    scss = models.TextField(
        "Additional scss styles",
        null=True,
        blank=True,
        editable=False,
    )
    css = models.TextField(
        "Css styles",
        null=True,
        blank=True,
        editable=False,
    )
    page_header = models.TextField(
        "Page header",
        null=True,
        blank=True,
        editable=False,
    )
    page_footer = models.TextField(
        "Page footer",
        null=True,
        blank=True,
        editable=False,
    )
    git_repository = models.CharField(
        "Git repository", null=True, blank=True, editable=True, max_length=256
    )

    def get_css(self):
        import sass

        if self.scss:
            buf = self.scss.replace("page_class", "wiki_" + self.subject.lower())
            style = sass.compile(string=buf, indented=True)
            return style
        return ""

    def save(self, *args, **kwargs):
        self.css = self.get_css()
        ret = super().save(*args, **kwargs)
        return ret

    def get_publish_fun_if_empty(
        self, request, template_name, ext, extra_context, target
    ):
        return PUBLISH_FUN


admin.site.register(WikiConf)
