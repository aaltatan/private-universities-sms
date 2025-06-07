from typing import Any, Callable

import magic
from django.core.exceptions import ValidationError
from django.core.validators import (
    FileExtensionValidator,
    MinLengthValidator,
    RegexValidator,
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

pdf_image_extension_validator = FileExtensionValidator(
    allowed_extensions=["pdf", "png", "jpg", "jpeg"],
    message=_("the field must be a valid pdf, png, jpg or jpeg file."),
)

image_extension_validator = FileExtensionValidator(
    allowed_extensions=["jpg", "jpeg", "png"],
    message=_("the field must be a valid jpg, jpeg or png file."),
)


def validate_file_mimetype(
    accepted_mimetypes: list[str], message: str = _("Unsupported file type.")
) -> Callable[[Any], None]:
    """
    Validates the file mimetype.

    Args:
        accepted_mimetypes (list[str]): The list of accepted mimetypes.
        message (str): The error message.

    Returns:
        Callable[[Any], None]: The validation function.
    """

    def _validate_file_mimetype(file) -> None:
        file_mimetype = magic.from_buffer(file.read(1024), mime=True)
        if file_mimetype not in accepted_mimetypes:
            raise ValidationError(message)

    return _validate_file_mimetype
