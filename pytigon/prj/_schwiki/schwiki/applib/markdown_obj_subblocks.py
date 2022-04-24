from pytigon_lib.schindent.indent_markdown import BaseObjRenderer, IndentMarkdownProcessor, register_obj_renderer
from pytigon_lib.schdjangoext.django_ihtml import ihtml_to_html


class IHtmlProcessor(IndentMarkdownProcessor):
    def render_wiki(self, ihtml_source):
        return ihtml_to_html(None, ihtml_source)


class IHtmlObjRenderer(BaseObjRenderer):
    
    @staticmethod
    def get_info():
        return { "name": "ihtml", "title": "IHtml", "icon": "fa fa-indent", "show_form": False, 'inline_content': True }

    def gen_context(self, param, lines):
        if lines:
            ihtml_processor = IHtmlProcessor()
            return { 'content': ihtml_processor.convert_to_html("\n".join(lines)), 'param': param }
        return { 'content': "", 'param': param }

register_obj_renderer("ihtml", IHtmlObjRenderer)


class HtmlObjRenderer(BaseObjRenderer):

    @staticmethod
    def get_info():
        return { "name": "html", "title": "Html", "icon": "fa fa-file-code-o", "show_form": False, 'inline_content': True }

    def gen_context(self, param, lines):
        if lines:
            return { 'content': "\n".join(lines) }
        return { 'content': "" }

register_obj_renderer("html", HtmlObjRenderer)


class BaseMarkdownObjRenderer(BaseObjRenderer):
    def gen_context(self, param, lines):
        if lines:
            i_markdown_processor = IndentMarkdownProcessor()
            return { 'content': i_markdown_processor.convert_to_html("\n".join(lines)), "param": param }
        return { 'content': "", "param": param }


DIV_OBJ_RENDERER_FORM = """
class
style
"""

class DivObjRenderer(BaseMarkdownObjRenderer):

    @staticmethod
    def get_info():
        return { "name": "div", "title": "Div", "icon": "fa fa-tag", "show_form": True, 'inline_content': True }

    def get_edit_form(self):
        return DIV_OBJ_RENDERER_FORM

    def render(self, param, lines):
        context = self.gen_context(param, lines)
        out = "<div"
        for key,value in context['param'].values():
            if value:
                out += f" {key}='{value}'"
        out += ">\n" + context['content'] + "\n</div>\n"
        return out

register_obj_renderer("div", DivObjRenderer)


TABLE_OBJ_RENDERER_FORM = """
tablestyle::[
-
primary
secondary
success
danger
warning
info
light
dark
]
borderstyle::[
-
borderless
bordered
bordered border-primary
bordered secondary
bordered success
bordered danger
bordered warning
bordered info
bordered light
bordered dark
]
narrow?
striped?
hover?
small?
responsive?
"""

class TableObjRenderer(BaseMarkdownObjRenderer):

    @staticmethod
    def get_info():
        return { "name": "table", "title": "Table", "icon": "fa fa-table", "show_form": True, 'inline_content': True }

    def get_edit_form(self):
        return TABLE_OBJ_RENDERER_FORM

    def render(self, param, lines):
        context = self.gen_context(param, lines)
        table_class = "table"
        if context['param']['tablestyle'] and context['param']['tablestyle'] != '-':
            table_class += ' table-' + context['param']['tablestyle']
        if context['param']['borderstyle'] and context['param']['borderstyle'] != '-':
            table_class += ' table-' + context['param']['borderstyle']
        if context['param']['striped']:
            table_class += ' table-striped'
        if context['param']['hover']:
            table_class += ' table-hover'
        if context['param']['small']:
            table_class += ' table-small'
        if context['param']['narrow']:
            out = context['content'].replace("<table>", "<table class='%s' style='width:auto'>" % table_class)
        else:
            out = context['content'].replace("<table>", "<table class='%s'>" % table_class)            
        if context['param']['responsive']:
            out = "<div class='table-responsive'>" + out + "</div>"
        return out

register_obj_renderer("table", TableObjRenderer)


class HasPermObjRenderer(BaseMarkdownObjRenderer):

    @staticmethod
    def get_info():
        return { "name": "has_perm", "title": "Permission", "icon": "fa fa-key", "show_form": True, 'inline_content': True }

    def get_edit_form(self):
        return "perm"

    def render(self, param, lines):
        context = self.gen_context(param, lines)
        out = "{% if perms." + context['param']['perm'] + "%}\n"
        out += context['content'] + "\n{% endif %}\n"
        return out

register_obj_renderer("has_perm", HasPermObjRenderer)
