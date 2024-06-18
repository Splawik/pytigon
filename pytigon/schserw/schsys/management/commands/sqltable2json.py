import sys
import json

from django.core.management.base import BaseCommand
from django.db import connection


def get_table(table_name):
    with connection.cursor() as cursor:
        cursor.execute("select * from %s" % table_name)
        r = [
            dict((cursor.description[i][0], value) for i, value in enumerate(row))
            for row in cursor.fetchall()
        ]
        return r


class Command(BaseCommand):
    help = "Export sql table to json"

    def add_arguments(self, parser):
        parser.add_argument("table_name", nargs="?", help="Table name to export")
        parser.add_argument(
            "--output",
            help="save output to file",
        )

    def handle(self, *args, **options):
        if not options["table_name"]:
            self.print_help("manage.py", "sqltable2json")
            sys.exit(1)

        if "output" in options and options["output"]:
            o = options["output"]
        else:
            o = None

        t = get_table(options["table_name"])
        if o:
            with open(o, "wt") as f:
                f.write(json.dumps(t))
        else:
            print(json.dumps(t))

