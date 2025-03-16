from rest_framework import serializers

from .. import models


class PositionSerializer(serializers.ModelSerializer):
    employees_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Position
        fields = (
            "id",
            "name",
            "order",
            "employees_count",
            "description",
        )
