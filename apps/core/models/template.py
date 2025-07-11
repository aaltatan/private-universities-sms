from django.db import models
from django.utils.translation import gettext as _

from .. import validators


class Template(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    uploaded_at = models.DateTimeField(auto_now=True)
    name = models.CharField(
        max_length=255,
        unique=True,
        validators=[validators.four_char_length_validator],
        verbose_name=_("name"),
    )
    file = models.FileField(
        upload_to="word_templates",
        verbose_name=_("file"),
        validators=[
            validators.docx_extension_validator,
            validators.validate_docx_mimetype,
        ],
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("template").title()
        verbose_name_plural = _("templates").title()
        ordering = ("name",)
