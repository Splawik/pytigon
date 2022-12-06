import sys
import os
import io

from pytigon_lib.schhtml.pdfdc import PdfDc
from pytigon_lib.schhtml.htmlviewer import HtmlViewerParser
from pytigon_lib.schindent.indent_style import ihtml_to_html_base
from django.core.files.storage import default_storage

BASE_PATH = os.path.abspath(os.getcwd())

default_storage.fs.mount("cwd", BASE_PATH)

ihtml_file_path = os.path.join("/cwd", sys.argv[-1])

f = default_storage.open(ihtml_file_path)
ihtml_str = f.read().decode("utf-8")
f.close()
buf = ihtml_to_html_base(None, input_str=ihtml_str)
output_stream = io.BytesIO()
dc = PdfDc(
    calc_only=False,
    output_name=os.path.join(
        BASE_PATH,
        "test",
        ihtml_file_path.replace(".ihtml", ".pdf"),
    ),
    output_stream=output_stream,
)
dc.set_paging(True)
p = HtmlViewerParser(dc=dc, calc_only=False)
p.feed(buf)
p.close()
dc.end_page()

f = default_storage.open(ihtml_file_path.replace(".ihtml", ".pdf"), "wb")
f.write(output_stream.getvalue())
f.close()
