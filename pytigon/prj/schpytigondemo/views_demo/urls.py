from django.urls import path, re_path, include, reverse
from django.utils.translation import gettext_lazy as _
from pytigon_lib.schviews import generic_table_start, gen_tab_action, gen_row_action
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path("odf_example", views.odf_example, {}, name="views_demo_odf_example"),
    path("pdf_example", views.pdf_example, {}, name="views_demo_pdf_example"),
    path("json", views.json_example, {}, name="views_demo_json_example"),
    path("xml_example", views.xml_example, {}, name="views_demo_xml_example"),
    path("xlsx_example", views.xlsx_example, {}, name="views_demo_xlsx_example"),
    path("txt_example", views.txt_example, {}, name="views_demo_txt_example"),
    path(
        "template_example",
        views.template_example,
        {},
        name="views_demo_template_example",
    ),
    path("hdoc_example", views.hdoc_example, {}, name="views_demo_hdoc_example"),
    path("plotly", views.plotly_example, {}, name="views_demo_plotly_example"),
    path(
        "plotly_export",
        views.plotly_export_example,
        {},
        name="views_demo_plotly_export_example",
    ),
]

gen = generic_table_start(urlpatterns, "views_demo", views)
