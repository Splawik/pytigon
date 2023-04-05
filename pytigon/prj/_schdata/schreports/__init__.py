from django.utils.translation import gettext_lazy as _

ModuleTitle = _("Data structures")
Title = _("Reports")
Perms = True
Index = "None"
Urls = (
    (
        "table/ReportDef/-/form/list/?view_in=desktop",
        _("Report definition"),
        "schreports.admin_repdef",
        """client://actions/document-properties.png""",
    ),
    (
        "table/Report/main_reports/form/list/?view_in=desktop",
        _("Reports"),
        "schreports.admin_report",
        """client://actions/format-justify-fill.png""",
    ),
    (
        "table/Plot/-/form/list/?view_in=desktop",
        _("Plots"),
        "schreports.admin_plot",
        """fa://pencil-square.png""",
    ),
    (
        "table/CommonGroupDef/-/form/list/?view_in=desktop",
        _("Common group definitons"),
        "schreports.admin_commongroupdef",
        """png://apps/system-file-manager.png""",
    ),
    (
        "table/CommonGroup/0/form/tree/?view_in=desktop",
        _("Common groups"),
        "schreports.admin_commongroup",
        """png://apps/system-file-manager.png""",
    ),
)
UserParam = {}
