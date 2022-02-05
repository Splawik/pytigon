from django.urls import path, re_path, include, reverse
from django.utils.translation import gettext_lazy as _
from pytigon_lib.schviews import generic_table_start, gen_tab_action, gen_row_action
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    re_path(
        "new_rep/(?P<rep_type>\w+)/(?P<doc_type_name>\w+)/$",
        views.new_rep,
        {},
        name="schreports_new_rep",
    ),
    re_path(
        "table/Report/(?P<rep_id>\d+)/edit__rep/$",
        views.edit__rep,
        {},
        name="schreports_edit__rep",
    ),
    re_path(
        "new_subrep/(?P<parent_rep_id>\d+)/(?P<rep_type>\w+)/$",
        views.new_subrep,
        {},
        name="schreports_new_subrep",
    ),
    re_path(
        "edit_subrep/(?P<parent_rep_id>\d+)/(?P<rep_type>\w+)/(?P<view_type>\w+)/$",
        views.edit_subrep,
        {},
        name="schreports_edit_subrep",
    ),
    gen_row_action("Report", "move_up", views.move_up),
    gen_row_action("Report", "move_down", views.move_down),
    re_path(
        "table/Report/(?P<dochead_id>\d+)/edit__rep2/$",
        views.edit__rep2,
        {},
        name="schreports_edit__rep2",
    ),
    re_path(
        "table/Report/(?P<dochead_id>\d+)/repaction/(?P<rep_action>\w+)/$",
        views.repaction,
        {},
        name="schreports_repaction",
    ),
    re_path(
        "table/Report/(?P<rep_id>\d+)/(?P<to_pos>\d+)/action/move_to/$",
        views.move_to,
        {},
        name="schreports_move_to",
    ),
    re_path(
        "plot_service/(?P<name>\w+)/$",
        views.plot_service,
        {},
        name="schreports_plot_service",
    ),
    re_path(
        "new_group/(?P<group_type>\w+)/(?P<parent_id>\d+)/$",
        views.new_group,
        {},
        name="schreports_new_group",
    ),
    re_path(
        "table/CommonGroup/(?P<group_id>\d+)/edit__group/$",
        views.edit__group,
        {},
        name="schreports_edit__group",
    ),
    re_path(
        "list_group_by_tag/(?P<group_tag>\w+)/$",
        views.list_group_by_tag,
        {},
        name="schreports_list_group_by_tag",
    ),
]

gen = generic_table_start(urlpatterns, "schreports", views)


gen.standard("ReportDef", _("Report definition"), _("Reports definitions"))
gen.standard("Report", _("Report"), _("Reports"))
gen.standard(
    "CommonGroupDef", _("Common group definition"), _("Common groups definition")
)
gen.standard("CommonGroup", _("Common group"), _("Common groups"))
gen.standard("Plot", _("Plot"), _("Polts"))


gen.for_field("schelements.DocHead", "report_set", _("Report"), _("Reports"))
