from django.forms import ModelChoiceField
from django.utils.translation import gettext_lazy as _


class CustomModelChoiceField(ModelChoiceField):
    """A custom ModelChoiceField."""

    default_error_messages = {
        "invalid_choice": _("this choice is not valid"),
    }
