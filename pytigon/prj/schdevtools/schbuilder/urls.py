from django.urls import path, re_path, include, reverse
from django.utils.translation import gettext_lazy as _
from pytigon_lib.schviews import generic_table_start, gen_tab_action, gen_row_action
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    gen_row_action("SChAppSet", "gen", views.gen),
    gen_row_action("SChAppSet", "prj_export", views.prj_export),
    gen_tab_action("SChAppSet", "prj_import", views.prj_import),
    gen_row_action("SChAppSet", "manage", views.manage),
    gen_row_action("SChTable", "template_edit", views.template_edit),
    gen_tab_action("SChAppSet", "prj_import/edit", views.edit),
    gen_row_action(
        "SChField",
        "field_up",
        views.change_pos,
        {"app": "schbuilder", "tab": "SChField", "forward": False, "field": "parent"},
    ),
    gen_row_action(
        "SChField",
        "field_down",
        views.change_pos,
        {"app": "schbuilder", "tab": "SChField", "forward": True, "field": "parent"},
    ),
    gen_row_action(
        "SChField",
        "field_duplicate",
        views.duplicate_row,
        {"app": "schbuilder", "tab": "SChField", "field": "parent"},
    ),
    gen_row_action(
        "SChTable",
        "field_up",
        views.change_tab_pos,
        {"app": "schbuilder", "tab": "SChTable", "forward": False, "field": "parent"},
    ),
    gen_row_action(
        "SChTable",
        "field_down",
        views.change_tab_pos,
        {"app": "schbuilder", "tab": "SChTable", "forward": True, "field": "parent"},
    ),
    gen_row_action("SChForm", "template_edit2", views.template_edit2),
    gen_row_action(
        "SChAppMenu",
        "field_up",
        views.change_menu_pos,
        {"app": "schbuilder", "tab": "SChAppMenu", "forward": False, "field": "parent"},
    ),
    gen_row_action(
        "SChAppMenu",
        "field_down",
        views.change_menu_pos,
        {"app": "schbuilder", "tab": "SChAppMenu", "forward": True, "field": "parent"},
    ),
    gen_row_action("SChAppSet", "installer", views.installer),
    gen_tab_action("SChAppSet", "restart_server", views.restart_server),
    gen_row_action(
        "SChFormField",
        "field_up",
        views.change_pos_form_field,
        {
            "app": "schbuilder",
            "tab": "SChFormField",
            "forward": False,
            "field": "parent",
        },
    ),
    gen_row_action(
        "SChFormField",
        "field_down",
        views.change_pos_form_field,
        {
            "app": "schbuilder",
            "tab": "SChFormField",
            "forward": True,
            "field": "parent",
        },
    ),
    gen_row_action("SChView", "template_edit3", views.template_edit3),
    gen_tab_action("SChAppSet", "update", views.update),
    gen_row_action("SChLocale", "translate_sync", views.translate_sync),
    gen_row_action("SChAppSet", "locale_gen", views.locale_gen),
    re_path(
        r"download_installer/(?P<name>\w+)/$",
        views.download_installer,
        {},
        name="schbuilder_download_installer",
    ),
    gen_row_action(
        "SChChoiceItem",
        "field_up",
        views.change_pos,
        {
            "app": "schbuilder",
            "tab": "SChChoiceItem",
            "forward": False,
            "field": "parent",
        },
    ),
    gen_row_action(
        "SChChoiceItem",
        "field_down",
        views.change_pos,
        {
            "app": "schbuilder",
            "tab": "SChChoiceItem",
            "forward": True,
            "field": "parent",
        },
    ),
    re_path(
        r"autocomplete/(?P<id>\d+)/(?P<key>\w+)/$",
        views.autocomplete,
        {},
        name="schbuilder_autocomplete",
    ),
    gen_row_action("SChAppSet", "gen_milestone", views.gen_milestone),
    gen_tab_action("SChAppSet", "prj_import2", views.prj_import2),
    gen_row_action("SChAppSet", "run", views.run),
    gen_row_action(
        "SChApp",
        "app_up",
        views.change_pos,
        {"app": "schbuilder", "tab": "SChApp", "forward": False, "field": "parent"},
    ),
    gen_row_action(
        "SChApp",
        "app_down",
        views.change_pos,
        {"app": "schbuilder", "tab": "SChApp", "forward": True, "field": "parent"},
    ),
    gen_row_action("SChAppSet", "run2", views.run2),
    path(
        "devtools", TemplateView.as_view(template_name="schbuilder/devtools.html"), {}
    ),
    path("form/Installer/", views.view_installer, {}),
    path("form/Install/", views.view_install, {}),
    path("form/ImportFromGit/", views.view_importfromgit, {}),
]

