from django.urls import path, re_path, include, reverse
from django.utils.translation import gettext_lazy as _
from pytigon_lib.schviews import generic_table_start, gen_tab_action, gen_row_action
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    re_path(
        r"new_group/(?P<group_type>\w+)/(?P<parent_id>\d+)/$",
        views.new_group,
        {},
        name="schstruct_new_group",
    ),
    re_path(
        r"table/CommonGroup/(?P<group_id>\d+)/edit__group/$",
        views.edit__group,
        {},
        name="schstruct_edit__group",
    ),
    path(
        "list_group_by_tag/<slug:group_tag>/<slug:template>/",
        views.list_group_by_tag,
        {},
        name="schstruct_list_group_by_tag",
    ),
]

gen = generic_table_start(urlpatterns, "schstruct", views)


gen.standard(
    "CommonGroupDef", _("Common group definition"), _("Common groups definition")
)
gen.standard("CommonGroup", _("Common group"), _("Common groups"))
