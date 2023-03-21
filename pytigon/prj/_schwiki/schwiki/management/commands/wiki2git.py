from django.core.management.base import BaseCommand, CommandError

import sys
import io
import os
import getopt

from django.conf import settings
from schwiki.applib.wiki_git import WikiGit
from schwiki.models import WikiConf

class Command(BaseCommand):
    help ="Push wiki articles to git repository"

    def add_arguments(self, parser):
        parser.add_argument(
            '--subjects', 
            default=None,
            help='Subjects to push',
        )

    def handle(self, *args, **options):
        if options['subjects']:
            subjects_to_push = options['subjects'].replace(',',';').split(';')
        else:
            subjects_to_push = []
        
        for wikiconf in WikiConf.objects.all():    
            if wikiconf.git_repository and ((not subjects_to_push) or wikiconf.subject in subjects_to_push):
                print("Export subject: ", wikiconf.subject)
                gitobj = WikiGit(wikiconf)
                gitobj.wiki_push()
