from django.utils.translation import gettext_lazy as _

from apps.core.widgets import get_numeric_widget
from apps.core.forms import CustomModelForm

from .. import models


class PhoneForm(CustomModelForm):
    class Meta:
        model = models.Phone
        fields = ("number", "kind")
        widgets = {
            "number": get_numeric_widget(
                placeholder=_("phone number"),
            ),
        }
