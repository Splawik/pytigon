from pytigon_lib.schindent.indent_markdown import BaseObjRenderer, IndentMarkdownProcessor, register_obj_renderer
from pytigon_lib.schdjangoext.django_ihtml import ihtml_to_html


class IHtmlProcessor(IndentMarkdownProcessor):
    def render_wiki(self, ihtml_source):
        return ihtml_to_html(None, ihtml_source)


class IHtmlObjRenderer(BaseObjRenderer):
    
    @staticmethod
    def get_info():
        return { "name": "ihtml", "title": "IHtml", "icon": "fa fa-indent", "show_form": False, }

    def gen_context(self, param, lines):
        if lines:
            ihtml_processor = IHtmlProcessor()
            return { 'content': ihtml_processor.convert_to_html("\n".join(lines)), 'param': param }
        return { 'content': "", 'param': param }

register_obj_renderer("ihtml", IHtmlObjRenderer)


class HtmlObjRenderer(BaseObjRenderer):

    @staticmethod
    def get_info():
        return { "name": "html", "title": "Html", "icon": "fa fa-file-code-o", "show_form": False,}

    def gen_context(self, param, lines):
        if lines:
            return { 'content': "\n".join(lines) }
        return { 'content': "" }

register_obj_renderer("html", HtmlObjRenderer)


class BaseMarkdownObjRenderer(BaseObjRenderer):
    def gen_context(self, param, lines):
        if lines:
            i_markdown_processor = IndentMarkdownProcessor()
            return { 'content': i_markdown_processor.convert_to_html("\n".join(lines)) }
        return { 'content': "" }


DIV_OBJ_RENDERER_FORM = """
class
style
"""

class DivObjRenderer(BaseMarkdownObjRenderer):

    @staticmethod
    def get_info():
        return { "name": "div", "title": "Div", "icon": "fa fa-tag", "show_form": True,}

    def get_edit_form(self):
        return DIV_OBJ_RENDERER_FORM

    def render(self, param, lines):
        context = self.get_context(param, lines)
        out = "<div"
        for key,value in context['param'].values():
            if value:
                out += f" {key}='{value}'"
        out += ">\n" + context['content'] + "\n</div>\n"
        return out

register_obj_renderer("div", DivObjRenderer)


class HasPermObjRenderer(BaseMarkdownObjRenderer):

    @staticmethod
    def get_info():
        return { "name": "has_perm", "title": "Permission", "icon": "fa fa-key", "show_form": True,}

    def get_edit_form(self):
        return "perm"

    def render(self, param, lines):
        context = self.get_context(param, lines)
        out = "{% if perms." + context['param']['perm'] + "%}\n"
        out += context['content'] + "\n{% endif %}\n"
        return out

register_obj_renderer("has_perm", HasPermObjRenderer)
