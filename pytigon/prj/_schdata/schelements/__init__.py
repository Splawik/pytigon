from django.utils.translation import gettext_lazy as _

ModuleTitle = _("main tools")
Title = _("Elements")
Perms = True
Index = "None"
Urls = (
    (
        "table/Element/0/form/tree/?schtml=desktop",
        _("Elements"),
        "schelements.view_elements",
        """bi-stack""",
    ),
    (
        "table/DocReg/-/form/list/?schtml=desktop",
        _("Documents register"),
        "schelements.view_docreg",
        """client://actions/folder-new.png""",
    ),
    (
        "table/DocType/-/form/list/?schtml=desktop",
        _("Types of documents"),
        "schelements.view_doctype",
        """""",
    ),
    (
        "table/DocRegStatus/-/form/list/?schtml=desktop",
        _("Definition of document status"),
        "schelements.view_docregstatus",
        """""",
    ),
    (
        "table/Account/0/form/tree/?schtml=desktop",
        _("Accounts"),
        "schelements.view_account",
        """client://apps/system-file-manager.png""",
    ),
    (
        "table/AccountState/-/form/list/?schtml=desktop",
        _("States of accounts"),
        "schelements.view_accountstate",
        """client://mimetypes/package-x-generic.png""",
    ),
    (
        "table/AccountOperation/-/form/list/?schtml=desktop",
        _("Account operations"),
        "schelements.view_accountoperation",
        """client://actions/edit-find-replace.png""",
    ),
    (
        "table/DocHead/-/form/list/?schtml=desktop",
        _("Documents"),
        "schelements.view_dochead",
        """client://actions/format-justify-fill.png""",
    ),
)
UserParam = {}
