# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError

import sys
import io
import os
import getopt

from zipfile import ZipFile

from pytigon_lib.schtools.install import extract_ptig

class Command(BaseCommand):
    help ="Install .ptig file"

    def add_arguments(self, parser):
        parser.add_argument(
            'filename', 
            help='Pytigon instalation file (*.ptig)',
        )

    def handle(self, *args, **options):
        filename = options['filename']
        if os.path.exists(filename):
            name=filename.replace('\\', '/').split('/')[-1].split('.')[0]
            with ZipFile(filename) as zip_file:
                extract_ptig(zip_file, name)
