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

from __future__ import unicode_literals

import collections

from django.conf.urls import patterns
from django.core.urlresolvers import get_script_prefix
from django.shortcuts import render_to_response
from django.db import models
from django.apps import apps
from django.template.response import TemplateResponse
from django.utils import six
from django.views import generic
from django.template import loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings
#from django.apps.apps import get_model
#from django.apps import apps
from django.conf.urls import url

from django.db.models import CharField
from django.db.models import  Q

from .viewtools import transform_template_name, LocalizationTemplateResponse, ExtTemplateResponse
from .form_fun import form_with_perms
from .perms import make_perms_test_fun

from django.utils.translation import ugettext_lazy as _
import uuid

# url:  /table/TableName/filter/target/list url width field:
# /table/TableName/parent_pk/field/filter/target/list

def make_path(view_name, args=None):
    if settings.URL_ROOT_FOLDER:
        return settings.URL_ROOT_FOLDER+"/"+reverse(view_name, args=args)
    else:
        return reverse(view_name, args=args)

def gen_tab_action(
    table,
    action,
    fun,
    extra_context=None,
    ):
    return url(r'table/%s/action/%s$' % (table, action), fun, extra_context)


def gen_tab_field_action(
    table,
    field,
    action,
    fun,
    extra_context=None,
    ):
    return url(r'table/%s/(?P<parent_pk>\d+)/%s/action/%s$' % (table, field, action), fun, extra_context)


def gen_row_action(
    table,
    action,
    fun,
    extra_context=None,
    ):
    return url('table/%s/(?P<pk>\d+)/action/%s$' % (table, action), fun, extra_context)


def transform_extra_context(context1, context2):
    if context2:
        for (key, value) in context2.items():
            if isinstance(value, collections.Callable):
                context1[key] = value()
            else:
                context1[key] = value
    return context1

def view_editor(
    request,
    pk,
    app,
    tab,
    model,
    template_name,
    field_edit_name,
    post_save_redirect,
    ext='py',
    extra_context=None,
    target=None,
    parent_pk=0,
    field_name=None,
    ):
    if request.POST:
        data = request.POST['data']
        buf = data.replace('\r\n', '\n')
        obj = model.objects.get(id=pk)
        setattr(obj, field_edit_name, buf)
        obj.save()
        return HttpResponse('OK')
    else:
        obj = model.objects.get(id=pk)
        table_name = model._meta.object_name
        txt = getattr(obj, field_edit_name)
        f = None
        for field in obj._meta.fields:
            if field.name == field_edit_name:
                f = field
                break
        if field_name:
            save_path = '/' + app + '/table/' + tab + '/' + str(parent_pk) + '/'\
                 + table_name + '/' + str(pk) + '/' + field_edit_name\
                 + '/py/editor/'
        else:
            save_path = '/' + app + '/table/' + table_name + '/' + str(pk) + '/'\
                 + field_edit_name + '/py/editor/'
        c = RequestContext(request, {
            'app': app,
            'tab': table_name,
            'pk': pk,
            'object': obj,
            'field_name': field_edit_name,
            'ext': ext,
            'save_path': save_path,
            'txt': txt,
            'verbose_field_name': f.verbose_name,
            })

        return render_to_response(transform_template_name(obj, request, 'schsys/db_field_edt.html'), context_instance=c)



