from decimal import Decimal

from django.db import models

from apps.core.utils import db_round_to_nearest
from apps.fin.models import Tax, TaxBracket


def db_calculate_tax_brackets(
    amount: Decimal | int | float, tax_object: Tax
) -> Decimal:
    layer_tax = (models.F("amount_to") - models.F("amount_from")) * models.F("rate")

    net = models.Window(
        expression=models.Sum("layer_tax"),
        frame=models.RowRange(start=None, end=0),
        order_by=models.F("amount_from").asc(),
    ) - models.F("layer_tax")

    in_range = models.Q(
        amount_from__lte=models.Value(amount),
        amount_to__gte=models.Value(amount),
    )

    result_with_fractions = models.Case(
        models.When(
            condition=in_range,
            then=(models.Value(amount) - models.F("amount_from")) * models.F("rate")
            + models.F("net"),
        ),
        default=models.Value(0),
        output_field=models.DecimalField(),
    )

    result = db_round_to_nearest(
        amount_field="result_with_fractions",
        rounded_to="tax__rounded_to",
        round_method_field="tax__round_method",
    )

    tax_value = (
        TaxBracket.objects.filter(tax=tax_object)
        .annotate(
            **{
                "layer_tax": layer_tax,
                "net": net,
                "in_range": in_range,
                "result_with_fractions": result_with_fractions,
                "result": result,
            }
        )
        .aggregate(tax_value=models.Sum("result"))["tax_value"]
    )

    return tax_value


def run():
    amount = 1_500_000
    tax_object = Tax.objects.get(
        ~models.Q(
            calculation_method=Tax.CalculationMethodChoices.BRACKETS,
        )
    )

    print(db_calculate_tax_brackets(amount, tax_object))
