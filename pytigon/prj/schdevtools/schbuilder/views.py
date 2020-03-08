#!/usr/bin/python

# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django import forms
from django.template.loader import render_to_string
from django.template import Context, Template
from django.template import RequestContext
from django.conf import settings
from django.views.generic import TemplateView

from pytigon_lib.schviews.form_fun import form_with_perms
from pytigon_lib.schviews.viewtools import dict_to_template, dict_to_odf, dict_to_pdf, dict_to_json, dict_to_xml
from pytigon_lib.schviews.viewtools import render_to_response
from pytigon_lib.schdjangoext.tools import make_href

from django.utils.translation import ugettext_lazy as _

from . import models
import os
import sys
import datetime

import shutil
import json
import zipfile
import base64
import platform
import polib
import locale
import codecs
import signal
import os
import io
import time
import configparser

from django.db import transaction
from django.urls import reverse

from pytigon_lib.schviews.viewtools import change_pos, duplicate_row
#from pytigon_lib.schtasks.base_task import get_process_manager
import pytigon_lib.schindent.indent_style
from pytigon_lib.schindent.indent_tools import convert_js
from pytigon_lib.schdjangoext.django_ihtml import ihtml_to_html

from pytigon_lib.schfs.vfstools import ZipWriter, open_and_create_dir
from pytigon_lib.schtools.install import extract_ptig
from pytigon_lib.schtools.process import py_run
from pytigon_lib.schtools.platform_info import platform_name

from pytigon_lib.schtools.cc import import_plugin, make

from pytigon.ext_lib.pygettext import main as gtext

try:
    import sass
except:
    sass =  None

import pytigon.schserw.settings

 
_template="""
        [ gui_style | {{prj.gui_type}}({{prj.gui_elements}}) ]
        [ title  | {{prj.title}} ]
        [ start_page | {{start_page}} ]
        [ plugins | {{prj.plugins}} ]
"""

prj_attr=sorted([field.name for field in models.SChAppSet._meta.fields if field.name not in ('parent','id')])
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
consumer_attr=sorted([field.name for field in models.SChChannelConsumer._meta.fields if field.name not in ('parent','id')])

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
        if type(txt_in)==str:
            txt2 = txt_in.replace('$$'+'$', txt)
        else:
            txt2 = txt_in.decode('utf-8').replace('$$'+'$', txt)
    except:
        import traceback
        import sys
        print(sys.exc_info()[0])
        print(traceback.print_exc())

    f = open(base_path+"/"+file_name,"wb")
    if type(txt_in)==str:
        f.write(txt2.encode('utf-8'))
    else:
        f.write(txt2.encode('utf-8'))
    f.close()

def str_to_file(base_path, buf, file_name):
    f = open(base_path+"/"+file_name,"wb")
    if buf:
        if type(buf)==str:
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
    from pytigon_lib.schtasks.base_task import get_process_manager
    id = get_process_manager().put(request, "python-shell", "python3", '-i')
    new_url = make_href("../../schsys/thread/%d/edit/" % id)
    return HttpResponseRedirect(new_url)

def run_python_shell_task_base(request, base_path, prj_name):
    from pytigon_lib.schtasks.base_task import get_process_manager
    command = "from app_sets.%s.manage import *" % prj_name
    pconsole = settings.PYTHON_CONSOLE.split(' ')
    pconsole[0]=">>>" + pconsole[0]
    pconsole.append('-i')
    pconsole.append('-c')
    pconsole.append(command)
    param = ["python-shell",] + pconsole
    id = get_process_manager().put(request, *param)
    return id

def run_python_shell_task(request, base_path, prj_name):
    id = run_python_shell_task_base(request, base_path, prj_name)
    new_url = make_href("../../schsys/thread/%d/edit/" % id)
    return HttpResponseRedirect(new_url)


