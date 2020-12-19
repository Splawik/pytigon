# Template filters

Definiując szablony w aplikacjach Pytigon możesz wykorzystywać wszystkie szablony zdefiniowane standardowo przez Django, listę i dokumentację znajdziesz pod adresem:

https://docs.djangoproject.com/en/dev/ref/templates/builtins/

Dodatkowo Pytigon definiuje następujące filtry:

## class_name

> def class_name(value)

Returns class name of value

## is_private

> def is_private(value):

    """Check if function is private"""
    return value.startswith('_')

## get_value

> def getvalue(value, argv):

    """Returns value[argv]"""
    return value[argv]

## get_attr

> def get_attr(value, attr):

    """Returns getattr(value, attr)"""
    try:
        obj = getattr(value, attr)
    except:
        obj = None
    return obj

## range

> def \_range(value):

    """Returns list(range(int(value)))"""
    return list(range(int(value)))

## dir

> def f_dir(value):

    """Returns dir(value)"""
    return dir(value)

## split

> def filter_split(obj, sep=';'):

    "split obj and return result"
    return obj.split(sep)

## feval

> def \_eval(value):

    """Returns eval(value)"""
    return eval(value)

## left

> def left(value, arg):

    return str(value)[:int(arg)]

## truncate

> def truncate(value, arg):

    """truncate result"""
    try:
        retstr = str(value)
    except:
        retstr = unicode(value)

    if len(retstr) > int(arg):
        return retstr[:int(arg) - 3] + '...'
    else:
        return retstr

## last_elem

> def last_elem(value, sep='/'):

    """split value and return last element"""
    return value.split(sep)[-1]

## first_section

> def first_section(html):

    """part of string before $$$"""
    if html:
        return html.split('$$$')[0]
    else:
        return ""

## second_section

> def second_section(html):

    """part of string after $$$"""
    if html:
        x = html.split('$$$')
        if len(x)>1:
            return x[1]
        else:
            return ""
    else:
        return ""

## replace

> def replace(value, replace_str):

    """replace_str: 'old_value|new_value' """
    l = replace_str.split('|')
    if len(l) == 2:
        value2 = value.replace(l[0], l[1])
        return value2
    else:
        return value

## hasattr

> def filter_hasattr(obj, attr_name):

    return hasattr(obj, attr_name)

## has_ext

> def has_ext(value, arg):

    if value.lower().endswith(arg.lower()):
        return True
    else:
        return False

## append_get_param

> def append_get_param(href, parm):

    if '?' in href:
        return href+"&"+str(parm)
    else:
        return href+"?"+str(parm)

## call

> def \_call(obj, methodName):

    method = getattr(obj, methodName)
    if hasattr(obj, "__callArg"):
        ret = method(*obj.__callArg)
        del obj.__callArg
        return ret
    return method()

## args

> def args(obj, arg):

    if not hasattr(obj, "__callArg"):
        obj.__callArg = []
    obj.__callArg += [arg]
    return obj

## bencode

> def bencode(value):

    """Returns b64encode(value)"""

    if value:
        return b64encode(value.encode('utf-8')).decode('utf-8')
    else:
        return ''

## bdecode

> def bdecode(value):

    """Returns b64decode(value)"""

    return b64decode(value.encode('utf-8')).decode('utf-8')

## to_str

> def to_str(value):

    """Converts value to str"""
    try:
        ret = str(value)
    except:
        ret = ""
    return ret

## to_int

> def to_int(value):

    try:
        ret = int(value)
    except:
        ret = 0
    return ret

## to_float

> def to_int(value):

    try:
        ret = float(value)
    except:
        ret = 0.0
    return ret

## format

> def format(value, id):

    return value % id

## genericfloatformat

> def genericfloatformat(text, arg="{: .2f}"):

    space_convert = False
    try:
        f = float(text)
        if ': ' in arg:
            space_convert = True
            arg2 = arg.replace(': ', ':,')
        else:
            arg2 = arg
        x = arg2.format(f)
        if space_convert:
            return x.replace(',', ' ')
        else:
            return ""
    except ValueError:
        return ''

## genericfloatnullformat

> def genericfloatnullformat(text, arg="{: .2f}"):

    try:
        f = float(text)
        if not f:
            return "-"
        else:
            return genericfloatformat(text, arg)
    except:
        return "-"

## floatformat2

> def floatformat2(text):

    return genericfloatformat(text, "{: .2f}")

## floatformat3

> def floatformat3(text):

    return genericfloatformat(text, "{: .3f}")

