from rest_framework import serializers

from apps.governorates.serializers import GovernorateSerializer

from .models import City



class CitySerializer(serializers.ModelSerializer):

    governorate = GovernorateSerializer(read_only=True)

    class Meta:
        model = City
        fields = "__all__"