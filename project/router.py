from rest_framework import routers

from apps.governorates.views import APIViewSet as GovernorateAPIViewSet
from apps.cities.views import APIViewSet as CityAPIViewSet


router = routers.DefaultRouter()

router.register(r"governorates", GovernorateAPIViewSet)
router.register(r"cities", CityAPIViewSet)
