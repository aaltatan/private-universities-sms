from rest_framework import routers

from apps.governorates.viewsets import GovernorateViewSet

router = routers.DefaultRouter()
router.register(r"governorates", GovernorateViewSet)
