from rest_framework import serializers

from .. import models


class DegreeSerializer(serializers.ModelSerializer):
    is_academic = serializers.BooleanField()

    class Meta:
        model = models.Degree
        fields = (
            "id",
            "name",
            "order",
            "is_academic",
            "description",
        )


class DegreeActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Degree
        fields = (
            "id",
            "name",
            "order",
            "is_academic",
            "description",
        )
