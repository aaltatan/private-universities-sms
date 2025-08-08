from rest_framework import serializers

from .. import models


class CompensationSerializer(serializers.ModelSerializer):
    class TaxSerializer(serializers.ModelSerializer):
        class Meta:
            model = models.Tax
            fields = (
                "id",
                "name",
                "shortname",
                "percentage",
                "amount",
                "formula",
                "round_method",
                "rounded_to",
                "accounting_id",
                "description",
            )

    tax = TaxSerializer(read_only=True)

    class Meta:
        model = models.Compensation
        fields = (
            "id",
            "name",
            "shortname",
            "kind",
            "calculation_method",
            "round_method",
            "rounded_to",
            "value",
            "min_value",
            "max_value",
            "min_total",
            "min_total_formula",
            "restrict_to_min_total_value",
            "max_total",
            "max_total_formula",
            "restrict_to_max_total_value",
            "formula",
            "tax",
            "tax_classification",
            "affected_by_working_days",
            "is_active",
            "accounting_id",
            "description",
        )


class CreateUpdateCompensationSerializer(serializers.ModelSerializer):
    tax = serializers.PrimaryKeyRelatedField(
        queryset=models.Tax.objects.all(),
    )

    class Meta:
        model = models.Compensation
        fields = (
            "name",
            "shortname",
            "kind",
            "calculation_method",
            "tax",
            "tax_classification",
            "round_method",
            "rounded_to",
            "value",
            "min_value",
            "max_value",
            "min_total",
            "restrict_to_min_total_value",
            "max_total",
            "restrict_to_max_total_value",
            "affected_by_working_days",
            "formula",
            "accounting_id",
            "description",
        )
