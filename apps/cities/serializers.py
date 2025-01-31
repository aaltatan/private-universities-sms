from rest_framework import serializers

from apps.governorates.serializers import GovernorateSerializer

from .models import City


class CitySerializer(serializers.ModelSerializer):
    governorate = GovernorateSerializer(read_only=True)

    class Meta:
        model = City
        fields = "__all__"


class ActivitySerializer(serializers.ModelSerializer):
    governorate = serializers.SerializerMethodField()

    def get_governorate(self, obj: City):
        return obj.governorate.name

    class Meta:
        model = City
        fields = ("name", "governorate", "description")
