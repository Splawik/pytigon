from django.utils.translation import gettext_lazy as _

ModuleName = "config"
ModuleTitle = _("Config")
Name = "schelements"
Title = _("Elements")
Perms = True
Index = ""
Urls = (
    (
        "table/Element/0/form/tree/?view_in=desktop",
        _("Elements"),
        "schelements.admin_element",
        """bi-stack""",
    ),
    (
        "table/DocReg/-/form/list/?view_in=desktop",
        _("Documents register"),
        "schelements.admin_docreg",
        """client://actions/folder-new.png""",
    ),
    (
        "table/DocType/-/form/list/?view_in=desktop",
        _("Types of documents"),
        "schelements.admin_doctype",
        """""",
    ),
    (
        "table/DocRegStatus/-/form/list/?view_in=desktop",
        _("Definition of document status"),
        "schelements.admin_docregstatus",
        """""",
    ),
    (
        "table/Account/0/form/tree/?view_in=desktop",
        _("Accounts"),
        "schelements.admin_account",
        """client://apps/system-file-manager.png""",
    ),
    (
        "table/AccountState/-/form/list/?view_in=desktop",
        _("States of accounts"),
        "schelements.admin_accountstate",
        """client://mimetypes/package-x-generic.png""",
    ),
    (
        "table/AccountOperation/-/form/list/?view_in=desktop",
        _("Account operations"),
        "schelements.admin_accountoperation",
        """client://actions/edit-find-replace.png""",
    ),
    (
        "table/DocHead/-/form/list/?view_in=desktop",
        _("Documents"),
        "schelements.admin_accountoperation",
        """client://actions/format-justify-fill.png""",
    ),
)
UserParam = {}
