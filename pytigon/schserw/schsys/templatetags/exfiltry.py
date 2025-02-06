"""
This module defines custom template filters for use in Django templates.

Filters:
- class_name: Returns the class name of the value.
- to_console: Prints the value to the console and returns an empty string.
- is_private: Checks if the function is private.
- get_value: Returns value[argv] if value is a dictionary, otherwise returns an empty string.
- get_attr: Returns getattr(value, attr) if possible, otherwise returns None.
- range: Returns a list of integers from 0 to int(value) - 1.
- dir: Returns the list of attributes of the value.
- split: Splits the object by the separator and returns the result.
- feval: Evaluates the value as a Python expression.
- left: Returns the leftmost 'arg' characters of the value.
- truncate: Truncates the value to 'arg' characters, appending '...' if necessary.
- first_elem: Splits the value by the separator and returns the first element.
- last_elem: Splits the value by the separator and returns the last element.
- penultimate_elem: Splits the value by the separator and returns the penultimate element.
- first_section: Returns the part of the string before '$$$'.
- second_section: Returns the part of the string after '$$$'.
- replace: Replaces 'old_value' with 'new_value' in the value.
- nbsp: Replaces spaces with '&nbsp;'.
- hasattr: Checks if the object has the specified attribute.
- has_ext: Checks if the value ends with the specified extension.
- append_get_param: Appends a GET parameter to the href.
- call: Calls the method on the object if it exists.
- args: Adds an argument to the object's __callArg list.
- call_with: Calls the proxy's call method with the argument.
- bencode: Returns the base64 encoded value.
- bdecode: Returns the base64 decoded value.
- to_str: Converts the value to a string.
- none_to_empty: Converts None to an empty string, otherwise converts the value to a string.
- to_int: Converts the value to an integer.
- to_float: Converts the value to a float.
- num2str: Converts the number to a string, replacing commas with dots and removing spaces.
- format: Formats the value using the specified format string.
- genericfloatformat: Formats the float value using the specified format string.
- genericfloatnullformat: Formats the float value, returning '-' if the value is zero or invalid.
- floatformat2: Formats the float value to 2 decimal places.
- floatformat3: Formats the float value to 3 decimal places.
- floatnullformat: Formats the float value to 2 decimal places, returning '-' if the value is zero or invalid.
- floatnullformat3: Formats the float value to 3 decimal places, returning '-' if the value is zero or invalid.
- amount: Formats the amount with thousand separators.
- isoformat: Formats the value as an ISO date string.
- sysisoformat: Formats the value as an ISO date string, handling system-specific formats.
- isoformat_short: Formats the value as a short ISO date string.
- d_isoformat: Formats the value as an ISO date string (date only).
- one_line_block: Cleans the value by removing unnecessary spaces and characters.
- one_line_code: Cleans the value by removing newlines and tabs.
- clean: Cleans the value by removing unnecessary spaces and characters.
- fadd: Returns the sum of value and arg as floats.
- subtract: Returns the difference between value and arg as integers.
- fsubtract: Returns the difference between value and arg as floats.
- multiply: Returns the product of value and arg as integers.
- fmultiply: Returns the product of value and arg as floats.
- divide: Returns the quotient of value and arg as integers.
- fdivide: Returns the quotient of value and arg as floats.
- append_str: Appends the string s to the value if s is not None or empty.
- date_inc: Increments the date value by the specified number of days.
- date_dec: Decrements the date value by the specified number of days.
- get_model_fields: Returns the fields of the model without many-to-many fields.
- get_model_meta: Returns the _meta attribute of the model.
- get_model_app: Returns the app label of the model.
- get_model_row: Returns a list of field values for the model instance.
- get_model_ooxml_row: Returns a list of field values formatted for OOXML.
- get_all_model_fields: Returns all fields of the model, including many-to-many fields.
- get_all_model_parents: Returns a list of all parent models.
- get_model_fields_names: Returns a list of field names for the model instance.
- get_model_fields_verbose_names: Returns a list of verbose names for the model fields.
- user_in_group: Checks if the user is in the specified group.
- field_as_widget: Renders the field as a widget with the specified attributes.
- model_has_children: Checks if the model instance has children.
- model_can_have_children: Checks if the model instance can have children.
- choices_from_field: Returns the choices for the specified field.
- reverse: Returns the reversed URL for the given view name.
- errormessage: Checks if the value ends with '!'.
- aggregate: Returns the aggregate value for the specified field.
- wikify: Converts the value to wiki format.
- wiki: Converts the value to wiki format.
- wiki_href: Converts the value to a wiki link.
- markdown: Converts the value to HTML using Markdown.
- preferred_enctype: Returns the preferred enctype for the form.
- to_bootstrap: Converts the form to a Bootstrap-styled form.
- textfiel_row_col: Sets the rows and cols attributes for the text field.
- ooxml: Converts the value to a string suitable for OOXML.
- ihtml2html: Converts iHTML to HTML.
- get_or_tree: Returns 'gettree' if getattr is True, otherwise returns 'tree'.
- append_class_to_attrs: Appends a class to the object's attributes.
- is_menu_checked: Checks if the URL matches the full path.
- import_var: Imports a variable from a module.
- json_dumps: Serializes the object to JSON.
- only_items_containing: Removes items from the select field that do not contain the mask.
- user_can_change_password: Checks if the user can change their password.
- prefetch_related: Prefetches related objects for the object list.
- append_uuid: Appends a UUID to the variable.
- append_suffix: Appends the suffix to the value.
- remove_suffix: Removes the suffix from the value.
"""

