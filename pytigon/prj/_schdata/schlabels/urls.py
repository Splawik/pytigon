from django.urls import path, re_path, include, reverse
from django.utils.translation import gettext_lazy as _
from pytigon_lib.schviews import generic_table_start, gen_tab_action, gen_row_action
from django.views.generic import TemplateView
from . import views

urlpatterns = []

gen = generic_table_start(urlpatterns, "schlabels", views)


gen.standard("LabelType", _("Label type"), _("Label types"))
gen.standard("ElementLabel", _("Element label"), _("Element labels"))
gen.standard("CommonGroupLabel", _("Common group label"), _("Common groups labels"))
gen.standard("Label", _("Label"), _("Labels"))

gen.for_field(
    "schelements.Element", "elementlabel_set", _("Element label"), _("Element labels")
)
gen.for_field("LabelType", "elementlabel_set", _("Element label"), _("Element labels"))
gen.for_field(
    "schstruct.CommonGroup",
    "commongrouplabel_set",
    _("Common group label"),
    _("Common groups labels"),
)
gen.for_field(
    "LabelType",
    "commongrouplabel_set",
    _("Common group label"),
    _("Common groups labels"),
)
gen.for_field("LabelType", "label_set", _("Label"), _("Labels"))
