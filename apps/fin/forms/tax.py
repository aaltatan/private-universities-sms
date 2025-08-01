from django import forms
from django.utils.translation import gettext as _

from apps.core.forms import CustomModelForm
from apps.core.widgets import get_text_widget, get_textarea_widget

from .. import models


class BaseTaxForm(CustomModelForm):
    calculation_method = forms.ChoiceField(
        choices=models.Tax.CalculationMethodChoices,
        label=_("calculation method"),
    )
    affected_by_working_days = forms.ChoiceField(
        choices=models.Tax.AffectedByWorkingDaysChoices,
        label=_("affected by working days"),
    )

    class Meta:
        model = models.Tax
        fields = (
            "name",
            "shortname",
            "calculation_method",
            "amount",
            "percentage",
            "formula",
            "rounded_to",
            "round_method",
            "affected_by_working_days",
            "accounting_id",
            "description",
        )
        widgets = {
            "name": get_text_widget(placeholder=_("e.g. Fixed Tax")),
            "shortname": get_text_widget(placeholder=_("e.g. Fixed")),
            "accounting_id": get_text_widget(placeholder=_("e.g. 3111")),
            "formula": get_textarea_widget(
                rows=4,
                placeholder=_(
                    "e.g. 1000 if obj.gender == 'male' else 1000",
                ),
            ),
            "description": get_textarea_widget(),
        }


class TaxForm(BaseTaxForm):
    pass
