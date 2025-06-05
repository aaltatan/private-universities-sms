from django import forms
from django.utils.translation import gettext as _

from apps.core.widgets import get_text_widget, get_textarea_widget

from .. import models


class BaseCompensationForm(forms.ModelForm):
    calculation_method = forms.ChoiceField(
        choices=models.Compensation.CalculationUserChoices,
        label=_("calculation method"),
        help_text=_("calculation method"),
    )
    affected_by_working_days = forms.ChoiceField(
        choices=models.Compensation.AffectedByWorkingDaysChoices,
        label=_("affected by working days"),
        help_text=_("whether compensation value is affected by working days"),
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
            "description",
        )
        widgets = {
            "name": get_text_widget(placeholder=_("compensation name")),
            "description": get_textarea_widget(),
        }


class CompensationForm(BaseCompensationForm):
    pass
