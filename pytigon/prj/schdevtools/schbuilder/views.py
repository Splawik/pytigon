from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, reverse
from django import forms
from django.template.loader import render_to_string
from django.template import Context, Template
from django.template import RequestContext
from django.conf import settings
from django.views.generic import TemplateView

from pytigon_lib.schviews.form_fun import form_with_perms
from pytigon_lib.schviews.viewtools import (
    dict_to_template,
    dict_to_odf,
    dict_to_pdf,
    dict_to_json,
    dict_to_xml,
    dict_to_ooxml,
    dict_to_txt,
    dict_to_hdoc,
)
from pytigon_lib.schviews.viewtools import render_to_response
from pytigon_lib.schdjangoext.tools import make_href
from pytigon_lib.schdjangoext import formfields as ext_form_fields
from pytigon_lib.schviews import actions

from django.utils.translation import gettext_lazy as _

from . import models
import os
import sys
import datetime
from django.utils import timezone

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
import hashlib

from os import environ
import subprocess
import traceback


from django.db import transaction
from django.urls import reverse

from pytigon_lib.schviews.viewtools import change_pos, duplicate_row
import pytigon_lib.schindent.indent_style
from pytigon_lib.schindent.indent_tools import convert_js
from pytigon_lib.schdjangoext.django_ihtml import ihtml_to_html

from pytigon_lib.schfs.vfstools import ZipWriter, open_and_create_dir
from pytigon_lib.schtools.install import Ptig
from pytigon_lib.schtools.process import py_run
from pytigon_lib.schtools.platform_info import platform_name

from pytigon_lib.schtools.cc import import_plugin, make
from pytigon_lib.schdjangoext.python_style_template_loader import compile_template

from pytigon.ext_lib.pygettext import main as gtext

from pytigon.schserw.schsys.context_processors import sch_standard

from dulwich import porcelain
from dulwich.repo import Repo
from dulwich import index

try:
    import sass
except:
    sass = None

import pytigon.schserw.settings

from django_q.tasks import async_task, result
from pytigon_lib.schtasks.publish import publish

try:
    import black
except:
    black = None

_template = """
        [ gui_style | {{prj.gui_type}}({{prj.gui_elements}}) ]
        [ title  | {{prj.title}} ]
        [ start_page | {{start_page}} ]
        [ plugins | {{prj.plugins}} ]
"""

prj_attr = sorted(
    [
        field.name
        for field in models.SChAppSet._meta.fields
        if field.name not in ("parent", "id")
    ]
)
app_attr = sorted(
    [
        field.name
        for field in models.SChApp._meta.fields
        if field.name not in ("parent", "id")
    ]
)
choice_attr = sorted(
    [
        field.name
        for field in models.SChChoice._meta.fields
        if field.name not in ("parent", "id")
    ]
)
choice_item_attr = sorted(
    [
        field.name
        for field in models.SChChoiceItem._meta.fields
        if field.name not in ("parent", "id")
    ]
)
table_attr = sorted(
    [
        field.name
        for field in models.SChTable._meta.fields
        if field.name not in ("parent", "id")
    ]
)
field_attr = sorted(
    [
        field.name
        for field in models.SChField._meta.fields
        if field.name not in ("parent", "id")
    ]
)
view_attr = sorted(
    [
        field.name
        for field in models.SChView._meta.fields
        if field.name not in ("parent", "id")
    ]
)
static_attr = sorted(
    [
        field.name
        for field in models.SChStatic._meta.fields
        if field.name not in ("parent", "id")
    ]
)
template_attr = sorted(
    [
        field.name
        for field in models.SChTemplate._meta.fields
        if field.name not in ("parent", "id")
    ]
)
appmenu_attr = sorted(
    [
        field.name
        for field in models.SChAppMenu._meta.fields
        if field.name not in ("parent", "id")
    ]
)
form_attr = sorted(
    [
        field.name
        for field in models.SChForm._meta.fields
        if field.name not in ("parent", "id")
    ]
)
formfield_attr = sorted(
    [
        field.name
        for field in models.SChFormField._meta.fields
        if field.name not in ("parent", "id")
    ]
)
task_attr = sorted(
    [
        field.name
        for field in models.SChTask._meta.fields
        if field.name not in ("parent", "id")
    ]
)
files_attr = sorted(
    [
        field.name
        for field in models.SChFiles._meta.fields
        if field.name not in ("parent", "id")
    ]
)
consumer_attr = sorted(
    [
        field.name
        for field in models.SChChannelConsumer._meta.fields
        if field.name not in ("parent", "id")
    ]
)


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


def change_tab_pos(request, app, tab, pk, forward=True, field=None, callback_fun=None):
    return change_pos(request, app, tab, pk, forward, field, callback_fun_tab)


def change_menu_pos(request, app, tab, pk, forward=True, field=None, callback_fun=None):
    return change_pos(request, app, tab, pk, forward, field)


def change_pos_form_field(
    request, app, tab, pk, forward=True, field=None, callback_fun=None
):
    return change_pos(request, app, tab, pk, forward, field)


def template_to_file(base_path, template, file_name, context):
    txt = render_to_string("schbuilder/wzr/%s.html" % template, context)
    if black and file_name.endswith(".py"):
        try:
            txt2 = black.format_file_contents(txt, fast=True, mode=black.mode.Mode())
            if txt2:
                txt = txt2
        except:
            pass
    f = codecs.open(base_path + "/" + file_name, "w", encoding="utf-8")
    f.write(txt)
    f.close()


def template_to_i_file(base_path, template, file_name, context):
    f = open(template, "rt")
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
        if type(txt_in) == str:
            txt2 = txt_in.replace("$$" + "$", txt)
        else:
            txt2 = txt_in.decode("utf-8").replace("$$" + "$", txt)
    except:
        import traceback
        import sys

        print(sys.exc_info()[0])
        print(traceback.print_exc())

    f = open(base_path + "/" + file_name, "wb")
    if type(txt_in) == str:
        f.write(txt2.encode("utf-8"))
    else:
        f.write(txt2.encode("utf-8"))
    f.close()


def str_to_file(base_path, buf, file_name):
    f = open(base_path + "/" + file_name, "wb")
    if buf:
        if type(buf) == str:
            f.write(buf.encode("utf-8"))
        else:
            f.write(buf)
    f.close()


def obj_to_dict(obj, attrs):
    ret = {}
    for attr in attrs:
        ret[attr.strip()] = getattr(obj, attr.strip())
    return ret


def array_dict(array, attrs):
    return array


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

    id = get_process_manager().put(request, "python-shell", "python3", "-i")
    new_url = make_href("../../schsys/thread/%d/edit/" % id)
    return HttpResponseRedirect(new_url)


def run_python_shell_task_base(request, base_path, prj_name):
    from pytigon_lib.schtasks.base_task import get_process_manager

    command = "from app_sets.%s.manage import *" % prj_name
    pconsole = settings.PYTHON_CONSOLE.split(" ")
    pconsole[0] = ">>>" + pconsole[0]
    pconsole.append("-i")
    pconsole.append("-c")
    pconsole.append(command)
    param = [
        "python-shell",
    ] + pconsole
    id = get_process_manager().put(request, *param)
    return id


def run_python_shell_task(request, base_path, prj_name):
    id = run_python_shell_task_base(request, base_path, prj_name)
    new_url = make_href("../../schsys/thread/%d/edit/" % id)
    return HttpResponseRedirect(new_url)


