from django.core.management.base import BaseCommand, CommandError

import sys
import io
import os
import getopt

from django.conf import settings
from schwiki.applib.wiki_git import WikiGit
from schwiki.models import WikiConf

class Command(BaseCommand):
    help ="Pull wiki articles from git repository"

    def add_arguments(self, parser):
        parser.add_argument(
            '--subjects', 
            default=None,
            help='Subjects to pull',
        )
        parser.add_argument(
            '--erase-previous-data',
            action="store_true", 
            help='Erase previous data',
        )

        parser.add_argument(
            '--main-menu',
            action="store_true", 
            help='Subfolders in main menu',
        )

    def handle(self, *args, **options):
        if options['subjects']:
            subjects_to_pull = options['subjects'].replace(',',';').split(';')
        else:
            subjects_to_pull = []
            
        for wikiconf in WikiConf.objects.all():
            if wikiconf.git_repository and ((not subjects_to_pull) or wikiconf.subject in subjects_to_pull):            
                print("Import subject: ", wikiconf.subject)
                gitobj = WikiGit(wikiconf)
                gitobj.wiki_pull(options['erase_previous_data'], options['main_menu'])
