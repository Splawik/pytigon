from django.urls import path, re_path, include, reverse
from django.utils.translation import gettext_lazy as _
from pytigon_lib.schviews import generic_table_start, gen_tab_action, gen_row_action
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path("terminal", TemplateView.as_view(template_name="schadmin/terminal.html"), {}),
    path(
        "administration",
        TemplateView.as_view(template_name="schadmin/administration.html"),
        {},
    ),
    path(
        "filemanager",
        TemplateView.as_view(template_name="schadmin/filemanager.html"),
        {},
    ),
    path(
        "sqlexplore", TemplateView.as_view(template_name="schadmin/sqlexplore.html"), {}
    ),
    path("graphql", TemplateView.as_view(template_name="schadmin/graphql.html"), {}),
    path("rest", TemplateView.as_view(template_name="schadmin/rest.html"), {}),
    path("oauth2", TemplateView.as_view(template_name="schadmin/oauth2.html"), {}),
]

gen = generic_table_start(urlpatterns, "schadmin", views)
from django.contrib import admin
from django.conf import settings
from pytigon_lib.schtools.platform_info import platform_name

urlpatterns.append(path("explorer/", include("explorer.urls")))

if platform_name() != "Android" and "filer" in settings.INSTALLED_APPS:
    urlpatterns.append(path("filer/", include("filer.urls")))