def make_messages(src_path, path, name, outpath=None, ext_locales=[]):
    backup_argv = sys.argv

    sys.argv = [None, "-a", "-d", name, "-p", path]

    for root, dirs, files in os.walk(src_path):
        for f in files:
            if f.endswith(".py"):
                p = os.path.join(root, f)
                sys.argv.append(p)
    gtext()

    wzr_filename = os.path.join(path, name + ".pot")
    for pos in os.scandir(path):
        if pos.is_dir():
            lang = pos.name
            ftmp = os.path.join(path, lang)
            if outpath:
                ftmp = os.path.join(ftmp, outpath)
            filename = os.path.join(ftmp, name + ".po")
            old_filename = filename.replace(".po", ".bak")
            mo_filename = filename.replace(".po", ".mo")
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

            # for pos2 in ext_locales:
            #    ftmp = os.path.join(pos2[1],lang)
            #    if outpath:
            #        ftmp = os.path.join(ftmp, outpath)
            #    ext_filename = os.path.join(ftmp, name+'.po')
            #    if os.path.exists(ext_filename):
            #        ext_po = polib.pofile(ext_filename)
            #        ext_po = polib.pofile(ext_filename)
            #        po.merge(ext_po)

            po.save(filename)
            po.save_as_mofile(mo_filename)

    sys.argv = backup_argv


def locale_gen_internal(pk):
    prj = models.SChAppSet.objects.get(id=pk)

    base_path = settings.PRJ_PATH_ALT
    app_path = os.path.join(base_path, prj.name)
    if not os.path.exists(app_path):
        base_path = settings.PRJ_PATH
        app_path = os.path.join(base_path, prj.name)

    locale_path = os.path.join(app_path, "locale")

    ext_apps = []
    ext_locales = []
    if prj.ext_apps:
        for pos in prj.ext_apps.replace("\n", ",").replace(";", ",").split(","):
            pos2 = pos.split(".")[0]
            if pos2 and not pos2 in ext_apps:
                ext_apps.append(pos2)
                app_path2 = os.path.join(base_path, pos2)
                locale_path2 = os.path.join(app_path2, "locale")
                ext_locales.append([app_path2, locale_path2])
    make_messages(app_path, locale_path, "django", "LC_MESSAGES", ext_locales)

    template_path = os.path.join(app_path, "templates")

    to_remove = []
    for root, dirs, files in os.walk(template_path):
        for f in files:
            if f.endswith(".html"):
                p = os.path.join(root, f)
                to_remove.append(p)

    for pos in to_remove:
        os.unlink(pos)

    return {
        "object_list": [
            ["OK"],
        ]
    }


def prj_import_from_str(s, backup_old=False, backup_this=False):
    object_list = []
    prj = json.loads(s)
    with transaction.atomic():
        prj_instence = models.SChAppSet(**prj[0])
        prj_instence.main_view = True
        prj_instence.save()

        apps_array = prj[1]
        for app_pos in apps_array:
            app = models.SChApp(**app_pos[0])
            app.parent = prj_instence
            app.save()

            tables_array = app_pos[1]
            for table_pos in tables_array:
                table = models.SChTable(**table_pos[0])
                table.parent = app
                table.save()

                fields_array = table_pos[1]
                for field_pos in fields_array:
                    field = models.SChField(**field_pos)
                    field.parent = table
                    field.save()

            choices_array = app_pos[2]
            for choice_pos in choices_array:
                choice = models.SChChoice(**choice_pos[0])
                choice.parent = app
                choice.save()

                choice_item_array = choice_pos[1]
                for item_pos in choice_item_array:
                    choice_item = models.SChChoiceItem(**item_pos)
                    choice_item.parent = choice
                    choice_item.save()

            views_array = app_pos[3]
            for view_pos in views_array:
                view = models.SChView(**view_pos)
                view.parent = app
                view.save()

            templates_array = app_pos[4]
            for template_pos in templates_array:
                template = models.SChTemplate(**template_pos)
                template.parent = app
                template.save()

            appmenus = app.schappmenu_set.all()
            appmenus_array = app_pos[5]
            for appmenu_pos in appmenus_array:
                appmenu = models.SChAppMenu(**appmenu_pos)
                appmenu.parent = app
                appmenu.save()

            forms_array = app_pos[6]
            for form_pos in forms_array:
                form = models.SChForm(**form_pos[0])
                form.parent = app
                form.save()

                formfields_array = form_pos[1]
                for field_pos in formfields_array:
                    field = models.SChFormField(**field_pos)
                    field.parent = form
                    field.save()

            tasks_array = app_pos[7]
            for task_pos in tasks_array:
                task = models.SChTask(**task_pos)
                task.parent = app
                task.save()

            consumers_array = app_pos[8]
            for consumer_pos in consumers_array:
                consumer = models.SChChannelConsumer(**consumer_pos)
                consumer.parent = app
                consumer.save()

            files_array = app_pos[9]
            for file_pos in files_array:
                f = models.SChFiles(**file_pos)
                f.parent = app
                f.save()

        statics_array = prj[2]
        for static in statics_array:
            s = models.SChStatic(**static)
            s.parent = prj_instence
            s.save()

    if backup_old:
        projects = models.SChAppSet.objects.filter(
            name=prj_instence.name, main_view=True
        )
        if len(projects) > 0:
            for prj in projects:
                if prj.id != prj_instence.id:
                    if prj.version == "latest":
                        prj.version = version = "v" + datetime.date.today().isoformat()
                    prj.main_view = False
                    prj.save()
                    object_list.append(
                        (
                            datetime.datetime.now(),
                            "prj has been archived:",
                            prj.name + ":" + prj.version,
                        )
                    )
    elif backup_this:
        prj_instence.main_view = False
        if prj_instence.version == "latest":
            prj_instence.version = "v" + datetime.date.today().isoformat()
        prj_instence.save()

    object_list.append(
        (
            datetime.datetime.now(),
            "prj imported from file",
            prj_instence.name + ":" + prj_instence.version,
        )
    )
    return {"object_list": object_list, "prj_instance": prj_instence}


def prj_export_to_str(pk):
    prj_tab = []
    prj = models.SChAppSet.objects.get(id=pk)
    prj_tab.append(obj_to_dict(prj, prj_attr))
    apps = prj.schapp_set.all()
    apps_array = []
    for app in apps:
        tables = app.schtable_set.all()
        tables_array = []
        for table in tables:
            tmp = obj_to_dict(table, table_attr)
            fields = table.schfield_set.all()
            fields_array = []
            for field in fields:
                fields_array.append(obj_to_dict(field, field_attr))
            tables_array.append([tmp, fields_array])

        choices = app.schchoice_set.all()
        choices_array = []
        for choice in choices:
            tmp = obj_to_dict(choice, choice_attr)
            choice_items = choice.schchoiceitem_set.all()
            choice_items_array = []
            for item in choice_items:
                choice_items_array.append(obj_to_dict(item, choice_item_attr))
            choices_array.append([tmp, choice_items_array])

        views = app.schview_set.all()
        views_array = []
        for view in views:
            views_array.append(obj_to_dict(view, view_attr))

        templates = app.schtemplate_set.all()
        templates_array = []
        for template in templates:
            templates_array.append(obj_to_dict(template, template_attr))

        appmenus = app.schappmenu_set.all()
        appmenus_array = []
        for appmenu in appmenus:
            appmenus_array.append(obj_to_dict(appmenu, appmenu_attr))

        forms = app.schform_set.all()
        forms_array = []
        for form in forms:
            tmp = obj_to_dict(form, form_attr)
            fields = form.schformfield_set.all()
            fields_array = []
            for field in fields:
                fields_array.append(obj_to_dict(field, formfield_attr))
            forms_array.append([tmp, fields_array])

        tasks = app.schtask_set.all()
        tasks_array = []
        for task in tasks:
            tasks_array.append(obj_to_dict(task, task_attr))

        consumers = app.schchannelconsumer_set.all()
        consumers_array = []
        for consumer in consumers:
            consumers_array.append(obj_to_dict(consumer, consumer_attr))

        files = app.schfiles_set.all()
        files_array = []
        for file in files:
            files_array.append(obj_to_dict(file, files_attr))

        tmp = obj_to_dict(app, app_attr)
        apps_array.append(
            [
                tmp,
                tables_array,
                choices_array,
                views_array,
                templates_array,
                appmenus_array,
                forms_array,
                tasks_array,
                consumers_array,
                files_array,
            ]
        )
    prj_tab.append(apps_array)

    statics = prj.schstatic_set.all()
    statics_array = []
    for static in statics:
        statics_array.append(obj_to_dict(static, static_attr))

    prj_tab.append(statics_array)

    return json.dumps(prj_tab, indent=4)


