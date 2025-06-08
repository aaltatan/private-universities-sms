from rest_framework import serializers

from .. import models


class CompensationSerializer(serializers.ModelSerializer):
    class TaxSerializer(serializers.ModelSerializer):
        class Meta:
            model = models.Tax
            fields = ("id", "name", "fixed", "rate", "rounded_to", "description")

    tax = TaxSerializer(read_only=True)

    class Meta:
        model = models.Compensation
        fields = (
            "id",
            "name",
            "shortname",
            "calculation_method",
            "round_method",
            "rounded_to",
            "value",
            "min_value",
            "max_value",
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
            "calculation_method",
            "tax",
            "tax_classification",
            "round_method",
            "rounded_to",
            "value",
            "min_value",
            "max_value",
            "affected_by_working_days",
            "formula",
            "accounting_id",
            "description",
        )
