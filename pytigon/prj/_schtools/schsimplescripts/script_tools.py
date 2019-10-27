from pytigon_lib.schdjangoext.django_ihtml import ihtml_to_html

def _transform_view(name, txt1, txt2):
    fun = ""
    for row in txt2.split('\n'):
        fun = fun + "    "+row+"\n"

    x2 = """def scripts_%s(request, argv):
%s
""" % (name, fun)

    return txt1+"\n"+x2

def _transform_template(txt):
    return ihtml_to_html(None, txt)


def decode_script(name, code):    
    elements = code.split('===')
    if len(elements)>=4:
        _form = elements[1]
        _view = _transform_view(name, elements[0], elements[2])
        _template = _transform_template(elements[3])
        return [ _form, _view, _template ]
    return None        
