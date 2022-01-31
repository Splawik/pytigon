import os

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from pytigon_lib.schdjangoext.python_style_template_loader import compile_template


class Command(BaseCommand):
    help = "Compile ihtml templates to standard django html files"

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            help="compile only file",
        )

    def handle(self, *args, **options):
        if "file" in options:
            file_name = options["file"]
        else:
            file_name = None
        compiled = []
        if settings.PRJ_NAME == "_schall":
            base_path = settings.ROOT_PATH
        else:
            base_path = os.path.join(settings.PRJ_PATH_ALT, settings.PRJ_NAME)
        print(settings.PRJ_PATH, settings.PRJ_NAME)
        l = len(base_path)
        itemplate_path = os.path.join(base_path, "templates_src")
        print(itemplate_path)
        for root, dirs, files in os.walk(itemplate_path):
            for f in files:
                if f.endswith(".ihtml"):
                    p = os.path.join(root, f)
                    x = p[l + 15 :]
                    if not file_name or file_name in x:
                        compile_template(x, compiled=compiled, force=True)
        # print(compiled)
