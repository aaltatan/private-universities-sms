from typing import Iterable

from django.db import models, connection
from django.conf import settings
from django.db.models.functions import Concat


def annotate_search(fields: Iterable[str]) -> Concat:
    fields = fields * 2

    args: list[models.F | models.Value] = []

    for field in fields:
        args.append(models.F(field))
        args.append(models.Value(" "))

    return Concat(*args[:-1], output_field=models.CharField())


def is_table_exists(table_name: str) -> bool:
    """
    Check if a table exists in the database.
    Supports MySQL and SQLite.
    """
    with connection.cursor() as cursor:
        engine: str = settings.DATABASES["default"]["ENGINE"]

        if engine.endswith("mysql"):
            cursor.execute("SHOW TABLES;")
            tables = [t[0] for t in cursor.fetchall()]
            return table_name in tables

        elif engine.endswith("sqlite3"):
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name=%s;",
                [table_name],
            )
            return cursor.fetchone() is not None

        else:
            raise NotImplementedError(f"Unsupported database engine: {engine}")
