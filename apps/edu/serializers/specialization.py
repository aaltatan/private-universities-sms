from rest_framework import serializers

from .. import models


class SpecializationSerializer(serializers.ModelSerializer):
    is_specialist = serializers.BooleanField()

    class Meta:
        model = models.Specialization
        fields = (
            "id",
            "name",
            "is_specialist",
            "description",
        )


class SpecializationActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Specialization
        fields = (
            "id",
            "name",
            "is_specialist",
            "description",
        )
