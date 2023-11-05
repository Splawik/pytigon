from django.utils.translation import gettext_lazy as _

ModuleTitle = _("Config")
Title = _("Workflow")
Perms = True
Index = "None"
Urls = (
    (
        "table/WorkflowType/-/form/list/",
        _("Workflow types"),
        "schworkflow.admin_workflowtype",
        """png://categories/applications-system.png""",
    ),
    (
        "table/WorkflowItem/-/form/list/",
        _("Workflow items"),
        "schworkflow.admin_workflowitem",
        """png://apps/system-users.png""",
    ),
)
UserParam = {}
