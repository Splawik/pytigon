from django.urls import path, re_path, include, reverse
from django.utils.translation import gettext_lazy as _
from pytigon_lib.schviews import generic_table_start, gen_tab_action, gen_row_action
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path("search/", views.search, name="schbrowser_search"),
    path("form/MultiDownload/", views.view_multidownload, {}),
]

gen = generic_table_start(urlpatterns, "schbrowser", views)


gen.standard("bookmarks", _("Bookmarks"), _("Bookmarks"))
gen.standard("history", _("History"), _("History"))
