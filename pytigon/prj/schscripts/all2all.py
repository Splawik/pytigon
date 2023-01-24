import sys
import os
import argparse

from pytigon_lib.schhtml.pdfdc import PdfDc
from pytigon_lib.schhtml.cairodc import CairoDc
from pytigon_lib.schhtml.docxdc import DocxDc
from pytigon_lib.schhtml.xlsxdc import XlsxDc
from pytigon_lib.schhtml.basedc import BaseDc
from pytigon_lib.schhtml.htmlviewer import HtmlViewerParser
from pytigon_lib.schindent.indent_style import ihtml_to_html_base
from pytigon_lib.schindent.indent_markdown import markdown_to_html

from pytigon_lib.schindent.indent_markdown import (
    IndentMarkdownProcessor,
    REG_OBJ_RENDERER,
)

BASE_PATH = os.getcwd()


def main():
    import schwiki.applib.makdown_obj_simple
    import schwiki.applib.markdown_obj_subblocks

    parser = argparse.ArgumentParser(description="Converter")
    parser.add_argument(
        "filename", help="filename to convert (*.html, *.ihtml, *.md, *.imd)"
    )
    parser.add_argument(
        "-o", "--output", help="output filename (*.pdf, *.spdf, *.docx, *.xlsx, *.svg)"
    )
    parser.add_argument("-i", "--icss", help="input icss filename (*.icss)")

    args = parser.parse_args(sys.argv[2:])

    if args.icss:
        if args.icss.startswith("/") or args.icss[1] == ":":
            icss_filename = args.icss
        else:
            icss_filename = os.path.join(BASE_PATH, args.icss)

        with open(os.path.join(BASE_PATH, args.icss), "r") as f:
            init_css_str = f.read()
    else:
        init_css_str = "@wiki.icss"

    if args.filename.startswith("/") or args.filename[1] == ":":
        input_filename = args.filename
    else:
        input_filename = os.path.join(BASE_PATH, args.filename)

    if args.output.startswith("/") or args.output[1] == ":":
        output_filename = args.output
    else:
        output_filename = os.path.join(BASE_PATH, args.output)

    (width, height) = (595, 842)

    if ".pdf" in output_filename or ".xpdf" in output_filename:
        if ".xpdf" in output_filename:
            dc = PdfDc(
                output_name=output_filename.replace(".xpdf", ".pdf"),
            )
        else:
            dc = PdfDc(output_name=output_filename)

        dc.set_paging(True)

    elif ".spdf" in output_filename:

        def notify_callback(event_name, data):
            if event_name == "end":
                dc = data["dc"]
                if dc.output_name:
                    dc.save(dc.output_name)
                else:
                    result_buf = NamedTemporaryFile(delete=False)
                    spdf_name = result_buf.name
                    result_buf.close()

                    dc.save(spdf_name)
                    with open(spdf_name, "rb") as f:
                        dc.ouput_stream.write(f.read())

        dc = PdfDc(
            output_name=output_filename,
            calc_only=True,
            width=width,
            height=height,
            notify_callback=notify_callback,
            record=True,
        )
        dc.set_paging(True)
    elif ".docx" in output_filename:
        dc = DocxDc(
            output_name=output_filename,
            # docx_template_path=os.path.join(BASE_PATH, "default.docx"),
        )
    elif ".xlsx" in output_filename:
        dc = XlsxDc(output_name=output_filename)
    else:
        dc = None

    if ".ihtml" in input_filename and ".html" in output_filename:
        with open(input_filename, "rt", encoding="utf-8") as f:
            buf = f.read()
            buf = ihtml_to_html_base(None, input_str=buf)
            with open(output_filename, "wt", encoding="utf-8") as f2:
                f2.write(buf)
        return

    p = HtmlViewerParser(dc=dc, calc_only=False, init_css_str=init_css_str, css_type=1)

    with open(input_filename, "rt", encoding="utf-8") as f:
        buf = f.read()
        if ".ihtml" in input_filename:
            buf = ihtml_to_html_base(None, input_str=buf)
        elif ".md" in input_filename:
            buf = markdown_to_html(buf)
            buf = "<html><body class='wiki'>" + buf + "</body></html>"
        elif ".imd" in input_filename:
            x = IndentMarkdownProcessor(output_format="html")
            buf = x.convert(buf)
            buf = "<html><body class='wiki'>" + buf + "</body></html>"

        if ".xpdf" in output_filename:

            def notify_callback(event_name, data):
                if event_name == "end":
                    dc = data["dc"]
                    dc.surf.pdf.set_subject(buf)

            dc.notify_callback = notify_callback
        p.feed(buf)

    p.close()
