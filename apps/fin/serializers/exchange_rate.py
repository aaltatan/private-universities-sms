from rest_framework import serializers

from .. import models


class ExchangeRateSerializer(serializers.ModelSerializer):
    currency = serializers.CharField(source="currency.name", read_only=True)
    code = serializers.CharField(source="currency.code", read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = models.ExchangeRate
        fields = (
            "id",
            "currency",
            "code",
            "created_at",
            "updated_at",
            "date",
            "rate",
            "notes",
        )


class ExchangeRateCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ExchangeRate
        fields = ("currency", "date", "rate", "notes")
