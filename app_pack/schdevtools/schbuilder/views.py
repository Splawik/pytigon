#!/usr/bin/python

# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django import forms
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.template import Context, Template
from django.template import RequestContext
from django.conf import settings
from django.views.generic import TemplateView

from schlib.schviews.form_fun import form_with_perms
from schlib.schviews.viewtools import dict_to_template, dict_to_odf, dict_to_pdf, dict_to_json, dict_to_xml

from django.utils.translation import ugettext_lazy as _

from . import models
import os
import sys
import datetime

import shutil
import json
from base64 import b32decode
from schlib.schviews.viewtools import change_pos, duplicate_row
from schlib.schtools.tools import ZipWriter
import codecs
import six
import signal, os, ctypes 
from schlib.schtasks.base_task import get_process_manager
from django.core.management import call_command
from django.db import transaction
from subprocess import call, Popen, PIPE, STDOUT
import io
import schlib.schindent.indent_style
from schlib.schindent.indent_tools import convert_js
from schlib.schdjangoext.django_ihtml import ihtml_to_html
from schlib.schtools.tools import open_and_create_dir

 
_template="""
        [ gui_style | {{appset.gui_type}}({{appset.gui_elements}}) ]
        [ hybrid | {%if appset.is_hybrid %}1{%else%}0{%endif%} ]
        [ title  | {{appset.title}} ]
        [ start_page | {{start_page}} ]
        [ plugins | {{appset.plugins}} ]
"""

appset_attr=sorted([field.name for field in models.SChAppSet._meta.fields if field.name not in ('parent','id')])
app_attr=sorted([field.name for field in models.SChApp._meta.fields if field.name not in ('parent','id')])
choice_attr=sorted([field.name for field in models.SChChoice._meta.fields if field.name not in ('parent','id')])
choice_item_attr=sorted([field.name for field in models.SChChoiceItem._meta.fields if field.name not in ('parent','id')])
table_attr=sorted([field.name for field in models.SChTable._meta.fields if field.name not in ('parent','id')])
field_attr=sorted([field.name for field in models.SChField._meta.fields if field.name not in ('parent','id')])
view_attr=sorted([field.name for field in models.SChView._meta.fields if field.name not in ('parent','id')])
static_attr=sorted([field.name for field in models.SChStatic._meta.fields if field.name not in ('parent','id')])
template_attr=sorted([field.name for field in models.SChTemplate._meta.fields if field.name not in ('parent','id')])
appmenu_attr=sorted([field.name for field in models.SChAppMenu._meta.fields if field.name not in ('parent','id')])
form_attr=sorted([field.name for field in models.SChForm._meta.fields if field.name not in ('parent','id')])
formfield_attr=sorted([field.name for field in models.SChFormField._meta.fields if field.name not in ('parent','id')])
task_attr=sorted([field.name for field in models.SChTask._meta.fields if field.name not in ('parent','id')])
files_attr=sorted([field.name for field in models.SChFiles._meta.fields if field.name not in ('parent','id')])

def callback_fun_tab(obj1, obj2):
    fields_tmp = []
    for field in obj1.schfield_set.all():
        field.parent = obj2
        fields_tmp.append(field)
    for field in obj2.schfield_set.all():
        field.parent = obj1
        field.save()
    for field in fields_tmp:
        field.save()

def change_tab_pos(
    request,
    app,
    tab,
    pk,
    forward=True,
    field=None,
    callback_fun=None
    ):
    return change_pos(request, app, tab, pk, forward, field, callback_fun_tab)

def change_menu_pos(
    request,
    app,
    tab,
    pk,
    forward=True,
    field=None,
    callback_fun=None
    ):
    return change_pos(request, app, tab, pk, forward, field)

def change_pos_form_field(
    request,
    app,
    tab,
    pk,
    forward=True,
    field=None,
    callback_fun=None
    ):
    return change_pos(request, app, tab, pk, forward, field)


def template_to_file(base_path, template, file_name, context):
    txt = render_to_string('schbuilder/wzr/%s.html' % template, context)
    f = codecs.open(base_path+"/"+file_name, 'w', encoding='utf-8')
    f.write(txt)
    f.close()

