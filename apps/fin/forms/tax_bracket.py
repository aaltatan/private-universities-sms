from django.utils.translation import gettext as _

from apps.core import widgets
from apps.core.fields import get_autocomplete_field
from apps.core.forms import CustomModelForm

from .. import models


class BaseTaxBracketForm(CustomModelForm):
    tax = get_autocomplete_field(
        queryset=models.Tax.objects.filter(
            calculation_method=models.Tax.CalculationMethodChoices.BRACKETS
        ),
        to_field_name="name",
        widget_attributes={"placeholder": _("search taxes")},
        queryset_filters={
            "calculation_method": models.Tax.CalculationMethodChoices.BRACKETS,
        },
        app_label="fin",
        model_name="Tax",
        object_name="tax",
        field_name="search",
    )

    class Meta:
        model = models.TaxBracket
        fields = (
            "tax",
            "amount_from",
            "amount_to",
            "rate",
            "notes",
        )
        widgets = {
            "amount_from": widgets.get_number_widget(placeholder=_("e.g. 1000")),
            "amount_to": widgets.get_number_widget(placeholder=_("e.g. 50000")),
            "rate": widgets.get_number_widget(placeholder=_("e.g. 0.1")),
            "notes": widgets.get_textarea_widget(),
        }


class TaxBracketForm(BaseTaxBracketForm):
    pass
