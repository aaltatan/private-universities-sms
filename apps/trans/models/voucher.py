from typing import Any
import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_delete, pre_delete, pre_save
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext as _
from rest_framework import serializers

from apps.core import signals, validators
from apps.core.choices import MonthChoices, QuarterChoices
from apps.core.mixins import AddCreateActivityMixin
from apps.core.models import SoftDeleteAbstractModel, TimeStampAbstractModel, User
from apps.core.models.abstracts import UrlsMixin
from apps.fin.models import Period, VoucherKind

from ..managers import VoucherManager, VoucherProxyManager


class Voucher(
    UrlsMixin,
    AddCreateActivityMixin,
    SoftDeleteAbstractModel,
    TimeStampAbstractModel,
):
    class AuditedChoices(models.TextChoices):
        YES = True, _("audited").title()
        NO = False, _("not audited").title()

    class MigratedChoices(models.TextChoices):
        YES = True, _("migrated").title()
        NO = False, _("not migrated").title()

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
    )
    voucher_serial = models.CharField(
        max_length=20,
        verbose_name=_("voucher serial"),
        unique=True,
        editable=False,
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="vouchers",
        verbose_name=_("user"),
        blank=True,
        null=True,
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="updated_vouchers",
        verbose_name=_("updated by"),
        blank=True,
        null=True,
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        null=True,
        blank=True,
    )
    # basics
    title = models.CharField(
        max_length=255,
        verbose_name=_("title"),
    )
    date = models.DateField(
        verbose_name=_("date"),
    )
    # classification
    kind = models.ForeignKey(
        VoucherKind,
        on_delete=models.PROTECT,
        verbose_name=_("kind"),
        related_name="vouchers",
    )
    month = models.CharField(
        max_length=255,
        choices=MonthChoices.choices,
        default=MonthChoices.JANUARY,
        verbose_name=_("month"),
    )
    quarter = models.CharField(
        max_length=255,
        choices=QuarterChoices.choices,
        default=QuarterChoices.Q1,
        verbose_name=_("quarter"),
    )
    period = models.ForeignKey(
        Period,
        on_delete=models.PROTECT,
        verbose_name=_("period"),
        related_name="vouchers",
    )
    # organization
    notes = models.TextField(
        verbose_name=_("notes"),
        default="",
        blank=True,
    )
    serial_id = models.CharField(
        max_length=255,
        verbose_name=_("serial id"),
        default="",
        blank=True,
        help_text=_("dewan id if exists"),
    )
    serial_date = models.DateField(
        verbose_name=_("serial date"),
        blank=True,
        null=True,
        help_text=_("dewan date if exists"),
    )
    approve_date = models.DateField(
        verbose_name=_("approve date"),
        blank=True,
        null=True,
        help_text=_("date of approve by vouchers orderer (signature)"),
    )
    due_date = models.DateField(
        verbose_name=_("due date"),
        blank=True,
        null=True,
    )
    document = models.FileField(
        upload_to="vouchers",
        verbose_name=_("document"),
        blank=True,
        null=True,
        validators=[
            validators.pdf_image_extension_validator,
            validators.validate_pdf_image_mimetype,
        ],
    )
    accounting_journal_sequence = models.CharField(
        max_length=255,
        verbose_name=_("accounting journal sequence"),
        blank=True,
        default="",
        help_text=_(
            "the sequence of the accounting journal in accounting system e.g. JOV0001"
        ),
    )
    # functional
    is_audited = models.BooleanField(
        default=False,
        verbose_name=_("is audited"),
    )
    audited_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="audited_vouchers",
        verbose_name=_("audited by"),
        blank=True,
        null=True,
    )
    is_migrated = models.BooleanField(
        default=False,
        verbose_name=_("is migrated"),
    )

    objects: VoucherManager = VoucherManager()
    all_objects: VoucherProxyManager = VoucherProxyManager()

    def clean(self):
        errors: dict[str, ValidationError] = {}

        if self.is_migrated:
            raise ValidationError(
                _("you can't edit a voucher that is already migrated"),
            )

        if getattr(self, "due_date", None) and self.due_date < self.date:
            errors["due_date"] = ValidationError(
                _("due date cannot be earlier than date"),
            )

        if getattr(self, "approve_date", None) and self.approve_date > self.date:
            errors["approve_date"] = ValidationError(
                _("approve date cannot be later than date"),
            )

        if errors:
            raise ValidationError(errors)

    def save(
        self,
        *args,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
        audit=False,
    ):
        if not audit:
            self.is_audited = False
            self.audited_by = None

        return super().save(
            *args,
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )

    def audit(self, audited_by: User):
        """Audit the voucher"""
        if not self.is_audited:
            self.is_audited = True
            self.audited_by = audited_by
            self.save(audit=True)

    def migrate(self):
        """Migrate the voucher and generate a journal entry."""
        if not self.is_migrated:
            for transaction in self.transactions.all():
                transaction.migrate()

            self.is_migrated = True
            self.save(audit=True)

    def unmigrate(self):
        """Unmigrate the voucher."""
        if self.is_migrated:
            self.journals.all().delete()
            self.is_migrated = False
            self.accounting_journal_sequence = ""
            self.save()

    def get_totals(self, formatted: bool = True) -> dict[str, Any]:
        transactions = self.transactions.all()

        data = {
            "quantity": sum(trans.quantity for trans in transactions),
            "value": sum(trans.value for trans in transactions),
            "total": sum(trans.total for trans in transactions),
            "tax": sum(trans.tax for trans in transactions),
            "net": sum(trans.net for trans in transactions),
        }

        if formatted:
            data = {k: f"{v:,.2f}" for k, v in data.items()}

        return data

    def get_audit_url(self):
        return reverse(
            "trans:vouchers:audit",
            kwargs={"slug": self.slug},
        )

    def get_migrate_url(self):
        return reverse(
            "trans:vouchers:migrate",
            kwargs={"slug": self.slug},
        )

    def get_unmigrate_url(self):
        return reverse(
            "trans:vouchers:unmigrate",
            kwargs={"slug": self.slug},
        )

    def get_word_url(self):
        return reverse(
            "trans:vouchers:word",
            kwargs={"slug": self.slug},
        )

    def get_import_url(self):
        return reverse(
            "trans:vouchers:import",
            kwargs={"slug": self.slug},
        )

    def __str__(self):
        return f"{self.voucher_serial} ({self.title})"

    class Meta:
        icon = "document-check"
        ordering = ("is_migrated", "date", "-created_at", "voucher_serial")
        codename_plural = "vouchers"
        verbose_name = _("voucher").title()
        verbose_name_plural = _("vouchers").title()
        permissions = (
            ("export_voucher", "Can export voucher"),
            ("migrate_voucher", "Can migrate voucher"),
            ("unmigrate_voucher", "Can unmigrate voucher"),
            ("audit_voucher", "Can audit voucher"),
            ("unaudit_voucher", "Can unaudit voucher"),
            ("view_activity_voucher", "Can view voucher activity"),
        )


