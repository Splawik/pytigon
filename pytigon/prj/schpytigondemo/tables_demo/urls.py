from django.urls import path, re_path, include, reverse
from django.utils.translation import gettext_lazy as _
from pytigon_lib.schviews import generic_table_start, gen_tab_action, gen_row_action
from django.views.generic import TemplateView
from . import views

urlpatterns = []

gen = generic_table_start(urlpatterns, "tables_demo", views)


gen.standard("Example1User", _("User"), _("Users"))
gen.standard("Example1Computer", _("Computer"), _("Computers"))
gen.standard("Example2Peripheral", _("Peripheral"), _("Peripherals"))
gen.standard("Example3Tag", _("Tag"), _("Tags"))
gen.standard("Example4Parameter", _("Parameter"), _("Parameters"))
gen.standard("Example5ParamGroup", _("Group of parameters"), _("Groups of parameters"))
gen.standard(
    "Example6ComputerFromExample1", _("Proxy to computer"), _("Proxy to computers")
)
gen.standard(
    "Example7ComputerFromExample1", _("Proxy to computer"), _("Proxy to computers")
)

gen.for_field(
    "Example1Computer", "example2peripheral_set", _("Peripheral"), _("Peripherals")
)

gen.for_field(
    "Example4Parameter",
    "example5paramgroup_set",
    _("Group of parameters"),
    _("Groups of parameters"),
)
gen.for_field(
    "Example4Parameter",
    "second_parameters",
    _("Group of parameters"),
    _("Groups of parameters"),
)
gen.for_field(
    "Example4Parameter",
    "group_parameters",
    _("Group of parameters"),
    _("Groups of parameters"),
)