def make_messages(src_path, path, name, outpath=None, ext_locales=[]):
    backup_argv = sys.argv
    
    sys.argv = [None, '-a', '-d', name, '-p', path]

    for root, dirs, files in os.walk(src_path):
        for f in files:
            if f.endswith('.py'):
                p = os.path.join(root, f)
                sys.argv.append(p)
    gtext()

    wzr_filename = os.path.join(path, name+'.pot')
    for pos in os.scandir(path):
        if pos.is_dir():            
            lang = pos.name
            ftmp = os.path.join(path, lang)
            if outpath:
                ftmp = os.path.join(ftmp, outpath)
            filename = os.path.join(ftmp, name + '.po')
            old_filename = filename.replace('.po', '.bak')
            mo_filename = filename.replace('.po', '.mo')
            try:
                os.remove(old_filename)
            except:
                pass
            try:
                os.rename(filename, old_filename)
            except:
                pass

            wzr = polib.pofile(wzr_filename)
            if os.path.exists(old_filename):
                po = polib.pofile(old_filename)
            else:
                po = polib.POFile()
            po.merge(wzr)
            
            #for pos2 in ext_locales:
            #    ftmp = os.path.join(pos2[1],lang)
            #    if outpath:
            #        ftmp = os.path.join(ftmp, outpath)
            #    ext_filename = os.path.join(ftmp, name+'.po')
            #    if os.path.exists(ext_filename):
            #        ext_po = polib.pofile(ext_filename)
            #        po.merge(ext_po)
                
            po.save(filename)
            po.save_as_mofile(mo_filename)

    sys.argv = backup_argv


def locale_gen_internal(pk):
    prj = models.SChAppSet.objects.get(id=pk)

    base_path = settings.PRJ_PATH
    app_path = os.path.join(base_path, prj.name)
    locale_path = os.path.join(app_path, 'locale')

    ext_apps = []
    ext_locales = []
    if prj.ext_apps:
        for pos in prj.ext_apps.split(','):
            pos2 = pos.split('.')[0]
            if pos2 and not pos2 in ext_apps:
                ext_apps.append(pos2)
                app_path2 = os.path.join(base_path, pos2)
                locale_path2 = os.path.join(app_path2, 'locale')                
                ext_locales.append([app_path2, locale_path2])
    make_messages(app_path, locale_path, 'django', 'LC_MESSAGES', ext_locales)

    template_path = os.path.join(app_path, "templates")

    to_remove = []
    for root, dirs, files in os.walk(template_path):
        for f in files:
            if f.endswith('.html'):
                p = os.path.join(root, f)
                to_remove.append(p)

    for pos in to_remove:
        os.unlink(pos)

    return { 'object_list': [[ 'OK' ],] }
        

def prj_import_from_str(s):
    object_list = []
    prj = json.loads(s)
    with transaction.atomic():
        prj_instence = models.SChAppSet(**array_dict(prj[0], prj_attr))
        prj_instence.save()
    
        apps_array=prj[1]
        for app_pos in apps_array:
            app = models.SChApp(**array_dict(app_pos[0], app_attr))
            app.parent=prj_instence
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
                task = models.SChTask(**array_dict(task_pos, task_attr))
                task.parent=app
                task.save()
    
            consumers_array=app_pos[8]
            for consumer_pos in consumers_array:
                consumer = models.SChChannelConsumer(**array_dict(consumer_pos, consumer_attr))
                consumer.parent=app
                consumer.save()
    
    
            files_array=app_pos[9]
            for file_pos in files_array:
                f = models.SChFiles(**array_dict(file_pos, files_attr))
                f.parent=app
                f.save()
    
        statics_array=prj[2]
        for static in statics_array:
            s = models.SChStatic(**array_dict(static, static_attr))
            s.parent=prj_instence
            s.save()
    
    object_list.append((datetime.datetime.now().time().isoformat(), 'SUCCESS:', ""))    

    return { 'object_list': reversed(object_list) }

 

PFORM = form_with_perms('schbuilder') 


class Installer(forms.Form):
    name = forms.ChoiceField(label=_('Application package name'), required=True, choices=models.apppack)
    
    def process(self, request, queryset=None):
    
        name = self.cleaned_data['name']
        return installer(request, name)
    

def view_installer(request, *argi, **argv):
    return PFORM(request, Installer, 'schbuilder/forminstaller.html', {})


class Install(forms.Form):
    install_file = forms.FileField(label=_('Install file (*.ptig)'), required=True, )
    
    def process(self, request, queryset=None):
    
        install_file = request.FILES['install_file']
        name = install_file.name.split('.')[0]
        zip_file = zipfile.ZipFile(install_file.file)
        ret = extract_ptig(zip_file, name)
        
        extract_to = os.path.join(settings.PRJ_PATH, name)
        (ret_code, output, err) = py_run([os.path.join(extract_to, 'manage.py'), 'post_installation'])
        
        
        return { "object_list": ret }
    

def view_install(request, *argi, **argv):
    return PFORM(request, Install, 'schbuilder/forminstall.html', {})



@dict_to_template('schbuilder/v_gen.html')