class VoucherProxy(Voucher):
    objects: VoucherProxyManager = VoucherProxyManager()

    class Meta:
        proxy = True
        verbose_name = _("voucher proxy")
        verbose_name_plural = _("all vouchers")
        codename_plural = "proxy_vouchers"


class ActivitySerializer(serializers.ModelSerializer):
    kind = serializers.CharField(source="kind.name")
    period = serializers.CharField(source="period.name")
    audited_by = serializers.SerializerMethodField()
    updated_by = serializers.SerializerMethodField()

    def get_updated_by(self, obj):
        return obj.updated_by.username if obj.updated_by else ""

    def get_audited_by(self, obj):
        return obj.audited_by.username if obj.audited_by else ""

    class Meta:
        model = Voucher
        fields = (
            "updated_by",
            "title",
            "date",
            "kind",
            "month",
            "quarter",
            "period",
            "notes",
            "serial_id",
            "serial_date",
            "approve_date",
            "due_date",
            "document",
            "accounting_journal_sequence",
            "is_audited",
            "audited_by",
            "is_migrated",
            "is_deleted",
        )


def slugify_voucher(sender, instance: Voucher, *args, **kwargs):
    if instance.slug is None:
        instance.slug = slugify(instance.voucher_serial, allow_unicode=True)


def generate_voucher_serial(sender, instance: Voucher, *args, **kwargs):
    Klass = instance.__class__
    if not instance.voucher_serial:
        instance.voucher_serial = Klass.all_objects.get_next_voucher_serial()


def voucher_post_delete(sender, instance: Voucher, *args, **kwargs):
    instance.document.delete()


pre_save.connect(generate_voucher_serial, sender=Voucher)
pre_save.connect(slugify_voucher, sender=Voucher)
pre_save.connect(signals.add_update_activity(ActivitySerializer), sender=Voucher)
pre_delete.connect(signals.add_delete_activity(ActivitySerializer), sender=Voucher)
pre_delete.connect(signals.add_delete_activity(ActivitySerializer), sender=VoucherProxy)
post_delete.connect(voucher_post_delete, sender=Voucher)
