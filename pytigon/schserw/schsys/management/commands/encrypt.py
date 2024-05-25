import sys
import getpass

from django.core.management.base import BaseCommand
from pytigon_lib.schtools import encrypt


class Command(BaseCommand):
    help = "Encrypt or decrypt the file"

    def add_arguments(self, parser):
        parser.add_argument(
            "input",
            help="read from file",
        )
        parser.add_argument(
            "--output",
            help="save output to file",
        )
        parser.add_argument(
            "--password",
            help="password",
        )
        parser.add_argument(
            "--decrypt",
            action="store_true",
            help="decrypt",
        )
        parser.add_argument(
            "--base64",
            action="store_true",
            help="base64 encoded output",
        )

    def handle(self, *args, **options):
        print(options)
        if "input" in options and options["input"]:
            with open(options["input"], "rb") as f:
                buf = f.read()
        else:
            buf = sys.stdin.read()

        if "password" in options and options["password"]:
            password = options["password"]
        else:
            password = getpass.getpass()

        if "base64" in options and options["base64"]:
            b64 = True
        else:
            b64 = False

        if "decrypt" in options and options["decrypt"]:
            output_buf = encrypt.decrypt(buf, password, b64)
        else:
            output_buf = encrypt.encrypt(buf, password, b64)

        if "output" in options and options["output"]:
            with open(options["output"], "wb") as f:
                f.write(output_buf)
        else:
            print(output_buf)
