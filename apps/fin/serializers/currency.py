from rest_framework import serializers

from .. import models


class CurrencySerializer(serializers.ModelSerializer):
    is_primary = serializers.BooleanField(read_only=True)

    class Meta:
        model = models.Currency
        fields = (
            "id",
            "name",
            "symbol",
            "code",
            "decimal_places",
            "fraction_name",
            "is_primary",
            "description",
        )
