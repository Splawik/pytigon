from django.utils.translation import gettext_lazy as _

ModuleName = "config"
ModuleTitle = _("Config")
Name = "schlabels"
Title = _("Labels")
Perms = True
Index = ""
Urls = (
    (
        "table/LabelType/-/form/list/",
        _("Label types"),
        None,
        """png://actions/tab-new.png""",
    ),
    ("table/Label/-/form/list/", _("Labels"), None, """png://actions/tab-new.png"""),
    (
        "table/ElementLabel/-/form/list/",
        _("Element labels"),
        None,
        """png://actions/tab-new.png""",
    ),
    (
        "table/CommonGroupLabel/-/form/list/",
        _("Groups labels"),
        None,
        """png://actions/tab-new.png""",
    ),
)
UserParam = {}
