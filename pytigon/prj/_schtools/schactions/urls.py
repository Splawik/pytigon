from django.urls import path, re_path, include, reverse
from django.utils.translation import gettext_lazy as _
from pytigon_lib.schviews import generic_table_start, gen_tab_action, gen_row_action
from django.views.generic import TemplateView
from . import views

urlpatterns = []

gen = generic_table_start(urlpatterns, "schactions", views)


gen.standard("ActionType", _("Action type"), _("Action types"))
gen.standard("Action", _("Action"), _("Actions"))

gen.for_field("ActionType", "action_set", _("Action"), _("Actions"))
