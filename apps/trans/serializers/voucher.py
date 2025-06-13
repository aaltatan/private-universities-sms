from rest_framework import serializers

from apps.core.models import User
from apps.fin.models import Period, VoucherKind, Year

from .. import models


class VoucherSerializer(serializers.ModelSerializer):
    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = (
                "id",
                "username",
                "firstname",
                "lastname",
                "email",
            )

    class VoucherKindSerializer(serializers.ModelSerializer):
        class Meta:
            model = VoucherKind
            fields = (
                "id",
                "name",
                "description",
            )

    class PeriodSerializer(serializers.ModelSerializer):
        class YearSerializer(serializers.ModelSerializer):
            class Meta:
                model = Year
                fields = (
                    "id",
                    "name",
                    "description",
                )

        year = YearSerializer(read_only=True)

        class Meta:
            model = Period
            fields = (
                "id",
                "name",
                "year",
                "start_date",
                "is_closed",
                "description",
            )

    created_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)
    audited_by = UserSerializer(read_only=True)
    kind = VoucherKindSerializer(read_only=True)
    period = PeriodSerializer(read_only=True)

    class Meta:
        model = models.Voucher
        fields = (
            "id",
            "created_at",
            "created_by",
            "updated_at",
            "updated_by",
            "slug",
            "uuid",
            #####
            "title",
            "date",
            #####
            "kind",
            "month",
            "quarter",
            "period",
            #####
            "notes",
            "serial_id",
            "serial_date",
            "approve_date",
            "due_date",
            "document",
            "accounting_journal_sequence",
            #####
            "is_audited",
            "audited_by",
            "is_migrated",
            "is_deleted",
        )
