from django import forms
from django.utils.translation import gettext as _

from apps.core.widgets import get_date_widget, get_text_widget, get_textarea_widget

from .. import models


class BasePeriodForm(forms.ModelForm):
    is_closed = forms.ChoiceField(
        choices=models.Period.ClosedChoices,
        label=_("is closed"),
    )

    class Meta:
        model = models.Period
        fields = ("name", "year", "start_date", "is_closed", "description")
        widgets = {
            "name": get_text_widget(placeholder=_("e.g. 20221 - First Chapter")),
            "start_date": get_date_widget(placeholder=_("e.g. 2022-01-01")),
            "description": get_textarea_widget(),
        }


class PeriodForm(BasePeriodForm):
    pass
