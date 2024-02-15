from django.utils.translation import gettext_lazy as _

ModuleName = "frontend views"
ModuleTitle = _("Frontend views")
Name = "frontend_demo"
Title = _("Frontend Views")
Perms = False
Index = ""
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
