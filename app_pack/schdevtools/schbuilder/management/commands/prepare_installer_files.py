# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError

import sys
import io
import os
import getopt

from django.conf import settings

from schlib.schtools.install import install
from schbuilder.views import prj_export
from schbuilder.models import SChAppSet

APP_SETS_TO_EXPORT =  [
    'schdevtools', #prepare with initial data
    'schsetup', 'schportal', 'schpytigondemo', 'schwebtrapper', 'scheditor', #prepare db but without initial data
    'schcomponents', 'scheditor', '_schdata', '_schremote', '_schtasks', '_schtools', '_schwiki', #without db
]    


class Command(BaseCommand):
    help ="Prepare installer files"

    def add_arguments(self, parser):
        parser.add_argument(
            '--app_sets', 
            default=None,
            help='Specifies app_sets',
        )

    def handle(self, *args, **options):
        if options['app_sets']:
            app_sets_to_export = options['app_sets'].replace(',',';').split(';')
        else:
            app_sets_to_export = APP_SETS_TO_EXPORT
            
        for app_set_name in app_sets_to_export:
            if not app_set_name:
                continue
            app_sets = list(SChAppSet.objects.filter(name = app_set_name))
            if len(app_sets)>0:
                app_set = app_sets[-1]        
                x = prj_export(None, app_set.pk)
                path = os.path.join(os.path.join(settings.ROOT_PATH, "install"), f"{app_set_name}.prj")
                print("Export prj: ", path)
                with open(path, "wt") as f: 
                    if type(x.content)==bytes:
                        f.write(x.content.decode('utf-8'))
                    else:
                        f.write(x.content)
