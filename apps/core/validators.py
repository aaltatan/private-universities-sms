from django.core.validators import MinLengthValidator
from django.utils.translation import gettext_lazy as _


four_char_length_validator = MinLengthValidator(
  limit_value=4,
  message=_('the field must be at least 4 characters long.'),
)