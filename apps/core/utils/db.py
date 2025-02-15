from typing import Iterable

from django.db import models
from django.db.models.functions import Concat


def annotate_search(fields: Iterable[str]) -> Concat:
    fields = fields * 2

    args: list[models.F | models.Value] = []

    for field in fields:
        args.append(models.F(field))
        args.append(models.Value(" "))

    return Concat(*args[:-1], output_field=models.CharField())
