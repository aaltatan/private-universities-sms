from rest_framework import serializers

from .. import models


class DepartmentSerializer(serializers.ModelSerializer):
    class CostCenterSerializer(serializers.ModelSerializer):
        class Meta:
            model = models.Department
            fields = ("id", "name", "description")

    cost_center = CostCenterSerializer(read_only=True)

    def get_fields(self):
        fields = super().get_fields()
        fields["children"] = DepartmentSerializer(many=True, read_only=True)
        return fields

    class Meta:
        model = models.Department
        fields = ("id", "name", "cost_center", "children", "description")


class DepartmentActivitySerializer(serializers.ModelSerializer):
    cost_center = serializers.CharField(source="cost_center.name")
    parent = serializers.SerializerMethodField()

    def get_parent(self, obj: models.Department):
        return obj.parent.name if obj.parent else "-"

    class Meta:
        model = models.Department
        fields = ("name", "cost_center", "parent", "description")


class CreateUpdateDepartmentSerializer(serializers.ModelSerializer):
    cost_center = serializers.PrimaryKeyRelatedField(
        queryset=models.CostCenter.objects.all(),
    )
    parent = serializers.PrimaryKeyRelatedField(
        queryset=models.Department.objects.all(),
    )

    class Meta:
        model = models.Department
        fields = ("name", "cost_center", "parent", "description")
