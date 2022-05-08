from pytigon_lib.schindent.indent_markdown import BaseObjRenderer, IndentMarkdownProcessor, register_obj_renderer
from pytigon_lib.schdjangoext.django_ihtml import ihtml_to_html
from pytigon_lib.schfs.vfstools import get_temp_filename
from pytigon_lib.schtools.tools import bencode, bdecode
from django.template import Template, Context
import os
import csv

class IHtmlProcessor(IndentMarkdownProcessor):
    def render_wiki(self, ihtml_source):
        return ihtml_to_html(None, ihtml_source)


class IHtmlObjRenderer(BaseObjRenderer):
    
    @staticmethod
    def get_info():
        return { "name": "ihtml", "title": "IHtml", "icon": "fa fa-indent", "show_form": False, 'inline_content': True }

    def gen_context(self, param, lines, output_format, parent_processor):
        if lines:
            ihtml_processor = IHtmlProcessor(output_format="html", parent_processor=parent_processor)
            return { 'content': ihtml_processor.convert("\n".join(lines)), 'param': param }
        return { 'content': "", 'param': param }

register_obj_renderer("ihtml", IHtmlObjRenderer)


class HtmlObjRenderer(BaseObjRenderer):

    @staticmethod
    def get_info():
        return { "name": "html", "title": "Html", "icon": "fa fa-code", "show_form": False, 'inline_content': True }

    def gen_context(self, param, lines, output_format, parent_processor):
        if lines:
            return { 'content': "\n".join(lines) }
        return { 'content': "" }

register_obj_renderer("html", HtmlObjRenderer)


class BaseMarkdownObjRenderer(BaseObjRenderer):
    def gen_context(self, param, lines, output_format, parent_processor):
        if lines:
            i_markdown_processor = IndentMarkdownProcessor(output_format=output_format, parent_processor=parent_processor)
            return { 'content': i_markdown_processor.convert("\n".join(lines)), "param": param }
        return { 'content': "", "param": param }


class DivObjRenderer(BaseMarkdownObjRenderer):

    @staticmethod
    def get_info():
        return { "name": "div", "title": "Div", "icon": "fa fa-tag", "show_form": True, 'inline_content': True }

    def get_edit_form(self):
        return "attributes"

    def render(self, param, lines, output_format, parent_processor):
        context = self.gen_context(param, lines, output_format, parent_processor)
        out = "<div style='position:relative;'>" + self.edit_on_page_link(parent_processor) + "</div><div " + context['param']['attributes'] + ">\n" + context['content'] + "</div>\n"
        return out

register_obj_renderer("div", DivObjRenderer)


class AjaxObjRenderer(BaseMarkdownObjRenderer):

    @staticmethod
    def get_info():
        return { "name": "ajax-frame", "title": "Ajax frame", "icon": "fa fa-arrows-v", "show_form": False, 'inline_content': True }

    def render(self, param, lines, output_format, parent_processor):
        context = self.gen_context(param, lines, output_format, parent_processor)
        return "<div class='ajax-region ajax-frame' data-region='wiki'>\n" + context['content'] + "\n</div>\n"

register_obj_renderer("ajax-frame", AjaxObjRenderer)


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

    def render(self, param, lines, output_format, parent_processor):
        context = self.gen_context(param, lines, output_format, parent_processor)

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
            out = "<div class='table-responsive' style='position:relative;'>" + self.edit_on_page_link(parent_processor, right=True) + out + "</div>"
        else:
            out = "<div style='position:relative;'>" + self.edit_on_page_link(parent_processor, right=True) + out + "</div>"
        return out

register_obj_renderer("table", TableObjRenderer)


class CsvObjRenderer(TableObjRenderer):

    @staticmethod
    def get_info():
        return { "name": "csv", "title": "CSV", "icon": "fa fa-columns", "show_form": True, 'inline_content': True }

    def gen_context(self, param, lines, output_format, parent_processor):
        if lines:
            out = "<table>"
            csv_reader = csv.reader(lines)
            for row in csv_reader:
                out += "<tr>"
                for item in row:
                    out += "<td>"
                    out += str(item)
                    out += "</td>"
                out += "</tr>"
            out += "</table>"
            return { 'content': out, "param": param }
        return { 'content': "", "param": param }

