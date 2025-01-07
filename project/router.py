from rest_framework import routers

from apps.governorates.views import GovernorateViewSet

router = routers.DefaultRouter()
router.register(r"governorates", GovernorateViewSet)
