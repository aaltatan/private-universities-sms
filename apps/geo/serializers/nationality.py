from rest_framework import serializers

from .. import models


class NationalitySerializer(serializers.ModelSerializer):
    is_local = serializers.BooleanField(required=False)
    employees_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Nationality
        fields = ("id", "name", "is_local", "description", "employees_count")
