from django.urls import path, re_path, include, reverse
from django.utils.translation import gettext_lazy as _
from pytigon_lib.schviews import generic_table_start, gen_tab_action, gen_row_action
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path(
        "example_template/",
        TemplateView.as_view(template_name="templates_demo/example_template.html"),
        {},
    ),
]

gen = generic_table_start(urlpatterns, "templates_demo", views)