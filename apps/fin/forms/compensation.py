from django import forms
from django.utils.translation import gettext as _

from apps.core import widgets

from .. import models


class BaseCompensationForm(forms.ModelForm):
    calculation_method = forms.ChoiceField(
        choices=models.Compensation.CalculationUserChoices,
        label=_("calculation method"),
    )
    affected_by_working_days = forms.ChoiceField(
        choices=models.Compensation.AffectedByWorkingDaysChoices,
        label=_("affected by working days"),
    )
    is_active = forms.ChoiceField(
        choices=models.Compensation.AffectedByWorkingDaysChoices,
        label=_("is active"),
    )

    class Meta:
        model = models.Compensation
        fields = (
            "name",
            "calculation_method",
            "value",
            "min_value",
            "max_value",
            "round_method",
            "rounded_to",
            "tax",
            "tax_classification",
            "affected_by_working_days",
            "is_active",
            "accounting_id",
            "description",
        )
        widgets = {
            "name": widgets.get_text_widget(placeholder=_("e.g. Salary")),
            "value": widgets.get_number_widget(placeholder=_("e.g. 1000")),
            "min_value": widgets.get_number_widget(placeholder=_("e.g. 0")),
            "max_value": widgets.get_number_widget(placeholder=_("e.g. 50000")),
            "rounded_to": widgets.get_number_widget(placeholder=_("e.g. 100")),
            "accounting_id": widgets.get_text_widget(placeholder=_("e.g. 3111")),
            "description": widgets.get_textarea_widget(),
        }


class CompensationForm(BaseCompensationForm):
    pass
