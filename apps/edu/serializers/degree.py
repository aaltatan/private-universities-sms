from rest_framework import serializers

from .. import models


class DegreeSerializer(serializers.ModelSerializer):
    is_academic = serializers.BooleanField()
    employees_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Degree
        fields = (
            "id",
            "name",
            "order",
            "is_academic",
            "description",
            "employees_count",
        )
