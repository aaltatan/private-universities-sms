from rest_framework import serializers

from .. import models


class SpecializationSerializer(serializers.ModelSerializer):
    is_specialist = serializers.BooleanField()
    employees_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Specialization
        fields = (
            "id",
            "name",
            "is_specialist",
            "description",
            "employees_count",
        )
