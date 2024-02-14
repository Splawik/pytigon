from django.urls import path, re_path, include, reverse
from django.utils.translation import gettext_lazy as _
from pytigon_lib.schviews import generic_table_start, gen_tab_action, gen_row_action
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    re_path(
        r"grid/(?P<folder>.*)/(?P<value>[\w=]*)/$",
        views.grid,
        {},
        name="schcommander_grid",
    ),
    re_path(r"open/(?P<file_name>.*)/$", views.open, {}, name="schcommander_open"),
    re_path(r"save/(?P<file_name>.*)/$", views.save, {}, name="schcommander_save"),
    re_path(
        r"open_page/(?P<file_name>.*)/(?P<page>\d+)/$",
        views.open_page,
        {},
        name="schcommander_open_page",
    ),
    re_path(r"view/(?P<file_name>.*)/$", views.view, {}, name="schcommander_view"),
    re_path(
        r"convert_html/(?P<file_name>.*)/$",
        views.convert_html,
        {},
        name="schcommander_convert_html",
    ),
    re_path(
        r"convert_pdf/(?P<file_name>.*)/$",
        views.convert_pdf,
        {},
        name="schcommander_convert_pdf",
    ),
    re_path(
        r"convert_docx/(?P<file_name>.*)/$",
        views.convert_docx,
        {},
        name="schcommander_convert_docx",
    ),
    re_path(
        r"convert_xlsx/(?P<file_name>.*)/$",
        views.convert_xlsx,
        {},
        name="schcommander_convert_xlsx",
    ),
    re_path(
        r"convert_spdf/(?P<file_name>.*)/$",
        views.convert_spdf,
        {},
        name="schcommander_convert_spdf",
    ),
    path("form/FileManager/", views.view_filemanager, {}),
    path("form/Move/", views.view_move, {}),
    path("form/Copy/", views.view_copy, {}),
    path("form/MkDir/", views.view_mkdir, {}),
    path("form/Rename/", views.view_rename, {}),
    path("form/NewFile/", views.view_newfile, {}),
    path("form/Delete/", views.view_delete, {}),
    path("form/Setup/", views.view_setup, {}),
]

gen = generic_table_start(urlpatterns, "schcommander", views)
