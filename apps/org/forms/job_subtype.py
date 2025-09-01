from django.utils.translation import gettext_lazy as _

from apps.core.widgets import get_text_widget, get_textarea_widget
from apps.core.forms import CustomModelForm
from apps.core.fields import get_autocomplete_field

from .. import models


class BaseJobSubtypeForm(CustomModelForm):
    job_type = get_autocomplete_field(
        models.JobType.objects.all(),
        to_field_name="name",
        widget_attributes={"placeholder": _("search job types")},
        app_label="org",
        model_name="JobType",
        object_name="job_type",
        field_name="search",
    )

    class Meta:
        model = models.JobSubtype
        fields = ("name", "job_type", "description")
        widgets = {
            "name": get_text_widget(placeholder=_("e.g. Software Developer")),
            "description": get_textarea_widget(placeholder=_("some description")),
        }


class JobSubtypeForm(BaseJobSubtypeForm):
    pass
