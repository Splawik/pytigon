from django.utils.translation import gettext_lazy as _

ModuleTitle = _("main tools")
Title = _("Pytigon builder")
Perms = True
Index = "None"
Urls = (
    (
        "table/SChAppSet/main_view/form/list/?schtml=desktop",
        _("Projects"),
        "schbuilder.change_schappset",
        """client://status/folder-open.png""",
    ),
    (
        "table/SChAppSet/not_main_view/form/list/?schtml=desktop",
        _("Archived projects"),
        "schbuilder.change_schappset",
        """png://actions/edit-delete.png""",
    ),
    (
        "form/Installer/?schtml=browser",
        _("Make installer"),
        None,
        """client://categories/applications-internet.png""",
    ),
    (
        "form/Install/?schtml=browser",
        _("Install app"),
        None,
        """client://devices/drive-optical.png""",
    ),
)
UserParam = {}