from base64 import b64encode, b64decode
import datetime
import importlib
import uuid

from django import template
from django.urls import reverse
from django.db.models import Count, Max, Min, Sum, Avg
from django.utils import formats
import markdown


from pytigon_lib.schdjangoext.django_ihtml import ihtml_to_html
from pytigon_lib.schtools.wiki import wiki_from_str, make_href, wikify
from pytigon_lib.schtools.schjson import json_dumps


from django_bootstrap5.forms import render_form

register = template.Library()


# tools


@register.filter(name="class_name")
def class_name(value):
    """Returns the class name of the value."""
    try:
        return value.__class__.__name__
    except AttributeError:
        return ""


@register.filter(name="to_console")
def to_console(value):
    """Prints the value to the console and returns an empty string."""
    print(value)
    return ""


@register.filter(name="is_private")
def is_private(value):
    """Checks if the function is private."""
    return value.startswith("_")


@register.filter(name="get_value")
def get_value(value, argv):
    """Returns value[argv] if value is a dictionary, otherwise returns an empty string."""
    if isinstance(value, dict):
        return value.get(argv, "")
    try:
        return value[argv]
    except (TypeError, KeyError, IndexError):
        return ""


@register.filter(name="get_attr")
def get_attr(value, attr):
    """Returns getattr(value, attr) if possible, otherwise returns None."""
    try:
        return getattr(value, attr)
    except AttributeError:
        return None


@register.filter(name="range")
def _range(value):
    """Returns a list of integers from 0 to int(value) - 1."""
    try:
        return list(range(int(value)))
    except (ValueError, TypeError):
        return []


@register.filter(name="dir")
def f_dir(value):
    """Returns the list of attributes of the value."""
    return dir(value)


@register.filter(name="split")
def filter_split(obj, sep=";"):
    """Splits the object by the separator and returns the result."""
    return obj.split(sep)


@register.filter(name="feval")
def _eval(value):
    """Evaluates the value as a Python expression."""
    try:
        return eval(value)
    except (SyntaxError, NameError):
        return ""


@register.filter(name="left")
def left(value, arg):
    """Returns the leftmost 'arg' characters of the value."""
    try:
        return str(value)[: int(arg)]
    except (ValueError, TypeError):
        return value


@register.filter(name="truncate")
def truncate(value, arg):
    """Truncates the value to 'arg' characters, appending '...' if necessary."""
    try:
        retstr = str(value)
    except:
        retstr = unicode(value)

    if len(retstr) > int(arg):
        return retstr[: int(arg) - 3] + "..."
    else:
        return retstr


@register.filter(name="first_elem")
def first_elem(value, sep="/"):
    """Splits the value by the separator and returns the first element."""
    return value.split(sep)[0]


@register.filter(name="last_elem")
def last_elem(value, sep="/"):
    """Splits the value by the separator and returns the last element."""
    return value.split(sep)[-1]


