from django.utils.translation import gettext_lazy as _

ModuleTitle = _("Workflow")
Title = _("Workflow")
Perms = True
Index = "None"
Urls = (
    (
        "table/WorkflowType/-/form/list/",
        _("Workflow types"),
        None,
        """png://categories/applications-system.png""",
    ),
    (
        "table/WorkflowItem/-/form/list/",
        _("Workflow items"),
        None,
        """png://apps/system-users.png""",
    ),
)
UserParam = {}