def build_prj(pk):
    prj = models.SChAppSet.objects.get(id=pk)

    if hasattr(pytigon.schserw.settings, "_PRJ_PATH_ALT"):
        base_path = os.path.join(pytigon.schserw.settings._PRJ_PATH_ALT, prj.name)
    else:
        if os.path.exists(os.path.join(environ["START_PATH"], "prj")):
            base_path = os.path.join(environ["START_PATH"], "prj", prj.name)
        else:
            base_path = os.path.join(settings.PRJ_PATH_ALT, prj.name)

    object_list = []
    gmt = time.gmtime()
    gmt_str = "%04d.%02d.%02d %02d:%02d:%02d" % (
        gmt[0],
        gmt[1],
        gmt[2],
        gmt[3],
        gmt[4],
        gmt[5],
    )

    os.makedirs(base_path + "/templates/theme", exist_ok=True)
    os.makedirs(base_path + "/templates_src/theme", exist_ok=True)

    apps = prj.schapp_set.all()

    with open(os.path.join(base_path, "README.md"), "wt") as f:
        if prj.readme_file:
            f.write(prj.readme_file)
    with open(os.path.join(base_path, "LICENSE"), "wt") as f:
        if prj.license_file:
            f.write(prj.license_file)
    with open(os.path.join(base_path, "install.ini"), "wt") as f:
        f.write("[DEFAULT]\nPRJ_NAME=%s\n" % prj.name)
        f.write("PRJ_TITLE=%s\n" % prj.title)
        f.write("GEN_TIME='%s'\n" % gmt_str)
        if prj.install_file:
            f.write(prj.install_file)

    template_to_file(base_path, "manage", "manage.py", {"prj": prj})
    template_to_file(base_path, "init", "__init__.py", {"prj": prj})
    template_to_file(
        base_path,
        "wsgi",
        "wsgi.py",
        {"prj": prj, "base_path": base_path.replace("\\", "/")},
    )
    template_to_file(
        base_path,
        "asgi",
        "asgi.py",
        {"prj": prj, "base_path": base_path.replace("\\", "/")},
    )

    app_names = []
    for app in apps:
        object_list.append((datetime.datetime.now(), "create app:", app.name))
        os.makedirs(base_path + "/" + app.name, exist_ok=True)
        os.makedirs(base_path + "/templates_src/" + app.name, exist_ok=True)
        os.makedirs(base_path + "/templates/" + app.name, exist_ok=True)

        app_names.append(app.name)

        tables = app.schtable_set.all()
        choices = app.schchoice_set.all()
        templates = app.schtemplate_set.all()

        is_tree_table = False
        gfields = []
        for table in tables:
            object_list.append((datetime.datetime.now(), "create tab:", table.name))
            table.tree_table = 0
            for field in table.schfield_set.filter(
                type__in=[
                    "PtigForeignKey",
                    "PtigManyToManyField",
                    "PtigHiddenForeignKey",
                    "PtigTreeForeignKey",
                    "PtigHiddenTreeForeignKey",
                ]
            ):
                if field.type in ("PtigTreeForeignKey", "PtigHiddenTreeForeignKey"):
                    is_tree_table = True
                    if (
                        table.base_table in (None, "", "models.Model")
                        and not table.proxy_model
                    ):
                        table.base_table = "TreeModel"
                        table.tree_tab = 1
                    else:
                        table.tree_tab = 2
                gfields.append(field)

        template_to_file(
            base_path,
            "models",
            app.name + "/models.py",
            {
                "tables": tables,
                "app": app,
                "prj": prj,
                "choices": choices,
                "is_tree_table": is_tree_table,
            },
        )

        views = app.schview_set.all()
        forms = app.schform_set.all()
        tasks = app.schtask_set.all()
        consumers = app.schchannelconsumer_set.all()
        template_to_file(
            base_path,
            "views",
            app.name + "/views.py",
            {"views": views, "forms": forms, "app": app},
        )
        template_to_file(
            base_path,
            "urls",
            app.name + "/urls.py",
            {
                "views": views,
                "templates": templates,
                "tables": tables,
                "forms": forms,
                "app": app,
                "gfields": gfields,
            },
        )
        template_to_file(
            base_path, "tasks", app.name + "/tasks.py", {"tasks": tasks, "app": app}
        )
        template_to_file(
            base_path,
            "consumers",
            app.name + "/consumers.py",
            {"consumers": consumers, "app": app},
        )

        for template in templates:
            if "." in template.name and not ".ihtml" in template.name:
                str_to_file(
                    base_path,
                    template.template_code,
                    "templates/" + app.name + "/" + template.name,
                )
            else:
                str_to_file(
                    base_path,
                    template.template_code,
                    "templates_src/"
                    + app.name
                    + "/"
                    + template.name.lower().replace(" ", "_")
                    + ".ihtml",
                )

        appmenus = list(app.schappmenu_set.all())

        if app.user_param:
            user_param = str(
                dict(
                    [
                        pos.split("=")
                        for pos in app.user_param.split("\n")
                        if pos and "=" in pos
                    ]
                )
            )
        else:
            user_param = "{}"

        template_to_file(
            base_path,
            "app_init",
            app.name + "/__init__.py",
            {"appmenus": appmenus, "app": app, "user_param": user_param},
        )

        for file_obj in app.schfiles_set.all():
            if file_obj.file_type == "f":
                file_name = (
                    base_path
                    + "/"
                    + app.name
                    + "/templatetags/"
                    + file_obj.name
                    + ".py"
                )
            elif file_obj.file_type == "t":
                file_name = (
                    base_path
                    + "/"
                    + app.name
                    + "/templatetags/"
                    + file_obj.name
                    + ".py"
                )
            elif file_obj.file_type == "c":
                init_file = os.path.join(base_path, app.name, "applib", "__init__.py")
                if not os.path.exists(init_file):
                    f = open_and_create_dir(init_file, "wb")
                    f.close()
                file_name = base_path + "/" + app.name + "/" + file_obj.name
            elif file_obj.file_type == "m":
                f = open_and_create_dir(
                    base_path + "/" + app.name + "/management/__init__.py", "wb"
                )
                f.close()
                f = open_and_create_dir(
                    base_path + "/" + app.name + "/management/commands/__init__.py",
                    "wb",
                )
                f.close()
                file_name = (
                    base_path + "/" + app.name + "/management/commands/" + file_obj.name
                )
            elif file_obj.file_type == "p":
                if "/" in file_obj.name:
                    x = file_obj.name.split("/")
                    plugin_name = x[0]
                    file_name = x[1]
                else:
                    plugin_name = file_obj.name
                    file_name = "__init__"
                file_name = (
                    base_path
                    + "/plugins/"
                    + app.name
                    + "/"
                    + plugin_name
                    + "/"
                    + file_name
                    + ".py"
                )
            elif file_obj.file_type == "i":
                if "/" in file_obj.name:
                    x = file_obj.name.split("/")
                    plugin_name = x[0]
                    file_name = x[1]
                else:
                    plugin_name = file_obj.name
                    file_name = "index"
                file_name = (
                    base_path
                    + "/plugins/"
                    + app.name
                    + "/"
                    + plugin_name
                    + "/"
                    + file_name
                    + ".html"
                )
                content = ihtml_to_html(None, file_obj.content)
                f = open_and_create_dir(file_name, "wb")
                f.write(content.encode("utf-8"))
                f.close()
                file_name = None
            elif file_obj.file_type == "T":
                template_name = file_obj.name
                file_name = (
                    base_path
                    + "/static/"
                    + app.name
                    + "/views/"
                    + template_name
                    + ".html"
                )
                content = ihtml_to_html(None, file_obj.content)
                f = open_and_create_dir(file_name, "wb")
                f.write(content.encode("utf-8"))
                f.close()
                file_name = None
            elif file_obj.file_type == "j":
                template_name = file_obj.name
                file_name = (
                    base_path
                    + "/static/"
                    + app.name
                    + "/views/"
                    + template_name
                    + ".js"
                )
                try:
                    codejs = pytigon_lib.schindent.indent_style.py_to_js(
                        file_obj.content, None
                    )
                    codejs = codejs.replace(
                        "./org.transcrypt.__runtime__.js",
                        "../../pytigon_js/org.transcrypt.__runtime__.js",
                    ).replace("__globals__,", "")
                except:
                    codejs = ""
                f = open_and_create_dir(file_name, "wb")
                f.write(codejs.encode("utf-8"))
                f.close()
                file_name = None
            elif file_obj.file_type == "l":
                init_file = os.path.join(base_path, app.name, "applib", "__init__.py")
                if not os.path.exists(init_file):
                    f = open_and_create_dir(init_file, "wb")
                    f.close()
                file_name = os.path.join(base_path, app.name, "applib", file_obj.name)
                if not file_name.endswith(".py"):
                    file_name += ".py"
            elif file_obj.file_type == "s":
                file_name = base_path + "/" + app.name + "/schema.py"
            elif file_obj.file_type == "r":
                file_name = base_path + "/" + app.name + "/rest_api.py"
            else:
                file_name = None

            if file_name:
                f = open_and_create_dir(file_name, "wb")
                if type(file_obj.content) == str:
                    f.write(file_obj.content.encode("utf-8"))
                else:
                    f.write(file_obj.content)
                f.close()

    template_to_file(base_path, "apps", "apps.py", {"prj": prj, "app_names": app_names})

    static_files = prj.schstatic_set.all()

    static_root = os.path.join(base_path, "static", prj.name)
    static_scripts = os.path.join(static_root, "js")
    static_style = os.path.join(static_root, "css")
    static_components = os.path.join(static_root, "components")

    offline_support = False

    for static_file in static_files:
        txt = static_file.code
        typ = static_file.type
        dest_path = None
        if static_file.name == "sw.js":
            offline_support = True

        if static_file.type == "U":
            dest_path = os.path.join(static_root, static_file.name)
            if ".pyj" in static_file.name:
                dest_path = os.path.join(
                    static_root, static_file.name.replace(".pyj", ".js")
                )
                typ = "P"
            elif ".sass" in static_file.name:
                dest_path = os.path.join(
                    static_root, static_file.name.replace(".sass", ".css")
                )
                typ = "I"
            elif ".webc" in static_file.name:
                dest_path = os.path.join(
                    static_root, static_file.name.replace(".webc", ".js")
                )
                typ = "R"

        if typ == "C":
            t = Template(txt)
            txt2 = t.render(Context({"prj": prj}))
            f = open_and_create_dir(
                os.path.join(static_style, static_file.name + ".css"), "wb"
            )
            f.write(txt2.encode("utf-8"))
            f.close()
        if typ == "J":
            t = Template(txt)
            txt2 = t.render(Context({"prj": prj}))
            f = open_and_create_dir(
                os.path.join(static_scripts, static_file.name + ".js"), "wb"
            )
            f.write(txt2.encode("utf-8"))
            f.close()
        if typ == "P":
            t = Template(txt)
            txt2 = t.render(Context({"prj": prj}))
            try:
                codejs = pytigon_lib.schindent.indent_style.py_to_js(txt2, None)
                codejs = codejs.replace(
                    "./org.transcrypt.__runtime__.js",
                    "../../pytigon_js/org.transcrypt.__runtime__.js",
                ).replace("__globals__,", "")
            except:
                codejs = ""
            print(
                dest_path
                if dest_path
                else os.path.join(static_scripts, static_file.name + ".js")
            )
            f = open_and_create_dir(
                (
                    dest_path
                    if dest_path
                    else os.path.join(static_scripts, static_file.name + ".js")
                ),
                "wb",
            )
            f.write(codejs.encode("utf-8"))
            f.close()
        if typ == "R":
            try:
                codejs = pytigon_lib.schindent.indent_style.py_to_js(txt, None)
                codejs = codejs.replace(
                    "./org.transcrypt.__runtime__.js",
                    "../../pytigon_js/org.transcrypt.__runtime__.js",
                ).replace("__globals__,", "")
            except:
                codejs = ""
            print(
                dest_path
                if dest_path
                else os.path.join(static_components, static_file.name + ".js")
            )
            f = open_and_create_dir(
                (
                    dest_path
                    if dest_path
                    else os.path.join(static_components, static_file.name + ".js")
                ),
                "wb",
            )
            f.write(codejs.encode("utf-8"))
            f.close()
        if typ == "I":
            if sass:
                buf = sass.compile(
                    string=txt,
                    indented=True,
                )
                t = Template(buf)
                txt2 = t.render(Context({"prj": prj}))
                f = open_and_create_dir(
                    (
                        dest_path
                        if dest_path
                        else os.path.join(static_style, static_file.name + ".css")
                    ),
                    "wb",
                )
                f.write(txt2.encode("utf-8"))
                f.close()
        if typ == "U":
            t = Template(txt)
            txt2 = t.render(Context({"prj": prj}))
            f = open_and_create_dir(dest_path, "wb")
            f.write(txt2.encode("utf-8"))
            f.close()
        if typ == "O":
            p = os.path.join(base_path, static_file.name)
            dname = os.path.dirname(p)
            os.makedirs(dname, exist_ok=True)
            with open(p, "wt", encoding="utf-8") as f:
                f.write(txt)

    component_elements = []

    if prj.custom_tags:
        component_elements += [
            pos
            for pos in prj.custom_tags.replace("\n", ";").replace("\r", "").split(";")
            if pos and "." in pos
        ]
    component_elements += [
        prj.name + "/components/" + pos.name + ".js"
        for pos in static_files
        if pos.type in ("R",)
    ]

    js_static_files = [pos for pos in static_files if pos.type in ("J", "P")]
    css_static_files = [pos for pos in static_files if pos.type in ("C", "I")]

    static_for_ext_apps = []

    if prj.ext_apps:
        prj_tab = []
        tab = prj.get_ext_pytigon_apps()
        for pos in tab:
            if pos:
                x = pos.split(".")[0]
                if not x in prj_tab:
                    prj_tab.append(x)

        for pos in prj_tab:
            try:
                prj2 = models.SChAppSet.objects.get(name=pos)
            except:
                prj2 = None
            if prj2:
                static_files2 = prj2.schstatic_set.all()
                js_static_files2 = [
                    pos2 for pos2 in static_files2 if pos2.type in ("J", "P")
                ]
                css_static_files2 = [
                    pos2 for pos2 in static_files2 if pos2.type in ("C", "I")
                ]
                static_for_ext_apps.append((pos, js_static_files2, css_static_files2))

                if prj2.custom_tags:
                    for pos in (
                        prj2.custom_tags.replace("\n", ";").replace("\r", "").split(";")
                    ):
                        if pos and "." in pos and not pos in component_elements:
                            component_elements.append(pos)
                component_elements += [
                    prj2.name + "/components/" + pos.name + ".js"
                    for pos in static_files2
                    if pos.type in ("R",)
                ]

    template_to_file(
        base_path,
        "theme_base",
        "templates_src/theme_base.ihtml",
        {
            "prj": prj,
            "js_static_files": sorted(set(js_static_files)),
            "css_static_files": sorted(set(css_static_files)),
            "static_for_ext_apps": static_for_ext_apps,
            "component_elements": sorted(set(component_elements)),
            "initial_state": prj.components_initial_state,
        },
    )
    for field, file_path in (
        (prj.template_desktop, "theme/desktop.ihtml"),
        (prj.template_smartfon, "theme/smartfon.ihtml"),
        (prj.template_tablet, "theme/tablet.ihtml"),
        (prj.template_schweb, "theme/schweb.ihtml"),
        (prj.template_theme, "theme.ihtml"),
    ):
        if field:
            _file_name = os.path.join(
                base_path, "templates_src", *(file_path.split("/"))
            )
            with open(_file_name, "wt") as f:
                f.write(field)

    consumers_dict = {}
    for _app in apps:
        consumers = _app.schchannelconsumer_set.all()
        for consumer in consumers:
            consumers_dict[_app.name + "/" + consumer.url + "/channel/"] = (
                _app.name + ".consumers." + consumer.name
            )

    for pos in prj.get_ext_pytigon_apps():
        if pos:
            x = pos.split(".")
            tab1 = models.SChAppSet.objects.filter(name=x[0])
            for _prj in tab1:
                tab2 = _prj.schapp_set.filter(name=x[1])
                for _app in tab2:
                    consumers = _app.schchannelconsumer_set.all()
                    for consumer in consumers:
                        consumers_dict[_app.name + "/" + consumer.url + "/channel/"] = (
                            _app.name + ".consumers." + consumer.name
                        )

    template_to_file(
        base_path,
        "settings_app",
        "settings_app.py",
        {
            "prj": prj,
            "gmtime": gmt_str,
            "offline_support": offline_support,
            "consumers": consumers_dict.items(),
        },
    )

    base_path_src = base_path + "/src"

    if os.path.exists(base_path_src):
        copy_files_and_dirs(base_path_src, base_path)

    file_name = None
    file_content = []
    file_append = -1

    def output(file_name, file_append, file_content):
        os.makedirs(os.path.dirname(os.path.join(base_path, file_name)), exist_ok=True)
        if file_append == -1:
            f = open(os.path.join(base_path, file_name), "wb")
            f.write(("\n".join(file_content)).encode("utf-8"))
            f.close()
        elif file_append == -2:
            f = open(os.path.join(base_path, file_name), "ab")
            f.write(("\n".join(file_content)).encode("utf-8"))
            f.close()
        else:
            f = open(os.path.join(base_path, file_name), "rb")
            txt = f.read().decode("utf-8").split("\n")
            f.close()
            try:
                file_append_pos = int(file_append)
            except:
                if file_append.startswith("|"):
                    f = file_append[1:]
                    delta = 0
                elif file_append.endswith("|"):
                    f = file_append[:-1]
                    delta = 1
                else:
                    f = file_append
                    delta = 1

                file_append_pos = delta
                for buf in txt:
                    if f in buf:
                        break
                    file_append_pos += 1

            if file_append_pos < len(txt):
                txt = txt[:file_append_pos] + file_content + txt[file_append_pos:]
            else:
                txt = txt + file_content
            f = open(os.path.join(base_path, file_name), "wb")
            f.write(("\n".join(txt)).encode("utf-8"))
            f.close()

    if prj.user_app_template and len(prj.user_app_template) > 0:
        txt = prj.user_app_template
        tab = txt.split("\n")
        for row in tab:
            if row.startswith("###"):
                if file_name and len(file_content) > 0:
                    output(file_name, file_append, file_content)
                file_content = []
                file_name = row[3:]
                if file_name.startswith(">"):
                    file_name = file_name[1:].strip()
                    file_append = -2
                elif file_name.startswith("<") and ">" in file_name:
                    f = file_name[1:].split(">")
                    file_name = f[1].strip()
                    file_append = f[0]
                else:
                    file_name = file_name.strip()
                    file_append = -1
            else:
                file_content.append(row)

        if file_name and len(file_content) > 0:
            output(file_name, file_append, file_content)

    if prj.encoded_zip:
        bcontent = base64.decodebytes(prj.encoded_zip.encode("utf-8"))
        bstream = io.BytesIO(bcontent)
        with zipfile.ZipFile(bstream, "r") as izip:
            izip.extractall(base_path)

    (exit_code, output_tab, err_tab) = make(settings.DATA_PATH, base_path, prj.name)
    if output_tab:
        for pos in output_tab:
            if pos:
                object_list.append((datetime.datetime.now(), "compile info", pos))
    if err_tab:
        for pos in err_tab:
            if pos:
                object_list.append((datetime.datetime.now(), "compile error", pos))
                success = False

    return object_list


