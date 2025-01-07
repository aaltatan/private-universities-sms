from rest_framework import serializers

from .models import Governorate


class GovernorateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Governorate
        fields = "__all__"