@register.filter(name="penultimate_elem")
def penultimate_elem(value, sep="/"):
    """Splits the value by the separator and returns the penultimate element."""
    x = value.split(sep)
    return x[-2] if len(x) > 1 else ""


@register.filter(name="first_section")
def first_section(html):
    """Returns the part of the string before '$$$'."""
    return html.split("$$$")[0] if html else ""


@register.filter(name="second_section")
def second_section(html):
    """Returns the part of the string after '$$$'."""
    if html:
        x = html.split("$$$")
        return x[1] if len(x) > 1 else ""
    return ""


@register.filter(name="replace")
def replace(value, replace_str):
    """replace_str: 'old_value|new_value'"""
    l = replace_str.split("|")
    return value.replace(l[0], l[1]) if len(l) == 2 else value


@register.filter(name="nbsp")
def nbsp(value):
    """Replaces spaces with '&nbsp;'."""
    return value.replace(" ", "&nbsp;")


@register.filter(name="hasattr")
def filter_hasattr(obj, attr_name):
    """Checks if the object has the specified attribute."""
    return hasattr(obj, attr_name)


@register.filter(name="has_ext")
def has_ext(value, arg):
    """Checks if the value ends with the specified extension."""
    return value.lower().endswith(arg.lower())


@register.filter(name="append_get_param")
def append_get_param(href, param):
    """Appends a GET parameter to the href."""
    return f"{href}&{param}" if "?" in href else f"{href}?{param}"


@register.filter(name="call")
def _call(obj, method_name):
    """Calls the method on the object if it exists."""
    if hasattr(obj, method_name):
        method = getattr(obj, method_name)
        if hasattr(obj, "__callArg"):
            param = obj.__callArg
            del obj.__callArg
            return method(*param)
        return method()
    return ""


@register.filter(name="args")
def args(obj, arg):
    """Adds an argument to the object's __callArg list."""
    if not hasattr(obj, "__callArg"):
        obj.__callArg = []
    obj.__callArg += [arg]
    return obj


@register.filter(name="call_with")
def call_with(proxy, arg):
    """Calls the proxy's call method with the argument."""
    return proxy.call(arg)


# Conversion functions


@register.filter(name="bencode")
def bencode(value):
    """Returns the base64 encoded value."""
    return (
        b64encode(value.encode("utf-8")).decode("utf-8")
        if value
        else b64encode(b"").decode("utf-8")
    )


@register.filter(name="bdecode")
def bdecode(value):
    """Returns the base64 decoded value."""
    return b64decode(value.encode("utf-8")).decode("utf-8")


@register.filter(name="to_str")
def to_str(value):
    """Converts the value to a string."""
    try:
        return str(value)
    except (ValueError, TypeError):
        return ""


@register.filter(name="none_to_empty")
def none_to_empty(value):
    """Converts None to an empty string, otherwise converts the value to a string."""
    return str(value) if value else ""


@register.filter(name="to_int")
def to_int(value):
    """Converts the value to an integer."""
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0


@register.filter(name="to_float")
def to_float(value):
    """Converts the value to a float."""
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0


@register.filter(name="num2str")
def num2str(value):
    """Converts the number to a string, replacing commas with dots and removing spaces."""
    return str(value).replace(",", ".").replace(" ", "")


@register.filter(name="format")
def format(value, id):
    """Formats the value using the specified format string."""
    return value % id


@register.filter(name="genericfloatformat")
def genericfloatformat(text, arg="{: .2f}"):
    """Formats the float value using the specified format string."""
    try:
        f = float(text)
        if ": " in arg:
            space_convert = True
            arg2 = arg.replace(": ", ":,")
        else:
            arg2 = arg
        x = arg2.format(f)
        if space_convert:
            return x.replace(",", " ")
        else:
            return ""
    except ValueError:
        return ""


@register.filter(name="genericfloatnullformat")
def genericfloatnullformat(text, arg="{: .2f}"):
    """Formats the float value, returning '-' if the value is zero or invalid."""
    try:
        f = float(text)
        return "-" if not f else genericfloatformat(text, arg)
    except ValueError:
        return "-"


