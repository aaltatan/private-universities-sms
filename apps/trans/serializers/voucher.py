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
                "first_name",
                "last_name",
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

    class TransactionsSerializer(serializers.ModelSerializer):
        employee = serializers.SerializerMethodField()
        compensation = serializers.SerializerMethodField()
        total = serializers.SerializerMethodField()
        net = serializers.SerializerMethodField()

        def get_total(self, obj):
            return obj.total
        
        def get_net(self, obj):
            return obj.net

        def get_employee(self, obj):
            return obj.employee.get_fullname()

        def get_compensation(self, obj):
            return str(obj.compensation)

        class Meta:
            model = models.VoucherTransaction
            fields = (
                "id",
                "employee",
                "compensation",
                "quantity",
                "value",
                "total",
                "tax",
                "net",
                "notes",
            )

    created_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)
    audited_by = UserSerializer(read_only=True)
    kind = VoucherKindSerializer(read_only=True)
    period = PeriodSerializer(read_only=True)
    month = serializers.SerializerMethodField()
    quarter = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()
    transactions_count = serializers.SerializerMethodField()
    quantity_total = serializers.SerializerMethodField()
    value_total = serializers.SerializerMethodField()
    tax_total = serializers.SerializerMethodField()
    net = serializers.SerializerMethodField()
    transactions = TransactionsSerializer(many=True, read_only=True)

    def get_total(self, obj):
        return obj.total
    
    def get_transactions_count(self, obj):
        return obj.transactions_count
    
    def get_quantity_total(self, obj):
        return obj.quantity_total
    
    def get_value_total(self, obj):
        return obj.value_total
    
    def get_tax_total(self, obj):
        return obj.tax_total
    
    def get_net(self, obj):
        return obj.net

    def get_month(self, obj):
        return obj.get_month_display()

    def get_quarter(self, obj):
        return obj.get_quarter_display()

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
            #####
            "total",
            "transactions_count",
            "quantity_total",
            "value_total",
            "tax_total",
            "net",
            "transactions",
        )
