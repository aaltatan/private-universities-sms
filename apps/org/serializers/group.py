from rest_framework import serializers

from .. import models


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Group
        fields = ("id", "name", "kind", "description")


class GroupActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Group
        fields = ("name", "kind", "description")