@register.filter(name="floatformat2")
def floatformat2(text):
    """Formats the float value to 2 decimal places."""
    return genericfloatformat(text, "{: .2f}")


@register.filter(name="floatformat3")
def floatformat3(text):
    """Formats the float value to 3 decimal places."""
    return genericfloatformat(text, "{: .3f}")


@register.filter(name="floatnullformat")
def floatnullformat(text):
    """Formats the float value to 2 decimal places, returning '-' if the value is zero or invalid."""
    return genericfloatnullformat(text, "{: .2f}")


@register.filter(name="floatnullformat3")
def floatnullformat3(text):
    """Formats the float value to 3 decimal places, returning '-' if the value is zero or invalid."""
    return genericfloatnullformat(text, "{: .3f}")


@register.filter(name="amount")
def amount(text):
    """Formats the amount with thousand separators."""
    try:
        f = float(text)
    except ValueError:
        return ""
    if f == 0.0:
        return "-  "

    def split_len(seq, length):
        return [seq[i : i + length] for i in range(0, len(seq), length)]

    s = "%.02f" % f
    t = s.split(".")
    return " ".join(split_len(t[0][::-1], 3))[::-1] + "." + t[1]


def parse_locale_date(formatted_date):
    """Parses a locale-specific date string into a datetime object."""
    for date_format in formats.get_format("DATE_INPUT_FORMATS"):
        try:
            parsed_date = datetime.datetime.strptime(formatted_date, date_format)
        except ValueError:
            continue
        else:
            break
    if not parsed_date:
        raise ValueError
    return parsed_date


@register.filter(name="isoformat")
def isoformat(value):
    """Formats the value as an ISO date string."""
    if value:
        if isinstance(value, str):
            value2 = parse_locale_date(value)
        else:
            value2 = value
        try:
            iso = value2.isoformat()[:19].replace("T", " ")
            if isinstance(value, str) and len(value) <= 10:
                return iso[:10]
            else:
                return iso
        except:
            return value
    else:
        return ""


@register.filter(name="sysisoformat")
def sysisoformat(value):
    """Formats the value as an ISO date string, handling system-specific formats."""
    if value:
        try:
            if type(value) == str:
                x = value[:10].replace("-", " ").replace(".", " ").split(" ")
                if len(x[0]) == 4:
                    x2 = value[:10]
                elif len(x[2]) == 4:
                    x2 = x[2] + "-" + x[1] + "-" + x[0]
                else:
                    x2 = value[:10]
                iso = x2 + value[10:].replace(" ", "T")
            else:
                value2 = value
                iso = value2.isoformat()[:19].replace(" ", "T")
            return iso
        except:
            return value.replace(" ", "T")
    else:
        return ""


@register.filter(name="isoformat_short")
def isoformat_short(value):
    """Formats the value as a short ISO date string."""
    return value.isoformat()[:16].replace("T", " ") if value else ""


@register.filter(name="d_isoformat")
def d_isoformat(value):
    """Formats the value as an ISO date string (date only)."""
    return value.isoformat()[:10] if value else ""


@register.filter(name="one_line_block")
def one_line_block(value):
    """Cleans the value by removing unnecessary spaces and characters."""
    return (
        value.replace("        ", " ")
        .replace("    ", " ")
        .replace("  ", " ")
        .replace("\n", "")
        .replace("\t", "")
    )


@register.filter(name="one_line_code")
def one_line_code(value):
    """Cleans the value by removing newlines and tabs."""
    return value.replace("\n", "").replace("\r", "").replace("\t", "")


@register.filter(name="clean")
def clean(value):
    """Cleans the value by removing unnecessary spaces and characters."""
    return " ".join(value.replace("\n", "").replace("\t", "").split())


# Arithmetic operations


@register.filter(name="fadd")
def fadd(value, arg):
    """Returns the sum of value and arg as floats."""
    return float(value) + float(arg)


@register.filter(name="subtract")
def subtract(value, arg):
    """Returns the difference between value and arg as integers."""
    return int(value) - int(arg)


@register.filter(name="fsubtract")
def fsubtract(value, arg):
    """Returns the difference between value and arg as floats."""
    return float(value) - float(arg)


@register.filter(name="multiply")
def multiply(value, arg):
    """Returns the product of value and arg as integers."""
    return int(value) * int(arg)


