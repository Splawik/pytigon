from django.utils.translation import gettext_lazy as _

ModuleName = "config"
ModuleTitle = _("Config")
Name = "schadmin"
Title = _("Administration")
Perms = True
Index = ""
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
        "schadmin.can_administer|schadmin.applib.perms.if_filer",
        """png://apps/system-file-manager.png""",
    ),
    (
        "sqlexplore?view_in=desktop",
        _("SQL explorer"),
        "schadmin.can_administer",
        """png://mimetypes/x-office-spreadsheet.png""",
    ),
    (
        "oauth2",
        _("OAuth2 applications"),
        "schadmin.can_administer|schadmin.applib.perms.if_oauth2",
        """png://actions/format-indent-more.png""",
    ),
    (
        "graphql?view_in=desktop",
        _("GraphQL"),
        "schadmin.can_administer|schadmin.applib.perms.if_graphql",
        """fa://building.png""",
    ),
    (
        "rest",
        _("REST api"),
        "schadmin.can_administer|schadmin.applib.perms.if_rest",
        """png://actions/document-properties.png""",
    ),
)
UserParam = {}
