from django.utils.translation import gettext_lazy as _

ModuleTitle = _("administration")
Title = _("Administration")
Perms = True
Index = "None"
Urls = (
    (
        "terminal?view_in=desktop",
        _("Terminal"),
        "schadmin.can_administer",
        """png://apps/utilities-terminal.png""",
    ),
    (
        "administration?view_in=desktop",
        _("Administration"),
        "schadmin.can_administer",
        """png://apps/utilities-system-monitor.png""",
    ),
    (
        "filemanager?view_in=desktop",
        _("File manager"),
        "schadmin.can_administer",
        """png://apps/system-file-manager.png""",
    ),
    (
        "sqlexplore?view_in=desktop",
        _("SQL explorer"),
        "schadmin.can_administer",
        """png://mimetypes/x-office-spreadsheet.png""",
    ),
    (
        "graphql?view_in=desktop",
        _("GraphQL"),
        "schadmin.can_administer",
        """fa://building.png""",
    ),
)
UserParam = {}
