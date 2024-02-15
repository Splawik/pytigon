from django.utils.translation import gettext_lazy as _

ModuleName = "tables"
ModuleTitle = _("tables")
Name = "tables_demo"
Title = _("Tables")
Perms = False
Index = ""
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
        "table/Example6ComputerFromExample1/-/form__scrolled/list/?view_in=desktop",
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
    (
        "../schworkflow/table/WorkflowItem//tables_demo__Example1User__0__-current_user_and_active/form__tables_demo__myacceptations/sublist/?version=tables_demo__myacceptations",
        _("My acceptations"),
        None,
        """png://actions/document-save-as.png""",
    ),
)
UserParam = {}
