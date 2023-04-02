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

from tables_demo.models import Example1Computer


def make_csum_fun():
    from pytigon_lib.schtools.llvm_exec import compile_str_to_module, get_function
    from ctypes import CFUNCTYPE, c_int

    fun_str = """
    define dso_local i32 @cadd(i32 %0, i32 %1) #0 {
      %3 = alloca i32, align 4
      %4 = alloca i32, align 4
      store i32 %0, i32* %3, align 4
      store i32 %1, i32* %4, align 4
      %5 = load i32, i32* %3, align 4
      %6 = load i32, i32* %4, align 4
      %7 = add nsw i32 %5, %6
      ret i32 %7
    }
    """

    compile_str_to_module(fun_str)
    func_ptr = get_function("cadd")
    cfunc = CFUNCTYPE(c_int, c_int, c_int)(func_ptr)
    return cfunc


csum = make_csum_fun()


@dict_to_template("views_demo/v_test_llvm.html")
def test_llvm(request, **argv):

    ret = csum(2, 3)
    return {"result": ret}


@dict_to_odf("views_demo/v_odf_example.ods")
def odf_example(request, **argv):

    return {"name": "odf test", "description": "Hello!"}


@dict_to_pdf("views_demo/v_pdf_example_pdf.html")
def pdf_example(request, **argv):

    return {"name": "pdf test", "description": "Hello!"}


@dict_to_json
def json_example(request, **argv):

    return {"name": "json test", "description": "Hello!"}


@dict_to_xml
def xml_example(request, **argv):

    return Example1Computer.objects.all()


@dict_to_ooxml("views_demo/v_xlsx_example.xlsx")
def xlsx_example(request, **argv):

    return {"name": "xlsx test", "description": "Hello!", "x": 1.4}


@dict_to_txt("views_demo/v_txt_example_txt.html")
def txt_example(request, **argv):

    return {"name": "txt test", "description": "Hello!"}


@dict_to_template("views_demo/v_template_example.html")
def template_example(request, **argv):

    return {"name": "template test", "description": "Hello!"}


@dict_to_hdoc("views_demo/v_hdoc_example_hdoc.html")
def hdoc_example(request, **argv):

    return {"name": "txt test", "description": "Hello!"}


@dict_to_template("views_demo/v_plotly_example.html")
def plotly_example(request, **argv):

    import plotly.graph_objects as go
    import numpy as np
    from io import StringIO

    np.random.seed(1)

    N = 100
    x = np.random.rand(N)
    y = np.random.rand(N)
    colors = np.random.rand(N)
    sz = np.random.rand(N) * 30

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="markers",
            marker=go.scatter.Marker(
                size=sz, color=colors, opacity=0.6, colorscale="Viridis"
            ),
        )
    )
    # fig.write_image("fig1.svg")
    # fig.write_image("fig1.svg")
    buf = StringIO()
    fig.write_html(buf, include_plotlyjs=False, full_html=False)
    return {"plotly_content": buf.getvalue()}


@dict_to_template("views_demo/v_seaborn_example.html")
def seaborn_example(request, **argv):

    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    import io

    df = pd.DataFrame(
        {
            "Date": [
                "2022-01-01",
                "2022-02-01",
                "2022-03-01",
                "2022-04-01",
                "2022-05-01",
                "2022-06-01",
            ],
            "Attendance": [88, 78, 90, 68, 84, 75],
        }
    )
    df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d")

    ax = sns.barplot(x="Date", y="Attendance", data=df)
    ax.figure.set_size_inches(7, 8)
    xticks = ax.get_xticks()
    ax.set_xticklabels(
        [pd.to_datetime(tm, unit="ms").strftime("%Y-%m-%d") for tm in xticks],
        rotation=45,
    )
    # plt.xticks(rotation=20)

    imgdata = io.StringIO()
    ax.get_figure().savefig(imgdata, format="svg")
    return {"img_svg": imgdata.getvalue()}
