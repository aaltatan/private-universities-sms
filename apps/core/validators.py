from django.core.validators import MinLengthValidator, RegexValidator
from django.utils.translation import gettext_lazy as _


four_char_length_validator = MinLengthValidator(
    limit_value=4,
    message=_("the field must be at least 4 characters long."),
)

numeric_validator = RegexValidator(
    regex=r"^\d+$",
    message=_("the field must be numeric."),
)
