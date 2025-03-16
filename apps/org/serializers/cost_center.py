from rest_framework import serializers

from .. import models


class CostCenterSerializer(serializers.ModelSerializer):
    employees_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.CostCenter
        fields = (
            "id",
            "name",
            "accounting_id",
            "employees_count",
            "description",
        )
