from rest_framework import serializers

from .. import models


class TaxBracketSerializer(serializers.ModelSerializer):
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
        model = models.TaxBracket
        fields = (
            "id",
            "tax",
            "amount_from",
            "amount_to",
            "rate",
            "notes",
        )


class CreateUpdateTaxBracketSerializer(serializers.ModelSerializer):
    tax = serializers.PrimaryKeyRelatedField(
        queryset=models.Tax.objects.all(),
    )

    class Meta:
        model = models.TaxBracket
        fields = (
            "tax",
            "amount_from",
            "amount_to",
            "rate",
            "notes",
        )
