from rest_framework import routers

from apps.geo.views.governorates import APIViewSet as GovernorateAPIViewSet
from apps.geo.views.cities import APIViewSet as CityAPIViewSet
from apps.geo.views.nationalities import APIViewSet as NationalityAPIViewSet


router = routers.DefaultRouter()

router.register(r"governorates", GovernorateAPIViewSet)
router.register(r"cities", CityAPIViewSet)
router.register(r"nationalities", NationalityAPIViewSet)
