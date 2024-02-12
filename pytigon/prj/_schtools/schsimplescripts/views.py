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

from django.http import Http404
from pytigon_lib.schdjangoext.django_ihtml import ihtml_to_html
from pytigon_lib.schdjangoext.fastform import form_from_str
from schsimplescripts.script_tools import decode_script
from django.core.exceptions import PermissionDenied
from pytigon_lib.schdjangoext.import_from_db import run_code_from_db_field, ModuleStruct

SCRIPT_TEMPLATE = """
{%% extends 'schsimplescripts/script_form.html' %%}

{%% load exfiltry %%}
{%% load exsyntax %%}
{%% load django_bootstrap5 %%}

"""

SCRIPT_TEMPLATE1 = (
    SCRIPT_TEMPLATE
    + """
%s
"""
)

SCRIPT_TEMPLATE2 = (
    SCRIPT_TEMPLATE
    + """
{%% block content %%}
<div class="ajax-frame"></div>
<div class="ajax-region">
%s
<div class="ajax-frame"></div> 
</div>

{%% endblock %%}
"""
)


def run(request, pk):

    script = models.Script.objects.get(pk=pk)
    form = None
    if script:
        if script.rights_group:
            test = False
            if request.user:
                if request.user.is_superuser:
                    test = True
                else:
                    if "." in script.rights_group:
                        if request.user.has_perm(script.rights_group):
                            test = True
                    else:
                        if user.groups.filter(name=script.rights_group).exists():
                            test = True
            if not test:
                raise PermissionDenied()

        form = None
        ret = {}
        show_result = False
        if script._form:
            form_class = form_from_str(script._form)
            if form_class:
                if request.method == "POST":
                    form = form_class(request.POST)
                    if form.is_valid():
                        data = form.cleaned_data
                        show_result = True
                    else:
                        data = None
                        show_result = False

                else:
                    form = form_class()
                    data = None
                    show_result = False
            else:
                data = None
                show_result = True
        else:
            data = None
            show_result = True

        ret = run_code_from_db_field(
            f"script__view_{script.pk}.py",
            script,
            "_view",
            "view",
            request=request,
            data=data,
        )

        if type(ret) == dict and script._template:
            ret["form"] = form
            ret["SHOW_RESULT"] = show_result
            x = script._template.strip()
            if x.startswith("{% block") or x.startswith("%%"):
                template_script = SCRIPT_TEMPLATE1 % script._template
            else:
                template_script = SCRIPT_TEMPLATE2 % script._template
            template = Template(template_script)
            context = RequestContext(request, ret)
            ret_str = template.render(context)
            return HttpResponse(ret_str)
        elif type(ret) == dict:
            ret["form"] = form
            return render_to_response(
                "schsimplescripts/script_form.html", ret, request=request
            )
        elif type(ret) == str:
            return run_script_by_name(request, ret)
        else:
            return ret

    raise Http404("Script does not exist")


def run_script_by_name(request, script_name):

    script = models.Script.objects.get(name=script_name)
    if script:
        p = reverse("row_action_scripts_run", kwargs={"pk": int(script.id)})
        if "only_content" in request.GET:
            return HttpResponseRedirect(p + "?childwin=1&only_content=1")
        else:
            return HttpResponseRedirect(p + "?childwin=1")
    else:
        raise Http404("Script does not exist")
