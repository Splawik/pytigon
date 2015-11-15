from django.db import models
from django.db.models.fields.related import ManyToOneRel
from django_select2 import AutoModelSelect2Field
from django_select2.widgets import AutoHeavySelect2Widget
from django.forms.widgets import HiddenInput
from django.utils.safestring import mark_safe
from django.conf import settings

buttons="""
<div class="input-group-btn">
    <button type="button" name ="get_tbl_value" class="btn btn-default btn-flat foreignkey_button get_tbl_value" href='%s'>
      <span class="fa-table fa"></span>
    </button>s
    <button type="button" name="new_tbl_value" class="btn btn-default btn-flat foreignkey_button new_tbl_value" href='%s'>
      <span class="fa-plus fa"></span>
    </button>
</div>
"""

def make_select_widget(href1, href2):
    class _AutoHeavySelect2WidgetExt(AutoHeavySelect2Widget):
        def render(self, name, value, attrs=None, choices=()):
            x = super().render(name, value, attrs, choices)
            if len(self.choices.queryset)>0:
                txt = str(self.choices.queryset[0])
            else:
                txt=""
            buttons2 = buttons % (href1, href2)
            return mark_safe("<div class='select2 input-group' item_id='%s' item_str='%s'>%s%s</div>" % (value, txt, x, buttons2))
    return _AutoHeavySelect2WidgetExt


class ForeignKey(models.ForeignKey):

    def __init__(self, *args, **kwargs):
        if 'search_fields' in kwargs:
            self.search_fields = kwargs['search_fields']
            del kwargs['search_fields']
        else:
            self.search_fields = None
        super().__init__(*args, **kwargs)
        if len(args)>0:
            self.to = args[0]

    def formfield(self, **kwargs):
        if settings.URL_ROOT_FOLDER:
            href1 = "/%s/%s/table/%s/-/form/get?schtml=1" % (settings.URL_ROOT_FOLDER, self.to._meta.app_label, self.to._meta.object_name)
            href2 = "/%s/%s/table/%s/-/add?schtml=1" % (settings.URL_ROOT_FOLDER, self.to._meta.app_label, self.to._meta.object_name)
        else:
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
