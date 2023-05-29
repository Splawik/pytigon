from django.urls import path, re_path, include, reverse
from django.utils.translation import gettext_lazy as _
from pytigon_lib.schviews import generic_table_start, gen_tab_action, gen_row_action
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path(
        "project_view/<str:prj_name>/",
        views.project_view,
        {},
        name="schbi_project_view",
    ),
    path("page_view/<int:page_id>/", views.page_view, {}, name="schbi_page_view"),
    path("chart_view/<int:chart_id>/", views.chart_view, {}, name="schbi_chart_view"),
]

gen = generic_table_start(urlpatterns, "schbi", views)


gen.standard("Project", _("Project"), _("Projects"))
gen.standard("Page", _("Page"), _("Pages"))
gen.standard("Chart", _("Chart"), _("Charts"))

gen.for_field("Project", "page_set", _("Page"), _("Pages"))
gen.for_field("Page", "chart_set", _("Chart"), _("Charts"))