def template_to_i_file(base_path, template, file_name, context):
    f=open(template,"rt")
    txt_in = f.read()
    f.close()
    t = Template(_template)
    try:
        txt = t.render(Context(context))
    except:
        import traceback
        import sys
        print(sys.exc_info()[0])
        print(traceback.print_exc())
    try:
        if isinstance(txt_in, six.text_type):
            txt2 = txt_in.replace('$$'+'$', txt)
        else:
            txt2 = txt_in.decode('utf-8').replace('$$'+'$', txt)
    except:
        import traceback
        import sys
        print(sys.exc_info()[0])
        print(traceback.print_exc())

    f = open(base_path+"/"+file_name,"wb")
    if isinstance(txt_in, six.text_type):
        f.write(txt2.encode('utf-8'))
    else:
        f.write(txt2.encode('utf-8'))
    f.close()

def str_to_file(base_path, buf, file_name):
    f = open(base_path+"/"+file_name,"wb")
    if buf:
        if isinstance(buf, six.text_type):
            f.write(buf.encode('utf-8'))
        else:
            f.write(buf)
    f.close()

def obj_to_array(obj, attrs):
    ret = []
    for attr in attrs:
        ret.append(getattr(obj, attr.strip()))
    return ret

def array_dict(array, attrs):
    ret = {}
    i=0
    for attr in attrs:
        ret[attr.strip()]=array[i]
        i+=1
    return ret

def copy_files_and_dirs(src, dst):
    names = os.listdir(src)
    if not os.path.exists(dst):
        os.makedirs(dst)
    errors = []
    for name in names:
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        try:
            if os.path.isdir(srcname):
                copy_files_and_dirs(srcname, dstname)
            else:
                shutil.copy2(srcname, dstname)
        except (IOError, os.error) as why:
            errors.append((srcname, dstname, str(why)))
        except shutil.Error as err:
            errors.extend(err.args[0])
    if errors:
        raise shutil.Error(errors)

def run_python_shell_task2(request):
    id = get_process_manager().put(request, "python-shell", "python3", '-i')
    new_url = "../../schsys/thread/%d/edit/" % id
    return HttpResponseRedirect(new_url)

def run_python_shell_task_base(request, base_path, appset_name):
    command = "from app_sets.%s.manage import *" % appset_name
    pconsole = settings.PYTHON_CONSOLE.split(' ')
    pconsole[0]=">>>" + pconsole[0]
    pconsole.append('-i')
    pconsole.append('-c')
    pconsole.append(command)
    param = ["python-shell",] + pconsole
    id = get_process_manager().put(request, *param)
    return id

def run_python_shell_task(request, base_path, appset_name):
    id = run_python_shell_task_base(request, base_path, appset_name)
    new_url = "../../schsys/thread/%d/edit/" % id
    return HttpResponseRedirect(new_url)
     





@dict_to_template('schbuilder/v_gen.html')




