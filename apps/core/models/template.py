from django.db import models
from django.utils.translation import gettext as _

from .. import validators
from .abstracts import SingletonModelMixin


class TemplateItem(models.Model):
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
        verbose_name = _("template item").title()
        verbose_name_plural = _("template items").title()
        ordering = ("name",)


class Template(SingletonModelMixin, models.Model):
    voucher = models.OneToOneField(
        TemplateItem,
        on_delete=models.PROTECT,
        related_name="voucher_template",
        verbose_name=_("voucher template"),
    )
    employee = models.OneToOneField(
        TemplateItem,
        on_delete=models.PROTECT,
        related_name="employee_template",
        verbose_name=_("employee template"),
    )
    ledger = models.OneToOneField(
        TemplateItem,
        on_delete=models.PROTECT,
        related_name="ledger_template",
        verbose_name=_("ledger template"),
    )

    @classmethod
    def get_ledger_template(cls):
        return cls.objects.first().ledger.file

    @classmethod
    def get_employee_template(cls):
        return cls.objects.first().employee.file

    @classmethod
    def get_voucher_template(cls):
        return cls.objects.first().voucher.file

    def __str__(self):
        return f"VoucherSetting(voucher={self.voucher}, employee={self.employee}, ledger={self.ledger})"

    class Meta:
        verbose_name = _("template").title()
        verbose_name_plural = _("templates").title()
        ordering = ("voucher__name",)
