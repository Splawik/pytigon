import sys
import os
from contextlib import chdir

from pytigon_lib.schindent.indent_markdown import (
    IndentMarkdownProcessor,
)

from schwiki.applib import makdown_obj_simple, markdown_obj_subblocks

from django.core.management.base import BaseCommand
from django.template import Context, Template


def render_string_template(template_str: str, context_dict: dict) -> str:
    """Renderuje szablon Django przekazany jako ciąg znaków."""
    template = Template(template_str)
    context = Context(context_dict)
    return template.render(context)


def md2html(input_str):
    x = IndentMarkdownProcessor(output_format="html", line_number=0)
    return x.convert(input_str)


class Command(BaseCommand):
    help = "convert indented markdown file to html"

    def add_arguments(self, parser):
        parser.add_argument(
            "input",
            help="read from file",
        )
        parser.add_argument(
            "--output",
            help="save output to file",
        )

    def handle(self, *args, **options):
        with chdir(os.environ["START_PATH"]):
            print(os.getcwd())
            if "input" in options and options["input"]:
                with open(options["input"], "rt") as f:
                    buf = f.read()
            else:
                buf = sys.stdin.read()

            buf2 = md2html("{% load exfiltry %}{% load exsyntax %}" + buf)
            try:
                buf3 = render_string_template(buf2, {})
            except Exception:
                print("ERROR!", options["input"])
                return

            if "output" in options and options["output"]:
                if options["output"] == ".":
                    file_name = options["input"].replace(".md", "") + ".html"
                else:
                    file_name = options["output"]
                with open(file_name, "wt") as f:
                    f.write(buf3)
            else:
                print(buf3)