gen = generic_table_start(urlpatterns, "schbuilder", views)
gen.for_field(
    "SChAppSet",
    "schapp_set",
    "Applications",
    prefix="up",
    template_name="schbuilder/schapp2.html",
)
gen.for_field(
    "SChApp",
    "schappmenu_set",
    "Menu",
    prefix="wiki",
    template_name="schbuilder/schappmenu2.html",
)
# gen.standard('SChAppMenu', u'SChAppMenu', prefix="wiki")


gen.standard("SChAppSet", _("Application package"), _("Application packages"))
gen.standard("SChApp", _("SChApp"), _("SChApp"))
gen.standard("SChChoice", _("SChChoice"), _("SChChoice"))
gen.standard("SChChoiceItem", _("SChChoiceItem"), _("SChChoiceItem"))
gen.standard("SChTable", _("SChTable"), _("SChTable"))
gen.standard("SChField", _("SChField"), _("SChField"))
gen.standard("SChView", _("SChView"), _("SChView"))
gen.standard("SChStatic", _("Static file"), _("Static files"))
gen.standard("SChTemplate", _("SChTemplate"), _("SChTemplate"))
gen.standard("SChAppMenu", _("SChAppMenu"), _("SChAppMenu"))
gen.standard("SChForm", _("Form"), _("Form"))
gen.standard("SChFormField", _("Form field"), _("Form field"))
gen.standard("SChTask", _("SChTask"), _("SChTask"))
gen.standard("SChFiles", _("SChFiles"), _("SChFiles"))
gen.standard("SChLocale", _("Locale"), _("Locales"))
gen.standard("SChTranslate", _("Translate"), _("Translate"))
gen.standard("SChChannelConsumer", _("Channel consumer"), _("Channel consumers"))

gen.for_field("SChAppSet", "schapp_set", _("SChApp"), _("SChApp"))
gen.for_field("SChApp", "schchoice_set", _("SChChoice"), _("SChChoice"))
gen.for_field("SChChoice", "schchoiceitem_set", _("SChChoiceItem"), _("SChChoiceItem"))
gen.for_field("SChApp", "schtable_set", _("SChTable"), _("SChTable"))
gen.for_field("SChTable", "schfield_set", _("SChField"), _("SChField"))
gen.for_field("SChApp", "schview_set", _("SChView"), _("SChView"))
gen.for_field("SChAppSet", "schstatic_set", _("Static file"), _("Static files"))
gen.for_field("SChApp", "schtemplate_set", _("SChTemplate"), _("SChTemplate"))
gen.for_field("SChApp", "schappmenu_set", _("SChAppMenu"), _("SChAppMenu"))
gen.for_field("SChApp", "schform_set", _("Form"), _("Form"))
gen.for_field("SChForm", "schformfield_set", _("Form field"), _("Form field"))
gen.for_field("SChApp", "schtask_set", _("SChTask"), _("SChTask"))
gen.for_field("SChApp", "schfiles_set", _("SChFiles"), _("SChFiles"))
gen.for_field("SChAppSet", "schlocale_set", _("Locale"), _("Locales"))
gen.for_field("SChLocale", "schtranslate_set", _("Translate"), _("Translate"))
gen.for_field(
    "SChApp", "schchannelconsumer_set", _("Channel consumer"), _("Channel consumers")
)
