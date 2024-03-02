from django.core.management.base import BaseCommand, CommandError

import sys
import io
import os
import getopt

from django.conf import settings

from pytigon_lib.schtools.install import install
from schbuilder.views import prj_export
from schbuilder.models import SChAppSet

PRJS_TO_EXPORT  =  [
    'schdevtools', #prepare with initial data
    'schmanage', 'schscripts', '_schsetup', '_schot', 'schportal', 'schpytigondemo', 'schwebtrapper', 'scheditor', #prepare db but without initial data
    '_schcomponents', 'scheditor', '_schdata', '_schremote', '_schtools', '_schwiki', '_schserverless', #without db
    'schemail', '_schall', 'schodf', '_schplaywright', 'mobile_demo', '_schbi', '_schbusiness', 
]    


class Command(BaseCommand):
    help ="Prepare installer files"

    def add_arguments(self, parser):
        parser.add_argument(
            '--prjs', 
            default=None,
            help='Specifies projects',
        )

    def handle(self, *args, **options):
        if options['prjs']:
            prjs_to_export = options['prjs'].replace(',',';').split(';')
        else:
            prjs_to_export = PRJS_TO_EXPORT
            
        for prj_name in prjs_to_export:
            if not prj_name:
                continue
            prjs = list(SChAppSet.objects.filter(name = prj_name, main_view=True))
            if len(prjs)>0:
                prj = prjs[-1]        
                x = prj_export(None, prj.pk)
                path = os.path.join(os.path.join(settings.ROOT_PATH, "install"), f"{prj_name}.prj")
                print("Export prj: ", path)
                with open(path, "wt") as f: 
                    if type(x.content)==bytes:
                        f.write(x.content.decode('utf-8'))
                    else:
                        f.write(x.content)
