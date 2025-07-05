from rest_framework import serializers

from .. import models


class StatusSerializer(serializers.ModelSerializer):
    is_payable = serializers.BooleanField(required=False)
    is_separated = serializers.BooleanField(required=False)
    employees_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Status
        fields = (
            "id",
            "name",
            "is_payable",
            "is_separated",
            "employees_count",
            "description",
        )
