from django.urls import path, re_path, include, reverse
from django.utils.translation import gettext_lazy as _
from pytigon_lib.schviews import generic_table_start, gen_tab_action, gen_row_action
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    gen_row_action("WorkflowItem", "accept", views.accept),
    gen_row_action("WorkflowItem", "reject", views.reject),
]

gen = generic_table_start(urlpatterns, "schworkflow", views)


gen.standard("WorkflowType", _("Workflow type"), _("Workflow types"))
gen.standard("WorkflowItem", _("Workflow item"), _("Workflow items"))

gen.for_field(
    "WorkflowType", "workflowitem_set", _("Workflow item"), _("Workflow items")
)
