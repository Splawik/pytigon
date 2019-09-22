from django.core.management.base import BaseCommand, CommandError
#from polls.models import Poll

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        for poll_id in options['poll_id']:
            self.stdout.write('Successfully closed poll "%s"' % poll_id)
            