register_obj_renderer("csv", CsvObjRenderer)


class RowObjRenderer(BaseMarkdownObjRenderer):

    @staticmethod
    def get_info():
        return { "name": "row", "title": "Row", "icon": "fa fa-arrows-h", "show_form": False, 'inline_content': True }

    def render(self, param, lines, output_format, parent_processor):
        context = self.gen_context(param, lines, output_format, parent_processor)
        return "<div class='row'>\n" + context['content'] + "\n</div>\n"
        return out

register_obj_renderer("row", RowObjRenderer)


COL_OBJ_RENDERER_FORM = """
lg//width for large screen::[-,1,2,3,4,5,6,7,8,9,10,11,12]
md//widt for medium_screen::[-,1,2,3,4,5,6,7,8,9,10,11,12]
sm//width small screen::[-,1,2,3,4,5,6,7,8,9,10,11,12]
"""

class ColObjRenderer(BaseMarkdownObjRenderer):
    @staticmethod
    def get_info():
        return {
            "name": "col",
            "title": "Col",
            "icon": "fa fa-angle-double-right",
            "show_form": True,
            "inline_content": True,
        }

    def get_edit_form(self):
        return COL_OBJ_RENDERER_FORM

    def render(self, param, lines, output_format, parent_processor):
        context = self.gen_context(param, lines, output_format, parent_processor)
        c = ""
        if context["param"]["lg"] != "-":
            c += " col-lg-" + str(context["param"]["lg"])
        if context["param"]["md"] != "-":
            c += " col-md-" + str(context["param"]["md"])
        if context["param"]["sm"] != "-":
            c += " col-" + str(context["param"]["sm"])
        return "<div class='" + c[1:] + " position-relative'>\n" + self.edit_on_page_link(parent_processor) + context["content"] + "\n</div>\n"


register_obj_renderer("col", ColObjRenderer)


class HasPermObjRenderer(BaseMarkdownObjRenderer):

    @staticmethod
    def get_info():
        return { "name": "has_perm", "title": "Permission", "icon": "fa fa-key", "show_form": True, 'inline_content': True }

    def get_edit_form(self):
        return "perm"

    def render(self, param, lines, output_format, parent_processor):
        context = self.gen_context(param, lines, output_format, parent_processor)
        out = "{% if perms." + context['param']['perm'] + "%}\n"
        out += context['content'] + "\n{% endif %}\n"
        return out

register_obj_renderer("has_perm", HasPermObjRenderer)


class LangObjRenderer(BaseMarkdownObjRenderer):

    @staticmethod
    def get_info():
        return { "name": "language", "title": "Language", "icon": "fa fa-language", "show_form": True, 'inline_content': True }

    def get_edit_form(self):
        return "language"

    def render(self, param, lines, output_format, parent_processor):
        context = self.gen_context(param, lines, output_format, parent_processor)
        lang = context['param']['language']
        if lang.startswith("!"):
            out = "{% if lang not in '" + lang + "' %}\n"
        else:
            out = "{% if lang in '" + lang + "' %}\n"
        out += context['content'] + "\n{% endif %}\n"
        return out

register_obj_renderer("language", LangObjRenderer)


GRAPHVIZ_OBJ_RENDERER_FORM = """
svg_attr_class//SVG class
svg_style//SVG style
"""

