from django.db import models
from django_select2.forms import ModelSelect2Widget
from django import forms
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

class _ModelSelect2WidgetExt(ModelSelect2Widget):
    def __init__(self, href1=None, href2=None, *argi, **argv):
        ModelSelect2Widget.__init__(self, *argi, **argv)
        self.href1 = href1
        self.href2 = href2

    #def render(self, name, value, attrs=None, choices=()):
    #    x = super().render(name, value, attrs, choices)
    #    if len(self.choices.queryset)>0:
    #        txt = str(self.choices.queryset[0])
    #    else:
    #        txt=""
    #    buttons2 = buttons % (self.href1, self.href2)
    #    return mark_safe("<div class='select2 input-group' item_id='%s' item_str='%s'>%s%s</div>" % (value, txt, x, buttons2))

    def render(self, name, value, attrs=None):
        x = super().render(name, value, attrs)
        if len(self.choices.queryset)>0:
            txt = str(self.choices.queryset[0])
        else:
            txt=""
        buttons2 = buttons % (self.href1, self.href2)
        return mark_safe("<div class='select2 input-group' item_id='%s' item_str='%s'>%s%s</div>" % (value, txt, x, buttons2))



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
            _search_fields = self.search_fields
            class _Field(forms.ModelChoiceField):
                def __init__(self, queryset, *argi, **argv):
                    widget=_ModelSelect2WidgetExt(href1, href2, queryset = queryset,search_fields=_search_fields)
                    widget.attrs['style'] = 'width:400px;'
                    argv['widget'] = widget
                    forms.ModelChoiceField.__init__(self, queryset, *argi, **argv)
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