def gen(request, pk):
    
    prj = models.SChAppSet.objects.get(id=pk)
    root_path = settings.ROOT_PATH
    
    if hasattr(pytigon.schserw.settings,"_PRJ_PATH"):
        base_path = os.path.join(pytigon.schserw.settings._PRJ_PATH, prj.name)
    else:
        base_path = os.path.join(settings.PRJ_PATH, prj.name)
    src_path = os.path.join(settings.PRJ_PATH, "schdevtools")
    object_list = []
    gmt = time.gmtime()
    gmt_str = "%04d.%02d.%02d %02d:%02d:%02d" % (gmt[0], gmt[1], gmt[2], gmt[3], gmt[4], gmt[5])
    
    if not os.path.exists(base_path):
        object_list.append((datetime.datetime.now().time().isoformat(), 'mkdir:', base_path))
        os.makedirs(base_path, exist_ok=True)
        os.makedirs(base_path+"/templates", exist_ok=True)
        os.makedirs(base_path+"/templates/template", exist_ok=True)
        os.makedirs(base_path+"/templates_src", exist_ok=True)
        os.makedirs(base_path+"/templates_src/template", exist_ok=True)
        os.makedirs(base_path+"/apache", exist_ok=True)
    
    apps = prj.schapp_set.all()
    
    #template_to_file(base_path, "license", "LICENSE.txt", {'prj': prj})
    #template_to_file(base_path, "readme", "README.txt",  {'prj': prj})
    with open(os.path.join(base_path, "README.txt"), "wt") as f:
        if prj.readme_file:
            f.write(prj.readme_file)
    with open(os.path.join(base_path, "LICENSE.txt"), "wt") as f:
        if prj.license_file:
            f.write(prj.license_file)
    with open(os.path.join(base_path, "install.ini"), "wt") as f:
        f.write("[DEFAULT]\nPRJ_NAME=%s\n" % prj.name)
        f.write("PRJ_TITLE=%s\n" % prj.title)
        f.write("GEN_TIME='%s'\n" % gmt_str)
        if prj.install_file:
            f.write(prj.install_file)
    if prj.app_main:
        with open(os.path.join(base_path, "prj_main.py"), "wt") as f:
            f.write(prj.app_main)
    
    template_to_file(base_path, "manage", "manage.py",  {'prj': prj})
    template_to_file(base_path, "init", "__init__.py",  {'prj': prj})
    template_to_file(base_path, "wsgi", "wsgi.py",  {'prj': prj, 'base_path': base_path.replace('\\','/')})
    template_to_file(base_path, "asgi", "asgi.py",  {'prj': prj, 'base_path': base_path.replace('\\','/')})
    
    app_names = []
    for app in apps:
        object_list.append((datetime.datetime.now().time().isoformat(), 'create app:', app.name))
        if not os.path.exists(base_path+"/"+app.name):
            os.makedirs(base_path+"/"+app.name, exist_ok=True)
        if not os.path.exists(base_path+"/templates_src/"+app.name):
            os.makedirs(base_path+"/templates_src/"+app.name, exist_ok=True)
        if not os.path.exists(base_path+"/templates/"+app.name):
            os.makedirs(base_path+"/templates/"+app.name, exist_ok=True)
    
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
                    if table.base_table in (None, "", "models.Model") and not table.proxy_model:
                        table.base_table = 'TreeModel'
                        table.tree_tab = 1
                    else: 
                        table.tree_tab = 2
                gfields.append(field)
    
        template_to_file(base_path, "models", app.name+"/models.py",  {'tables': tables, 'app': app, 'prj': prj, 'choices': choices, 'is_tree_table': is_tree_table })
    
        views = app.schview_set.all()
        forms = app.schform_set.all()
        tasks = app.schtask_set.all()
        consumers = app.schchannelconsumer_set.all()
        template_to_file(base_path, "views", app.name+"/views.py",  {'views': views, 'forms': forms, 'app': app})
        template_to_file(base_path, "urls",  app.name+"/urls.py",  {'views': views, 'templates': templates, 'tables': tables, 'forms': forms, 'app': app, 'gfields': gfields})
        template_to_file(base_path, "tasks", app.name+"/tasks.py",  {'tasks': tasks, 'app': app})
        template_to_file(base_path, "consumers", app.name+"/consumers.py",  {'consumers': consumers, 'app': app})
    
        for template in templates:
            str_to_file(base_path, template.template_code, "templates_src/"+app.name+"/"+template.name.lower().replace(' ','_')+".ihtml")
    
        appmenus = app.schappmenu_set.all()
        
        if app.user_param:
            user_param = str(dict([ pos.split('=') for pos in app.user_param.split('\n') if pos and '=' in pos ]))
        else:
            user_param = '{}'
        
        template_to_file(base_path, "app_init", app.name+"/__init__.py",  {'appmenus': appmenus, 'app': app, 'user_param': user_param})
    
        for file_obj in app.schfiles_set.all():
            if file_obj.file_type=='f':
                file_name = base_path + "/" + app.name+"/templatetags/"+ file_obj.name + ".py"
            elif file_obj.file_type=='t':
                file_name = base_path + "/" + app.name+"/templatetags/"+ file_obj.name + ".py"
            elif file_obj.file_type=='c':
                file_name = base_path + "/" + app.name+"/"+ file_obj.name
            elif file_obj.file_type=='m':
                f = open_and_create_dir(base_path + "/" + app.name+"/management/__init__.py", "wb")
                f.close()
                f = open_and_create_dir(base_path + "/" + app.name+"/management/commands/__init__.py","wb")
                f.close()
                file_name = base_path + "/" + app.name+"/management/commands/"+ file_obj.name
            elif file_obj.file_type=='p':
                if '/' in file_obj.name:
                    x = file_obj.name.split('/')
                    plugin_name = x[0]
                    file_name = x[1]
                else:
                    plugin_name = file_obj.name
                    file_name = '__init__'
                file_name = base_path + "/plugins/" + app.name + "/" + plugin_name + "/" + file_name + ".py"
            elif file_obj.file_type=='i':
                if '/' in file_obj.name:
                    x = file_obj.name.split('/')
                    plugin_name = x[0]
                    file_name = x[1]
                else:
                    plugin_name = file_obj.name
                    file_name = 'index'
                file_name = base_path + "/plugins/" + app.name + "/" + plugin_name + "/" + file_name + ".html"
                content =  ihtml_to_html(None, file_obj.content)
                f = open_and_create_dir(file_name,"wb")
                f.write(content.encode('utf-8'))
                f.close()
                file_name = None
            elif file_obj.file_type in ('l', 'x', 'C'):
                f = open_and_create_dir(base_path + "/applib/__init__.py", "wb")
                f.close()
                f = open_and_create_dir(base_path + "/applib/" + app.name + "lib/__init__.py", "wb")
                f.close()
                file_name = base_path + "/applib/" + app.name + "lib/"+ file_obj.name 
                if file_obj.file_type == 'l':
                    file_name += ".py"
                elif file_obj.file_type == 'x':
                    file_name += ".pyx"
                else:
                    file_name += '.c'
            elif file_obj.file_type == 's':
                file_name = base_path + "/" + app.name+"/schema.py"
            else: 
                file_name = None
                
            if file_name:
                f = open_and_create_dir(file_name,"wb")
                if type(file_obj.content)==str:
                    f.write(file_obj.content.encode('utf-8'))
                else:
                    f.write(file_obj.content)
                f.close()
            
    
    template_to_file(base_path, "apps", "apps.py",  {'prj': prj, 'app_names': app_names })
    
    static_files = prj.schstatic_set.all()
    
    #if settings.STATIC_APP_ROOT:
    #    static_root = os.path.join(settings.STATIC_APP_ROOT, prj.name)
    #else:
    #    if settings.STATIC_ROOT:
    #        static_root = os.path.join(os.path.join(settings.STATIC_ROOT, 'app'),prj.name)
    #    else:
    #        static_root = os.path.join(os.path.join(settings.STATICFILES_DIRS[0], 'app'),prj.name)
    
    static_root = os.path.join(base_path, "static", prj.name)
    
    static_scripts = os.path.join(static_root,'js')
    static_style = os.path.join(static_root,'css')
    static_components = os.path.join(static_root,'components')
    
    offline_support = False
    vue_init = ""
    
    for static_file in static_files:
        txt = static_file.code
        typ = static_file.type
        dest_path = None
        if static_file.name=='sw.js':
            offline_support = True
            
        if static_file.type=='U':
            dest_path = os.path.join(static_root,static_file.name)
            if '.pyj' in static_file.name:
                dest_path = os.path.join(static_root,static_file.name.replace('.pyj', '.js'))
                typ = 'P'
            elif '.sass' in static_file.name:
                dest_path = os.path.join(static_root,static_file.name.replace('.sass', '.css'))
                typ = 'I'
            elif '.vue' in static_file.name:
                dest_path = os.path.join(static_root,static_file.name.replace('.vue', '.js'))
                typ = 'R'
                        
        if typ=='C':
            t = Template(txt)
            txt2 = t.render(Context({'prj': prj} ))
            f = open_and_create_dir(os.path.join(static_style, static_file.name+".css"),"wb")
            f.write(txt2.encode('utf-8'))
            f.close()        
        if typ=='J':
            t = Template(txt)
            txt2 = t.render(Context({'prj': prj} ))
            f = open_and_create_dir(os.path.join(static_scripts,static_file.name+".js"),"wb")
            f.write(txt2.encode('utf-8'))
            f.close()        
        if typ=='P':
            t = Template(txt)
            txt2 = t.render(Context({'prj': prj} ))
            try:
                codejs = pytigon_lib.schindent.indent_style.py_to_js(txt2, None)
                codejs = codejs.replace('./org.transcrypt.__runtime__.js','../../sch/org.transcrypt.__runtime__.js').replace('__globals__,', '')
                #codejs = codejs.split("__pragma__ ('<all>')",1)[0]
            except:
                codejs = ""
            print(dest_path if dest_path else os.path.join(static_scripts,static_file.name+".js"))
            f = open_and_create_dir(dest_path if dest_path else os.path.join(static_scripts,static_file.name+".js"),"wb")
            f.write(codejs.encode('utf-8'))
            f.close()        
        if typ=='R':
            try:
                codejs = pytigon_lib.schindent.indent_style.py_to_js(txt, None)
                #codejs = codejs.split("__pragma__ ('<all>')",1)[0]
                codejs = codejs.replace('./org.transcrypt.__runtime__.js','../../sch/org.transcrypt.__runtime__.js').replace('__globals__,', '')
            except:
                codejs = ""
            print(dest_path if dest_path else os.path.join(static_components, static_file.name+'.js'))    
            f = open_and_create_dir(dest_path if dest_path else os.path.join(static_components, static_file.name+'.js'),"wb")
            f.write(codejs.encode('utf-8'))
            f.close()        
        if typ=='I':
            if sass:
                buf = sass.compile(string=txt, indented=True,)
                t = Template(buf)
                txt2 = t.render(Context({'prj': prj} ))
                f = open_and_create_dir(dest_path if dest_path else os.path.join(static_style,static_file.name+".css"),"wb")
                f.write(txt2.encode('utf-8'))
                f.close()        
        if typ=='U':
            t = Template(txt)
            txt2 = t.render(Context({'prj': prj} ))
            f = open_and_create_dir(dest_path,"wb")
            f.write(txt2.encode('utf-8'))
            f.close()        
        if static_file.type=='G':
            vue_init += txt
    component_elements = []
    
    if prj.custom_tags:
        #component_elements += [ pos.split('/')[0] + '/components/' + pos.split('/')[1] for pos in prj.custom_tags.replace('\n',';').replace('\r','').split(';') if pos and '/' in pos ]    
        component_elements += [ pos for pos in prj.custom_tags.replace('\n',';').replace('\r','').split(';') if pos and '.' in pos ]    
    component_elements += [ prj.name + "/components/" + pos.name + ".js" for pos in static_files if pos.type in ('R',) ]
    
    js_static_files = [ pos for pos in static_files if pos.type in ('J', 'P') ]
    css_static_files = [ pos for pos in static_files if pos.type in ('C', 'I') ]
    
    
    static_for_ext_apps = []
    
    if prj.ext_apps:
        prj_tab = []
        tab = prj.get_ext_apps()
        for pos in tab:
            if pos:
                x = pos.split('.')[0]
                if not x in prj_tab:
                    prj_tab.append(x)
        
        #for pos in prj.ext_apps.split(','):
        #    if pos:
        #        x = pos.split('.')[0]
        #        if not x in prj_tab:
        #            prj_tab.append(x)
        for pos in prj_tab:
            try:
                prj2 = models.SChAppSet.objects.get(name=pos)
            except:
                prj2 = None
            if prj2:
                static_files2 = prj2.schstatic_set.all()
                js_static_files2 = [ pos2 for pos2 in static_files2 if pos2.type in ('J', 'P') ]
                css_static_files2 = [ pos2 for pos2 in static_files2 if pos2.type in ('C', 'I') ]
                static_for_ext_apps.append((pos, js_static_files2, css_static_files2))
    
                if prj2.custom_tags:
                    component_elements += [ pos for pos in prj2.custom_tags.replace('\n',';').replace('\r','').split(';') if pos and '.' in pos ]    
                component_elements += [ prj2.name + "/components/" + pos.name + ".js" for pos in static_files2 if pos.type in ('R',) ]
    
    template_to_file(base_path, "desktop", "templates_src/template/desktop.ihtml",  {'prj': prj, 'js_static_files': set(js_static_files), 'css_static_files': set(css_static_files), 'static_for_ext_apps': static_for_ext_apps, 'component_elements': set(component_elements), 'vue_init': vue_init })
    
    
    #print(component_elements)
    #template_to_i_file(base_path, src_path+"templates_src/schbuilder/wzr/schweb.ihtml","templates_src/template/schweb.ihtml",  {'prj': prj, 'component_elements': component_elements })
    
    template_to_file(base_path, "schweb", "templates_src/template/schweb.ihtml",  {'prj': prj, 'component_elements': component_elements })
    
    consumers_tab = []
    for _app in apps:
        consumers = _app.schchannelconsumer_set.all()
        for consumer in consumers:
            consumers_tab.append((app.name+"/"+consumer.url+"/socket.io/", _app.name+".consumers."+consumer.name))
    
    for pos in prj.get_ext_apps():
        if pos:
            x = pos.split('.')
            tab1 = models.SChAppSet.objects.filter(name=x[0])
            for _prj in tab1:
                tab2 = _prj.schapp_set.filter(name=x[1])
                for _app in tab2:
                    consumers = _app.schchannelconsumer_set.all()
                    for consumer in consumers:
                        consumers_tab.append((_app.name+"/"+consumer.url+"/socket.io/", _app.name+".consumers."+consumer.name))
                
    template_to_file(base_path, "settings_app", "settings_app.py",  {'prj': prj, 'gmtime': gmt_str, 'offline_support': offline_support, 'consumers': consumers_tab })
    
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
            
    if prj.user_app_template and len(prj.user_app_template)>0:
        txt = prj.user_app_template
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
    
    if prj.encoded_zip:
        bcontent = base64.decodebytes(prj.encoded_zip.encode('utf-8'))
        bstream = io.BytesIO(bcontent)
        with zipfile.ZipFile(bstream, "r") as izip:
            izip.extractall(base_path)
    
    success = True
    
    if platform_name()!='Android' and prj.install_file:
        init_str = "[DEFAULT]\n"+prj.install_file
        config = configparser.ConfigParser(allow_no_value=True)
        config.read_string(init_str)
        pip_str = config['DEFAULT']['pip']
        if pip_str:
            applib_path  = os.path.join(base_path, "applib")
            if not os.path.exists(applib_path):
                os.mkdir(applib_path)
            packages = [ x.strip() for x in pip_str.split(' ') if x ]
            exit_code, output_tab, err_tab = py_run(['-m', 'pip', 'install', f'--target={applib_path}', '--upgrade', ] + packages)
            if output_tab:
                for pos in output_tab:
                    if pos:
                        object_list.append((datetime.datetime.now().time().isoformat(), "pip info", pos))
            if err_tab:
                for pos in err_tab:
                    if pos:
                        object_list.append((datetime.datetime.now().time().isoformat(), "pip error", pos))
                        success = False
    if success:    
        object_list.append((datetime.datetime.now().time().isoformat(), 'SUCCESS:', ""))    
    else:
        object_list.append((datetime.datetime.now().time().isoformat(), 'ERRORS:', ""))    
    
    (exit_code, output_tab, err_tab) = make(settings.DATA_PATH, base_path)
    if output_tab:
        for pos in output_tab:
            if pos:
                object_list.append((datetime.datetime.now().time().isoformat(), "compile info", pos))
    if err_tab:
        for pos in err_tab:
            if pos:
                object_list.append((datetime.datetime.now().time().isoformat(), "compile error", pos))
                success = False
        
    return { 'object_list': reversed(object_list) }
    






