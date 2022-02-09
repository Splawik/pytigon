from django.urls import path, re_path, include, reverse
from django.utils.translation import gettext_lazy as _
from pytigon_lib.schviews import generic_table_start, gen_tab_action, gen_row_action
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path(
        "action_ctrl",
        TemplateView.as_view(template_name="schadvcontrols_demo/action_ctrl.html"),
        {},
    ),
    path(
        "plots",
        TemplateView.as_view(template_name="schadvcontrols_demo/plots.html"),
        {},
    ),
]

gen = generic_table_start(urlpatterns, "schadvcontrols_demo", views)
