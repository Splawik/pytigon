from django.utils.translation import gettext_lazy as _

ModuleTitle = _("Actions")
Title = _("Actions")
Perms = True
Index = "None"
Urls = (
    (
        "table/ActionType/-/form/list/",
        _("Action types"),
        None,
        """png://categories/applications-system.png""",
    ),
    (
        "table/Action/-/form/list/",
        _("Action"),
        None,
        """png://apps/office-calendar.png""",
    ),
)
UserParam = {"icon": "fa-check"}
