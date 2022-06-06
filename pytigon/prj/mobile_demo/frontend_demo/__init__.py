from django.utils.translation import gettext_lazy as _

ModuleTitle = _("Frontend views")
Title = _("Frontend Views")
Perms = False
Index = "None"
Urls = (
    (
        "../static/frontend_demo/views/todo_demo.fview",
        _("ToDo demo"),
        None,
        """png://devices/drive-removable-media.png""",
    ),
    (
        "dynamic_fragment/",
        _("Dynamic fragment"),
        None,
        """png://actions/view-fullscreen.png""",
    ),
)
UserParam = {}
