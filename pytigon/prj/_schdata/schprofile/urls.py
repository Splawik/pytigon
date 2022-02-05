from django.urls import path, re_path, include, reverse
from django.utils.translation import gettext_lazy as _
from pytigon_lib.schviews import generic_table_start, gen_tab_action, gen_row_action
from django.views.generic import TemplateView
from . import views

urlpatterns = []

gen = generic_table_start(urlpatterns, "schprofile", views)


gen.standard("Profile", _("Profile"), _("Profiles"))

gen.for_field("schelements.Element", "profile_owners", _("Profile"), _("Profiles"))
gen.for_field("schelements.Element", "profile_configs", _("Profile"), _("Profiles"))