@register.filter(name="fmultiply")
def fmultiply(value, arg):
    """Returns the product of value and arg as floats."""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return ""


@register.filter(name="divide")
def divide(value, arg):
    """Returns the quotient of value and arg as integers."""
    return int(value) / int(arg)


@register.filter(name="fdivide")
def fdivide(value, arg):
    """Returns the quotient of value and arg as floats."""
    try:
        return float(value) / float(arg) if float(arg) != 0 else ""
    except (ValueError, TypeError):
        return ""


@register.filter(name="append_str")
def append_str(value, s):
    """Appends the string s to the value if s is not None or empty."""
    return value + str(s) if s else value


@register.filter(name="date_inc")
def date_inc(value, arg):
    """Increments the date value by the specified number of days."""
    try:
        date, time = value.split()
        y, m, d = date.split("-")
        return datetime.datetime(int(y), int(m), int(d)) + datetime.timedelta(int(arg))
    except ValueError:
        return None


@register.filter(name="date_dec")
def date_dec(value, arg):
    """Decrements the date value by the specified number of days."""
    try:
        y, m, d = value.split("-")
        return (
            datetime.datetime(int(y), int(m), int(d)) - datetime.timedelta(int(arg))
        ).date()
    except ValueError:
        return None


# Models and fields


@register.filter(name="get_model_fields")
def get_model_fields(value):
    """Returns the fields of the model without many-to-many fields."""
    ret = []
    if value and hasattr(value, "_meta"):
        for f in value._meta.fields:
            if f.name == "id":
                ret.insert(0, f)
            else:
                ret.append(f)
    return ret


@register.filter(name="get_model_meta")
def get_model_meta(value):
    """Returns the _meta attribute of the model."""
    return value._meta if value and hasattr(value, "_meta") else None


@register.filter(name="get_model_app")
def get_model_app(value):
    """Returns the app label of the model."""
    return value._meta.app_label if value and hasattr(value, "_meta") else "x"


@register.filter(name="get_model_row")
def get_model_row(obj):
    """Returns a list of field values for the model instance."""
    if hasattr(obj, "_meta"):
        ret = []
        for field in obj._meta.get_fields():
            if hasattr(obj, field.name):
                if field.name == "id":
                    ret.insert(0, getattr(obj, field.name))
                else:
                    ret.append(getattr(obj, field.name))
        return ret
    else:
        return []


@register.filter(name="get_model_ooxml_row")
def get_model_ooxml_row(obj):
    """Returns a list of field values formatted for OOXML."""
    if hasattr(obj, "_meta"):
        ret = []
        for field in obj._meta.get_fields():
            if hasattr(obj, field.name):
                if field.name == "id":
                    ret.insert(0, ooxml(getattr(obj, field.name)))
                else:
                    ret.append(ooxml(getattr(obj, field.name)))
        return ret
    else:
        return []


@register.filter(name="get_all_model_fields")
def get_all_model_fields(value):
    """Returns all fields of the model, including many-to-many fields."""
    return [f for f in value._meta.fields + value._meta.many_to_many]


@register.filter(name="get_all_model_parents")
def get_all_model_parents(parent):
    """Returns a list of all parent models."""
    ret = []
    while parent:
        ret.append(parent)
        parent = parent.parent
    return ret


@register.filter(name="get_model_fields_names")
def get_model_fields_names(obj):
    """Returns a list of field names for the model instance."""
    ret = []
    for field in obj._meta.get_fields():
        if hasattr(obj, field.name):
            if field.name == "id":
                ret.insert(0, field.name)
            else:
                ret.append(field.name)
    return ret


@register.filter(name="get_model_fields_verbose_names")
def get_model_fields_verbose_names(obj):
    """Returns a list of verbose names for the model fields."""
    if hasattr(obj, "_meta"):
        for field in obj._meta.get_fields():
            if hasattr(obj, field.name):
                if hasattr(field, "verbose_name"):
                    if field.name == "id":
                        ret.insert(0, field.verbose_name)
                    else:
                        ret.append(field.verbose_name)
                else:
                    ret.append(field.name)
    else:
        for i in range(0, len(obj)):
            ret.append("x%d" % i)
    return ret


