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


@dict_to_template("views_demo/v_matplotlib_example.html")
def matplotlib_example(request, **argv):

    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    import io

    # image 1
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
    img1 = imgdata.getvalue()

    # image 2

    df = pd.DataFrame(
        {
            "Dates": [
                "2021-06-10",
                "2021-06-11",
                "2021-06-12",
                "2021-06-13",
                "2021-06-14",
                "2021-06-15",
            ],
            "Female": [200, 350, 150, 600, 500, 350],
            "Male": [450, 400, 800, 250, 500, 900],
        }
    )

    ax = df.plot(x="Dates", y=["Female", "Male"], kind="bar")

    ax.get_figure().set_size_inches(14, 12)

    imgdata2 = io.StringIO()
    ax.get_figure().savefig(imgdata2, format="svg")
    img2 = imgdata2.getvalue()

    return {"img1_svg": img1, "img2_svg": img2}