def gen(request, pk):
    
    appset = models.SChAppSet.objects.get(id=pk)
    base_path = settings.ROOT_PATH+"/app_pack/"+appset.name
    src_path = settings.ROOT_PATH+"/app_pack/schdevtools/"
    object_list = []
    
    if not os.path.exists(base_path):
        object_list.append((datetime.datetime.now().time().isoformat(), 'mkdir:', base_path))
        os.mkdir(base_path)
        os.mkdir(base_path+"/templates")
        os.mkdir(base_path+"/templates/template")
        os.mkdir(base_path+"/templates_src")
        os.mkdir(base_path+"/templates_src/template")
        os.mkdir(base_path+"/apache")
    
    apps = appset.schapp_set.all()
    
    template_to_file(base_path, "license", "LICENSE.txt", {'appset': appset})
    template_to_file(base_path, "readme", "README.txt",  {'appset': appset})
    template_to_file(base_path, "settings_app", "settings_app.py",  {'appset': appset})
    template_to_file(base_path, "manage", "manage.py",  {'appset': appset})
    template_to_file(base_path, "init", "__init__.py",  {'appset': appset})
    template_to_file(base_path, "wsgi", "run.wsgi",  {'appset': appset, 'base_path': base_path.replace('\\','/')})
    
    app_names = []
    for app in apps:
        object_list.append((datetime.datetime.now().time().isoformat(), 'create app:', app.name))
        if not os.path.exists(base_path+"/"+app.name):
            os.mkdir(base_path+"/"+app.name)
        if not os.path.exists(base_path+"/templates_src/"+app.name):
            os.mkdir(base_path+"/templates_src/"+app.name)
        if not os.path.exists(base_path+"/templates/"+app.name):
            os.mkdir(base_path+"/templates/"+app.name)
    
        app_names.append(app.name)
    
        tables = app.schtable_set.all()
        choices = app.schchoice_set.all()
        templates = app.schtemplate_set.all()
    
        is_tree_table = False
        gfields = []
        for table in tables:
            object_list.append((datetime.datetime.now().time().isoformat(), 'create tab:', table.name))
            table.tree_table = 0
            for field in table.schfield_set.filter(type__in=['GForeignKey','GManyToManyField', 'GHiddenForeignKey', 'GTreeForeignKey', 'GHiddenTreeForeignKey']):
                if field.type in ('GTreeForeignKey', 'GHiddenTreeForeignKey'):
                    is_tree_table = True
                    if table.base_table in ("", "models.Model"):
                        table.base_table = 'models.TreeModel'
                        table.tree_tab = 1
                    else: 
                        table.tree_tab = 2
                gfields.append(field)
    
        template_to_file(base_path, "models", app.name+"/models.py",  {'tables': tables, 'app': app, 'appset': appset, 'choices': choices, 'is_tree_table': is_tree_table })
    
        views = app.schview_set.all()
        forms = app.schform_set.all()
        tasks = app.schtask_set.all()
        template_to_file(base_path, "views", app.name+"/views.py",  {'views': views, 'forms': forms, 'app': app})
        template_to_file(base_path, "urls",  app.name+"/urls.py",  {'views': views, 'templates': templates, 'tables': tables, 'forms': forms, 'app': app, 'gfields': gfields})
        template_to_file(base_path, "tasks", app.name+"/tasks.py",  {'tasks': tasks, 'app': app})
    
        for template in templates:
            str_to_file(base_path, template.template_code, "templates_src/"+app.name+"/"+template.name.lower().replace(' ','_')+".ihtml")
    
        appmenus = app.schappmenu_set.all()
        
        if app.user_param:
            user_param = str(dict([ pos.split('=') for pos in app.user_param.split('\n') if pos and '=' in pos ]))
        else:
            user_param = '{}'
        
        template_to_file(base_path, "app_init", app.name+"/__init__.py",  {'appmenus': appmenus, 'app': app, 'user_param': user_param})
    
    template_to_file(base_path, "apps", "apps.py",  {'appset': appset, 'app_names': app_names })
    
    static_files = appset.schstatic_set.all()
    
    static_root = settings.ROOT_PATH+"/static/"+appset.name+"/"
    
    for static_file in static_files:
        txt = static_file.code
        if static_file.type=='C':
            t = Template(txt)
            txt2 = t.render(Context({'appset': appset} ))
            f = open_and_create_dir(static_root+static_file.name,"wb")
            f.write(txt2.encode('utf-8'))
            f.close()        
        if static_file.type=='J':
            t = Template(txt)
            txt2 = t.render(Context({'appset': appset} ))
            f = open_and_create_dir(static_root+static_file.name,"wb")
            f.write(txt2.encode('utf-8'))
            f.close()        
        if static_file.type=='P':
            t = Template(txt)
            txt2 = t.render(Context({'appset': appset} ))
            codejs = schlib.schindent.indent_style.py_to_js(txt2, None)
            f = open_and_create_dir(static_root+static_file.name,"wb")
            f.write(codejs.encode('utf-8'))
            f.close()        
        if static_file.type=='R':
            txt2 = ihtml_to_html(None, input_str=txt, lang='en')
            txt2 = txt2.replace("\"{", '{').replace("}\"", '}').replace('function on_', '').replace("""var __name__ = "__main__";""", '')
            t = Template(txt2)
            txt3 = t.render(Context({'appset': appset} ))
            buf = []
            buf.append("<%s>" % static_file.name)
            for line in txt3.split('\n'):
                buf.append('    '+line.replace('\r',''))
            buf.append("</%s>" % static_file.name)
            f = open_and_create_dir(settings.ROOT_PATH+"/static/components/"+appset.name+"/"+static_file.name+'.tag',"wb")
            f.write("\n".join(buf).encode('utf-8'))
            f.close()        
        if static_file.type=='I':
            in_str = io.StringIO(txt)
            out_str = io.StringIO()
            convert_js(in_str, out_str)
            t = Template(out_str.getvalue())
            txt2 = t.render(Context({'appset': appset} ))
            f = open_and_create_dir(static_root+static_file.name,"wb")
            f.write(txt2.encode('utf-8'))
            f.close()        
    
    riot_elements = []
    if appset.custom_tags:
        riot_elements += [ pos for pos in appset.custom_tags.replace('\n',';').replace('\r','').split(';') if pos ]
    riot_elements += [ appset.name+"/"+pos.name for pos in static_files if pos.type in ('R',) ]
    
    js_static_files = [ pos for pos in static_files if pos.type in ('J', 'P') ]
    css_static_files = [ pos for pos in static_files if pos.type in ('C', 'I') ]
    
    template_to_file(base_path, "desktop", "templates_src/template/desktop.ihtml",  {'appset': appset, 'js_static_files': js_static_files, 'css_static_files': css_static_files, 'riot_elements': riot_elements })
    print(riot_elements)
    #template_to_i_file(base_path, src_path+"templates_src/schbuilder/wzr/schweb.ihtml","templates_src/template/schweb.ihtml",  {'appset': appset, 'riot_elements': riot_elements })
    
    template_to_file(base_path, "schweb", "templates_src/template/schweb.ihtml",  {'appset': appset, 'riot_elements': riot_elements })
    
    base_path_src = base_path + "/src"
    
    if os.path.exists(base_path_src):
        copy_files_and_dirs(base_path_src, base_path)
    
    file_name = None
    file_content = []
    file_append = -1
    
    def output(file_name, file_append, file_content):
        os.makedirs(os.path.dirname(os.path.join(base_path, file_name)), exist_ok=True)
        if file_append==-1:        
            f = open(os.path.join(base_path, file_name), "wb")
            f.write(("\n".join(file_content)).encode('utf-8'))
            f.close()
        elif file_append==-2:
            f = open(os.path.join(base_path, file_name), "ab")
            f.write(("\n".join(file_content)).encode('utf-8'))
            f.close()
        else:
            f = open(os.path.join(base_path, file_name), "rb")
            txt = f.read().decode('utf-8').split('\n')
            f.close()
            if file_append < len(txt):
                txt = txt[:file_append] + file_content+txt[file_append:]
            else:
                txt = txt+file_content
            f = open(os.path.join(base_path, file_name), "wb")
            f.write(("\n".join(txt)).encode('utf-8'))
            f.close()
            
    if appset.user_app_template and len(appset.user_app_template)>0:
        txt = appset.user_app_template
        tab = txt.split('\n')
        for row in tab:
            if row.startswith('###'):
                if file_name and len(file_content)>0:
                    output(file_name, file_append, file_content)
                file_content = []
                file_name = row[3:]
                if file_name.startswith('>'):
                    file_name = file_name[1:].strip()
                    file_append = -2
                elif file_name.startswith('<') and '>' in file_name:
                    f = file_name[1:].split('>')
                    file_name = f[1].strip()
                    file_append = int(f[0])                
                else:
                    file_name = file_name.strip()
                    file_append = -1
            else:
                file_content.append(row)
                    
        if file_name and len(file_content)>0:
            output(file_name, file_append, file_content)
        
    object_list.append((datetime.datetime.now().time().isoformat(), 'SUCCESS:', ""))    
        
    return { 'object_list': reversed(object_list) }
    