@register.filter(name="user_in_group")
def user_in_group(user, group_name):
    """Checks if the user is in the specified group."""
    return user.groups.filter(name=group_name).exists()


@register.filter(name="field_as_widget")
def field_as_widget(value, arg):
    """Renders the field as a widget with the specified attributes."""
    d = {}
    l = arg.split(",")
    for x in l:
        x2 = x.split(":")
        d[x2[0]] = x2[1]
    return value.as_widget(attrs=d)


@register.filter(name="model_has_children")
def model_has_children(value):
    """Checks if the model instance has children."""
    if hasattr(value, "has_children"):
        return value.has_children
    set_name = value._meta.model_name
    if hasattr(value, set_name + "_set"):
        o = getattr(value, set_name + "_set")
    else:
        o = getattr(value, "children")
    l = o.all()
    if len(l) > 0:
        return True
    else:
        return False


@register.filter(name="model_can_have_children")
def model_can_have_children(value):
    """Checks if the model instance can have children."""
    if hasattr(value, "can_have_children"):
        if value.can_have_children == False:
            return False
    return True


@register.filter(name="choices_from_field")
def choices_from_field(obj, field):
    """Returns the choices for the specified field."""
    return obj._meta.get_field(field).choices


# HTML


@register.filter(name="reverse")
def _reverse(value):
    """Returns the reversed URL for the given view name."""
    return reverse(value)


@register.filter(name="errormessage")
def errormessage(value):
    """Checks if the value ends with '!'."""

    if value.endswith("!"):
        return True
    else:
        return False


@register.filter(name="aggregate")
def aggregate(objects, field_name):
    """Returns the aggregate value for the specified field."""
    if field_name.startswith("max_"):
        field = field_name[4:]
        x = objects.aggregate(Max(field))
        return x[field + "__max"]
    elif field_name.startswith("min_"):
        field = field_name[4:]
        x = objects.aggregate(Min(field))
        return x[field + "__min"]
    elif field_name.startswith("sum_"):
        field = field_name[4:]
        x = objects.aggregate(Sum(field))
        return x[field + "__sum"]
    elif field_name.startswith("avg_"):
        field = field_name[4:]
        x = objects.aggregate(Avg(field))
        return x[field + "__avg"]
    elif field_name.startswith("count_"):
        field = field_name[6:]
        x = objects.aggregate(Count(field))
        return x[field + "__count"]
    return 0


# Wiki and Markdown


@register.filter(name="wikify")
def _wikify(value, path=None):
    """Converts the value to wiki format."""
    return wikify(value, path)


@register.filter(name="wiki")
def wiki(value):
    """Converts the value to wiki format."""
    return wiki_from_str(value)


@register.filter(name="wiki_href")
def wiki_href(value, section="help"):
    """Converts the value to a wiki link."""
    if section.startswith("+"):
        path = section
        section = "help"
    else:
        path = None
    return make_href(value, section=section, path=path)


@register.filter(name="markdown", is_safe=True)
def _markdown(value):
    """Converts the value to HTML using Markdown."""
    if value:
        return markdown.markdown(
            value,
            extensions=[
                "abbr",
                "attr_list",
                "def_list",
                "fenced_code",
                "footnotes",
                "md_in_html",
                "tables",
                "admonition",
                "codehilite",
            ],
        )
    else:
        return ""


# Forms


@register.filter(name="preferred_enctype")
def _preferred_enctype(form):
    """Returns the preferred enctype for the form."""
    if hasattr(form, "visible_fields"):
        for field in form.visible_fields():
            if type(field.field).__name__ in ("FileField", "ImageField"):
                return "multipart/form-data"
    return "application/x-www-form-urlencoded"


class BootstrapForm:
    def __init__(self, form):
        self.form = form

    def as_p(self):
        """Renders the form as a Bootstrap-styled form."""
        return render_form(self.form)


@register.filter(name="to_bootstrap")
def to_bootstrap(form):
    """Converts the form to a Bootstrap-styled form."""
    return BootstrapForm(form)


@register.filter(name="textfiel_row_col")
def textfiel_row_col(field, arg):
    """Sets the rows and cols attributes for the text field."""
    row, col = arg.split("x")
    field.field.widget.attrs["rows"] = int(row)
    field.field.widget.attrs["cols"] = int(col)
    return field