def prj_export(request, pk):
    
    prj_tab = []
    prj = models.SChAppSet.objects.get(id=pk)
    prj_tab.append(obj_to_array(prj,prj_attr))
    apps = prj.schapp_set.all()
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
    
        consumers = app.schchannelconsumer_set.all()
        consumers_array=[]
        for consumer in consumers:
            consumers_array.append(obj_to_array(consumer,consumer_attr))
    
        files = app.schfiles_set.all()
        files_array=[]
        for file in files:
            files_array.append(obj_to_array(file,files_attr))
    
        tmp = obj_to_array(app, app_attr)
        apps_array.append([tmp, tables_array, choices_array, views_array, templates_array, appmenus_array, forms_array, tasks_array, consumers_array, files_array])
    prj_tab.append(apps_array)
    
    statics = prj.schstatic_set.all()
    statics_array=[]
    for static in statics:
        statics_array.append(obj_to_array(static,static_attr))
    
    prj_tab.append(statics_array)
    
    ex_str = json.dumps(prj_tab, indent=4)
    return HttpResponse(ex_str, content_type="text/plain")
    

@dict_to_template('schbuilder/v_prj_import.html')




def prj_import(request):
    
    ex_str = request.POST['EDITOR']
    return prj_import_from_str(ex_str)
    






