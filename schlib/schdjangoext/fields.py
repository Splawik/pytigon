#!/usr/bin/python
# -*- coding: utf-8 -*-
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation; either version 3, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.

#Pytigon - wxpython and django application framework

#author: "Slawomir Cholaj (slawomir.cholaj@gmail.com)"
#copyright: "Copyright (C) ????/2012 Slawomir Cholaj"
#license: "LGPL 3.0"
#version: "0.1a"


from itertools import chain
import collections

from django.db import models
from django import forms
from django.utils.safestring import mark_safe
from django.conf import settings
from django.utils.html import conditional_escape
from django_select2.forms import ModelSelect2Widget
from django.forms.widgets import HiddenInput, CheckboxInput, CheckboxSelectMultiple, RadioChoiceInput, RadioSelect
from django.db.models.fields import TextField


BUTTONS="""
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

    def render(self, name, value, attrs=None):
        x = super().render(name, value, attrs)
        if len(self.choices.queryset)>0:
            txt = str(self.choices.queryset[0])
        else:
            txt=""
        buttons2 = BUTTONS % (self.href1, self.href2)
        return mark_safe("<div class='select2 input-group' item_id='%s' item_str='%s'>%s%s</div>" %
            (value, txt, x, buttons2))


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
            href1 = "/%s/%s/table/%s/-/form/get?schtml=1" % (settings.URL_ROOT_FOLDER, self.to._meta.app_label,
                self.to._meta.object_name)
            href2 = "/%s/%s/table/%s/-/add?schtml=1" % (settings.URL_ROOT_FOLDER, self.to._meta.app_label,
                self.to._meta.object_name)
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


class ManyToManyFieldAlternateRel(models.ManyToManyField):

    def __init__(self,to,queryset_field,**kwargs):
        models.ManyToManyField.__init__(self, to, **kwargs)
        self.queryset_field = queryset_field

    def formfield(self, **kwargs):
        defaults = {'form_class': forms.ModelMultipleChoiceField,
            'queryset': self.queryset_field.rel.to._default_manager.complex_filter(self.rel.limit_choices_to)}
        defaults.update(kwargs)
        if defaults.get('initial') is not None:
            defaults['initial'] = [i._get_pk_val() for i in defaults['initial']]
        return super(models.ManyToManyField, self).formfield(**defaults)


class CheckboxSelectMultipleWithIcon(CheckboxSelectMultiple):

    def render(self,name,value,attrs=None,choices=()):
        if value is None:
            value = []
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name)
        output = ['<ul>']
        str_values = set([v for v in value])
        for (i, (option_value, option_label)) in enumerate(chain(self.choices,
                choices)):
            if has_id:
                final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], i))
                label_for = ' for="%s"' % final_attrs['id']
            else:
                label_for = ''
            cb = CheckboxInput(final_attrs, check_test=lambda value: value in str_values)
            rendered_cb = cb.render(name, option_value)
            option_label = conditional_escape(option_label)
            x = option_label.split('|')
            if len(x) > 1:
                icon = x[0]
                option_label = x[1]
            else:
                icon = None
            if icon:
                image = "<img src='%s' />" % icon
            else:
                image = ''
            output.append('<li><label%s>%s %s %s</label></li>' % (label_for,
                          rendered_cb, image, option_label))
        output.append('</ul>')
        return mark_safe('\n'.join(output))


class ModelMultipleChoiceFieldWidthIcon(forms.ModelMultipleChoiceField):

    widget = CheckboxSelectMultipleWithIcon


class ManyToManyFieldWidthIcon(models.ManyToManyField):

    def formfield(self, **kwargs):
        db = kwargs.pop('using', None)
        defaults = {'form_class': ModelMultipleChoiceFieldWidthIcon,
                    'queryset': self.rel.to._default_manager.using(db).complex_filter(self.rel.limit_choices_to)}
        defaults.update(kwargs)
        if defaults.get('initial') is not None:
            initial = defaults['initial']
            if isinstance(initial, collections.Callable):
                initial = initial()
            defaults['initial'] = [i._get_pk_val() for i in initial]
        return super(models.ManyToManyField, self).formfield(**defaults)


class RadioInput2(RadioChoiceInput):

    def __str__(self):
        if 'id' in self.attrs:
            label_for = ' for="%s_%s"' % (self.attrs['id'], self.index)
        else:
            label_for = ''
        choice_label = conditional_escape(self.choice_label)
        x = choice_label.split('|')
        if len(x) > 1:
            label = "<img src='%s' /> &nbsp; " % x[0] + x[1]
        else:
            label = x[0]
        self.attrs['class'] = 'radioselectwithicon'
        return mark_safe("<div><label>%s %s</label></div>" % (self.tag(), label))


class RadioFieldRendererWithIcon(object):
    """An object used by RadioSelect to enable customization of radio widgets."""

    def __init__(self,name,value,attrs,choices):
        (self.name, self.value, self.attrs) = (name, value, attrs)
        self.choices = choices

    def __iter__(self):
        for (i, choice) in enumerate(self.choices):
            yield RadioInput2(self.name, self.value, self.attrs.copy(), choice, i)

    def __getitem__(self, idx):
        choice = self.choices[idx]
        return RadioInput2(self.name, self.value, self.attrs.copy(), choice, idx)

    def __str__(self):
        return self.render()

    def render(self):
        """Outputs a <ul> for this set of radio fields."""
        return mark_safe('<ul class=\'radio\' width="100%%">%s</ul>' % ' '.join(['<li li-symbol="">%s</li>' %
            w for w in self]))


class RadioSelectWithIcon(RadioSelect):
    renderer = RadioFieldRendererWithIcon


class ModelChoiceFieldWidthIcon(forms.ModelChoiceField):
    widget = RadioSelectWithIcon


class ForeignKeyWidthIcon(models.ForeignKey):
    def formfield(self, **kwargs):
        db = kwargs.pop('using', None)
        defaults = {'form_class': ModelChoiceFieldWidthIcon,
                    'queryset': self.rel.to._default_manager.using(db).complex_filter(self.rel.limit_choices_to),
                    'to_field_name': self.rel.field_name}
        defaults.update(kwargs)
        return super(models.ForeignKey, self).formfield(**defaults)


class RadioInputTree(RadioChoiceInput):

    def __str__(self):
        if 'id' in self.attrs:
            label_for = ' for="%s_%s"' % (self.attrs['id'], self.index)
        else:
            label_for = ''
        choice_label = conditional_escape(self.choice_label)
        x = choice_label.split('|')
        if len(x) > 1:
            label = "<img src='%s' /><br/>" % x[0] + x[1]
        else:
            label = x[0]
        return mark_safe('<label%s>%s</label>%s' % (label_for, label, self.tag()))


class RadioFieldRendererExt(object):
    """An object used by RadioSelect to enable customization of radio widgets."""

    def __init__(self,name,value,attrs,choices):
        (self.name, self.value, self.attrs) = (name, value, attrs)
        self.choices = choices

    def __iter__(self):
        for (i, choice) in enumerate(self.choices):
            yield RadioInputTree(self.name, self.value, self.attrs.copy(), choice, i)

    def __getitem__(self, idx):
        choice = self.choices[idx]
        return RadioInputTree(self.name, self.value, self.attrs.copy(), choice, idx)

    def __str__(self):
        return self.render()

    def render(self):
        """Outputs a <ul> for this set of radio fields."""
        return mark_safe("""<ul class='radio'>%s</ul>""" % '\n'.join(['<li>%s</li>' % w for w in self]))


class PyRadioFieldRendererExt(object):

    def __init__(self,name,value,attrs,choices):
        (self.name, self.value, self.attrs) = (name, value, attrs)
        self.choices = choices

    def __str__(self):
        return self.render()

    def render(self):
        s1 = "<CTRLDBCHOICE_EXT href='%s' name='%s' READONLY='1' VALUETYPE='str' value='%s:%s!!'></CTRLDBCHOICE_EXT>"
        s2 = "<CTRLDBCHOICE_EXT href='%s' name='%s' READONLY='1' ></CTRLDBCHOICE_EXT>"
        href = ''
        if hasattr(self.model_to, 'gen_url'):
            href = self.model_to.gen_url(self.value)
            if self.value:
                objs = self.model_to.objects.filter(id=int(self.value))
                if len(objs) > 0:
                    return mark_safe(s1 % (href, self.name, self.value, str(objs[0])))
        return mark_safe(s2 % (href, self.name))


class RadioSelectExt(RadioSelect):

    renderer = RadioFieldRendererExt

    def __init__(self, *args, **kwargs):
        self.py_client = False
        self.ext_data = None
        RadioSelect.__init__(self, *args, **kwargs)

    def set_py_client(self, py_client):
        self.py_client = py_client

    def set_ext_data(self, ext_data):
        self.ext_data = ext_data

    def get_renderer(self, name, value, attrs=None, choices=()):
        if self.py_client:
            rend = PyRadioFieldRendererExt(name, value, attrs, choices)
        else:
            rend = RadioSelect.get_renderer(self, name, value, attrs, choices)
        rend.py_client = self.py_client
        rend.model_to = self.ext_data
        return rend


class ModelChoiceFieldExt(forms.ModelChoiceField):

    widget = RadioSelectExt

    def __init__(self, queryset, empty_label="---------", required=True, widget=None, label=None, initial=None,
                 help_text='', to_field_name=None, limit_choices_to=None, *args, **kwargs):
        self.model_to = queryset.model
        forms.ModelChoiceField.__init__(self, queryset, empty_label, required, widget, label, initial,
            help_text, to_field_name, limit_choices_to, *args, **kwargs)
        self.widget.set_ext_data(self.model_to)


class ForeignKeyExt(models.ForeignKey):

    def formfield(self, **kwargs):
        db = kwargs.pop('using', None)
        defaults = {
            'form_class': ModelChoiceFieldExt,
            'queryset': self.rel.to._default_manager.using(db).complex_filter(self.rel.limit_choices_to),
            'to_field_name': self.rel.field_name,
            }
        defaults.update(kwargs)
        return super(models.ForeignKey, self).formfield(**defaults)


class AutoCharField(forms.CharField):

    def __init__(self, max_length=None, min_length=None, *args, **kwargs):
        if 'src' in kwargs:
            self.src = kwargs['src']
            del kwargs['src']
        else:
            self.src = None
        super(AutoCharField, self).__init__(max_length, min_length,
                *args, **kwargs)

    def widget_attrs(self, widget):
        if self.src:
            return {'src': self.src}


class AutocompleteTextField(TextField):

    def __init__(self, *args, **kwargs):
        if 'src' in kwargs:
            self.src = kwargs['src']
            del kwargs['src']
        else:
            self.src = None
        super(AutocompleteTextField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        if self.src:
            defaults = {'widget': forms.Textarea, 'form_class': AutoCharField, 'src': self.src}
        else:
            defaults = {'widget': forms.Textarea}
        defaults.update(kwargs)
        return super(AutocompleteTextField, self).formfield(**defaults)