class GenericTable(object):

    def __init__(self, urlpatterns, app, views_module=None):
        self.urlpatterns = urlpatterns
        self.app = app
        self.base_url = get_script_prefix()
        self.views_module = views_module

    def new_rows(
        self,
        tab,
        field=None,
        title='',
        title_plural='',
        template_name=None,
        extra_context=None,
        queryset=None,
        prefix=None,
        ):
        rows = GenericRows(self, prefix, title, title_plural)
        rows.tab = tab
        if field:
            rows.set_field(field)
        #rows.title = title
        rows.extra_context = extra_context
        rows.base_path = 'table/' + tab + '/'
        if template_name:
            rows.template_name = template_name
        else:
            if field:
                if '.' in tab:
                    pos = tab.rfind('.')
                    m = apps.get_model(tab[:pos], tab[pos+1:])
                else:
                    m = apps.get_model(self.app, tab)
                try:
                    f = getattr(m, field).related
                except:
                    f = getattr(m, field).rel
                #f = getattr(apps.get_model(self.app, tab), field).related
                #f = getattr(apps.get_model(self.app + "." + tab), field).rel
                try:
                    table_name = f.name
                except:
                    table_name = f.var_name
            else:
                table_name = tab.lower()
            if ':' in table_name:
                rows.template_name = self.app.lower() + '/' + table_name.split(':')[-1] + '.html'
            else:
                rows.template_name = self.app.lower() + '/' + table_name + '.html'
        #rows.base_model = models.get_model(self.app, tab)
        if '.' in tab:
            rows.base_model = apps.get_model(tab)
        else:
            rows.base_model = apps.get_model(self.app + "." + tab)
        rows.queryset = queryset
        if '.' in tab:
            pos = tab.rfind('.')
            rows.base_perm = tab[:pos]+ '.%s_' + tab[pos+1:].lower()
        else:
            rows.base_perm = self.app + '.%s_' + tab.lower()
        return rows

    def append_from_schema(self, rows, schema):
        for char in schema.split(';'):
            if hasattr(rows, char):
                rows = getattr(rows, char)()

    def from_schema(
        self,
        schema,
        tab,
        field=None,
        title='',
        title_plural='',
        template_name=None,
        extra_context=None,
        queryset=None,
        prefix=None,
        ):
        if not title_plural:
            title_plural = title
        rows = self.new_rows(
            tab,
            field,
            title,
            title_plural,
            template_name,
            extra_context,
            queryset,
            prefix,
            )
        self.append_from_schema(rows, schema)
        return rows

    def standard(
        self,
        tab,
        title='',
        title_plural='',
        template_name=None,
        extra_context=None,
        queryset=None,
        prefix=None,
        ):
        schema = 'list;detail;edit;add;delete;editor'
        return self.from_schema(
            schema,
            tab,
            None,
            title,
            title_plural,
            template_name,
            extra_context,
            queryset,
            prefix,
            ).gen()

    def for_field(
        self,
        tab,
        field,
        title='',
        title_plural='',
        template_name=None,
        extra_context=None,
        queryset=None,
        prefix=None,
        ):
        rows = self.new_rows(
            tab,
            field,
            title,
            title_plural,
            template_name,
            extra_context,
            queryset,
            prefix,
            )
        schema = 'list;detail;edit;add;delete;editor'
        self.append_from_schema(rows, schema)
        return rows.gen()

    def tree(
        self,
        tab,
        title='',
        title_plural='',
        template_name=None,
        extra_context=None,
        queryset=None,
        prefix=None,
        ):
        #schema = 'list;detail;edit;add;delete;editor;tree'
        schema = 'add'
        rows = self.from_schema(
            schema,
            tab,
            None,
            title,
            title_plural,
            template_name,
            extra_context,
            queryset,
            prefix,
            )
        rows.set_field('this')
        return rows.add().gen()