def prj_export(request, pk):
    
    prj = []
    appset = models.SChAppSet.objects.get(id=pk)
    prj.append(obj_to_array(appset,appset_attr))
    apps = appset.schapp_set.all()
    apps_array=[]
    for app in apps:
        tables = app.schtable_set.all()
        tables_array=[]
        for table in tables:
            tmp=obj_to_array(table, table_attr)
            fields = table.schfield_set.all()
            fields_array=[]
            for field in fields:
                fields_array.append(obj_to_array(field, field_attr))
            tables_array.append([tmp,fields_array])
    
        choices = app.schchoice_set.all()
        choices_array=[]
        for choice in choices:
            tmp=obj_to_array(choice, choice_attr)
            choice_items = choice.schchoiceitem_set.all()
            choice_items_array=[]
            for item in choice_items:
                choice_items_array.append(obj_to_array(item, choice_item_attr))
            choices_array.append([tmp,choice_items_array])
    
        views = app.schview_set.all()
        views_array=[]
        for view in views:
            views_array.append(obj_to_array(view,view_attr))
    
        templates = app.schtemplate_set.all()
        templates_array=[]
        for template in templates:
            templates_array.append(obj_to_array(template,template_attr))
            
        appmenus = app.schappmenu_set.all()
        appmenus_array=[]
        for appmenu in appmenus:
            appmenus_array.append(obj_to_array(appmenu,appmenu_attr))
    
        forms = app.schform_set.all()
        forms_array=[]
        for form in forms:
            tmp=obj_to_array(form, form_attr)
            fields = form.schformfield_set.all()
            fields_array=[]
            for field in fields:
                fields_array.append(obj_to_array(field, formfield_attr))
            forms_array.append([tmp,fields_array])
    
        tasks = app.schtask_set.all()
        tasks_array=[]
        for task in tasks:
            tasks_array.append(obj_to_array(task,task_attr))
    
        files = app.schfiles_set.all()
        files_array=[]
        for file in files:
            files_array.append(obj_to_array(file,files_attr))
    
        tmp = obj_to_array(app, app_attr)
        apps_array.append([tmp, tables_array, choices_array, views_array, templates_array, appmenus_array, forms_array, tasks_array, files_array])
    prj.append(apps_array)
    
    statics = appset.schstatic_set.all()
    statics_array=[]
    for static in statics:
        statics_array.append(obj_to_array(static,static_attr))
    
    prj.append(statics_array)
    
    ex_str = json.dumps(prj, indent=4)
    return HttpResponse(ex_str, content_type="text/plain")
    

