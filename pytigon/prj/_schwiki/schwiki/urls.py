from django.urls import path, re_path, include, reverse
from django.utils.translation import gettext_lazy as _
from pytigon_lib.schviews import generic_table_start, gen_tab_action, gen_row_action
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    re_path(
        r"^(?P<app_or_subject>[^/]*)/(?P<page_path>[^/]*)/view/$",
        views.view_page,
        name="schwiki_view_page",
    ),
    re_path(
        r"^(?P<app_or_subject>\w*)/(?P<page_name>\w*)/edit/$",
        views.edit_page,
        name="schwiki_edit_page",
    ),
    gen_row_action("WikiConf", "publish", views.publish),
    re_path(r"(?P<q>.*)/search/$", views.search, {}, name="schwiki_search"),
    path(
        "edit_page_object/", views.edit_page_object, {}, name="schwiki_edit_page_object"
    ),
    path(
        "edit_page_object_form/<slug:object_name>/",
        views.edit_page_object_form,
        {},
        name="schwiki_edit_page_object_form",
    ),
    path(
        "edit_object_on_page/<int:page_id>/<int:line_number>/",
        views.edit_object_on_page,
        {},
        name="schwiki_edit_object_on_page",
    ),
    path(
        "edit_object_on_page_form/<int:page_id>/<int:line_number>/<slug:object_name>/",
        views.edit_object_on_page_form,
        {},
        name="schwiki_edit_object_on_page_form",
    ),
]

gen = generic_table_start(urlpatterns, "schwiki", views)


gen.standard("Page", _("Page"), _("Page"))
gen.standard("WikiConf", _("Wiki config"), _("Wiki config"))
