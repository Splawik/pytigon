"""Form template tags for Pytigon exsyntax library."""

from functools import lru_cache

from django import forms, template
from django.forms import CheckboxInput, CheckboxSelectMultiple, FileInput, RadioSelect
from django.template.base import Node, token_kwargs
from django.utils.safestring import SafeText, mark_safe
from django_select2 import forms as s2forms

from pytigon_lib.schdjangoext.models import TreeModel
from pytigon_lib.schdjangoext.tools import import_model, make_href
from pytigon_lib.schtools.href_action import action_fun

register = template.Library()


@lru_cache(maxsize=256)
def _get_form_template(template_str):
    """Compile and cache a Django Template from a string.

    Avoids recompiling the same form template on every render call.
    """
    return template.Template(template_str)


@register.inclusion_tag("widgets/field.html")
def field(context, form_field, fieldformat=None, inline=False):
    field_obj = context["form"][form_field] if type(form_field) in (SafeText, str) else form_field

    label_class = "control-label float-left"
    offset = ""
    form_group_class = f"form-group group_{type(field_obj.field).__name__.lower()}"
    form_group_size_class = " col-sm-12 col-md-12"
    field_class = f"controls float-left {type(field_obj.field).__name__.lower()}"
    placeholder = ""
    show_label = True

    addon_after = ""
    addon_before = ""
    addon_after_class = ""
    addon_before_class = ""

    ff = None
    if fieldformat:
        ff = fieldformat
    else:
        if "formformat" in context:
            ff = context["formformat"]
        if not ff:
            ff = "12:3:3/12:12:12"
    hidden = False

    if ff == "!":
        hidden = True
    else:
        x = ff.split("/", 2)
        if len(x) < 2:
            return {}

        if x[0] == "^":
            form_group_class += " form-floating"
            field_class += " col-12"
            if not placeholder:
                placeholder = field_obj.label
        elif x[0] == "-":
            form_group_class += " label-over-field"
            field_class += " col-12"
        elif not x[0]:
            placeholder = field_obj.label
            show_label = False
            field_class += " col-12"
        else:
            y = [int(pos) for pos in x[0].split(":")]
            if len(y) == 3:
                label_class += f" col-sm-{y[0]} col-md-{y[1]} col-lg-{y[2]}"
                field_class += f" col-sm-{(11 - y[0]) % 12 + 1} col-md-{(11 - y[1]) % 12 + 1} col-lg-{(11 - y[2]) % 12 + 1}"
                offset = f" offset-sm-{y[0] % 12} offset-md-{y[1] % 12} offset-lg-{y[2] % 12}"
            else:
                label_class += f" col-sm-12 col-md-{y[0]}"
                field_class += f" col-sm-12 col-md-{(11 - y[0]) % 12 + 1}"
                offset = f"offset-sm-0 offset-md-{y[0] % 12}"

        if not inline:
            form_group_class += " mb-2"

        if x[1]:
            y = x[1].split(":")
            if len(y) == 3:
                form_group_size_class = f"col-sm-{y[0]} col-md-{y[1]} col-lg-{y[2]}"
            else:
                form_group_size_class = f" col-sm-12 col-md-{y[0]}"
            form_group_class += " " + form_group_size_class

        if len(x) > 2:
            addon = x[2]
            if addon:
                if addon.startswith("(-X)"):
                    addon_after = addon[4:]
                    addon_after_class = "input-group-btn"
                elif addon.startswith("(X-)"):
                    addon_before = addon[4:]
                    addon_before_class = "input-group-btn"
                elif addon.startswith("(-x)"):
                    addon_after = addon[4:]
                    addon_after_class = "input-group-addon"
                elif addon.startswith("(x-)"):
                    addon_before = addon[4:]
                    addon_before_class = "input-group-addon"

        if offset and type(field_obj.field.widget) in (
            CheckboxInput,
            RadioSelect,
            CheckboxSelectMultiple,
            FileInput,
        ):
            field_class += " " + offset

    ret = {}
    ret["form"] = context["form"]
    ret["field"] = field_obj
    ret["hidden"] = hidden
    ret["label_class"] = label_class
    ret["form_group_class"] = form_group_class
    ret["form_group_size_class"] = form_group_size_class
    ret["field_class"] = field_class
    ret["placeholder"] = placeholder
    ret["addon_after"] = addon_after
    ret["addon_after_class"] = addon_after_class
    ret["addon_before"] = addon_before
    ret["addon_before_class"] = addon_before_class
    ret["show_label"] = show_label
    ret["standard_web_browser"] = context["standard_web_browser"]
    ret["server_side_validation"] = (
        False
        if "server_side_validation" in context
        and context["server_side_validation"] == False
        else True
    )
    return ret


