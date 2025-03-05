import os
import datetime
from pytigon_lib.schdjangoext.spreadsheet_render import render_ooxml, render_odf
from pytigon_lib.schtools.doc_tools import soffice_convert
from pytigon_lib.schtest.html_test import html_content_cmp
from django.conf import settings

in_file_path = os.path.join(settings.PRJ_PATH, "_schtest/tests/schhtml/test1.md")


def main(argv):
    context = {
        "spreadsheets": ["X1", "X2", "X3"],
        "object_list": [
            [1, 1.5, "Hello world!", datetime.datetime.now()],
            [2, 2.5, "Hello world!", datetime.datetime.now()],
            [3, 3.5, "Hello world!", datetime.datetime.now()],
        ],
    }
    render_ooxml(in_file_path, context, in_file_path.replace(".xlsx", "_out.xlsx"))
    render_odf(
        in_file_path.replace(".xlsx", ".ods"),
        context,
        in_file_path.replace(".xlsx", "_out.ods"),
    )
    soffice_convert(
        in_file_path,
        in_file_path + ".html",
        "html",
    )
    soffice_convert(
        in_file_path.replace(".xlsx", ".ods"),
        in_file_path.replace(".xlsx", ".ods.html"),
        "html",
    )

    cmp1 = html_content_cmp(
        in_file_path + ".html",
        in_file_path.replace("rep_wzr.xlsx", "wzr/rep_wzr.xlsx.html"),
    )
    cmp2 = html_content_cmp(
        in_file_path.replace(".xlsx", ".ods.html"),
        in_file_path.replace("rep_wzr.xlsx", "wzr/rep_wzr.ods.html"),
    )

    return True if cmp1 and cmp2 else False
