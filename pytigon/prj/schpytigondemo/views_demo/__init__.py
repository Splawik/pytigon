from django.utils.translation import gettext_lazy as _

ModuleTitle = _("views")
Title = _("Views")
Perms = False
Index = "None"
Urls = (
    (
        "template_example?view_in=desktop",
        _("template example"),
        None,
        """png://mimetypes/x-office-presentation-template.png""",
    ),
    (
        "odf_example?view_in=desktop",
        _("odf example"),
        None,
        """png://mimetypes/x-office-spreadsheet-template.png""",
    ),
    (
        "pdf_example?view_in=desktop",
        _("pdf example"),
        None,
        """png://actions/format-justify-fill.png""",
    ),
    (
        "json?view_in=desktop",
        _("json example"),
        None,
        """png://actions/format-justify-right.png""",
    ),
    (
        "xml_example?view_in=desktop",
        _("xml example"),
        None,
        """png://actions/contact-new.png""",
    ),
    (
        "xlsx_example?view_in=desktop",
        _("xlsx example"),
        None,
        """png://mimetypes/x-office-spreadsheet-template.png""",
    ),
    (
        "txt_example?view_in=desktop",
        _("txt example"),
        None,
        """png://actions/format-justify-fill.png""",
    ),
    (
        "test_llvm?view_in=desktop",
        _("llvm_test"),
        None,
        """png://mimetypes/video-x-generic.png""",
    ),
    (
        "hdoc_example",
        _("hdoc example"),
        None,
        """png://actions/format-justify-center.png""",
    ),
)
UserParam = {}
