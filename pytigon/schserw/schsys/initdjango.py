"""
This module customizes Django form rendering and model field behavior.

Modifications:
- Adds a MIME type for SVG files.
- Customizes the HTML output of forms to have left-aligned headers.
- Overrides the `as_p` method of forms to use `django-bootstrap5` for rendering.
- Sets widget attributes for `CharField` based on `max_length`.
- Introduces a `FormProxy` class to render specific fields of a form as a table.
- Adds a `fields_as_table` method to `ModelForm` to return a `FormProxy` instance.

Functions:
- _html_output(self, normal_row, error_row, row_ender, help_text_html, errors_on_separate_row): Custom HTML output for forms with left-aligned headers.
- as_p(self): Render form using `django-bootstrap5`.
- widget_attrs(self, widget): Set widget attributes for `CharField` based on `max_length`.
- fields_as_table(self): Return a `FormProxy` instance for the form.

Classes:
- FormProxy: Proxy class to render specific fields of a form as a table.

Modifications to Django:
- `django.db.models.fields.prep_for_like_query`: Lambda function to escape backslashes.
- `BaseForm._html_output`: Overridden to use custom HTML output.
- `BaseForm.as_p`: Overridden to use `django-bootstrap5` for rendering.
- `django.forms.fields.CharField.widget_attrs`: Overridden to set widget attributes based on `max_length`.
- `django.forms.models.ModelForm.fields_as_table`: Added to return a `FormProxy` instance.
"""

import mimetypes
from django.forms.widgets import TextInput, PasswordInput
from django.db import models
from copy import deepcopy
from django.forms.forms import BaseForm


from django_bootstrap5.forms import render_form


django.db.models.fields.prep_for_like_query = lambda x: str(x).replace("\\", "\\\\")

BaseForm._old_html_output = BaseForm._html_output
BaseForm._old_as_p = BaseForm.as_p

models.TreeForeignKey = models.ForeignKey
models.GTreeForeignKey = models.ForeignKey


def _html_output(
    self, normal_row, error_row, row_ender, help_text_html, errors_on_separate_row
):
    """Custom HTML output for forms with left-aligned headers."""
    normal_row2 = normal_row.replace("<th>", "<th align='left'><em>").replace(
        "</th>", "</em></th>"
    )
    return self._old_html_output(
        normal_row2, error_row, row_ender, help_text_html, errors_on_separate_row
    )


BaseForm._html_output = _html_output


def as_p(self):
    """Render form using django-bootstrap5."""
    return render_form(self)


BaseForm.as_p = as_p


def widget_attrs(self, widget):
    """Set widget attributes for CharField based on max_length."""
    if self.max_length == None:
        max2 = 80
    else:
        if self.max_length > 80:
            max2 = 80
        else:
            max2 = self.max_length
    if self.max_length is not None and isinstance(widget, (TextInput, PasswordInput)):
        return {"max_length": str(self.max_length), "size": str(max2)}


django.forms.fields.CharField.widget_attrs = widget_attrs


class FormProxy:
    """Proxy class to render specific fields of a form as a table."""

    def __init__(self, form):
        self.form = form

    def __getitem__(self, fields):
        """Render specified fields as a table."""
        tmp_fields = self.form.fields
        tabfields = fields.split("__")
        new_fields = deepcopy(self.form.fields)
        for name, field in list(new_fields.items()):
            if not name in tabfields:
                del new_fields[name]
        self.form.fields = new_fields
        ret = self.form.as_table()
        self.form.fields = tmp_fields
        return ret


def fields_as_table(self):
    """Return a FormProxy instance for the form."""
    return FormProxy(self)


django.forms.models.ModelForm.fields_as_table = fields_as_table

# Add MIME type for SVG files
mimetypes.add_type("image/svg+xml", ".svg")
