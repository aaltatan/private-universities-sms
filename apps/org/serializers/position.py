from rest_framework import serializers

from .. import models


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Position
        fields = ("id", "name", "order", "description")


class PositionActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Position
        fields = ("name", "order", "description")
