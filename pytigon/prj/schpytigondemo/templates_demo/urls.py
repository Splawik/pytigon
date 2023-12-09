from django.urls import path, re_path, include, reverse
from django.utils.translation import gettext_lazy as _
from pytigon_lib.schviews import generic_table_start, gen_tab_action, gen_row_action
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path("excel/", views.excel_report, {}, name="templates_demo_excel_report"),
    path("odf/", views.odf_report, {}, name="templates_demo_odf_report"),
    path(
        "example_template/",
        TemplateView.as_view(template_name="templates_demo/example_template.html"),
        {},
    ),
    path(
        "min_template/",
        TemplateView.as_view(template_name="templates_demo/min_template.html"),
        {},
    ),
    path(
        "min_template2/",
        TemplateView.as_view(template_name="templates_demo/min_template2.html"),
        {},
    ),
    path("min/", TemplateView.as_view(template_name="templates_demo/min.html"), {}),
]

gen = generic_table_start(urlpatterns, "templates_demo", views)
