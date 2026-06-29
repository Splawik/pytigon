"""Django management command to export a database table to JSON."""

import json
import sys

from django.core.management.base import BaseCommand, CommandError
from django.db import connection


def get_table(table_name):
    """Fetch all rows from a table and return as a list of dictionaries.

    Uses parameterized queries to prevent SQL injection.

    Args:
        table_name: Name of the database table.

    Returns:
        list: List of dictionaries, each representing a row.

    Raises:
        CommandError: If the table name is invalid.
    """
    # Validate table name - only allow alphanumeric and underscore
    if not table_name.replace("_", "").isalnum():
        raise CommandError(
            f"Invalid table name: '{table_name}'. "
            "Only alphanumeric characters and underscores are allowed."
        )

    # Use the connection's ops to properly quote the table name
    quoted_name = connection.ops.quote_name(table_name)

    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM {quoted_name}")
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]


class Command(BaseCommand):
    """Export a database table to JSON format."""

    help = "Export SQL table to JSON"

    def add_arguments(self, parser):
        """Add command-line arguments.

        Args:
            parser: argparse argument parser.
        """
        parser.add_argument(
            "table_name",
            nargs="?",
            help="Table name to export",
        )
        parser.add_argument(
            "--output",
            help="Save output to file (prints to stdout if not specified)",
        )

    def handle(self, *args, **options):
        """Execute the command.

        Args:
            options: Parsed command-line options.
        """
        if not options["table_name"]:
            self.print_help("manage.py", "sqltable2json")
            sys.exit(1)

        output_file = options.get("output")

        try:
            data = get_table(options["table_name"])
        except CommandError as e:
            self.stderr.write(str(e))
            sys.exit(1)

        json_output = json.dumps(data, indent=2, default=str)

        if output_file:
            with open(output_file, "w") as f:
                f.write(json_output)
            self.stdout.write(f"Exported {len(data)} rows to {output_file}")
        else:
            self.stdout.write(json_output)