PFORM = form_with_perms("schbuilder")


class Installer(forms.Form):
    name = forms.ChoiceField(
        label=_("Application package name"), required=True, choices=models.apppack
    )

    def process(self, request, queryset=None):

        name = self.cleaned_data["name"]
        return installer(request, name)


def view_installer(request, *argi, **argv):
    return PFORM(request, Installer, "schbuilder/forminstaller.html", {})


class Install(forms.Form):
    install_file = forms.FileField(
        label=_("Install file (*.ptig)"),
        required=False,
    )

    def process(self, request, queryset=None):

        install_file = request.FILES["install_file"]
        name = install_file.name.split(".")[0].split("-")[0]

        ptig = Ptig(install_file.file)
        # zip_file = zipfile.ZipFile(install_file.file)
        object_list = ptig.extract_ptig()

        # extract_to = os.path.join(settings.PRJ_PATH, name)
        # (ret_code, output, err) = py_run(
        #    [os.path.join(extract_to, "manage.py"), "post_installation"]
        # )

        # if hasattr(pytigon.schserw.settings, "_PRJ_PATH_ALT"):
        #    base_path = pytigon.schserw.settings._PRJ_PATH_ALT
        # else:
        #    base_path = settings.PRJ_PATH_ALT

        prj_file_path = os.path.join(ptig.extract_to, name, name + ".prj")

        if os.path.exists(prj_file_path):
            with open(prj_file_path, "rt") as f:
                content = f.read()
                x = prj_import_from_str(content, backup_old=True)
                object_list.extend(x["object_list"])

        return {"object_list": object_list}


