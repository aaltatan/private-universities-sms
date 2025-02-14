from rest_framework import serializers

from .. import models


class JobTypeSerializer(serializers.ModelSerializer):
    class JobSubtypeSerializer(serializers.ModelSerializer):
        class Meta:
            model = models.JobSubtype
            fields = ("id", "name", "description")

    job_subtypes = JobSubtypeSerializer(many=True, read_only=True)

    class Meta:
        model = models.JobType
        fields = ("id", "name", "description", "job_subtypes")


class JobTypeActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.JobType
        fields = ("name", "description")
