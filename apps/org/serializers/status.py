from rest_framework import serializers

from .. import models


class StatusSerializer(serializers.ModelSerializer):
    is_payable = serializers.BooleanField(required=False)

    class Meta:
        model = models.Status
        fields = ("id", "name", "is_payable", "description")


class StatusActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Status
        fields = ("name", "is_payable", "description")
