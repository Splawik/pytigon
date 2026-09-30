import getpass
import sys

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
        input_file = options.get("input")
        if input_file:
            with open(input_file, "rb") as f:
                buf = f.read()
        else:
            buf = sys.stdin.buffer.read()

        password = options.get("password") or getpass.getpass()

        b64 = bool(options.get("base64"))

        if options.get("decrypt"):
            output_buf = encrypt.decrypt(buf, password, b64)
        else:
            output_buf = encrypt.encrypt(buf, password, b64)

        output_file = options.get("output")
        if output_file:
            # encrypt(b64=False) returns bytes, everything else returns str, so
            # the result is normalised to bytes before hitting the binary file.
            data = output_buf if isinstance(output_buf, bytes) else output_buf.encode()
            with open(output_file, "wb") as f:
                f.write(data)
        elif isinstance(output_buf, bytes):
            # Writing to stdout.buffer keeps the bytes intact; print() would
            # render them as a "b'...'" repr.
            sys.stdout.buffer.write(output_buf)
        else:
            sys.stdout.write(output_buf)