def view_install(request, *argi, **argv):
    return PFORM(request, Install, "schbuilder/forminstall.html", {})


class ImportFromGit(forms.Form):
    path = forms.CharField(
        label=_("Path to git repository"),
        required=True,
        max_length=None,
        min_length=None,
    )

    def process(self, request, queryset=None):

        object_list = []
        git_repository = self.cleaned_data["path"]
        prj_name = git_repository.split("/")[-1].split(".")[0]
        base_path = os.path.join(settings.DATA_PATH, "prj", prj_name)
        git_path = os.path.join(base_path, ".git")
        if os.path.exists(git_path):
            repo = Repo(base_path)
            try:
                remote_refs = porcelain.fetch(repo, git_repository)
                repo[b"HEAD"] = remote_refs.refs[b"refs/heads/master"]
                index_file = repo.index_path()
                tree = repo[b"HEAD"].tree
                index.build_index_from_tree(
                    repo.path, index_file, repo.object_store, tree
                )
                object_list.append(
                    (datetime.datetime.now(), "git fetch success", git_repository)
                )
            except Exception as e:
                object_list.append((datetime.datetime.now(), "git fetch error", str(e)))
        else:
            try:
                porcelain.clone(git_repository, base_path)
                object_list.append(
                    (datetime.datetime.now(), "git clone success", git_repository)
                )
            except Exception as e:
                object_list.append((datetime.datetime.now(), "git clone error", str(e)))

        prj_path = os.path.join(base_path, f"{prj_name}.prj")
        if os.path.exists(prj_path):
            with open(prj_path, "rt") as f:
                content = f.read()
                x = prj_import_from_str(content, backup_old=True)
                object_list.extend(x["object_list"])

        return {"object_list": reversed(object_list)}


