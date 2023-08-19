from django.core.management.base import BaseCommand, CommandError

import sys
import io
import os
import getopt

from django.conf import settings

from schbuilder.views import prj_import_from_str
from schbuilder.models import SChAppSet

PRJS_TO_IMPORT = [
    "schdevtools",  # prepare with initial data
    "schmanage",
    "schscripts",
    "_schsetup",
    "schportal",
    "schpytigondemo",
    "schwebtrapper",
    "scheditor",  # prepare db but without initial data
    "_schcomponents",
    "scheditor",
    "_schdata",
    "_schremote",
    "_schtools",
    "_schwiki",
    "_schserverless",  # without db
]


class Command(BaseCommand):
    help = "Prepare installer files"

    def handle(self, *args, **options):
        for prj_name in PRJS_TO_IMPORT:
            prjs = list(SChAppSet.objects.filter(name=prj_name))
            if len(prjs) == 0:
                path = os.path.join(
                    os.path.join(settings.ROOT_PATH, "install"), f"{prj_name}.prj"
                )
                print("Import prj: ", path)
                try:
                    with open(path, "rt") as f:
                        s = f.read()
                        prj_import_from_str(s)
                except:
                    print("Prj: ", path, " not imported!")