def manage(request, pk):
    
    prj = models.SChAppSet.objects.get(id=pk)
    base_path = os.path.join(settings.PRJ_PATH, prj.name)
    src_path = os.path.join(settings.PRJ_PATH, "schdevtools") 
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
    
        file_name = settings.PRJ_PATH + ("/schdevtools/templates_src/schbuilder/wzr/new_generic_%s_template.ihtml" % template_suffix)
    
        f = open(file_name, "rt")
        template.template_code = f.read()
        f.close()
        template.save()
        id = template.id
    else:
        id = templates[0].id
    
    new_url = make_href("/schbuilder/table/SChTemplate/%s/template_code/py/editor/" % str(id))
    
    return HttpResponseRedirect(new_url)
    
    






def edit(request):
    
    return TemplateView.as_view(template_name='schbuilder/import_form.html')(request)
    






def template_edit2(request, pk):
    
    form = models.SChForm.objects.get(id=pk)
    templates = models.SChTemplate.objects.filter(parent=form.parent).filter(name='Form'+form.name)
    if len(templates)==0:
        template=models.SChTemplate(parent=form.parent, name='Form'+form.name)
    
        file_name = settings.PRJ_PATH + "/schdevtools/templates_src/schbuilder/wzr/new_generic_form_template.ihtml"
        f = open(file_name, "rt")
        template.template_code = f.read()
        f.close()
        template.save()
        id = template.id
    else:
        id = templates[0].id
            
    new_url = make_href("/schbuilder/table/SChTemplate/%s/template_code/py/editor/" % str(id))
    
    return HttpResponseRedirect(new_url)
    