@dict_to_template('schbuilder/v_prj_import.html')




def prj_import(request):
    
    object_list = []
    
    ex_str = request.POST['EDITOR']
    prj=json.loads(ex_str)
    
    with transaction.atomic():
        appset = models.SChAppSet(**array_dict(prj[0], appset_attr))
        appset.save()
    
        apps_array=prj[1]
        for app_pos in apps_array:
            app = models.SChApp(**array_dict(app_pos[0], app_attr))
            app.parent=appset
            app.save()
    
            tables_array = app_pos[1]
            for table_pos in tables_array:
                table = models.SChTable(**array_dict(table_pos[0], table_attr))
                table.parent=app
                table.save()
    
                fields_array=table_pos[1]
                for field_pos in fields_array:
                    field = models.SChField(**array_dict(field_pos, field_attr))
                    field.parent=table
                    field.save()
    
    
            choices_array = app_pos[2]
            for choice_pos in choices_array:
                choice = models.SChChoice(**array_dict(choice_pos[0], choice_attr))
                choice.parent=app
                choice.save()
    
                choice_item_array=choice_pos[1]
                for item_pos in choice_item_array:
                    choice_item = models.SChChoiceItem(**array_dict(item_pos, choice_item_attr))
                    choice_item.parent=choice
                    choice_item.save()
    
            views_array=app_pos[3]
            for view_pos in views_array:
                view = models.SChView(**array_dict(view_pos, view_attr))
                view.parent=app
                view.save()
    
            templates_array=app_pos[4]
            for template_pos in templates_array:
                template = models.SChTemplate(**array_dict(template_pos, template_attr))
                template.parent=app
                template.save()
    
            appmenus = app.schappmenu_set.all()
            appmenus_array=app_pos[5]
            for appmenu_pos in appmenus_array:
                appmenu = models.SChAppMenu(**array_dict(appmenu_pos, appmenu_attr))
                appmenu.parent=app
                appmenu.save()
    
            forms_array = app_pos[6]
            for form_pos in forms_array:
                form = models.SChForm(**array_dict(form_pos[0], form_attr))
                form.parent=app
                form.save()
    
                formfields_array=form_pos[1]
                for field_pos in formfields_array:
                    field = models.SChFormField(**array_dict(field_pos, formfield_attr))
                    field.parent=form
                    field.save()
    
    
            tasks_array=app_pos[7]
            for task_pos in tasks_array:
                task = models.SChView(**array_dict(task_pos, task_attr))
                task.parent=app
                task.save()
    
            files_array=app_pos[8]
            for file_pos in files_array:
                f = models.SChFiles(**array_dict(file_pos, files_attr))
                f.parent=app
                f.save()
    
        statics_array=prj[2]
        for static in statics_array:
            s = models.SChStatic(**array_dict(static, static_attr))
            s.parent=appset
            s.save()
    
    object_list.append((datetime.datetime.now().time().isoformat(), 'SUCCESS:', ""))    
        
    return { 'object_list': reversed(object_list) }
    
    






