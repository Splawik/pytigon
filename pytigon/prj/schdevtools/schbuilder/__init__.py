from django.utils.translation import gettext_lazy as _

ModuleName = "main tools"
ModuleTitle = _("main tools")
Name = "schbuilder"
Title = _("Pytigon builder")
Perms = True
Index = ""
Urls = (
    (
        "table/SChProject/main_view/form/list/?view_in=desktop",
        _("Projects"),
        "schbuilder.change_schproject",
        """client://status/folder-open.png""",
    ),
    (
        "table/SChProject/not_main_view/form/list/?view_in=desktop",
        _("Archived projects"),
        "schbuilder.change_schproject",
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