@dict_to_template('schbuilder/v_installer.html')




def installer(request, pk):
    
    buf = []
    
    try:
        pki = int(pk)
        prj = models.SChAppSet.objects.get(id=pki)
        name = prj.name
    except:
        name = pk
    
    base_path = os.path.join(settings.PRJ_PATH, name)
    zip_path = os.path.join(settings.DATA_PATH, 'temp')
    
    
    buf.append("COMPILE TEMPLETE FILES:")
    
    (code, output, err) = py_run([os.path.join(base_path, 'manage.py'), 'compile_templates'])
    
    if output:
        for pos in output:
            buf.append(pos)
    
    if err:
        buf.append("ERRORS:")
        for pos in err:
            buf.append(pos)
    
    exclude=[".*\.pyc", ".*__pycache__.*"]
    zip = ZipWriter(os.path.join(zip_path, name+".ptig"), base_path, exclude=exclude)
    zip.toZip(base_path)
    
    buf.append("PACK PROGRAM FILES TO: " + zip_path + name + ".ptig")
    
    db_name = os.path.join(os.path.join(settings.DATA_PATH, name), name+".db")
    
    buf.append("ADDING DATABASE FILES")
    
    (code, output, err) = py_run([os.path.join(base_path, 'manage.py'), 'export_to_local_db'])
    
    buf.append("Export to local db:")
    if output:
        for pos in output:
            buf.append(pos)
    
    if err:
        buf.append("ERRORS:")
        for pos in err:
            buf.append(pos)
            
    zip.write(db_name, name_in_zip=name+".db")
    zip.close()
    
    buf.append("END")
    
    url = reverse('start')+'schbuilder/download_installer/'+name+'/'
    
    return { 'object_list': buf, 'name': name, 'url': url, 'tp': "SChAppSet" }
    
    






