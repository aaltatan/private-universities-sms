from typing import Iterable, Literal

from django.db import models
from django.db.models.functions import (
    Cast,
    Ceil,
    Concat,
    ExtractYear,
    Floor,
    Mod,
    Round,
)
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from ..choices import RoundMethodChoices


def db_round_to_nearest(
    *,
    amount_field: str,
    rounded_to: str | int,
    round_method_field: str | None = None,
    round_method: Literal["round", "floor", "ceil"] | None = None,
):
    """
    a function to round a number to the nearest value.
    Keyword arguments:
        amount_field (str): The name of the field containing the amount to round.
        rounded_to (str | int): The value to round to or the name of the field containing the value.
        round_method_field (str): The name of the field containing the round method.
        round_method (Literal["round", "floor", "ceil"] | None, optional): The round method to use. Defaults to None, if it used it will override the round_method_field.

    Returns:
        models.ExpressionWrapper: The rounded amount.
    """
    if round_method_field is None and round_method is None:
        raise ValueError("round_method or round_method_field must be provided.")

    if isinstance(rounded_to, int):
        if rounded_to < 1:
            raise ValueError("rounded_to must be greater than or equal to 1.")
        rounded_to_field = models.Value(rounded_to)
    else:
        rounded_to_field = models.F(rounded_to)

    amount = models.F(amount_field) / rounded_to_field

    if round_method is None:
        ceil_kwargs = {
            round_method_field: RoundMethodChoices.CEIL,
            "then": Ceil(amount) * rounded_to_field,
        }
        floor_kwargs = {
            round_method_field: RoundMethodChoices.FLOOR,
            "then": Floor(amount) * rounded_to_field,
        }
        round_logic = Round(amount) * rounded_to_field

        return models.Case(
            models.When(**ceil_kwargs),
            models.When(**floor_kwargs),
            default=round_logic,
            output_field=models.DecimalField(),
        )
    else:
        methods = {
            "round": Round,
            "floor": Floor,
            "ceil": Ceil,
        }

        return methods[round_method](amount) * rounded_to_field


def annotate_search(fields: Iterable[str]) -> Concat:
    fields = fields * 2

    args: list[models.F | models.Value] = []

    for field in fields:
        args.append(models.F(field))
        args.append(models.Value(" "))

    return Concat(*args[:-1], output_field=models.CharField())


def db_calculate_age_in_years(
    field_name: str, date: timezone.datetime | None = None
) -> models.ExpressionWrapper:
    """
    calculates the age of a specific DateField in years (on database level).
    """
    if date is None:
        date = timezone.now()

    current_date = date

    return models.ExpressionWrapper(
        models.Value(current_date.year)
        - ExtractYear(models.F(field_name))
        - models.Case(
            models.When(
                condition=models.Q(
                    **{f"{field_name}__month__gt": current_date.month},
                )
                | models.Q(
                    **{
                        f"{field_name}__month": current_date.month,
                        f"{field_name}__day__gt": current_date.day,
                    }
                ),
                then=models.Value(1),
            ),
            default=models.Value(0),
            output_field=models.IntegerField(),
        ),
        output_field=models.IntegerField(),
    )


def _db_get_concatenated_date(
    year: models.Value | models.F, field_name: str, is_leap: bool = False
) -> Concat:
    values = [
        year,
        models.Value("-"),
        models.F(f"{field_name}__month"),
        models.Value("-"),
    ]
    if is_leap:
        values.append(models.Value(28))
    else:
        values.append(models.F(f"{field_name}__day"))

    return Concat(*values)