def manage(request, pk):
    
    appset = models.SChAppSet.objects.get(id=pk)
    base_path = settings.ROOT_PATH+"/app_pack/"+appset.name
    src_path = settings.ROOT_PATH+"/app_pack/schdevtools/"
    command = "import sys; sys.path.append('%s'); from manage import *" % base_path
    pconsole = settings.PYTHON_CONSOLE.split(' ')
    pconsole[0]=">>>" + pconsole[0]
    pconsole.append('-i')
    pconsole.append('-c')
    pconsole.append(command)
    param = ["python-shell",] + pconsole
    id = get_process_manager().put(request, *param)
    new_url = "../../../tasks/form/TaskListForm/%d/edit2__task" % id
    #new_url = "../../schsys/thread/%d/edit/" % id
    return HttpResponseRedirect(new_url)
    






def template_edit(request, pk):
    
    table = models.SChTable.objects.get(id=pk)
    templates = models.SChTemplate.objects.filter(parent=table.parent).filter(name=table.name)
    if len(templates)==0:
        template=models.SChTemplate(parent=table.parent, name=table.name)
    
        generics =  table.schfield_set.filter(type__in=['GTreeForeignKey', 'GHiddenTreeForeignKey',])
        if len(generics) > 0:
            template_suffix = "tree"
        else:
            template_suffix = "tbl"
    
        file_name = settings.ROOT_PATH+("/app_pack/schdevtools/templates_src/schbuilder/wzr/new_generic_%s_template.ihtml" % template_suffix)
    
        f = open(file_name, "rt")
        template.template_code = f.read()
        f.close()
        template.save()
        id = template.id
    else:
        id = templates[0].id
    
    new_url = "/schbuilder/table/SChTemplate/%s/template_code/py/editor/" % str(id)
    
    return HttpResponseRedirect(new_url)
    
    






def edit(request):
    
    return TemplateView.as_view(template_name='schbuilder/import_form.html')(request)
    






def template_edit2(request, pk):
    
    form = models.SChForm.objects.get(id=pk)
    templates = models.SChTemplate.objects.filter(parent=form.parent).filter(name='Form'+form.name)
    if len(templates)==0:
        template=models.SChTemplate(parent=form.parent, name='Form'+form.name)
    
        file_name = settings.ROOT_PATH+"/app_pack/schdevtools/templates_src/schbuilder/wzr/new_generic_form_template.ihtml"
        f = open(file_name, "rt")
        template.template_code = f.read()
        f.close()
        template.save()
        id = template.id
    else:
        id = templates[0].id
    new_url = "/schbuilder/table/SChTemplate/%s/template_code/py/editor/" % str(id)
    return HttpResponseRedirect(new_url)
    

