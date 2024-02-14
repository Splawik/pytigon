from django.urls import path, re_path, include, reverse
from django.utils.translation import gettext_lazy as _
from pytigon_lib.schviews import generic_table_start, gen_tab_action, gen_row_action
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    re_path(
        r"table/DocHead/(?P<filter>[\w=_,;-]*)/(?P<target>[\w_-]*)/[_]?(?P<vtype>)docheadlist/",
        views.view_doc_heads,
        {},
        name="schelements_view_doc_heads",
    ),
    re_path(
        r"table/DocItem/(?P<parent_id>\d+)/docitemlist/",
        views.view_doc_items,
        {},
        name="schelements_view_doc_items",
    ),
    re_path(
        r"table/DocHead/(?P<id>\d+)/edit_head/",
        views.edit_head,
        {},
        name="schelements_edit_head",
    ),
    re_path(
        r"table/DocItem/(?P<id>\d+)/edit_item/",
        views.edit_item,
        {},
        name="schelements_edit_item",
    ),
    gen_row_action("DocHead", "approve", views.approve),
    gen_row_action("DocHead", "discard", views.discard),
    path(
        "view_elements/<slug:code>/<slug:filter>/<slug:template>/",
        views.view_elements,
        {},
        name="schelements_view_elements",
    ),
    path(
        "view_elements_as_tree/<slug:code>/<slug:filter>/<slug:template>/",
        views.view_elements_as_tree,
        {},
        name="schelements_view_elements_as_tree",
    ),
    path(
        "view_elements_of_type/<slug:type>/<slug:template>/",
        views.view_elements_of_type,
        {},
        name="schelements_view_elements_of_type",
    ),
    gen_tab_action(
        "AccountState", "refresh_account_states", views.refresh_account_states
    ),
]

gen = generic_table_start(urlpatterns, "schelements", views)
gen.for_field(
    "DocType",
    "dochead_set",
    "Documents",
    prefix="doc",
    template_name="schelements/dochead2.html",
)


gen.standard("Element", _("Element"), _("Elements"))
gen.standard("DocReg", _("Document register"), _("Document registers"))
gen.standard("DocType", _("Type of document"), _("Types of documents"))
gen.standard("DocHead", _("Document header"), _("Document headers"))
gen.standard("DocItem", _("Document item"), _("Document items"))
gen.standard("DocRegStatus", _("Document status"), _("Document status"))
gen.standard("DocHeadStatus", _("Document head status"), _("Documents head status"))
gen.standard("Account", _("Account"), _("Account"))
gen.standard("AccountState", _("State of account"), _("States of account"))
gen.standard("AccountOperation", _("Account operation"), _("Account operations"))


gen.for_field("DocReg", "doctype_set", _("Type of document"), _("Types of documents"))
gen.for_field("DocType", "dochead_set", _("Document header"), _("Document headers"))
gen.for_field("Element", "dochead_set", _("Document header"), _("Document headers"))
gen.for_field("DocHead", "docitem_set", _("Document item"), _("Document items"))

gen.for_field("Element", "owners", _("Document item"), _("Document items"))
gen.for_field("Element", "docitem_set", _("Document item"), _("Document items"))
gen.for_field("DocReg", "docregstatus_set", _("Document status"), _("Document status"))
gen.for_field(
    "DocHead",
    "docheadstatus_set",
    _("Document head status"),
    _("Documents head status"),
)

gen.for_field("Element", "baseaccount_rc1_set", _("Account"), _("Account"))
gen.for_field("Element", "baseaccount_rc2_set", _("Account"), _("Account"))
gen.for_field("Element", "baseaccount_rc3_set", _("Account"), _("Account"))
gen.for_field(
    "DocItem", "accountoperation_set", _("Account operation"), _("Account operations")
)
gen.for_field(
    "AccountState", "accountoper_set", _("Account operation"), _("Account operations")
)
