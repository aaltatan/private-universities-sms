from django import forms
from django.utils.translation import gettext as _

from apps.core import widgets, fields
from apps.core.forms import CustomModelForm

from .. import models


class BaseCompensationForm(CustomModelForm):
    kind = forms.ChoiceField(
        choices=models.Compensation.CompensationKindChoices,
        label=_("kind"),
    )
    calculation_method = forms.ChoiceField(
        choices=models.Compensation.CalculationChoices,
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
    tax = fields.get_autocomplete_field(
        models.Tax.objects.all(),
        to_field_name="name",
        widget_attributes={"placeholder": _("search taxes")},
        app_label="fin",
        model_name="Tax",
        object_name="tax",
        field_name="search",
        field_attributes={"required": False},
    )

    class Meta:
        model = models.Compensation
        fields = (
            "name",
            "shortname",
            "kind",
            "calculation_method",
            "value",
            "formula",
            "min_value",
            "max_value",
            "round_method",
            "rounded_to",
            "tax",
            "tax_classification",
            "affected_by_working_days",
            "is_active",
            "accounting_id",
            "document",
            "description",
        )
        widgets = {
            "name": widgets.get_text_widget(placeholder=_("e.g. Salary")),
            "shortname": widgets.get_text_widget(placeholder=_("e.g. Salary")),
            "value": widgets.get_number_widget(placeholder=_("e.g. 1000")),
            "min_value": widgets.get_number_widget(placeholder=_("e.g. 0")),
            "max_value": widgets.get_number_widget(placeholder=_("e.g. 50000")),
            "rounded_to": widgets.get_number_widget(placeholder=_("e.g. 100")),
            "accounting_id": widgets.get_text_widget(placeholder=_("e.g. 3111")),
            "description": widgets.get_textarea_widget(),
            "document": widgets.get_file_widget(),
            "formula": widgets.get_textarea_widget(
                rows=4,
                placeholder=_(
                    "e.g. 1000 if obj.gender == 'male' else 1000",
                ),
            ),
        }


class CompensationForm(BaseCompensationForm):
    pass
