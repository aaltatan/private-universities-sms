from rest_framework import serializers

from .. import models


class CostCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CostCenter
        fields = ("id", "name", "accounting_id", "description")