## floatnullformat

> def floatnullformat(text):

    return genericfloatnullformat(text, "{: .2f}")

## floatnullformat3

> def floatnullformat3(text):

    return genericfloatnullformat(text, "{: .3f}")

## amount

> def amount(text):

    try:
        f = float(text)
    except ValueError:
        return ''
    if f==0.0:
        return '-  '
    def split_len(seq, length):
        return [seq[i:i+length] for i in range(0, len(seq), length)]

    s = "%.02f" % f
    t = s.split('.')
    return ' '.join(split_len(t[0][::-1], 3))[::-1] + "." + t[1]

## isoformat

> def isoformat(value):

    if value:
        iso = value.isoformat()[:19].replace('T', ' ')
        return iso
    else:
        return ""

## isoformat_short

> def isoformat_short(value):

    if value:
        iso = value.isoformat()[:16].replace('T', ' ')
        return iso
    else:
        return ""

## d_isoformat

> def d_isoformat(value):

    if value:
        iso = value.isoformat()[:10]
        return iso
    else:
        return ""

## one_line_block

> def one_line_block(value):

    """Clean value by removing unnecessary spaces and characters: '\n', '\t' """
    return value.replace('        ', ' ').replace('    ', ' ').replace('  ', ' ').replace('\n', '').replace('\t', '')

## one_line_code

> def one_line_code(value):

    """Clean value by removing unnecessary spaces and characters: '\n', '\t' """
    return value.replace('\n', '').replace('\r', '').replace('\t', '')

## clean

> def clean(value):

    return ' '.join(value.replace('\n', '').replace('\t', '').split())

## fadd

> def fadd(value, arg):

    """Returns int(value) - int(arg)"""
    return float(value) + float(arg)

## subtract

> def subtract(value, arg):

    """Returns int(value) - int(arg)"""
    return int(value) - int(arg)

## fsubtract

> def fsubtract(value, arg):

    """Returns int(value) - int(arg)"""
    return float(value) - float(arg)

## multiply

> def multiply(value, arg):

    """Returns int(value) * int(arg)"""
    return int(value) * int(arg)

## fmultiply

> def fmultiply(value, arg):

    """return fvalue * float"""
    try:
        ret = float(value) * float(arg)
    except:
        ret = ""
    return ret

## divide

> def divide(value, arg):

    """Return int(value) / int(arg)"""
    return int(value) / int(arg)

## fdivide

> def fdivide(value, arg):

    """Returns float(value) / float(arg)"""
    if float(arg) != 0:
        return float(value) / float(arg)
    else:
        return ""

## append_str

> def append_str(value, s):

    if s==None or s=="":
        return value
    else:
        return value + str(s)

## date_inc

> def date_inc(value, arg):

    """Increment date value by timedelta(int(arg))"""
    try:
        (date, time) = value.split()
        (y, m, d) = date.split('-')
        return datetime.datetime(int(y), int(m), int(d))\
             + datetime.timedelta(int(arg))
    except ValueError:
        return None

## date_dec

> def date_dec(value, arg):

    """Decrement date value by timedelta(int(arg))"""
    try:
        (y, m, d) = value.split('-')
        return (datetime.datetime(int(y), int(m), int(d))
                 - datetime.timedelta(int(arg))).date()
    except ValueError:
        return None

## get_model_fields

> def get_model_fields(obj):

    if hasattr(obj, "_meta"):
        ret = []
        for field in obj._meta.get_fields():
            if hasattr(obj, field.name):
                if field.name == 'id':
                    ret.insert(0, getattr(obj, field.name))
                else:
                    ret.append(getattr(obj, field.name))
        return ret
    else:
        return obj

## get_all_model_fields

> def get_all_model_fields(value):

    """Returns all fields for model (value)"""
    ret = []
    for f in value._meta.fields + value._meta.many_to_many:
        ret.append(f)
    return ret

## get_all_model_parents

> def getparents(parent):

    """Returns fields for model (value) without many_to_many fields"""
    ret = []
    while parent:
        ret.append(parent)
        parent=parent.parent
    return ret

## get_model_fields_names

> def get_model_fields_names(obj):

    ret = []
    for field in obj._meta.get_fields():
        if hasattr(obj, field.name):
            if field.name == 'id':
                ret.insert(0,field.name)
            else:
                ret.append(field.name)
    return ret

## get_model_fields_verbose_names