def view_importfromgit(request, *argi, **argv):
    return PFORM(request, ImportFromGit, "schbuilder/formimportfromgit.html", {})


# Hello
@dict_to_template("schbuilder/v_gen.html")
def gen(request, pk):

    return {"object_list": reversed(build_prj(pk))}


def prj_export(request, pk):

    content = prj_export_to_str(pk)
    return HttpResponse(content, content_type="text/plain")


@dict_to_template("schbuilder/v_prj_import.html")
def prj_import(request):

    ex_str = request.POST["EDITOR"]
    return prj_import_from_str(ex_str, backup_old=True)


@dict_to_template("schbuilder/v_manage.html")
def manage(request, pk):

    prj = models.SChAppSet.objects.get(id=pk)
    return {"project": prj}

    # base_path = os.path.join(settings.PRJ_PATH, prj.name)
    # src_path = os.path.join(settings.PRJ_PATH, "schdevtools")

    # id = "spec"
    # task_id = async_task("schtasksdemo.tasks.fun2", task_publish_id=id)
    # return { "task_id": task_id, "id": "demo__"+id }

    # task_id = async_task("schbuilder.views.test")
    # print("TASK_ID: ", task_id)
    # task_id = async_task("schbuilder.tasks.test")
    # new_url = "../../../tasks/form/TaskListForm/%s/edit2__task" % task_id
    # return HttpResponseRedirect(new_url)

    # command = "import sys; sys.path.append('%s'); from manage import *" % base_path
    # pconsole = settings.PYTHON_CONSOLE.split(' ')
    # pconsole[0]=">>>" + pconsole[0]
    # pconsole.append('-i')
    # pconsole.append('-c')
    # pconsole.append(command)
    # param = ["python-shell",] + pconsole
    # id = get_process_manager().put(request, *param)
    # new_url = "../../../tasks/form/TaskListForm/%d/edit2__task" % id
    # new_url = "../../schsys/thread/%d/edit/" % id
    # return HttpResponseRedirect(new_url)


def template_edit(request, pk):

    table = models.SChTable.objects.get(id=pk)
    templates = models.SChTemplate.objects.filter(parent=table.parent).filter(
        name=table.name
    )
    if len(templates) == 0:
        template = models.SChTemplate(parent=table.parent, name=table.name)

        generics = table.schfield_set.filter(
            type__in=[
                "GTreeForeignKey",
                "GHiddenTreeForeignKey",
            ]
        )
        if len(generics) > 0:
            template_suffix = "tree"
        else:
            template_suffix = "tbl"

        file_name = settings.PRJ_PATH + (
            "/schdevtools/templates_src/schbuilder/wzr/new_generic_%s_template.ihtml"
            % template_suffix
        )

        f = open(file_name, "rt")
        s = f.read()
        f.close()

        template.save()

        t = Template(s)
        try:
            txt = t.render(Context({"template": template}))
        except:
            txt = s
        template.template_code = txt
        template.save()

        id = template.id
    else:
        id = templates[0].id

    new_url = make_href(
        "/schbuilder/table/SChTemplate/%s/template_code/py/editor/" % str(id)
    )

    return HttpResponseRedirect(new_url)


def edit(request):

    return TemplateView.as_view(template_name="schbuilder/import_form.html")(request)


def template_edit2(request, pk):

    form = models.SChForm.objects.get(id=pk)
    templates = models.SChTemplate.objects.filter(parent=form.parent).filter(
        name="Form" + form.name
    )
    if len(templates) == 0:
        template = models.SChTemplate(parent=form.parent, name="Form" + form.name)

        file_name = (
            settings.PRJ_PATH
            + "/schdevtools/templates_src/schbuilder/wzr/new_generic_form_template.ihtml"
        )
        f = open(file_name, "rt")
        template.template_code = f.read()
        f.close()
        template.save()
        id = template.id
    else:
        id = templates[0].id

    new_url = make_href(
        "/schbuilder/table/SChTemplate/%s/template_code/py/editor/" % str(id)
    )

    return HttpResponseRedirect(new_url)


@dict_to_template("schbuilder/v_installer.html")
def installer(request, pk):

    buf = []

    try:
        pki = int(pk)
        prj = models.SChAppSet.objects.get(id=pki)
        name = prj.name
    except:
        name = pk

    if hasattr(pytigon.schserw.settings, "_PRJ_PATH_ALT"):
        base_path = os.path.join(pytigon.schserw.settings._PRJ_PATH_ALT, prj.name)
    else:
        base_path = os.path.join(settings.PRJ_PATH_ALT, prj.name)

    zip_path = os.path.join(settings.DATA_PATH, "temp")

    buf.append("COMPILE TEMPLETE FILES:")

    (code, output, err) = py_run(
        [os.path.join(base_path, "manage.py"), "compiletemplates"]
    )

    if output:
        for pos in output:
            buf.append(pos)

    if err:
        buf.append("ERRORS:")
        for pos in err:
            buf.append(pos)

    exclude = [r".*\.pyc", r".*__pycache__.*"]
    ptig_name = os.path.join(zip_path, name + ".ptig")
    zip = ZipWriter(ptig_name, base_path, exclude=exclude, sha256=True)
    zip.to_zip(base_path, name + "/")
    path_to_meta = name + "-" + prj.version + ".dist-info/"
    zip.writestr(path_to_meta + "top_level.txt", (name + "\n").encode("utf-8"))
    zip.writestr(
        path_to_meta + "WHEEL",
        b"Wheel-Version: 1.0\nGenerator: pytigon\nRoot-Is-Purelib: true\nTag: py3-none-any",
    )
    txt = render_to_string(
        "schbuilder/wzr/METADATA.html", {"name": name, "version": prj.version}
    )
    zip.writestr(path_to_meta + "METADATA", txt.encode("utf-8"))
    with open(os.path.join(base_path, "LICENSE"), "rb") as f:
        btxt = f.read()
        zip.writestr(path_to_meta + "LICENSE", btxt)
    txt = ""
    with open(os.path.join(base_path, "install.ini"), "rt") as f:
        for line in f.readlines():
            if line.startswith("PIP ") or line.startswith("PIP="):
                x = line.split("=", 1)
                for item in x[1].replace(",", ";").split(";"):
                    txt += item + "\n"
                break
    zip.writestr("requirements.txt", txt.encode("utf-8"))

    buf.append("PACK PROGRAM FILES TO: " + zip_path + name + ".ptig")

    db_name = os.path.join(os.path.join(settings.DATA_PATH, name), name + ".db")

    buf.append("ADDING DATABASE FILES")

    (code, output, err) = py_run(
        [os.path.join(base_path, "manage.py"), "export_to_local_db"]
    )

    buf.append("Export to local db:")
    if output:
        for pos in output:
            buf.append(pos)

    if err:
        buf.append("ERRORS:")
        for pos in err:
            buf.append(pos)

    zip.write(db_name, name_in_zip=path_to_meta + name + ".db")

    record_str = ""
    for item in zip.sha256_tab:
        record_str += "%s,sha256=%s,%d\n" % item
    zip.writestr(path_to_meta + "RECORD", record_str.encode("utf-8"))

    zip.close()

    with open(ptig_name, "rb+") as f:
        content = f.read()
        f.seek(0, 0)
        f.write(b"#!/usr/bin/env ptig\n")
        f.write(content)
    try:
        os.chmod(ptig_name, 0o755)
    except:
        pass

    buf.append("Instaler file saved to: " + os.path.join(zip_path, name + ".ptig"))

    url = reverse("start") + "schbuilder/download_installer/" + name + "/"

    return {
        "object_list": list(reversed(buf)),
        "name": name,
        "url": url,
        "tp": "SChAppSet",
    }


