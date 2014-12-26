import sys

sys.path.append('./../..')
sys.path.insert(0,'./../../ext_lib')

from schlib.schhtml.pdfdc import PdfDc
from schlib.schhtml.cairodc import CairoDc
from schlib.schhtml.htmlviewer import HtmlViewerParser


if __name__ == '__main__':
    run_cairo = False
    
    f = open('./test/icss/form.icss', 'r')
    init_css_str = f.read()
    f.close()

    if len(sys.argv) > 1:
        name = sys.argv[1]
    else:
        name = 'test/test11.html'

    (width, height) = (595, 842)

    if run_cairo:
        dc = CairoDc(calc_only=False, width=width, height=height,
                     output_name='test/test.pdf')
    else:
        dc = PdfDc(calc_only=False, width=width, height=height,
                     output_name='test/test.pdf')
    dc.set_paging(False)
    url = None
    dc.set_paging(True)
    if url:
        p = HtmlViewerParser(dc=dc, calc_only=False, url=url)
    else:
        p = HtmlViewerParser(dc=dc, calc_only=False, init_css_str=init_css_str,
                             css_type=1)
        f = open(name, "rb")
        for line in f:
            p.feed(line.decode('utf-8'))
        f.close()

    p.close()
    dc.end_page()
    #dc.save('test/test.zip')