def restart_server(request):
    
    module = import_plugin("schbuilderlib.test1", "schdevtools")
    print(module.sum(2,2))
    
    import ctypes 
    restarted = False
    try:
        if platform.system() == "Linux":
            if platform.system() == "Linux":
                if type(request).__name__=="AsgiRequest":
                    os.kill(os.getpid(), signal.SIGINT)
                    restarted = True
                elif 'mod_wsgi.process_group' in request.environ:
                    if request.environ['mod_wsgi.process_group'] != '':
                        os.kill(os.getpid(), signal.SIGINT)
                        restarted = True
                else:
                    try:
                        import uwsgi
                        uwsgi.reload()
                        restarted = True
                    except:
                        pass
            else:
                try:
                    import uwsgi
                    uwsgi.reload()
                    restarted = True
                except:
                    pass
        else:
            ctypes.windll.libhttpd.ap_signal_parent(1)
            restarted = True
    except:
        pass
    
    script = "<script>jQuery('#ModalLabel').html('Restart');</script>"
    
    if restarted:
        return HttpResponse("<html>%s<body>Restarted</body></html>" % script)
    else:
        return HttpResponse("<html>%s<body>I can't restart server</body></html>" % script)
        
    






def template_edit3(request, pk):
    
    view = models.SChView.objects.get(id=pk)
    templates = models.SChTemplate.objects.filter(parent=view.parent).filter(name='v_'+view.name)
    if len(templates)==0:
        template=models.SChTemplate(parent=view.parent, name='v_'+view.name)
    
        file_name = settings.PRJ_PATH + "/schdevtools/templates_src/schbuilder/wzr/new_generic_form_template.ihtml"
        f = open(file_name, "rt")
        template.template_code = f.read()
        f.close()
        template.save()
        id = template.id
    else:
        id = templates[0].id
    new_url = make_href("/schbuilder/table/SChTemplate/%s/template_code/py/editor/" % str(id))
    return HttpResponseRedirect(new_url)
    