@dict_to_template("schbuilder/v_restart_server.html")
def restart_server(request):

    lck = os.path.join(settings.DATA_PATH, "restart_needed.lck")
    success = True
    try:
        with open(lck, "wt") as f:
            f.write("A restart of the Pytigon program needed\n")
    except:
        success = False
    return {"success": success}


def template_edit3(request, pk):

    view = models.SChView.objects.get(id=pk)
    templates = models.SChTemplate.objects.filter(parent=view.parent).filter(
        name="v_" + view.name
    )
    if len(templates) == 0:
        template = models.SChTemplate(parent=view.parent, name="v_" + view.name)

        file_name = (
            settings.PRJ_PATH
            + "/schdevtools/templates_src/schbuilder/wzr/new_generic_form_template.ihtml"
        )
        f = open(file_name, "rt")
        template.template_code = f.read()
        f.close()
        template.save()
        id = template.id
    else:
        id = templates[0].id
    new_url = make_href(
        "/schbuilder/table/SChTemplate/%s/template_code/py/editor/" % str(id)
    )
    return HttpResponseRedirect(new_url)


@dict_to_template("schbuilder/v_update.html")
def update(request):

    prj_names = (
        "schdevtools",
        "schsetup",
        "schcomponents",
        "_schwiki",
        "_schdata",
        "_schtools",
        "_schall",
        "_schremote",
        "_schserverless",
        "scheditor",
        "schodf",
        "schportal",
        "schwebtrapper",
        "schpytigondemo",
    )

    base_url = "https://splawik:GanawaanawaT1@git.pytigon.cloud/pytigon/"

    object_list = []

    if hasattr(pytigon.schserw.settings, "_PRJ_PATH_ALT"):
        base_path = pytigon.schserw.settings._PRJ_PATH_ALT
    else:
        base_path = settings.PRJ_PATH_ALT

    for prj_name in prj_names:
        git_repository = base_url + prj_name + ".git"
        prj_path = os.path.join(base_path, prj_name)
        git_path = os.path.join(prj_path, ".git")
        success = True

        hash1 = ""
        prj_file_path = os.path.join(prj_path, prj_name + ".prj")
        if os.path.exists(prj_file_path):
            with open(prj_file_path, "rt") as f:
                content = f.read()
                hash1 = hashlib.sha1(content.encode("utf-8")).hexdigest()

        if os.path.exists(git_path):
            repo = Repo(prj_path)
            try:
                remote_refs = porcelain.fetch(repo, git_repository)
                repo[b"HEAD"] = remote_refs.refs[b"refs/heads/master"]

                index_file = repo.index_path()
                tree = repo[b"HEAD"].tree
                index.build_index_from_tree(
                    repo.path, index_file, repo.object_store, tree
                )

                object_list.append(
                    (datetime.datetime.now(), "git fetch success", git_repository)
                )
            except Exception as e:
                success = False
                object_list.append((datetime.datetime.now(), "git fetch error", str(e)))
        else:
            try:
                porcelain.clone(git_repository, prj_path)
                object_list.append(
                    (datetime.datetime.now(), "git clone success", git_repository)
                )
            except Exception as e:
                success = False
                object_list.append((datetime.datetime.now(), "git clone error", str(e)))
        if success:
            prj_file_path = os.path.join(prj_path, prj_name + ".prj")
            if os.path.exists(prj_file_path):
                with open(prj_file_path, "rt") as f:
                    content = f.read()
                    hash2 = hashlib.sha1(content.encode("utf-8")).hexdigest()
                    if hash1 != hash2:
                        x = prj_import_from_str(content, backup_old=True)
                        object_list.extend(x["object_list"])

    return {"object_list": object_list}


@dict_to_template("schbuilder/v_translate_sync.html")
def translate_sync(request, pk):

    locale_obj = models.SChLocale.objects.get(id=pk)
    prj = locale_obj.parent

    base_path = settings.PRJ_PATH_ALT
    app_path = os.path.join(base_path, prj.name)
    if not os.path.exists(app_path):
        base_path = settings.PRJ_PATH
        app_path = os.path.join(base_path, prj.name)

    locale_path = os.path.join(app_path, "locale")
    lang_path = os.path.join(locale_path, locale_obj.name)
    msg_path = os.path.join(lang_path, "LC_MESSAGES")
    po_path = os.path.join(msg_path, "django.po")

    if not os.path.exists(po_path):
        if not os.path.isdir(locale_path):
            os.mkdir(locale_path)
        if not os.path.isdir(lang_path):
            os.mkdir(lang_path)
        if not os.path.isdir(msg_path):
            os.mkdir(msg_path)

        po_init = """#\nmsgid ""\nmsgstr ""\n"Project-Id-Version: pytigon\\n"\n"Language: %s\\n"\n"MIME-Version: 1.0\\n"\n"Content-Type: text/plain; charset=UTF-8\\n"\n"Content-Transfer-Encoding: 8bit\\n"\n"""
        if locale_obj.name in locale.locale_alias:
            locale_str = locale.locale_alias[locale_obj.name].split(".")[0]
        else:
            locale_str = locale_obj.name

        po_init2 = po_init % locale_str
        with open(po_path, "wt") as f:
            f.write(po_init2)

    (code, output, err) = py_run(
        [os.path.join(app_path, "manage.py"), "compiletemplates"]
    )
    locale_gen_internal(prj.id)

    po = polib.pofile(po_path)

    locale_obj.schtranslate_set.update(status="#")

    inserted = 0
    updated = 0
    save = False

    for entry in po:
        print(entry.msgid, entry.msgstr, entry.msgctxt)
        t = locale_obj.schtranslate_set.filter(description=entry.msgid)
        if len(t) > 0:
            obj = t[0]
            updated += 1
            if obj.translation:
                entry.msgstr = obj.translation
                save = True
        else:
            obj = models.SChTranslate()
            obj.description = entry.msgid
            obj.parent = locale_obj
            obj.translation = entry.msgstr
            inserted += 1
        if obj.translation:
            obj.status = "OK"
        else:
            obj.status = ""
        obj.save()

    if save:
        po.save(po_path)

    locale_gen_internal(prj.id)

    return {
        "object_list": [
            [updated, inserted],
        ]
    }


@dict_to_template("schbuilder/v_locale_gen.html")
def locale_gen(request, pk):

    ret = locale_gen_internal(pk)
    if ret:
        ret_str = "OK"
    else:
        ret_str = "Error"

    return {
        "object_list": [
            [ret_str],
        ]
    }


def download_installer(request, name):

    installer = os.path.join(os.path.join(settings.DATA_PATH, "temp"), name + ".ptig")
    if os.path.exists(installer):
        with open(installer, "rb") as zip_file:
            response = HttpResponse(zip_file, content_type="application/force-download")
            response["Content-Disposition"] = (
                'attachment; filename="%s"' % name + ".ptig"
            )
            return response
    return HttpResponse(_("No installer file to download"))


