from django.utils.translation import gettext_lazy as _

ModuleTitle = _("Reports")
Title = _("Reports")
Perms = True
Index = "None"
Urls = (
    (
        "table/ReportDef/-/form/list/?schtml=desktop",
        _("Report definition"),
        "schreports.view_reportdef",
        """client://actions/document-properties.png""",
    ),
    (
        "table/Report/main_reports/form/list/?schtml=desktop",
        _("Reports"),
        "schreports.view_report",
        """client://actions/format-justify-fill.png""",
    ),
    (
        "table/Plot/-/form/list/?schtml=desktop",
        _("Plots"),
        "schreports.view_plot",
        """fa://pencil-square.png""",
    ),
    (
        "table/CommonGroupDef/-/form/list/?schtml=desktop",
        _("Common group definitons"),
        "schreports.view_commongroupdef",
        """png://apps/system-file-manager.png""",
    ),
    (
        "table/CommonGroup/0/form/tree/?schtml=desktop",
        _("Common groups"),
        "schreports.view_commongroup",
        """png://apps/system-file-manager.png""",
    ),
)
UserParam = {}
