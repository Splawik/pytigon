from django.urls import path, re_path, include, reverse
from django.utils.translation import gettext_lazy as _
from pytigon_lib.schviews import generic_table_start, gen_tab_action, gen_row_action
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path(
        "standardcontrols",
        TemplateView.as_view(
            template_name="schsimplecontrols_demo/standard_controls.html"
        ),
        {"title": "Standard controls"},
    ),
    path(
        "htmlcontrols",
        TemplateView.as_view(template_name="schsimplecontrols_demo/html_controls.html"),
        {},
    ),
    path(
        "extendedcontrols",
        TemplateView.as_view(
            template_name="schsimplecontrols_demo/extended_controls.html"
        ),
        {},
    ),
    path("form/TestForm/", views.view_testform, {}),
]

gen = generic_table_start(urlpatterns, "schsimplecontrols_demo", views)
