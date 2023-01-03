from django.utils.translation import gettext_lazy as _

ModuleTitle = _("tables")
Title = _("Tables")
Perms = False
Index = "None"
Urls = (
    (
        "table/Example1User/-/form/list/?view_in=desktop",
        _("Example 1 - users"),
        None,
        """png://apps/system-users.png""",
    ),
    (
        "table/Example1Computer/-/form/list/?view_in=desktop",
        _("Example 1 - computers"),
        None,
        """png://devices/computer.png""",
    ),
    (
        "table/Example4Parameter/-/form/list/?view_in=desktop",
        _("Example 4 - parameters"),
        None,
        """png://actions/document-properties.png""",
    ),
    (
        "table/Example5ParamGroup/0/form/tree/?view_in=desktop",
        _("Example 5 - groups of parameters"),
        None,
        """png://apps/preferences-system-windows.png""",
    ),
    (
        "table/Example6ComputerFromExample1/-/form__datatable/list/?view_in=desktop",
        _("Example 6 - datatable"),
        None,
        """png://actions/format-justify-fill.png""",
    ),
    (
        "table/Example6ComputerFromExample1/-/form__simple/list/?view_in=desktop",
        _("Example 6 - simple"),
        None,
        """png://actions/format-justify-fill.png""",
    ),
    (
        "table/Example6ComputerFromExample1/-/form/list/?view_in=desktop",
        _("Example 6 - scrolled"),
        None,
        """png://actions/format-justify-fill.png""",
    ),
    (
        "table/Example7ComputerFromExample1/-/form/list/?view_in=desktop",
        _("Example 7 - table mass operations"),
        None,
        """png://actions/format-justify-fill.png""",
    ),
)
UserParam = {}