class Form(Node):
    def __init__(self, nodelist, def_param, param, inline=False):
        self.nodelist = nodelist
        self.def_param = def_param
        self.param = []
        if inline:
            self.inline = 1
        else:
            self.inline = 0
        for pos in param:
            self.param.append(template.Variable(pos))

    def render(self, context):
        output = self.nodelist.render(context).strip()

        form = context["form"]
        fields = []
        if output:
            if "((" in output:
                output_tab = []
                x = output.split("((")
                if x[0]:
                    value = x[0].strip().replace('"', "'").replace(";", "','")
                    if value:
                        output_tab.append(value)
                for item in x[1:]:
                    y = item.split("))")
                    output_tab.append("@" + y[0])
                    if len(y) > 1 and y[1]:
                        value = y[1].strip().replace('"', "'").replace(";", "','")
                        if value:
                            output_tab.append(value)
            else:
                output_tab = (output.replace('"', "'").replace(";", "','"),)

            for item in output_tab:
                if item.startswith("@"):
                    fields.append(item[1:])
                else:
                    for f in item.split(","):
                        x = f.split(":", 1)
                        name = x[0].replace("'", "").strip()
                        if len(x) > 1:
                            p = x[1]
                        elif len(self.param) > 1:
                            p = self.param[1].resolve(context)
                        else:
                            p = self.def_param
                        fields.append([name, p])
        else:
            for field in form:
                p = self.param[1].resolve(context) if len(self.param) > 1 else self.def_param
                fields.append([field.name, p])
        if self.def_param == "^/":
            template_str = "{% load exsyntax %}<div class='d-inline-flex flex-wrap'>"
        else:
            template_str = "{% load exsyntax %}<div class='row'>"
        for field in fields:
            if isinstance(field, str):
                template_str += field
            else:
                template_str += f"{{% field '{field[0]}' '{field[1]}' {self.inline} %}}"
            template_str += "</div>"
        t = _get_form_template(template_str)
        return t.render(context)


@register.tag
def form(parser, token):
    parm = token.split_contents()
    nodelist = parser.parse("endform")
    parser.delete_first_token()
    return Form(nodelist, "12:3:3/12:12:12", parm)


@register.tag
def vert_form(parser, token):
    parm = token.split_contents()
    nodelist = parser.parse(("endvert_form",))
    parser.delete_first_token()
    return Form(nodelist, "^/12", parm)


@register.tag
def inline_form(parser, token):
    parm = token.split_contents()
    nodelist = parser.parse(("endinline_form",))
    parser.delete_first_token()
    return Form(nodelist, "^/", parm, inline=True)


@register.tag
def col2_form(parser, token):
    parm = token.split_contents()
    nodelist = parser.parse(("endcol2_form",))
    parser.delete_first_token()
    return Form(nodelist, "^/12:6:6", parm)


class FormItemNode(Node):
    def __init__(self, nodelist, field_name, tag):
        self.nodelist = nodelist
        self.field_name = field_name
        self.tag = tag

    def render(self, context):
        x = self.nodelist.render(context)
        if "|" in x:
            pos = x.find("|")
            title = x[:pos].strip()
            content = x[pos + 1 :]
        else:
            title = context["form"][self.field_name].label
            content = x

        if not content:
            content = str(context["form"][self.field_name])

        if self.tag:
            elem0 = f""" <{self.tag} class="{self.field_name} form-control" name="{self.field_name}" id="id_{self.field_name}"> """
            elem1 = f"</{self.tag}>"
        else:
            elem0 = ""
            elem1 = ""

        ret = f"""
            <div id="div_id_{self.field_name}" class="form-group">
                <label for="id_{self.field_name}" class="control-label">{title}</label>
                <div class="controls">{elem0}{content}{elem1}</div>
            </div>
        """

        return ret


@register.tag
def form_item(parser, token):
    field_name = token.contents[10:]
    tag = None
    if "." in field_name:
        tmp = field_name.split(".")
        tag = tmp[1]
        field_name = tmp[0]
    nodelist = parser.parse(("endform_item",))
    parser.delete_first_token()
    return FormItemNode(nodelist, field_name, tag)


@register.inclusion_tag("widgets/get_table_row.html")
def get_table_row(
    context,
    field_or_name,
    app_name=None,
    table_name=None,
    search_fields=None,
    filter=None,
    label=None,
    initial=None,
    is_get_button=True,
    is_new_button=False,
    get_target="popup_edit",
    new_target="inline",
):
    if type(field_or_name) in (
        SafeText,
        str,
    ):
        model = import_model(app_name, table_name)
        _name = field_or_name
        _app_name = app_name
        _table_name = table_name
        _initial = initial
        _label = label if label else table_name
        _queryset = None
        _search_fields = search_fields
    else:
        _queryset = field_or_name.field.queryset
        model = _queryset.model
        _name = field_or_name.name
        _app_name = app_name if app_name else _queryset.model._meta.app_label
        _table_name = table_name if table_name else _queryset.model._meta.object_name
        _initial = initial if initial else field_or_name.initial
        _label = label if label else field_or_name.label
        if search_fields:
            _search_fields = search_fields
        else:
            if hasattr(field_or_name, "search_fields"):
                _search_fields = field_or_name.search_fields
            else:
                _search_fields = "name__icontains"

    formformat = context["formformat"] if "formformat" in context else "12:3:3/12:12:12"

    if TreeModel in model.__bases__:
        if filter:
            href1 = make_href(
                f"/{_app_name}/table/{_table_name}/{filter}/0/form/gettree/"
            )
            href2 = make_href(f"/{_app_name}/table/{_table_name}/-/add/")
        else:
            href1 = make_href(f"/{_app_name}/table/{_table_name}/0/form/gettree/")
            href2 = make_href(f"/{_app_name}/table/{_table_name}/-/add/")
    else:
        _filter = filter if filter else "-"
        href1 = make_href(
            f"/{_app_name}/table/{_table_name}/{_filter}/form/get/"
        )
        href2 = make_href(f"/{_app_name}/table/{_table_name}/{_filter}/add/")

    class _Form(forms.Form):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields[_name] = forms.ChoiceField(
                widget=s2forms.ModelSelect2Widget(
                    model=model,
                    search_fields=[
                        _search_fields,
                    ],
                    queryset=_queryset,
                    attrs={"href1": href1, "href2": href2},
                ),
            )

    form = _Form(initial={_name: _initial})
    return {
        "form": form,
        "field": form[_name],
        "formformat": formformat,
        "href1": href1,
        "href2": href2,
    }
