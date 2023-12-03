from django.utils.translation import gettext_lazy as _

ModuleTitle = _("Config")
Title = _("Actions")
Perms = True
Index = "None"
Urls = (
    (
        "table/ActionType/-/form/list/",
        _("Action types"),
        "admin_actiontype",
        """png://categories/applications-system.png""",
    ),
    (
        "table/Action/-/form/list/",
        _("Action"),
        "admin_action",
        """png://apps/office-calendar.png""",
    ),
)
UserParam = {"icon": "fa-check"}
