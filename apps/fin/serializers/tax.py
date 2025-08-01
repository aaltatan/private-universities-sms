from rest_framework import serializers

from .. import models


class TaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tax
        fields = (
            "id",
            "name",
            "shortname",
            "amount",
            "percentage",
            "formula",
            "rate",
            "rounded_to",
            "round_method",
            "affected_by_working_days",
            "accounting_id",
            "description",
        )
