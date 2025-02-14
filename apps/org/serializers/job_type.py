from rest_framework import serializers

from .. import models


class JobTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.JobType
        fields = ("id", "name", "description")


class JobTypeActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.JobType
        fields = ("name", "description")
