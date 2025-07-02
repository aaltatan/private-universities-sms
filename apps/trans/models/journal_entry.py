import uuid

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.translation import gettext as _

# from rest_framework import serializers
# from apps.core import signals
from apps.core.choices import MonthChoices, QuarterChoices

# from apps.core.mixins import AddCreateActivityMixin
from apps.core.models import TimeStampAbstractModel
from apps.core.models.abstracts import UrlsMixin
from apps.fin.models import Period
from apps.hr.models import Employee
from apps.org.models import CostCenter

from ..managers import JournalEntryManager


class JournalEntry(
    UrlsMixin,
    # AddCreateActivityMixin,
    TimeStampAbstractModel,
):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        null=True,
        blank=True,
    )
    date = models.DateField(
        verbose_name=_("date"),
        default=timezone.now,
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
        related_name="journals",
    )
    debit = models.DecimalField(
        max_digits=20,
        decimal_places=4,
        verbose_name=_("debit"),
        default=0,
    )
    credit = models.DecimalField(
        max_digits=20,
        decimal_places=4,
        verbose_name=_("credit"),
        default=0,
    )
    amount = models.GeneratedField(
        expression=models.F("debit") - models.F("credit"),
        verbose_name=_("amount"),
        output_field=models.DecimalField(max_digits=20, decimal_places=4),
        db_persist=False,
    )
    employee = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name="journals",
        verbose_name=_("employee"),
    )
    cost_center = models.ForeignKey(
        CostCenter,
        on_delete=models.PROTECT,
        related_name="journals",
        verbose_name=_("cost center"),
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={"model__in": ("compensation", "tax")},
    )
    fiscal_object_id = models.PositiveIntegerField(
        verbose_name=_("fiscal object id"),
        default=0,
    )
    fiscal_object = GenericForeignKey(
        ct_field="content_type",
        fk_field="fiscal_object_id",
    )
    voucher = models.ForeignKey(
        "Voucher",
        on_delete=models.PROTECT,
        related_name="journals",
        verbose_name=_("voucher"),
        blank=True,
        null=True,
    )
    explanation = models.TextField(
        verbose_name=_("explanation"),
        default="",
        blank=True,
    )
    notes = models.TextField(
        verbose_name=_("notes"),
        default="",
        blank=True,
    )
    ordering = models.PositiveIntegerField(
        default=0,
    )

    objects: JournalEntryManager = JournalEntryManager()

    def clean(self):
        errors: dict[str, ValidationError] = {}

        if self.debit != 0 and self.credit != 0:
            errors["debit"] = ValidationError(
                _("debit and credit cannot be both filled"),
            )
            errors["credit"] = ValidationError(
                _("debit and credit cannot be both filled"),
            )

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return f"{self.employee.fullname} ({self.amount:,.2f})"

    class Meta:
        icon = "circle-stack"
        ordering = ("-date", "ordering", "-debit")
        codename_plural = "journal_entries"
        verbose_name = _("journal entry").title()
        verbose_name_plural = _("journal entries").title()
        permissions = (
            ("export_journalentry", "Can export journal entry"),
            ("view_activity_journalentry", "Can view journal entry activity"),
        )


# class ActivitySerializer(serializers.ModelSerializer):
#     kind = serializers.CharField(source="kind.name")
#     period = serializers.CharField(source="period.name")
#     audited_by = serializers.SerializerMethodField()
#     updated_by = serializers.SerializerMethodField()

#     def get_updated_by(self, obj):
#         return obj.updated_by.username if obj.updated_by else ""

#     def get_audited_by(self, obj):
#         return obj.audited_by.username if obj.audited_by else ""

#     class Meta:
#         model = JournalEntry
#         fields = (
#             "updated_by",
#             "title",
#             "date",
#             "kind",
#             "month",
#             "quarter",
#             "period",
#             "notes",
#             "serial_id",
#             "serial_date",
#             "approve_date",
#             "due_date",
#             "document",
#             "accounting_journal_sequence",
#             "is_audited",
#             "audited_by",
#             "is_migrated",
#             "is_deleted",
#         )


def slugify_journal_entry(sender, instance: JournalEntry, *args, **kwargs):
    if instance.slug is None:
        instance.slug = instance.uuid.hex


pre_save.connect(slugify_journal_entry, sender=JournalEntry)
# pre_save.connect(signals.add_update_activity(ActivitySerializer), sender=JournalEntry)
# pre_delete.connect(signals.add_delete_activity(ActivitySerializer), sender=JournalEntry)
