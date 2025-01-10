from django.utils.translation import gettext_lazy as _

ModuleTitle = _("main tools")
Title = _("Pytigon builder")
Perms = True
Index = "None"
Urls = (
    (
        "table/SChAppSet/main_view/form/list/?view_in=desktop",
        _("Projects"),
        "schbuilder.change_schappset",
        """client://status/folder-open.png""",
    ),
    (
        "table/SChAppSet/not_main_view/form/list/?view_in=desktop",
        _("Archived projects"),
        "schbuilder.change_schappset",
        """png://actions/edit-delete.png""",
    ),
    (
        "form/Installer/?view_in=browser",
        _("Make installer"),
        None,
        """client://categories/applications-internet.png""",
    ),
    (
        "form/Install/?view_in=browser",
        _("Install app"),
        None,
        """client://devices/drive-optical.png""",
    ),
)
UserParam = {}
