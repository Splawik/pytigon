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


@dict_to_template("views_demo/v_plotly_export_example.html")
def plotly_export_example(request, **argv):

    from io import BytesIO
    import plotly.express as px

    df = px.data.iris()
    fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species")

    x1 = BytesIO()
    fig.write_image(x1, format="svg")

    df = px.data.gapminder().query("year == 2007").query("continent == 'Europe'")
    df.loc[df["pop"] < 2.0e6, "country"] = (
        "Other countries"  # Represent only large countries
    )
    fig = px.pie(
        df, values="pop", names="country", title="Population of European continent"
    )

    x2 = BytesIO()
    fig.write_image(x2, format="svg")

    return {"img1_svg": x1.getvalue(), "img2_svg": x2.getvalue()}
