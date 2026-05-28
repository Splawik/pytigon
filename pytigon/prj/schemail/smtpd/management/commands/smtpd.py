from django.core.management.base import BaseCommand, CommandError
import asyncio
from aiosmtpd.controller import Controller


class CustomHandler:
    async def handle_DATA(self, server, session, envelope):
        peer = session.peer
        mail_from = envelope.mail_from
        rcpt_tos = envelope.rcpt_tos
        data = envelope.content         # type: bytes
        # Process message data...
        print(data)
        # pass
        if error_occurred:
            return '500 Could not process your message'
        return '250 OK'


class Command(BaseCommand):
    help = 'run smtpd server'

    def add_arguments(self, parser):
        parser.add_argument('port', nargs='+', type=int)

    def handle(self, *args, **options):
        if 'port' in options:
            port = options['port']
        else:
            port = 25
            
        handler = CustomHandler()
        controller = Controller(handler, hostname='0.0.0.0', port=port)
        controller.start()
        # Wait for the user to press Return.
        input('SMTP server running. Press Return to stop server and exit.')
        controller.stop()
