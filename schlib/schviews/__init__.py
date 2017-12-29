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

#author: "Sławomir Chołaj (slawomir.cholaj@gmail.com)"
#copyright: "Copyright (C) ????/2012 Sławomir Chołaj"
#license: "LGPL 3.0"
#version: "0.1a"

"""Generic templates

"""


import collections
import uuid

from django.urls import get_script_prefix
from django.apps import apps
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from django.conf.urls import url
from django.db.models import CharField
from django.db.models import  Q
from django.utils.translation import ugettext_lazy as _

from schlib.schviews.actions import new_row_action, update_row_action
from schlib.schviews.viewtools import render_to_response

from .viewtools import transform_template_name, LocalizationTemplateResponse, ExtTemplateResponse
from .form_fun import form_with_perms
from .perms import make_perms_test_fun

# url:  /table/TableName/filter/target/list url width field:
# /table/TableName/parent_pk/field/filter/target/list

def make_path(view_name, args=None):
    if settings.URL_ROOT_FOLDER:
        return settings.URL_ROOT_FOLDER+"/"+reverse(view_name, args=args)
    else:
        return reverse(view_name, args=args)


def gen_tab_action(table, action, fun, extra_context=None):
    return url(r'table/%s/action/%s/$' % (table, action), fun, extra_context)


def gen_tab_field_action(table, field, action, fun, extra_context=None):
    return url(r'table/%s/(?P<parent_pk>\d+)/%s/action/%s/$' % (table, field, action), fun, extra_context)


def gen_row_action(table, action, fun, extra_context=None):
    return url('table/%s/(?P<pk>\d*)/action/%s/$' % (table, action), fun, extra_context)


def transform_extra_context(context1, context2):
    if context2:
        for (key, value) in context2.items():
            if isinstance(value, collections.Callable):
                context1[key] = value()
            else:
                context1[key] = value
    return context1


def view_editor(request, pk, app, tab, model, template_name, field_edit_name, post_save_redirect, ext='py',
            extra_context=None, target=None, parent_pk=0, field_name=None):
    if request.POST:
        data = request.POST['data']
        #print(type(data), data)
        buf = data.replace('\r\n', '\n')
        #if type(buf)==str:
        #    buf = buf.encode('utf-8')
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
            save_path =  app + '/table/' + tab + '/' + str(parent_pk) + '/' + table_name + '/' + str(pk) + \
                '/' + field_edit_name + '/py/editor/'
        else:
            save_path = app + '/table/' + table_name + '/' + str(pk) + '/' + field_edit_name + '/py/editor/'
        c = {
            'app': app,
            'tab': table_name,
            'pk': pk,
            'object': obj,
            'field_name': field_edit_name,
            'ext': ext,
            'save_path': save_path,
            'txt': txt,
            'verbose_field_name': f.verbose_name,
        }
        return render_to_response(transform_template_name(obj, request, 'schsys/db_field_edt.html'), context=c, request=request)


class GenericTable(object):
    """GenericTable"""

    def __init__(self, urlpatterns, app, views_module=None):
        """Constructor

        Args:
            urlpatterns -
            app - application
            views_module - module

        """
        self.urlpatterns = urlpatterns
        self.app = app
        self.base_url = get_script_prefix()
        self.views_module = views_module

    def new_rows(self, tab, field=None, title='', title_plural='', template_name=None, extra_context=None,
            queryset=None, prefix=None,):
        rows = GenericRows(self, prefix, title, title_plural)
        rows.tab = tab
        if field:
            rows.set_field(field)
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

    def from_schema(self, schema, tab, field=None, title='', title_plural='', template_name=None,
            extra_context=None, queryset=None, prefix=None,):
        if not title_plural:
            title_plural = title
        rows = self.new_rows(tab, field, title, title_plural, template_name, extra_context, queryset, prefix)
        self.append_from_schema(rows, schema)
        return rows

    def standard(self, tab, title='', title_plural='', template_name=None, extra_context=None,
            queryset=None, prefix=None,):
        schema = 'add'
        rows = self.from_schema(schema, tab, None, title, title_plural, template_name, extra_context, queryset, prefix)
        rows.set_field('this')
        rows.add().gen()

        schema = 'list;detail;edit;add;delete;editor'
        return self.from_schema(schema, tab, None, title, title_plural, template_name, extra_context, queryset, prefix)\
            .gen()

    def for_field(self, tab, field, title='', title_plural='', template_name=None, extra_context=None,
            queryset=None, prefix=None,):
        rows = self.new_rows(tab, field, title, title_plural, template_name, extra_context, queryset, prefix)
        schema = 'list;detail;edit;add;delete;editor'
        self.append_from_schema(rows, schema)
        return rows.gen()

    def tree(self, tab, title='', title_plural='', template_name=None, extra_context=None, queryset=None, prefix=None):
        return None