def update(request):
    
    #g = git.cmd.Git(settings.ROOT_PATH)
    #g.reset('--hard')
    #g.pull()
    
    return HttpResponse("GIT PULL", content_type="text/plain")
    
    

@dict_to_template('schbuilder/v_translate_sync.html')




def translate_sync(request, pk):
    
    locale_obj = models.SChLocale.objects.get(id=pk)
    prj = locale_obj.parent
    
    base_path = settings.PRJ_PATH
    
    app_path = os.path.join(base_path, prj.name)
    locale_path = os.path.join(app_path, 'locale')
    lang_path = os.path.join(locale_path, locale_obj.name)
    msg_path = os.path.join(lang_path, 'LC_MESSAGES')
    po_path = os.path.join(msg_path, 'django.po')
    
    if not os.path.exists(po_path):
        if not os.path.isdir(locale_path):
            os.mkdir(locale_path)
        if not os.path.isdir(lang_path):
            os.mkdir(lang_path)
        if not os.path.isdir(msg_path):
            os.mkdir(msg_path)
        
        po_init = """#\nmsgid ""\nmsgstr ""\n"Project-Id-Version: pytigon\\n"\n"Language: %s\\n"\n"MIME-Version: 1.0\\n"\n"Content-Type: text/plain; charset=UTF-8\\n"\n"Content-Transfer-Encoding: 8bit\\n"\n"""
        if locale_obj.name in locale.locale_alias:
            locale_str = locale.locale_alias[locale_obj.name].split('.')[0]
        else:
            locale_str = locale_obj.name
        
        po_init2 = po_init % locale_str
        with open(po_path, "wt") as f:
            f.write(po_init2)
        
    
    (code, output, err) = py_run([os.path.join(app_path, 'manage.py'), 'compile_templates'])
    locale_gen_internal(prj.id)
        
    po = polib.pofile(po_path)
    
    locale_obj.schtranslate_set.update(status='#')
    
    inserted = 0
    updated = 0
    save = False
    
    for entry in po:
        print(entry.msgid, entry.msgstr, entry.msgctxt)
        t = locale_obj.schtranslate_set.filter(description=entry.msgid)
        if len(t)>0:
            obj = t[0]
            updated += 1
            if obj.translation:
                entry.msgstr =  obj.translation
                save = True
        else:
            obj = models.SChTranslate()
            obj.description = entry.msgid
            obj.parent = locale_obj
            obj.translation = entry.msgstr
            inserted += 1    
        if obj.translation:
            obj.status = 'OK'
        else:
            obj.status = ''
        obj.save()
    
    if save:
        po.save(po_path)
    
    locale_gen_internal(prj.id)
    
    return { 'object_list': [[ updated, inserted ],] }
    
    

@dict_to_template('schbuilder/v_locale_gen.html')




def locale_gen(request, pk):
    
    ret = locale_gen_internal(pk)
    if ret:
        ret_str = 'OK'
    else:
        ret_str = 'Error'
    
    return { 'object_list': [[ ret_str ],] }
    






def download_installer(request, name):
    
    installer = os.path.join(os.path.join(settings.DATA_PATH, 'temp'), name+".ptig")
    if os.path.exists(installer):
        with open(installer, 'rb') as zip_file:
            response = HttpResponse(zip_file, content_type='application/force-download')
            response['Content-Disposition'] = 'attachment; filename="%s"' %  name+".ptig"
            return response
    return HttpResponse(_("No installer file to download"))
    


 
