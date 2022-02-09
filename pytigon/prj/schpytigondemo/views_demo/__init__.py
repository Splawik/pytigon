from django.utils.translation import gettext_lazy as _

ModuleTitle = _("views")
Title = _("Views")
Perms = False
Index = "None"
Urls = (
    (
        "template_example?schtml=desktop",
        _("template example"),
        None,
        """png://mimetypes/x-office-presentation-template.png""",
    ),
    (
        "odf_example?schtml=desktop",
        _("odf example"),
        None,
        """png://mimetypes/x-office-spreadsheet-template.png""",
    ),
    (
        "pdf_example?schtml=desktop",
        _("pdf example"),
        None,
        """png://actions/format-justify-fill.png""",
    ),
    (
        "json?schtml=desktop",
        _("json example"),
        None,
        """png://actions/format-justify-right.png""",
    ),
    (
        "xml_example?schtml=desktop",
        _("xml example"),
        None,
        """png://actions/contact-new.png""",
    ),
    (
        "xlsx_example?schtml=desktop",
        _("xlsx example"),
        None,
        """png://mimetypes/x-office-spreadsheet-template.png""",
    ),
    (
        "txt_example?schtml=desktop",
        _("txt example"),
        None,
        """png://actions/format-justify-fill.png""",
    ),
    (
        "test_llvm?schtml=desktop",
        _("llvm_test"),
        None,
        """png://mimetypes/video-x-generic.png""",
    ),
)
UserParam = {}
