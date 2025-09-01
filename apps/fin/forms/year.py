from django.utils.translation import gettext_lazy as _

from apps.core.forms import CustomModelForm
from apps.core.widgets import get_text_widget, get_textarea_widget

from .. import models


class BaseYearForm(CustomModelForm):
    class Meta:
        model = models.Year
        fields = ("name", "description")
        widgets = {
            "name": get_text_widget(placeholder=_("e.g. 2022")),
            "description": get_textarea_widget(placeholder=_("some description")),
        }


class YearForm(BaseYearForm):
    pass