@dict_to_json
def autocomplete(request, id, key):

    if key in ("object_fields", "object_methods", "object_fields_and_methods"):
        template = models.SChTemplate.objects.get(pk=int(id))
        ret = []
        if key in ("object_fields", "object_fields_and_methods"):
            ret += template.get_all_table_fields()
        if key in ("object_methods", "object_fields_and_methods"):
            ret += template.get_table_methods()
        return {
            "title": None,
            "choices": [
                {
                    "title": "Field",
                    "values": ret,
                },
            ],
            "template": "{{choice.0}}",
        }
    elif key.endswith("filters"):
        template = models.SChTemplate.objects.get(pk=int(id))
        ret = []
        if key in ("filters", "django_filters"):
            ret += template.get_django_filters()
        if key in ("filters", "pytigon_filters"):
            ret += template.get_pytigon_filters()
        return {
            "title": None,
            "choices": [
                {
                    "title": "Field",
                    "values": ret,
                },
            ],
            "template": "{{choice.0}}",
        }
    elif key.endswith("tags"):
        template = models.SChTemplate.objects.get(pk=int(id))
        ret = []
        if key in ("tags", "django_tags"):
            ret += template.get_django_tags()
        if key in ("tags", "pytigon_tags"):
            ret += template.get_pytigon_tags()
        return {
            "title": None,
            "choices": [
                {
                    "title": "Field",
                    "values": ret,
                },
            ],
            "template": "{{choice.0}}",
        }
    elif key.endswith("vars"):
        x = sch_standard(request)
        return {
            "title": None,
            "choices": [
                {
                    "title": "Field",
                    "values": list(x.keys()),
                },
            ],
            "template": "{{choice.0}}",
        }
    elif key == "relfields":
        template = models.SChTemplate.objects.get(pk=int(id))
        ret = template.get_table_rel_fields()
        return {
            "title": None,
            "choices": [
                {
                    "title": "Field",
                    "values": ret,
                },
            ],
            "template": "{{choice.0}}",
        }
    elif key == "txtfields":
        template = models.SChTemplate.objects.get(pk=int(id))
        ret = template.get_edit_table_fields()
        return {
            "title": None,
            "choices": [
                {
                    "title": "Field",
                    "values": ret,
                },
            ],
            "template": "{{choice.0}}",
        }
    elif key == "tables":
        template = models.SChTemplate.objects.get(pk=int(id))
        ret = [
            table.parent.name + "/" + table.name
            for table in template.get_tables_for_template()
        ]
        return {
            "title": None,
            "choices": [
                {
                    "title": "Field",
                    "values": ret,
                },
            ],
            "template": "{{choice.0}}",
        }
    elif key == "permissions":
        template = models.SChTemplate.objects.get(pk=int(id))
        tables = template.get_tables_for_template()
        ret = []
        for table in tables:
            app_perm = table.parent.name.lower()
            if not app_perm in ret:
                ret.append(app_perm)
            ret.append(table.parent.name.lower() + ".add_" + table.name.lower())
            ret.append(table.parent.name.lower() + ".change_" + table.name.lower())
            ret.append(table.parent.name.lower() + ".delete_" + table.name.lower())
            ret.append(table.parent.name.lower() + ".view_" + table.name.lower())

        return {
            "title": None,
            "choices": [
                {
                    "title": "Field",
                    "values": ret,
                },
            ],
            "template": "{{choice.0}}",
        }
    else:
        return key


@dict_to_template("schbuilder/v_gen_milestone.html")
def gen_milestone(request, pk):

    object_list = []

    prj = models.SChAppSet.objects.get(id=pk)
    root_path = settings.ROOT_PATH

    if hasattr(pytigon.schserw.settings, "_PRJ_PATH_ALT"):
        base_path = os.path.join(pytigon.schserw.settings._PRJ_PATH_ALT, prj.name)
    else:
        base_path = os.path.join(settings.PRJ_PATH_ALT, prj.name)

    git_path = os.path.join(base_path, ".git")

    if prj.git_repository:
        if hasattr(settings, "SYS_GIT_USER") and "//" in prj.git_repository:
            x = prj.git_repository.split("//", 1)
            git_repository = x[0] + "//" + settings.SYS_GIT_USER + "@" + x[1]
        else:
            git_repository = prj.git_repository

        print("A1: ", git_repository)
        print("A2: ", git_path)

        if os.path.exists(git_path):
            repo = Repo(base_path)
            try:
                remote_refs = porcelain.fetch(repo, git_repository)
                repo[b"HEAD"] = remote_refs.refs[b"refs/heads/master"]

                index_file = repo.index_path()
                tree = repo[b"HEAD"].tree
                index.build_index_from_tree(
                    repo.path, index_file, repo.object_store, tree
                )

                object_list.append(
                    (datetime.datetime.now(), "git fetch success", prj.git_repository)
                )
            except Exception as e:
                object_list.append((datetime.datetime.now(), "git fetch error", str(e)))
        else:
            try:
                porcelain.clone(git_repository, base_path)
                object_list.append(
                    (datetime.datetime.now(), "git clone success", prj.git_repository)
                )
            except Exception as e:
                object_list.append((datetime.datetime.now(), "git clone error", str(e)))

    object_list.extend(build_prj(pk))

    content = prj_export_to_str(prj.pk)

    prj_path = os.path.join(base_path, f"{prj.name}.prj")
    with open(prj_path, "wt") as f:
        f.write(content)

    object_list.append((datetime.datetime.now(), "prj exported", prj_path))

    x = prj_import_from_str(content, backup_this=True)
    object_list.extend(x["object_list"])
    prj2 = x["prj_instance"]

    object_list.append((datetime.datetime.now(), "prj copied to version:", prj.version))

    itemplate_path = os.path.join(base_path, "templates_src")
    l = len(base_path)
    compiled = []
    for root, dirs, files in os.walk(itemplate_path):
        for f in files:
            if f.endswith(".ihtml"):
                p = os.path.join(root, f)
                x = p[l + 15 :]
                compile_template(
                    x,
                    template_dirs=[
                        itemplate_path.replace("templates_src", "templates"),
                    ],
                    compiled=compiled,
                    force=True,
                )

    object_list.append(
        (
            datetime.datetime.now(),
            "compile templates",
            ", ".join([pos.split("/")[-1] for pos in set(compiled)]),
        )
    )

    if prj.git_repository:
        repo = Repo(base_path)
        for root, dirs, files in os.walk(base_path):
            if not ".git" in root.replace("\\", "/").split("/"):
                for file in files:
                    if not file in (
                        "global_db_settings.py",
                        "settings_app_local.py",
                    ) and not file.split(".")[-1].lower() in (
                        "pyc",
                        "pyo",
                        "so",
                        "exe",
                        "com",
                        "pkl",
                    ):
                        p = os.path.join(root, file)
                        porcelain.add(repo, p)
        try:
            porcelain.commit(repo, "New milestone version: " + prj2.version)
            porcelain.push(repo, git_repository)
            object_list.append(
                (datetime.datetime.now(), "git commit and push", prj.git_repository)
            )
        except Exception as e:
            object_list.append((datetime.datetime.now(), "git pull error", str(e)))

    return {"object_list": reversed(object_list)}


def prj_import2(request):

    return view_importfromgit(request)


@dict_to_template("schbuilder/v_run.html")
def run(request, pk):

    x = 1.5
    t = Template("X {{ x }}")
    c = Context({"x": x})
    z = t.render(c)
    print(z)

    prj = models.SChAppSet.objects.get(pk=pk)
    return {"project": prj}


def run2(request, pk):

    prj = models.SChAppSet.objects.get(pk=pk)
    environ["PYTHONPATH"] = os.path.join(settings.ROOT_PATH, "..")
    subprocess.run([sys.executable, "-m", "pytigon.ptig", prj.name], shell=False)
    return HttpResponse("")
