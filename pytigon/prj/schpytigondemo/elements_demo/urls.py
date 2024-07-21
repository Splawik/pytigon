from django.urls import path, re_path, include, reverse
from django.utils.translation import gettext_lazy as _
from pytigon_lib.schviews import generic_table_start, gen_tab_action, gen_row_action
from django.views.generic import TemplateView
from . import views

urlpatterns = []

gen = generic_table_start(urlpatterns, "elements_demo", views)


gen.standard("DemoDocHead", _("Demo document head"), _("Demo document heads"))
gen.standard("DemoDocItem", _("Demo document item"), _("Demo document items"))
