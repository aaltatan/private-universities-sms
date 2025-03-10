from django import forms
from django.utils.translation import gettext as _

from apps.core.fields import get_autocomplete_field
from apps.core.widgets import get_text_widget, get_textarea_widget

from .. import models


class BaseJobSubtypeForm(forms.ModelForm):
    class Meta:
        model = models.JobSubtype
        fields = ("name", "job_type", "description")
        widgets = {
            "name": get_text_widget(placeholder=_("job subtype name")),
            "description": get_textarea_widget(),
        }


class JobSubtypeForm(BaseJobSubtypeForm):
    job_type = get_autocomplete_field(
        queryset=models.JobType.objects.all(),
        to_field_name="name",
        widget_attributes={"placeholder": _("search job types")},
        app_label="org",
        model_name="JobType",
        object_name="jobtype",
        field_name="search",
    )
