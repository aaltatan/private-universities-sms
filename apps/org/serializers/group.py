from rest_framework import serializers

from .. import models


class GroupSerializer(serializers.ModelSerializer):
    employees_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Group
        fields = (
            "id",
            "name",
            "kind",
            "employees_count",
            "description",
        )
