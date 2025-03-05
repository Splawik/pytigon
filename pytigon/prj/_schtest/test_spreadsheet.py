import os
import datetime
import tempfile

from pytigon_lib.schdjangoext.spreadsheet_render import render_ooxml, render_odf
from pytigon_lib.schtools.doc_tools import soffice_convert
from pytigon_lib.schtest.html_test import html_content_cmp
from django.conf import settings

in_file_path = os.path.join(
    settings.PRJ_PATH, "_schtest/tests/schspreadsheet/rep_wzr.xlsx"
)

out_file_path = os.path.join(tempfile.gettempdir(), "rep_wzr_out.xlsx")


def main(argv):
    context = {
        "spreadsheets": ["X1", "X2", "X3"],
        "object_list": [
            [1, 1.5, "Hello world!", datetime.datetime.now()],
            [2, 2.5, "Hello world!", datetime.datetime.now()],
            [3, 3.5, "Hello world!", datetime.datetime.now()],
        ],
    }
    render_ooxml(in_file_path, context, out_file_path)
    render_odf(
        in_file_path.replace(".xlsx", ".ods"),
        context,
        out_file_path.replace(".xlsx", ".ods"),
    )
    soffice_convert(
        out_file_path,
        out_file_path + ".html",
        "html",
    )
    soffice_convert(
        out_file_path.replace(".xlsx", ".ods"),
        out_file_path.replace(".xlsx", ".ods.html"),
        "html",
    )

    cmp1 = html_content_cmp(
        out_file_path + ".html",
        in_file_path.replace("rep_wzr.xlsx", "wzr/rep_wzr_out.xlsx.html"),
    )
    cmp2 = html_content_cmp(
        out_file_path.replace(".xlsx", ".ods.html"),
        in_file_path.replace("rep_wzr.xlsx", "wzr/rep_wzr_out.ods.html"),
    )

    return True if cmp1 and cmp2 else False
