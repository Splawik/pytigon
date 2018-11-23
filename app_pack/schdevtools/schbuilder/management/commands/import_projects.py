# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError

import sys
import io
import os
import getopt

from django.conf import settings

from schbuilder.views import prj_import_from_str
from schbuilder.models import SChAppSet

APP_SETS_TO_IMPORT =  [
    'schdevtools', #prepare with initial data
    'schsetup', 'schportal', 'schpytigondemo', 'schwebtrapper', 'scheditor', #prepare db but without initial data
    'schcomponents', 'scheditor', '_schdata', '_schremote', '_schtasks', '_schtools', '_schwiki', #without db
]    


class Command(BaseCommand):
    help ="Prepare installer files"

    def handle(self, *args, **options):
        for app_set_name in APP_SETS_TO_IMPORT:
            app_sets = list(SChAppSet.objects.filter(name = app_set_name))
            if len(app_sets)==0:
                path = os.path.join(os.path.join(settings.ROOT_PATH, "install"), f"{app_set_name}.prj")
                print("Import prj: ", path)
                with open(path, "rt") as f: 
                    s = f.read()
                    prj_import_from_str(s)