> def get_model_fields_verbose_names(obj):

    ret = []
    if hasattr(obj, "_meta"):
        for field in obj._meta.get_fields():
            if hasattr(obj, field.name):
                if hasattr(field, "verbose_name"):
                    if field.name == 'id':
                        ret.insert(0,field.verbose_name)
                    else:
                        ret.append(field.verbose_name)
                else:
                    ret.append(field.name)
    else:
        for i in range(0, len(obj)):
            ret.append("x%d" % i)
    return ret

## user_in_group

> def user_in_group(user, group_name):

    return user.groups.filter(name=group_name).exists()

## field_as_widget

> def field_as_widget(value, arg):

    d = {}
    l = arg.split(',')
    for x in l:
        x2 = x.split(':')
        d[x2[0]] = x2[1]
    return value.as_widget(attrs=d)

## model_has_children

> def model_has_children(value):

    set_name = value._meta.model_name
    if hasattr(value, set_name + '_set'):
        o = getattr(value, set_name + '_set')
    else:
        o = getattr(value, 'children')
    l = o.all()
    if len(l) > 0:
        return True
    else:
        return False

## choices_from_field

> def choices_from_field(obj, field):

    return obj._meta.get_field(field).choices

## reverse

> def \_reverse(value):

    return reverse(value)

## errormessage

> def errormessage(value):

    """Returns True if value.endswith('!')"""
    if value.endswith('!'):
        return True
    else:
        return False

## to_html_icon

> def to_html_icon(icon_str, additional_class=""):

    if icon_str.startswith('fa://'):
        return "<i class='fa fa-%s %s'></i>" % (icon_str[5:].replace('.png',''), additional_class)
    elif icon_str.startswith('png://'):
        src = mhref("/static/icons/22x22/%s" % icon_str[6:])
        return "<img src='%s' class='%s'></img>" % (src, additional_class)
    elif icon_str.startswith('client://'):
        src = mhref("/static/icons/22x22/%s" % icon_str[9:])
        return "<img src='%s' class='%s'></img>" % (src, additional_class)
    elif icon_str.startswith('data:image/svg+xml'):
        x = icon_str.split(',',1)
        svg_code = x[1]
        return svg_code
    else:
        return "<i class='fa fa-circle-o'></i>"

## aggregate

> def aggregate(objects, field_name):

    if field_name.startswith('max_'):
        field = field_name[4:]
        x = objects.aggregate(Max(field))
        return x[field+'__max']
    elif field_name.startswith('min_'):
        field = field_name[4:]
        x = objects.aggregate(Min(field))
        return x[field+'__min']
    elif field_name.startswith('sum_'):
        field = field_name[4:]
        x = objects.aggregate(Sum(field))
        return x[field+'__sum']
    elif field_name.startswith('avg_'):
        field = field_name[4:]
        x = objects.aggregate(Avg(field))
        return x[field+'__avg']
    elif field_name.startswith('count_'):
        field = field_name[6:]
        x = objects.aggregate(Count(field))
        return x[field+'__count']
    return 0

## wikify

> def \_wikify(value, path=None):

    return wikify(value, path)

## wiki

> def wiki(value):

    return wiki_from_str(value)

## wiki_href

> def wiki_href(value, section="help"):

    if section.startswith('+'):
        path = section
        section = 'help'
    else:
        path=None
    return make_href(value, section=section, path=path)

## markdown

> def \_markdown(value):

    return markdown.markdown(value, extensions=['abbr', 'attr_list', 'def_list', 'fenced_code', 'footnotes', 'md_in_html', 'tables', 'admonition', 'codehilite',])

## preferred_enctype

> def \_preferred_enctype(form):

    if hasattr(form, 'visible_fields'):
        for field in form.visible_fields():
            if type(field.field).__name__ in ('FileField', 'ImageField'):
                return "multipart/form-data"
    return "application/x-www-form-urlencoded"

## to_bootstrap

> def to_bootstrap(form):

    return BootstrapForm(form)

## textfiel_row_col

> def textfiel_row_col(field, arg):

    row, col = arg.split('x')
    field.field.widget.attrs['rows']=int(row)
    field.field.widget.attrs['cols']=int(col)
    return field

## ooxml

> def ooxml(value):

    if type(value) in (datetime.datetime, datetime.date):
        if value:
            return value.isoformat()
        else:
            return '0'
    elif type(value) in (float, int):
        if value:
            return str(value)
        else:
            return '0'
    else :
        if value:
            return str(value)
        else:
            return ""

## ihtml2html

> def ihtml2html(html):

    return ihtml_to_html(None, input_str=html)
