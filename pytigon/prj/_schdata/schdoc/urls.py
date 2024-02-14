from django.urls import path, re_path, include, reverse
from django.utils.translation import gettext_lazy as _
from pytigon_lib.schviews import generic_table_start, gen_tab_action, gen_row_action
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    re_path(
        r"new_doc/(?P<doc_type>\w+)/(?P<doc_type_name>\w+)/$",
        views.new_doc,
        {},
        name="schdoc_new_doc",
    ),
    re_path(
        r"table/Doc/(?P<doc_id>\d+)/edit__doc/$",
        views.edit__doc,
        {},
        name="schdoc_edit__doc",
    ),
    re_path(
        r"new_subdoc/(?P<parent_doc_id>\d+)/(?P<doc_type>\w+)/$",
        views.new_subdoc,
        {},
        name="schdoc_new_subdoc",
    ),
    re_path(
        r"edit_subdoc/(?P<parent_doc_id>\d+)/(?P<doc_type>\w+)/(?P<view_type>\w+)/$",
        views.edit_subdoc,
        {},
        name="schdoc_edit_subdoc",
    ),
    gen_row_action("Doc", "move_up", views.move_up),
    gen_row_action("Doc", "move_down", views.move_down),
    re_path(
        r"table/Doc/(?P<dochead_id>\d+)/edit__doc2/$",
        views.edit__doc2,
        {},
        name="schdoc_edit__doc2",
    ),
    re_path(
        r"table/Doc/(?P<dochead_id>\d+)/repaction/(?P<doc_action>\w+)/$",
        views.repaction,
        {},
        name="schdoc_repaction",
    ),
    re_path(
        r"table/Doc/(?P<doc_id>\d+)/(?P<to_pos>\d+)/action/move_to/$",
        views.move_to,
        {},
        name="schdoc_move_to",
    ),
]

gen = generic_table_start(urlpatterns, "schdoc", views)


gen.standard("DocDef", _("Document definition"), _("Documents definitions"))
gen.standard("Doc", _("Document"), _("Documents"))


gen.for_field("schelements.DocHead", "doc_set", _("Document"), _("Documents"))
