import os

from django.core.management.base import BaseCommand
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
            template_paths = [
                os.path.join(settings.ROOT_PATH, "templates_src"),
                os.path.join(settings.ROOT_PATH, "appdata", "plugins_src"),
                os.path.join(settings.DATA_PATH, "appdata", "plugins_src"),
            ]
        else:
            template_paths = [
                os.path.join(settings.PRJ_PATH, settings.PRJ_NAME, "templates_src"),
                os.path.join(settings.PRJ_PATH_ALT, settings.PRJ_NAME, "templates_src"),
            ]
        for template_path in template_paths:
            print(template_path)
            if os.path.exists(template_path):
                print("TEMPLATE FOLDER: ", template_path)
                l = len(template_path)
                for root, dirs, files in os.walk(template_path):
                    for f in files:
                        if f.endswith(".ihtml"):
                            p = os.path.join(root, f)
                            x = p[l + 1 :]
                            if not file_name or file_name in x:
                                compiled = []
                                compile_template(x, compiled=compiled, force=True)
                                if compiled:
                                    for c in compiled:
                                        print(c)
