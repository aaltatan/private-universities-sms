from django.utils.translation import gettext_lazy as _

from apps.core.fields import get_autocomplete_field
from apps.core.forms import CustomModelForm
from apps.core.widgets import get_text_widget, get_textarea_widget

from .. import models


class BaseCityForm(CustomModelForm):
    governorate = get_autocomplete_field(
        models.Governorate.objects.all(),
        to_field_name="name",
        widget_attributes={"placeholder": _("search governorates")},
        field_attributes={"label": _("governorate")},
        app_label="geo",
        model_name="Governorate",
        object_name="governorate",
        field_name="search",
    )

    class Meta:
        model = models.City
        fields = ("name", "governorate", "kind", "description")
        widgets = {
            "name": get_text_widget(placeholder=_("e.g. Hamah")),
            "description": get_textarea_widget(placeholder=_("some description")),
        }


class CityForm(BaseCityForm):
    pass
