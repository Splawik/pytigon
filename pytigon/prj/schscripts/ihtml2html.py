import argparse

from pytigon_lib.schindent.indent_style import ihtml_to_html_base
from pytigon_lib.schindent.html2ihtml import convert
from pytigon_lib.schindent.py_to_js import compile
from pytigon_lib.schindent.indent_tools import convert_js


def main(argv):
    parser = argparse.ArgumentParser(description="Converter")
    parser.add_argument("filename", help="filename to convert (*.ihtml, *.html)")
    parser.add_argument("-o", "--output", help="output filename (*.ihtml, *.html)")

    args = parser.parse_args(argv)

    if args.filename.endswith(".html"):
        convert(args.filename, args.output)
    elif args.filename.endswith(".ihtml"):
        with open(args.output, "wt") as f:
            f.write(ihtml_to_html_base(args.filename))
    elif args.filename.endswith(".py"):
        with open(args.filename, "rt") as f_in, open(args.output, "wt") as f_out:
            error, js = compile(f_in.read())
            f_out.write(js)
    elif args.filename.endswith(".ijs"):
        with open(args.filename, "rt") as f_in, open(args.output, "wt") as f_out:
            convert_js(f_in, f_out)