class GenericRows(object):

    def __init__(self, table, prefix, title="", title_plural="", parent_rows=None):
        self.table = table
        self.prefix = prefix
        self.field = None
        self.title = _(title)
        self.title_plural = _(title_plural)
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
                return self.base_path[:-1] + '_' + self.prefix + '/' + '(?P<parent_pk>-?\d+)/%s/' % self.field
            else:
                return self.base_path + '(?P<parent_pk>-?\d+)/%s/' % self.field
        else:
            if self.prefix:
                return self.base_path[:-1] + '_' + self.prefix + '/'
            else:
                return self.base_path


    def table_paths_to_context(self, view_class, context):
        x = view_class.request.path.split('/table/', 1)
        x2 = x[1].split('/')
        #context['app_path'] = x[0] + "/"
        if 'parent_pk' in view_class.kwargs:
            context['table_path'] = x[0] + "/table/" + "/".join(x2[:3]) + "/"
            context['table_path_and_filter'] = x[0] + "/table/" + "/".join(x2[:-3]) + "/"
        else:
            context['table_path'] = x[0] + "/table/" + x2[0] + "/"
            context['table_path_and_filter'] = x[0] + "/table/" + "/".join(x2[:-3]) + "/"


    def set_field(self, field=None):
        self.field = field
        return self

    def _append(self, url_str, fun, parm=None):
        if parm:
            self.table.urlpatterns += [ url(self._get_base_path() + url_str, fun, parm), ]
        else:
            self.table.urlpatterns += [ url(self._get_base_path() + url_str, fun), ]
        return self

    def gen(self):
        return self

    def list(self):
        url = r'((?P<base_filter>[\w=_,;-]*)/|)(?P<filter>[\w=_,;-]*)/(?P<target>[\w_-]*)/[_]?(?P<vtype>list|sublist|tree|get|gettree)/$'

        parent_class = self

        class ListView(generic.ListView):

            model = self.base_model
            queryset = self.queryset
            paginate_by = 64
            allow_empty = True
            template_name = self.template_name
            response_class = ExtTemplateResponse
            base_class = self
            form = None
            form_valid = None

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
                elif self.kwargs['target']=='txt':
                    return "txt"
                else:
                    return "html"

            def get_paginate_by(self, queryset):
                if self.doc_type() in ('pdf', 'odf', 'txt'):
                    return None
                else:
                    return self.paginate_by

            def get(self, request, *args, **kwargs):
                if 'init' in kwargs:
                    kwargs['init'](self)
                if 'tree' in self.kwargs['vtype']:
                    parent = int(kwargs['filter'])
                    if parent < 0:
                        parent_old = parent
                        try:
                            parent = self.model.objects.get(id=-1 * parent).parent.id
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
                        self.form_valid = None

                return super(ListView, self).get(request, *args, **kwargs)

            def post(self, request, *args, **kwargs):
                return self.get(request, *args, **kwargs)

            def get_context_data(self, **kwargs):
                nonlocal parent_class
                context = super(ListView, self).get_context_data(**kwargs)
                context['title'] = self.title
                context['rel_field'] = self.rel_field
                context['filter'] = self.kwargs['filter']

                parent_class.table_paths_to_context(self, context)

                if 'base_filter' in self.kwargs and self.kwargs['base_filter']:
                    context['base_filter'] = self.kwargs['base_filter']

                context['app_name'] = parent_class.table.app
                context['table_name'] = parent_class.tab

                if self.form:
                    context['form'] = self.form

                context['doc_type'] = self.doc_type()
                context['uuid'] = uuid.uuid4()

                context['app_pack'] = ""
                for app in settings.APPS:
                    if '.' in app and parent_class.table.app in app:
                        _app = app.split('.')[0]
                        if not _app.startswith('_'):
                            context['app_pack'] = app.split('.')[0]
                        break

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
                            if 'base_filter' in self.kwargs and self.kwargs['base_filter']:
                                parent = int(self.kwargs['base_filter'])
                            else:
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

                if self.form:
                    if self.form_valid == True:
                        return self.form.process(self.request, ret)
                    else:
                        if hasattr(self.form, 'process_empty_or_invalid'):
                            return self.form.process_empty_or_invalid(self.request, ret)
                        else:
                            return ret
                else:
                    return ret

        fun = make_perms_test_fun(self.base_perm % 'list', ListView.as_view())
        self._append(url, fun)

        return self

    def detail(self):
        url = r'(?P<pk>\d+)/(?P<target>[\w_]*)/view/$'
        parent_class = self

        class DetailView(generic.DetailView):

            queryset = self.queryset

            if self.field:
                try:
                    f = getattr(self.base_model, self.field).related
                except:
                    f = getattr(self.base_model, self.field).rel
                model = f.related_model
            else:
                model = self.base_model

            template_name = self.template_name
            title = self.title
            response_class = ExtTemplateResponse

            def doc_type(self):
                if self.kwargs['target']=='pdf':
                    return "pdf"
                elif self.kwargs['target']=='odf':
                    return "odf"
                elif self.kwargs['target']=='txt':
                    return "txt"
                else:
                    return "html"

            def get_context_data(self, **kwargs):
                nonlocal parent_class
                context = super(DetailView, self).get_context_data(**kwargs)
                context['title'] = self.title + ' - '+str(_('element information'))
                context['app_pack'] = ""

                parent_class.table_paths_to_context(self, context)

                for app in settings.APPS:
                    if '.' in app and parent_class.table.app in app:
                        _app = app.split('.')[0]
                        if not _app.startswith('_'):
                            context['app_pack'] = app.split('.')[0]
                        break
                return context

        fun = make_perms_test_fun(self.base_perm % 'list', DetailView.as_view())
        return self._append(url, fun)

    def edit(self):
        url = r'(?P<pk>\d+)/edit/$'
        parent_class = self

        class UpdateView(generic.UpdateView):
            #response_class = LocalizationTemplateResponse
            doc_type = "html"
            response_class = ExtTemplateResponse

            if self.field:
                try:
                    f = getattr(self.base_model, self.field).related
                except:
                    f = getattr(self.base_model, self.field).rel
                model = f.related_model
            else:
                model = self.base_model
            success_url = make_path('ok')

            template_name = self.template_name
            title = self.title
            fields = "__all__"


            def doc_type(self):
                return "html"

            def get_context_data(self, **kwargs):
                nonlocal parent_class
                context = super(UpdateView, self).get_context_data(**kwargs)
                context['title'] = self.title + ' - ' + str(_('update element'))
                context['app_pack'] = ""

                parent_class.table_paths_to_context(self, context)

                for app in settings.APPS:
                    if '.' in app and parent_class.table.app in app:
                        _app = app.split('.')[0]
                        if not _app.startswith('_'):
                            context['app_pack'] = app.split('.')[0]
                        break
                return context

            def get(self, request, *args, **kwargs):
                self.object = self.get_object()

                if 'init' in kwargs:
                    kwargs['init'](self)

                form_class = self.get_form_class()

                if self.object and hasattr(self.object, 'get_form'):
                    form = self.object.get_form(self, request, form_class, False)
                else:
                    form = self.get_form(form_class)

                if form:
                    for field in form.fields:
                        if hasattr(form.fields[field].widget, 'py_client'):
                            if request.META['HTTP_USER_AGENT'].startswith('Py'):
                                form.fields[field].widget.set_py_client(True)
                return self.render_to_response(self.get_context_data(form=form))


            def post(self, request, *args, **kwargs):
                self.object = self.get_object()

                if 'init' in kwargs:
                    kwargs['init'](self)

                form_class = self.get_form_class()

                if self.object and hasattr(self.object, 'get_form'):
                    form = self.object.get_form(self, request, form_class, False)
                else:
                    form = self.get_form(form_class)

                if self.model and hasattr(self.model, 'is_form_valid'):
                    def vfun():
                        return self.model.is_form_valid(form)
                else:
                    vfun = form.is_valid

                if vfun():
                    return self.form_valid(form, request)
                else:
                    print("INVALID:", form.errors)
                    return self.form_invalid(form)

            def form_valid(self, form, request=None):
                """
                If the form is valid, save the associated model.
                """
                _data = {}
                for key, value in form.data.items():
                    if key.startswith('json_'):
                        _data[key[5:]] = value

                self.object = form.save(commit=False)

                if _data:
                    self.object._data = _data

                if hasattr(self.object, 'post_form'):
                    if self.object.post_form(self, form, request):
                        self.object.save()
                else:
                    self.object.save()
                form.save_m2m()

                if self.object:
                    return update_row_action(request, int(self.object.id), str(self.object))
                else:
                    return super(generic.edit.ModelFormMixin, self).form_valid(form)

        fun = make_perms_test_fun(self.base_perm % 'change', UpdateView.as_view())
        return self._append(url, fun)

    def add(self):
        url = r'(?P<add_param>[\w=_-]*)/add/$'
        parent_class = self

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
            template_name = self.template_name
            title = self.title
            field = self.field
            init_form = None
            fields = "__all__"

            def get_success_url(self):
                if self.object:
                    success_url = make_path('ret_ok', (int(self.object.id), str(self.object)))
                else:
                    success_url = make_path('ok')
                return success_url

            def _get_form(self, request, *args, **kwargs):
                self.object = self.model()
                if self.field:
                    ppk = int(kwargs['parent_pk'])
                    if ppk > 0:
                        self.object.parent = self.pmodel.objects.get(id=ppk)
                if hasattr(self.model, 'init_new'):
                    if kwargs['add_param'] and kwargs['add_param'] != '-':
                        self.init_form = self.object.init_new(request, self, kwargs['add_param'])
                    else:
                        self.init_form = self.object.init_new(request, self)

                    if self.init_form:
                        for pos in self.init_form:
                            if hasattr(self.object, pos):
                                try:
                                    setattr(self.object, pos, self.init_form[pos])
                                except:
                                    pass
                else:
                    self.init_form = None
                form_class = self.get_form_class()

                if self.object and hasattr(self.object, 'get_form'):
                    form = self.object.get_form(self, request, form_class, True)
                else:
                    form = self.get_form(form_class)
                return form

            def get(self, request, *args, **kwargs):
                form = self._get_form(request, *args, **kwargs)
                if form:
                    for field in form.fields:
                        if hasattr(form.fields[field].widget, 'py_client'):
                            if request.META['HTTP_USER_AGENT'].startswith('Py'):
                                form.fields[field].widget.set_py_client(True)
                return self.render_to_response(self.get_context_data(form=form))

            def post(self, request, *args, **kwargs):
                form = self._get_form(request, *args, **kwargs)

                #self.object = None

                #if hasattr(self.model, 'init_new'):
                #    if kwargs['add_param'] and kwargs['add_param'] != '-':
                #        self.init_form = self.object.init_new(request, self, kwargs['add_param'])
                #    else:
                #        self.init_form = self.object.init_new(request, self)#
                #else:
                #    self.init_form = None

                #form_class = self.get_form_class()

                #if self.object and hasattr(self.object, 'get_form'):
                #    form = self.object.get_form(self, request, form_class, True)
                #else:
                #    form = self.get_form(form_class)

                if self.model and hasattr(self.model, 'is_form_valid'):
                    def vfun():
                        return self.model.is_form_valid(form)
                else:
                    vfun = form.is_valid
                if vfun():
                    return self.form_valid(form, request)
                else:
                    print("INVALID:", form.errors)
                    return self.form_invalid(form)


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
                if self.init_form:
                    if 'data' in ret:
                        data = ret['data'].copy()
                        for key, value in self.init_form.items():
                            data[key] = value
                        ret.update({'data': data})

                return ret



            def form_valid(self, form, request=None):
                """
                If the form is valid, save the associated model.
                """

                _data = {}
                for key, value in form.data.items():
                    if key.startswith('json_'):
                        _data[key[5:]] = value

                self.object = form.save(commit=False)

                if _data:
                    self.object._data = _data

                #if hasattr(self.object, 'init_new'):
                #    if self.kwargs['add_param'] and self.kwargs['add_param'] != '-':
                #        self.init_form = self.object.init_new(request, self, self.kwargs['add_param'])
                #    else:
                #        self.init_form = self.object.init_new(request, self)

                if 'parent_pk' in self.kwargs and hasattr(self.object, 'parent_id'):
                    if int(self.kwargs['parent_pk'])!=0:
                        self.object.parent_id = int(self.kwargs['parent_pk'])

                if request and request.POST:
                    p = request.POST
                else:
                    p = {}
                if self.init_form:
                    for pos in self.init_form:
                        if hasattr(self.object, pos) and not pos in p:
                            try:
                                setattr(self.object, pos, self.init_form[pos])
                            except:
                                pass

                if hasattr(self.object, 'post_form'):
                    if self.object.post_form(self, form, request):
                        self.object.save()
                else:
                    self.object.save()
                form.save_m2m()

                if self.object:
                    return new_row_action(request, int(self.object.id), str(self.object))
                else:
                    return super(generic.edit.ModelFormMixin, self).form_valid(form)

            def get_context_data(self, **kwargs):
                nonlocal parent_class
                context = super(CreateView, self).get_context_data(**kwargs)
                context['title'] = self.title + ' - '+ str(_('new element'))
                context['object'] = self.object
                context['app_pack'] = ""

                parent_class.table_paths_to_context(self, context)

                for app in settings.APPS:
                    if '.' in app and parent_class.table.app in app:
                        _app = app.split('.')[0]
                        if not _app.startswith('_'):
                            context['app_pack'] = app.split('.')[0]
                        break
                return context

        fun = make_perms_test_fun(self.base_perm % 'change',
                                  CreateView.as_view())
        return self._append(url, fun)

    def delete(self):
        url = r'(?P<pk>\d+)/delete/$'
        parent_class = self

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
            success_url = make_path('ok')
            template_name = self.template_name
            title = self.title

            def get_context_data(self, **kwargs):
                nonlocal parent_class
                context = super(DeleteView, self).get_context_data(**kwargs)
                context['title'] = self.title + ' - ' + str(_('delete element'))

                parent_class.table_paths_to_context(self, context)

                context['app_pack'] = ""
                for app in settings.APPS:
                    if '.' in app and parent_class.table.app in app:
                        _app = app.split('.')[0]
                        if not _app.startswith('_'):
                            context['app_pack'] = app.split('.')[0]
                        break
                return context

        fun = make_perms_test_fun(self.base_perm % 'delete',
                                  DeleteView.as_view())
        return self._append(url, fun)

    def editor(self):
        url = r'(?P<pk>\d+)/(?P<field_edit_name>[\w_]*)/(?P<target>[\w_]*)/editor/$'
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
            post_save_redirect = make_path('ok'),
            template_name=self.template_name,
            extra_context=transform_extra_context({'title': self.title + ' - ' +str(_('update element')) },
                    self.extra_context),
            )
        return self._append(url, fun, parm)


def generic_table(urlpatterns, app, tab, title='', title_plural='', template_name=None, extra_context=None,
            queryset=None, views_module=None):
    GenericTable(urlpatterns, app, views_module).new_rows(tab, None, title, title_plural, template_name, extra_context,
            queryset).list().detail().edit().add().delete().editor().gen()


def generic_table_start(urlpatterns, app, views_module=None):
    """Start generic table urls

    Args:
        urlpatterns - urlpatterns object defined in urls.py
        app - name of app
        views_module - imported views.py module
    """
    return GenericTable(urlpatterns, app, views_module)

