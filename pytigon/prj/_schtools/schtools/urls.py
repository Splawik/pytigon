from django.urls import path, re_path, include, reverse
from django.utils.translation import gettext_lazy as _
from pytigon_lib.schviews import generic_table_start, gen_tab_action, gen_row_action
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    re_path(
        r"search/(?P<type>.+)/",
        views.autocomplete_search,
        {},
        name="schtools_autocomplete_search",
    ),
    path("set_user_param/", views.set_user_param, {}, name="schtools_set_user_param"),
    path("get_user_param/", views.get_user_param, {}, name="schtools_get_user_param"),
    re_path(
        r"(?P<app>[\w=_,;-]*)/(?P<table>[\w=_,;-]*)/import_table/$",
        views.import_table,
        {},
        name="schtools_import_table",
    ),
    path("form/ImportTableForm/", views.view_importtableform, {}),
]

gen = generic_table_start(urlpatterns, "schtools", views)


gen.standard("Parameter", _("Parameter"), _("Parameter"))