@dict_to_template('schbuilder/v_installer.html')




def installer(request, pk):
    
    buf = ""
    
    appset = models.SChAppSet.objects.get(id=pk)
    
    base_path = settings.ROOT_PATH+"/app_pack/"+appset.name+"/"
    zip_path = settings.ROOT_PATH+"/app_pack/"
    
    exclude=[".*\.pyc", ".*__pycache__.*"]
    zip = ZipWriter(zip_path+appset.name+".ptig", base_path, exclude=exclude)
    zip.toZip(base_path)
    
    buf += "PACK PROGRAM FILES TO: " + zip_path+appset.name+".ptig\n"
    
    p = os.path.expanduser("~")
    if isinstance(p, six.text_type):
        db_name = os.path.join(p, ".pytigon/"+appset.name+"/"+appset.name+".db")
    else:
        db_name = os.path.join(p, ".pytigon/"+appset.name+"/"+appset.name+".db").decode("cp1250")
    
    buf += "ADDING DATABASE FILES\n"
    
    if os.path.exists(base_path+"global_db_settings.py") or os.path.exists(settings.ROOT_PATH+"/global_db_settings.py"):
        if os.path.exists(db_name):
            os.rename(db_name, db_name+"."+datetime.datetime.now().strftime('%Y%m%d%H%M%S')+".bak")
        buf += "SYNC DATABASE FILE\n"
        p=Popen([settings.PYTHON_CONSOLE, base_path + 'manage.py', 'syncdb', '--database', 'local', '--noinput'], stdout=PIPE, stderr=STDOUT)
        output = p.communicate()[0]
        buf+=output.decode('utf-8')
        buf += "CREATE AUTO LOGIN ACCOUNT\n"
        p=Popen([settings.PYTHON_CONSOLE, base_path + 'manage.py', 'shell'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        script = b"""from django.contrib.auth.models import User; User.objects._db='local'; User.objects.create_superuser('auto', '', 'anawa')"""
        output = p.communicate(input=script)[0]
        buf+=output.decode('utf-8')
    else:
        if not os.path.exists(db_name):
            buf += "SYNC DATABASE FILE\n"
            p=Popen([settings.PYTHON_CONSOLE, base_path + 'manage.py', 'syncdb', '--noinput'], stdout=PIPE, stderr=STDOUT)
            output = p.communicate()[0]
            buf+=output.decode('utf-8')
            buf += "CREATE AUTO LOGIN ACCOUNT\n"
            p=Popen([settings.PYTHON_CONSOLE, base_path + 'manage.py', 'shell'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
            script = b"""from django.contrib.auth.models import User; User.objects.create_superuser('auto', '', 'anawa')"""
            output = p.communicate(input=script)[0]
            buf+=output.decode('utf-8')
    
    zip.write(db_name, name_in_zip=appset.name+".db")
    zip.close()
    buf += "END\n"
    
    return { 'object_list': buf.split('\n') }
    






def restart_server(request):
    
    if 'mod_wsgi.process_group' in request.environ:
        if request.environ['mod_wsgi.process_group'] != '':
            os.kill(os.getpid(), signal.SIGINT)
            print("restart_1")
        else:
            ctypes.windll.libhttpd.ap_signal_parent(1)
            print("restart_2")
    return HttpResponse('<html><body>Hello world</body></html>')
    






def template_edit3(request, pk):
    
    view = models.SChView.objects.get(id=pk)
    templates = models.SChTemplate.objects.filter(parent=view.parent).filter(name='v_'+view.name)
    if len(templates)==0:
        template=models.SChTemplate(parent=view.parent, name='v_'+view.name)
    
        file_name = settings.ROOT_PATH+"/app_pack/schdevtools/templates_src/schbuilder/wzr/new_generic_form_template.ihtml"
        f = open(file_name, "rt")
        template.template_code = f.read()
        f.close()
        template.save()
        id = template.id
    else:
        id = templates[0].id
    new_url = "/schbuilder/table/SChTemplate/%s/template_code/py/editor/" % str(id)
    return HttpResponseRedirect(new_url)
    


 