def db_get_next_anniversary(
    field_name: str,
    label: str,
    n: int = 1,
    date: timezone.datetime | None = None,
):
    """
    Returns the next anniversary of a specific DateField in years (on database level).

    Args:
        field_name (str): The name of the DateField.
        label (str): The label of generated DateField.
        date (timezone.datetime | None): The date to check for anniversaries.
            Defaults to None.

    Returns:
        models.ExpressionWrapper: The nth anniversary of the specified DateField.
    """
    if n < 1:
        raise ValueError("n must be greater than or equal to 1")

    if date is None:
        date = timezone.now()

    current_date = date

    _next_anniversary = Cast(
        models.Case(
            models.When(
                condition=models.Q(
                    **{f"{field_name}__month": 2, f"{field_name}__day": 29}
                ),
                then=_db_get_concatenated_date(
                    year=models.Value(current_date.year),
                    field_name=field_name,
                    is_leap=True,
                ),
            ),
            default=_db_get_concatenated_date(
                year=models.Value(current_date.year),
                field_name=field_name,
            ),
            output_field=models.CharField(),
        ),
        output_field=models.DateField(),
    )

    next_anniversary = Cast(
        models.Case(
            models.When(
                models.Q(**{f"_next_{label}__lt": models.Value(current_date)}),
                then=_db_get_concatenated_date(
                    year=models.F(f"_next_{label}__year") + models.Value(1),
                    field_name=f"_next_{label}",
                ),
            ),
            default=_db_get_concatenated_date(
                year=models.F(f"_next_{label}__year"),
                field_name=f"_next_{label}",
            ),
            output_field=models.CharField(),
        ),
        output_field=models.DateField(),
    )

    _mod_years_difference = Mod(
        models.ExpressionWrapper(
            models.F(f"next_{label}__year") - models.F(f"{field_name}__year"),
            output_field=models.IntegerField(),
        ),
        models.Value(n),
    )

    _next_nth_anniversary_year = models.Case(
        models.When(
            **{f"_mod_years_difference_{label}": models.Value(0)},
            then=models.F(f"next_{label}__year"),
        ),
        default=models.ExpressionWrapper(
            models.Value(n)
            - models.F(f"_mod_years_difference_{label}")
            + models.F(f"next_{label}__year"),
            output_field=models.IntegerField(),
        ),
    )

    next_nth_anniversary = Cast(
        models.Case(
            models.When(
                condition=models.Q(
                    **{
                        f"{field_name}__month": 2,
                        f"{field_name}__day": 29,
                    }
                ),
                then=_db_get_concatenated_date(
                    year=models.F(f"_next_nth_{label}_year"),
                    field_name=field_name,
                    is_leap=True,
                ),
            ),
            default=_db_get_concatenated_date(
                year=models.F(f"_next_nth_{label}_year"),
                field_name=field_name,
            ),
            output_field=models.CharField(),
        ),
        output_field=models.DateField(),
    )

    kwargs = {
        f"_next_{label}": _next_anniversary,
        f"next_{label}": next_anniversary,
    }

    if n == 1:
        return kwargs

    return {
        **kwargs,
        f"_mod_years_difference_{label}": _mod_years_difference,
        f"_next_nth_{label}_year": _next_nth_anniversary_year,
        f"next_nth_{label}": next_nth_anniversary,
    }


def db_get_age_groups(field_name: str, n: int = 2) -> models.Case:
    """
    Returns the age groups of a specific DateField in years (on database level).

    Args:
        field_name (str): The name of the DateField.
        n (int): The number of age groups.
            Defaults to 2.

    Returns:
        models.Case: The age groups of the specified DateField.
    """
    if n < 2:
        raise ValueError("n must be greater than or equal to 2")

    return models.Case(
        *[
            models.When(
                **{
                    f"{field_name}__gte": idx,
                    f"{field_name}__lt": idx + n,
                },
                then=models.Value(
                    _("between {} and below {} years").format(
                        str(idx).rjust(2, "0"),
                        str(idx + n).rjust(2, "0"),
                    ),
                ),
            )
            for idx in range(0, 30, n)
        ],
        default=models.Value(_("below {} years").format(n)),
        output_field=models.CharField(),
    )
