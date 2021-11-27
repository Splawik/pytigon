from pytigon_lib.schdjangoext.django_ihtml import ihtml_to_html

def _transform_template(txt):
    return ihtml_to_html(None, txt)
    
def decode_script(name, code):    
    elements = code.split('===')
    if len(elements)>=3:
        _form = elements[0]
        _view = elements[1]
        _template = _transform_template(elements[2])
    elif len(elements)>=2:
        if elements[0].strip().startswith('def '):
            _form = None
            _view = elements[0]
            _template = elements[1]
        else:
            _form = elements[0]
            _view = elements[1]
            _template = None
    else:
        _form = None
        _view = code
        _template = None
    return [ _form, _view, _template ]