class GenericRows(object):

    def __init__(
        self,
        table,
        prefix,
        title="",
        title_plural="",
        parent_rows=None,
        ):
        self.table = table
        self.prefix = prefix
        self.field = None
        self.title = title
        self.title_plural = title_plural
        if parent_rows:
            self.base_path = parent_rows.base_path
            self.base_model = parent_rows.base_model
            self.base_perm = parent_rows.base_perm
            self.update_view = parent_rows.update_view
            self.field = parent_rows.field
            self.tab = parent_rows.tab
            self.title = parent_rows.title
            self.title_plural = parent_rows.title_plural
            self.template_name = parent_rows.template_name
            self.extra_context = parent_rows.extra_context
            self.queryset = parent_rows.queryset

    def _get_base_path(self):
        if self.field:
            if self.prefix:
                return self.base_path[:-1] + '_' + self.prefix + '/'\
                     + '(?P<parent_pk>-?\d+)/%s/' % self.field
            else:
                return self.base_path + '(?P<parent_pk>-?\d+)/%s/' % self.field
        else:
            if self.prefix:
                return self.base_path[:-1] + '_' + self.prefix + '/'
            else:
                return self.base_path

    def set_field(self, field=None):
        self.field = field
        return self

    def _append(
        self,
        url_str,
        fun,
        parm=None,
        ):
        if parm:
            self.table.urlpatterns += [ url(self._get_base_path() + url_str, fun, parm), ]
        else:
            self.table.urlpatterns += [ url(self._get_base_path() + url_str, fun), ]
        return self

    def gen(self):
        return self

    def list(self):
        url = r'(?P<filter>[\w=_,;-]*)/(?P<target>[\w_-]*)/[_]?(?P<vtype>list|sublist|get|tree)$'

        class ListView(generic.ListView):

            model = self.base_model
            queryset = self.queryset
            paginate_by = 64
            allow_empty = True
            template_name = self.template_name
            response_class = ExtTemplateResponse
            base_class = self
            form = None
            form_valid = False

            title = self.title_plural

            extra_context = self.extra_context
            if self.field:
                rel_field = self.field
            else:
                rel_field = None

            sort = None
            order = None
            search = None

            def doc_type(self):
                if self.kwargs['target']=='pdf':
                    return "pdf"
                elif self.kwargs['target']=='odf':
                    return "odf"
                elif self.kwargs['target']=='json':
                    return "json"
                else:
                    return "html"

            def get_paginate_by(self, queryset):
                if self.doc_type() in ('pdf', 'odf'):
                    return None
                else:
                    return self.paginate_by

            def get(
                self,
                request,
                *args,
                **kwargs
                ):
                if 'tree' in self.kwargs['vtype']:
                    parent = int(kwargs['filter'])
                    if parent < 0:
                        parent_old = parent
                        try:
                            parent = self.model.objects.get(id=-1
                                     * parent).parent.id
                        except:
                            parent = 0
                        path2 = request.get_full_path().replace(str(parent_old), str(parent))
                        return HttpResponseRedirect(path2)

                offset = request.GET.get('offset')

                self.sort=request.GET.get('sort')
                self.order = request.GET.get('order')
                self.search = request.GET.get('search')

                if offset:
                    self.kwargs['page'] = int(int(offset)/64)+1

                #if self.search:
                #    self.kwargs['filter'] = self.search

                views_module = self.base_class.table.views_module
                form_name = '_FilterForm' + self.model._meta.object_name
                if hasattr(views_module, form_name):
                    if request.method == 'POST':
                        self.form = getattr(views_module, form_name)(request.POST)
                        if self.form.is_valid():
                            self.form_valid = True
                        else:
                            self.form_valid = False
                    else:
                        self.form = getattr(views_module, form_name)()
                return super(ListView, self).get(request, *args, **kwargs)

            def post(
                self,
                request,
                *args,
                **kwargs
                ):
                return self.get(request, *args, **kwargs)


            def get_context_data(self, **kwargs):
                context = super(ListView, self).get_context_data(**kwargs)
                context['title'] = self.title
                context['rel_field'] = self.rel_field
                context['filter'] = self.kwargs['filter']
                if self.form:
                    context['form'] = self.form

                context['doc_type'] = self.doc_type()
                context['uuid'] = uuid.uuid4()

                if 'tree' in self.kwargs['vtype']:
                    parent = int(self.kwargs['filter'])
                    context['parent_pk'] = parent
                    if parent > 0:
                        context['parent_obj'] = self.model.objects.get(id=parent)
                    else:
                        context['parent_obj'] = None

                return transform_extra_context(context, self.extra_context)

            def get_queryset(self):
                ret = None


                if 'tree' in self.kwargs['vtype']:
                    if self.queryset:
                        ret = self.queryset
                    else:
                        ret = self.model.objects.all()
                    parent = int(self.kwargs['filter'])
                    if parent >= 0:
                        if parent == 0:
                            parent = None
                        ret =  ret.filter(parent=parent)
                else:
                    if self.queryset:
                        ret = self.queryset
                    else:
                        if self.rel_field:
                            ppk = int(self.kwargs['parent_pk'])
                            parent = self.model.objects.get(id=ppk)
                            f = getattr(parent, self.rel_field)
                            ret = f.all()
                        else:
                            filter =  self.kwargs['filter']
                            if filter and filter != '-':
                                if hasattr(self.model, 'filter'):
                                    ret = self.model.filter(filter)
                                else:
                                    ret = self.model.objects.all()
                            else:
                                ret = self.model.objects.all()


                if self.search:
                    fields = [f for f in self.model._meta.fields if isinstance(f, CharField)]
                    queries = [Q(**{f.name+"__icontains": self.search}) for f in fields]
                    qs = Q()
                    for query in queries:
                        qs = qs | query
                    ret = ret.filter(qs)

                if hasattr(self.model, 'sort'):
                    ret = self.model.sort(ret, self.sort, self.order)
                else:
                    if self.sort=='cid':
                        if self.order=='asc':
                            ret = ret.order_by('id')
                        else:
                            ret = ret.order_by('-id')

                if self.form_valid == True:
                    return self.form.process(None, ret)
                else:
                    return ret


        fun = make_perms_test_fun(self.base_perm % 'list', ListView.as_view())
        self._append(url, fun)

        return self

    def detail(self):
        url = r'(?P<pk>\d+)/(?P<target>[\w_]*)/view/$'

        class DetailView(generic.DetailView):

            queryset = self.queryset

            if self.field:
                #print(dir(getattr(self.base_model, self.field)))
                try:
                    f = getattr(self.base_model, self.field).related
                except:
                    f = getattr(self.base_model, self.field).rel
                model = f.related_model
            else:
                model = self.base_model

            #model = self.base_model
            template_name = self.template_name
            title = self.title
            response_class = ExtTemplateResponse

            def doc_type(self):
                if self.kwargs['target']=='pdf':
                    return "pdf"
                elif self.kwargs['target']=='odf':
                    return "odf"
                else:
                    return "html"

            def get_context_data(self, **kwargs):
                context = super(DetailView, self).get_context_data(**kwargs)
                context['title'] = self.title + ' - '+str(_('element information'))
                return context


        fun = make_perms_test_fun(self.base_perm % 'list', DetailView.as_view())
        return self._append(url, fun)

    def edit(self):
        url = r'(?P<pk>\d+)/edit/$'


        class UpdateView(generic.UpdateView):

            response_class = LocalizationTemplateResponse

            if self.field:
                try:
                    f = getattr(self.base_model, self.field).related
                except:
                    f = getattr(self.base_model, self.field).rel
                model = f.related_model
            else:
                model = self.base_model
            #success_url = make_path('schserw.urls.ok', )
            success_url = make_path('ok')

            template_name = self.template_name
            title = self.title
            fields = "__all__"

            def get_context_data(self, **kwargs):
                context = super(UpdateView, self).get_context_data(**kwargs)
                context['title'] = self.title + ' - ' + str(_('update element'))
                return context

            def get(
                self,
                request,
                *args,
                **kwargs
                ):
                self.object = self.get_object()
                form_class = self.get_form_class()
                form = self.get_form(form_class)

                if self.object and hasattr(self.object, 'transform_form'):
                    self.object.transform_form(request, form, False)

                if form:
                    for field in form.fields:
                        if hasattr(form.fields[field].widget, 'py_client'):
                            if request.META['HTTP_USER_AGENT'].startswith('Py'):
                                form.fields[field].widget.set_py_client(True)
                return self.render_to_response(self.get_context_data(form=form))


            def post(self, request, *args, **kwargs):
                self.object = self.get_object()
                form_class = self.get_form_class()
                form = self.get_form(form_class)

                if self.object and hasattr(self.object, 'transform_form'):
                    self.object.transform_form(request, form, False)

                if form.is_valid():
                    return self.form_valid(form, request)
                else:
                    print("INVALID:", form.errors)
                    return self.form_invalid(form)

            def form_valid(self, form, request=None):
                """
                If the form is valid, save the associated model.
                """
                self.object = form.save(commit=False)
                if hasattr(self.object, 'post'):
                    self.object.post(request)
                self.object.save()
                form.save_m2m()
                return super(generic.edit.ModelFormMixin, self).form_valid(form)


        fun = make_perms_test_fun(self.base_perm % 'change',
                                  UpdateView.as_view())
        return self._append(url, fun)

    def add(self):
        url = r'(?P<add_param>[\w=_-]*)/add$'


        class CreateView(generic.CreateView):

            response_class = LocalizationTemplateResponse

            if self.field and self.field != 'this':
                try:
                    f = getattr(self.base_model, self.field).related
                except:
                    f = getattr(self.base_model, self.field).rel
                model = f.related_model
                pmodel = self.base_model
            else:
                model = self.base_model
                pmodel = model
            #success_url = make_path('schserw.urls.ok')
            template_name = self.template_name
            title = self.title
            field = self.field
            init_form = None
            fields = "__all__"

            def get_success_url(self):
                if self.object:
                    success_url = make_path('ret_ok', (int(self.object.id), str(self.object)))
                else:
                    #success_url = make_path('schserw.urls.ok')
                    success_url = make_path('ok')
                return success_url

            def get(
                self,
                request,
                *args,
                **kwargs
                ):
                self.object = self.model()
                if self.field:
                    ppk = int(kwargs['parent_pk'])
                    if ppk > 0:
                        self.object.parent = self.pmodel.objects.get(id=ppk)
                if hasattr(self.model, 'init_new'):
                    if kwargs['add_param'] and kwargs['add_param'] != '-':
                        self.init_form = self.object.init_new(kwargs['add_param'])
                    else:
                        self.init_form = self.object.init_new()

                    for pos in self.init_form:
                        if hasattr(self.object, pos):
                            setattr(self.object, pos, self.init_form[pos])
                else:
                    self.init_form = None
                form_class = self.get_form_class()
                form = self.get_form(form_class)

                if self.object and hasattr(self.object, 'transform_form'):
                    self.object.transform_form(request, form, True)

                if form:
                    for field in form.fields:
                        if hasattr(form.fields[field].widget, 'py_client'):
                            if request.META['HTTP_USER_AGENT'].startswith('Py'):
                                form.fields[field].widget.set_py_client(True)
                return self.render_to_response(self.get_context_data(form=form))


            def get_initial(self):
                d = super(CreateView, self).get_initial()
                if self.field:
                    if int(self.kwargs['parent_pk']) > 0:
                        d['parent'] = self.kwargs['parent_pk']
                    else:
                        d['parent'] = None
                if self.init_form:
                    transform_extra_context(d, self.init_form)
                return d

            def get_form_kwargs(self):
                ret = super(CreateView, self).get_form_kwargs()
                return ret

            def post(self, request, *args, **kwargs):
                self.object = None
                form_class = self.get_form_class()
                form = self.get_form(form_class)

                if self.object and hasattr(self.object, 'transform_form'):
                    self.object.transform_form(request, form, True)

                if form.is_valid():
                    return self.form_valid(form, request)
                else:
                    print("INVALID:", form.errors)
                    return self.form_invalid(form)

            def form_valid(self, form, request=None):
                """
                If the form is valid, save the associated model.
                """
                self.object = form.save(commit=False)

                if hasattr(self.object, 'init_new'):
                    if self.kwargs['add_param'] and self.kwargs['add_param'] != '-':
                        self.init_form = self.object.init_new(self.kwargs['add_param'])
                    else:
                        self.init_form = self.object.init_new()

                if 'parent_pk' in self.kwargs and hasattr(self.object, 'parent_id'):
                    self.object.parent_id = int(self.kwargs['parent_pk'])

                if request and request.POST:
                    p = request.POST
                else:
                    p = {}
                if self.init_form:
                    for pos in self.init_form:
                        if hasattr(self.object, pos) and not pos in p:
                            setattr(self.object, pos, self.init_form[pos])

                if hasattr(self.object, 'post'):
                    self.object.post(request)
                self.object.save()
                form.save_m2m()
                return super(generic.edit.ModelFormMixin, self).form_valid(form)

            def get_context_data(self, **kwargs):
                context = super(CreateView, self).get_context_data(**kwargs)
                context['title'] = self.title + ' - '+ str(_('new element'))
                context['object'] = self.object
                return context


        fun = make_perms_test_fun(self.base_perm % 'change',
                                  CreateView.as_view())
        return self._append(url, fun)

    def delete(self):
        url = r'(?P<pk>\d+)/delete/$'


        class DeleteView(generic.DeleteView):

            response_class = LocalizationTemplateResponse

            if self.field:
                try:
                    f = getattr(self.base_model, self.field).related
                except:
                    f = getattr(self.base_model, self.field).rel
                model = f.related_model
            else:
                model = self.base_model
            #success_url = make_path('schserw.urls.ok')
            success_url = make_path('ok')
            template_name = self.template_name
            title = self.title

            def get_context_data(self, **kwargs):
                context = super(DeleteView, self).get_context_data(**kwargs)
                context['title'] = self.title + ' - ' + str(_('delete element'))
                return context


        fun = make_perms_test_fun(self.base_perm % 'delete',
                                  DeleteView.as_view())
        return self._append(url, fun)

    def editor(self):
        url = \
            r'(?P<pk>\d+)/(?P<field_edit_name>[\w_]*)/(?P<target>[\w_]*)/editor/$'
        fun = make_perms_test_fun(self.base_perm % 'change', view_editor)
        if self.field:
            try:
                f = getattr(self.base_model, self.field).related
            except:
                f = getattr(self.base_model, self.field).rel
            model = f.related_model
        else:
            model = self.base_model
        parm = dict(
            app=self.table.app,
            tab=self.tab,
            ext='py',
            model=model,
            #post_save_redirect = make_path('schserw.urls.ok'),
            post_save_redirect = make_path('ok'),
            template_name=self.template_name,
            extra_context=transform_extra_context({'title': self.title
                     + ' - ' +str(_('update element')) }, self.extra_context),
            )
        return self._append(url, fun, parm)

    def tree(self):
        url = r'(?P<parent_pk>[\d-]*)/(?P<target>[\w_-]*)/[_]?tree$'

        #url = r'(?P<filter>[\w=_,;-]*)/(?P<target>[\w_-]*)/[_]?(list|sublist|get)$'

        class TreeView(generic.ListView):

            response_class = LocalizationTemplateResponse

            model = self.base_model
            paginate_by = 64
            allow_empty = True
            template_name = self.template_name
            title = self.title_plural
            if self.field:
                rel_field = field
            else:
                rel_field = None

            def doc_type(self):
                if self.kwargs['target']=='pdf':
                    return "pdf"
                elif self.kwargs['target']=='odf':
                    return "odf"
                elif self.kwargs['target']=='json':
                    return "json"
                else:
                    return "html"

            def get_context_data(self, **kwargs):
                context = super(TreeView, self).get_context_data(**kwargs)
                context['title'] = self.title
                context['rel_field'] = self.rel_field
                parent = int(self.kwargs['parent_pk'])
                context['parent_pk'] = parent
                if parent > 0:
                    context['parent_obj'] = self.model.objects.get(id=parent)
                else:
                    context['parent_obj'] = None
                return context

            def get(
                self,
                request,
                *args,
                **kwargs
                ):
                parent = int(kwargs['parent_pk'])
                if parent < 0:
                    parent_old = parent
                    try:
                        parent = self.model.objects.get(id=-1
                                 * parent).parent.id
                    except:
                        parent = 0
                    path2 = request.get_full_path().replace(str(parent_old), str(parent))
                    return HttpResponseRedirect(path2)
                else:
                    return super(TreeView, self).get(request, *args, **kwargs)

            def post(
                self,
                request,
                *args,
                **kwargs
                ):
                return self.get(request, *args, **kwargs)

            def get_queryset(self):
                parent = int(self.kwargs['parent_pk'])
                queryset = self.model.objects.all()
                if parent < 0:
                    return self.model.objects.all()
                else:
                    if parent == 0:
                        parent = None
                    return self.model.objects.filter(parent=parent)


        fun = make_perms_test_fun(self.base_perm % 'list', TreeView.as_view())
        return self._append(url, fun)


def generic_table(
    urlpatterns,
    app,
    tab,
    title='',
    title_plural='',
    template_name=None,
    extra_context=None,
    queryset=None,
    views_module=None,
    ):
    GenericTable(urlpatterns, app, views_module).new_rows(
        tab,
        None,
        title,
        title_plural,
        template_name,
        extra_context,
        queryset,
        ).list().detail().edit().add().delete().editor().tree().gen()


def generic_table_start(urlpatterns, app, views_module=None):
    return GenericTable(urlpatterns, app, views_module)
