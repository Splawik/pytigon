from django.utils.translation import gettext_lazy as _

ModuleTitle = _("Config")
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
)
UserParam = {}