class GraphvizObjRenderer(BaseObjRenderer):
    
    @staticmethod
    def get_info():
        return { "name": "graphviz", "title": "Graphviz", "icon": "fa fa-sitemap", "show_form": True, 'inline_content': True}
    
    def get_edit_form(self):
        return GRAPHVIZ_OBJ_RENDERER_FORM

    def gen_context(self, param, lines, output_format, parent_processor):
        import graphviz
        import lxml.etree as et
        context = {"param": param}
        if lines:
            file_name = get_temp_filename()
            src = graphviz.Source("\n".join(lines))
            file_name2 = src.render(file_name, view=False, format="svg")
            x = ""
            with open(file_name2, "rt") as f:
                x = f.read()
                tree = et.fromstring(x.encode("utf-8"))
                tree.attrib.pop("width")
                tree.attrib.pop("height")
                if "svg_style" in param:
                    tree.attrib["style"] = param["svg_style"]
                if "svg_attr_class" in param:
                    tree.attrib["class"] = param["svg_attr_class"]

                x2 = et.tostring(tree, pretty_print=True).decode("utf-8")

            context["param"]["svg_code"] = x2

            os.remove(file_name2)

        return context

    def get_renderer_template_name(self):
        return "schwiki/graphviz_wikiobj_view.html"


register_obj_renderer("graphviz", GraphvizObjRenderer)


class IncludeObjRenderer(BaseObjRenderer):

    @staticmethod
    def get_info():
        return { "name": "include", "title": "Include", "icon": "fa fa-plus-circle", "show_form": False,}
    
    def render(self, param, lines, output_format, parent_processor):
        if lines:
            with open(lines[0].strip(), "rt") as f:
                l= f.readlines()
                i = 0
                for line in l: 
                    parent_processor.lines.insert(self.line_number+i, line)
                    i += 1 
        return ""

register_obj_renderer("include", IncludeObjRenderer)


BLOCK_OBJ_RENDERER_FORM = """
start//Start of block
end//End of block
"""

class BlockObjRenderer(BaseMarkdownObjRenderer):
    @staticmethod
    def get_info():
        return {
            "name": "block",
            "title": "block",
            "icon": "fa fa-exchange",
            "show_form": True,
            "inline_content": True,
        }

    def get_edit_form(self):
        return BLOCK_OBJ_RENDERER_FORM

    def render(self, param, lines, output_format, parent_processor):
        context = self.gen_context(param, lines, output_format, parent_processor)
        return "<div style='position:relative'>" + self.edit_on_page_link(parent_processor, right=True) + context["param"]["start"] + context["content"] + context["param"]["end"] + "</div>"

register_obj_renderer("block", BlockObjRenderer)


class WikiFrameObjRenderer(BaseObjRenderer):

    @staticmethod
    def get_info():
        return { "name": "wiki-frame", "title": "Wiki frame", "icon": "fa fa-list-alt", "show_form": False, "inline_content": True}
    
    def render(self, param, lines, output_format, parent_processor):
        if lines:
            ret = ""
            for pos in lines:
                if pos.startswith('[['):
                    pos2 = pos[2:].split(']]')[0]
                    ret += "{%% include_wiki '%s' object wiki_path %%}" % pos2
            return ret
        return ""

register_obj_renderer("wiki-frame", WikiFrameObjRenderer)


class SuperBlockObjRenderer(BaseMarkdownObjRenderer):
    @staticmethod
    def get_info():
        return {
            "name": "super-block",
            "title": "Super block",
            "icon": "fa fa-superpowers",
            "show_form": True,
            "inline_content": True,
        }

    def get_edit_form(self):
        return "template::_"

    def convert_form_to_dict(self, form, old_dict=None):
        template = form.cleaned_data['template']
        return { 'template': bencode(template) }

    def form_from_dict(self, form_class, param):
        if param:
            template = param['template']
            return form_class(initial={ 'template': bdecode(template)} )
        else:
            return form_class()


    def render(self, param, lines, output_format, parent_processor):
        if lines:
            segments = []
            for line in lines:
                if not line:
                    if segments:
                        if segments[-1]:
                            segments.append([])
                else:
                    if segments:
                        segments[-1].append(line)
                    else:
                        segments.append([line,])
            context = self.gen_context(param, lines, output_format, parent_processor)
            context['lines'] = lines
            context['segments'] = segments
            context['line_number'] = self._get_line_number(parent_processor)
            template = bdecode(context['param']['template'])
            t = Template(template)
            c = Context(context)
            return t.render(c).replace('[%', '{%').replace('%]', '%}').replace('[{', '{{').replace('}]', '}}') 
        return ""

register_obj_renderer("super-block", SuperBlockObjRenderer)
