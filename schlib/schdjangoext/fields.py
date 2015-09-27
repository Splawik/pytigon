from django.db import models
from django.db.models.fields.related import ManyToOneRel
from django_select2 import AutoModelSelect2Field
from django_select2.widgets import AutoHeavySelect2Widget
from django.forms.widgets import HiddenInput
from django.utils.safestring import mark_safe

buttons="""
<div class="input-group-btn">
    <button type="button" name ="get_tbl_value" class="btn btn-default btn-flat foreignkey_button get_tbl_value" href='%s'>
      <span class="glyphicon glyphicon-th-large"></span>
    </button>s
    <button type="button" name="new_tbl_value" class="btn btn-default btn-flat foreignkey_button new_tbl_value" href='%s'>
      <span class="glyphicon glyphicon-plus"></span>
    </button>
</div>
"""

def make_select_widget(href1, href2):
    class _AutoHeavySelect2WidgetExt(AutoHeavySelect2Widget):
        def render(self, name, value, attrs=None, choices=()):
            print("U1:", name, value, attrs, choices)
            x = super().render(name, value, attrs, choices)
            buttons2 = buttons % (href1, href2)
            return mark_safe("<div class='input-group'>%s%s</div>" % (x, buttons2))
    return _AutoHeavySelect2WidgetExt


class ForeignKey(models.ForeignKey):

    def __init__(self, *args, **kwargs):
        if 'search_fields' in kwargs:
            self.search_fields = kwargs['search_fields']
            del kwargs['search_fields']
        else:
            self.search_fields = None
        super().__init__(*args, **kwargs)
        self.to = args[0]

    def formfield(self, **kwargs):
        href1 = "/%s/table/%s/-/form/get?schtml=1" % (self.to._meta.app_label, self.to._meta.object_name)
        href2 = "/%s/table/%s/-/add?schtml=1" % (self.to._meta.app_label, self.to._meta.object_name)

        if self.search_fields:
            class _Field(AutoModelSelect2Field):
                widget = make_select_widget(href1, href2)
                queryset = self.related_model.objects
                search_fields = self.search_fields

            defaults = {
                'form_class': _Field,
            }
        else:
            defaults = {}
        defaults.update(**kwargs)
        return super().formfield(**defaults)


class HiddenForeignKey(models.ForeignKey):

    def formfield(self, **kwargs):
        field = models.ForeignKey.formfield(self, **kwargs)
        field.widget = HiddenInput()
        field.widget.choices = None
        return field
