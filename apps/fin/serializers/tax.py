from rest_framework import serializers

from .. import models


class TaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tax
        fields = (
            "id",
            "name",
            "fixed",
            "rate",
            "rounded_to",
            "round_method",
            "description",
        )
