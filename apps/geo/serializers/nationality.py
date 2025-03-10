from rest_framework import serializers

from .. import models


class NationalitySerializer(serializers.ModelSerializer):
    is_local = serializers.BooleanField(required=False)

    class Meta:
        model = models.Nationality
        fields = ("id", "name", "is_local", "description")