# Other


def ooxml(value):
    """Converts the value to a string suitable for OOXML."""
    if type(value) in (datetime.datetime, datetime.date):
        if value:
            return value.isoformat()
        else:
            return "0"
    elif type(value) in (float, int):
        if value:
            return str(value)
        else:
            return "0"
    else:
        if value:
            return str(value)
        else:
            return ""


@register.filter(name="ooxml")
def _ooxml(value):
    """Converts the value to OOXML format."""
    return ooxml(value)


@register.filter(name="ihtml2html")
def ihtml2html(html):
    """Converts iHTML to HTML."""
    return ihtml_to_html(None, input_str=html)


@register.filter(name="get_or_tree")
def get_or_tree(getattr):
    """Returns 'gettree' if getattr is True, otherwise returns 'tree'."""
    return "gettree" if getattr else "tree"


@register.filter(name="append_class_to_attrs")
def append_class_to_attrs(obj, arg):
    """Appends a class to the object's attributes."""
    if obj:
        ret = ""
        test = False
        for pos in [x.split("=") for x in obj.split(" ")]:
            if pos[0] == "class":
                test = True
                ret += "%s='%s' " % (
                    "class",
                    pos[1].replace('"', "").replace("'", "") + " " + arg + " ",
                )
            else:
                if len(pos) == 2:
                    ret += "%s=%s " % (pos[0], pos[1])
                else:
                    ret += pos[0] + " "
        if not test:
            ret += "%s='%s' " % ("class", arg + " ")
        return ret[:-1]
    else:
        return "class='%s'" % arg


@register.filter(name="is_menu_checked")
def is_menu_checked(url, full_path):
    """Checks if the URL matches the full path."""
    if url and full_path:
        p = full_path.split("?")[0]
        if len(p) > 0 and p[0] == "/":
            p = p[1:]
        if len(p) > 0 and p[-1] == "/":
            p = p[:-1]

        u = url.split("?")[0]
        if len(u) > 0 and u[0] == "/":
            u = u[1:]
        if len(u) > 0 and u[-1] == "/":
            u = u[:-1]

        if (p in u and "wiki" in p) or u in p:
            return True
        else:
            return False
    else:
        return False


@register.filter(name="import_var")
def _import_var(obj):
    """Imports a variable from a module."""
    path = str(obj)
    base_path, item = path.split(":")
    m = importlib.import_module(base_path)
    return getattr(m, item)


@register.filter(name="json_dumps", is_safe=True)
def _json_dumps(obj):
    """Serializes the object to JSON."""
    return json_dumps(obj)


@register.filter(name="only_items_containing")
def only_items_containing(select_field, mask):
    """Removes items from the select field that do not contain the mask."""
    if mask:
        to_delete = []
        for item in select_field.field.widget.choices:
            if not mask in item[0]:
                to_delete.append(item)
        for item in to_delete:
            select_field.field.widget.choices.remove(item)
    return ""


@register.filter(name="user_can_change_password")
def user_can_change_password(user):
    """Checks if the user can change their password."""
    try:
        from allauth.account.models import EmailAddress
    except:
        return True

    object_list = EmailAddress.objects.filter(user=user)
    if len(object_list) > 0:
        return False
    else:
        return True


@register.filter(name="prefetch_related")
def prefetch_related(object_list, param):
    """Prefetches related objects for the object list."""
    l = object_list
    for related in param.replace(",", ";").split(";"):
        if related:
            l = l.prefetch_related(related)
    return l


@register.filter(name="append_uuid")
def append_uuid(var):
    """Appends a UUID to the variable."""
    return str(var) + str(uuid.uuid4())


@register.filter(name="append_suffix")
def append_suffix(value, s):
    """Appends the suffix to the value."""
    if s == None or s == "":
        return value
    else:
        if value.endswith(s):
            return value
        else:
            return value + str(s)


@register.filter(name="remove_suffix")
def remove_suffix(value, s):
    """Removes the suffix from the value"""
    if s == None or s == "":
        return value
    else:
        if value.endswith(s):
            return value[: -len(s)]
        else:
            return value
