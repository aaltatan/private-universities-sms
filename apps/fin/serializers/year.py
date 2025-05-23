from rest_framework import serializers

from .. import models


class YearSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Year
        fields = ("id", "name", "description")
