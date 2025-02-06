from rest_framework import routers

from apps.geo.views.governorates import APIViewSet as GovernorateAPIViewSet
from apps.geo.views.cities import APIViewSet as CityAPIViewSet


router = routers.DefaultRouter()

router.register(r"governorates", GovernorateAPIViewSet)
router.register(r"cities", CityAPIViewSet)
