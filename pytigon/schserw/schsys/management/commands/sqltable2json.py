"""Django management command to export a database table to JSON."""

import contextlib
import json
import os
import re
import tempfile

from django.core.management.base import BaseCommand, CommandError
from django.db import connection

_TABLE_NAME_RE = re.compile(r"[A-Za-z0-9_]+")


def get_table(table_name, batch_size=1000):
    """Fetch all rows from a table and return as a list of dictionaries.

    Uses parameterized queries to prevent SQL injection.

    Args:
        table_name: Name of the database table.
        batch_size: Number of rows fetched per round trip.

    Returns:
        list: List of dictionaries, each representing a row.

    Raises:
        CommandError: If the table name is invalid.
    """
    # Validate table name - only allow ASCII letters, digits and underscores.
    # str.isalnum() also accepts non-ASCII letters and full-width digits, which
    # produce a syntactically valid but unexpected quoted identifier.
    if not _TABLE_NAME_RE.fullmatch(table_name):
        raise CommandError(
            f"Invalid table name: '{table_name}'. "
            "Only ASCII letters, digits and underscores are allowed."
        )

    # Use the connection's ops to properly quote the table name
    quoted_name = connection.ops.quote_name(table_name)

    rows = []
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM {quoted_name}")
        columns = [col[0] for col in cursor.description]
        # fetchall() materialises the whole table in memory at once; a large
        # table can exhaust it.
        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            rows.extend(dict(zip(columns, row)) for row in batch)
    return rows


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
            raise CommandError("table_name is required")

        output_file = options.get("output")

        # get_table raises CommandError itself; letting it propagate gives
        # Django's standard error handling and exit code instead of sys.exit().
        data = get_table(options["table_name"])

        json_output = json.dumps(data, indent=2, default=str)

        if output_file:
            # Write to a temp file in the destination directory and rename, so
            # a crash mid-write cannot leave a truncated JSON file in place.
            directory = os.path.dirname(os.path.abspath(output_file)) or "."
            fd, tmp_path = tempfile.mkstemp(
                dir=directory, prefix=".sqltable2json-", suffix=".tmp"
            )
            try:
                with os.fdopen(fd, "w", encoding="utf-8") as f:
                    f.write(json_output)
                os.replace(tmp_path, output_file)
            except BaseException:
                with contextlib.suppress(OSError):
                    os.unlink(tmp_path)
                raise
            self.stdout.write(f"Exported {len(data)} rows to {output_file}")
        else:
            self.stdout.write(json_output)
