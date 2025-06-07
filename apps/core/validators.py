from django.core.validators import (
    MinLengthValidator,
    RegexValidator,
    FileExtensionValidator,
)
from django.utils.translation import gettext_lazy as _


four_char_length_validator = MinLengthValidator(
    limit_value=4,
    message=_("the field must be at least 4 characters long."),
)

two_chars_validator = MinLengthValidator(
    limit_value=2,
    message=_("the field must be at least 2 characters long."),
)

numeric_validator = RegexValidator(
    regex=r"^\d+$",
    message=_("the field must be numeric."),
)

syrian_mobile_validator = RegexValidator(
    regex=r"^09\d{8}$",
    message=_("the field must be syrian mobile number like 0947302503."),
)

syrian_phone_validator = RegexValidator(
    regex=r"^0\d{2}\d{6,7}$",
    message=_("the field must be syrian phone number like 0332756651."),
)

document_extension_validator = FileExtensionValidator(
    allowed_extensions=["pdf", "png", "jpg", "jpeg"],
    message=_("the field must be a valid pdf, png, jpg or jpeg file."),
)
