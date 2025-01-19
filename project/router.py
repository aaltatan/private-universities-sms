from rest_framework import routers

from apps.governorates.views import APIViewSet

router = routers.DefaultRouter()
router.register(r"governorates", APIViewSet)
