from rest_framework import routers

from apps.geo.views.governorates import APIViewSet as GovernorateAPIViewSet
from apps.geo.views.cities import APIViewSet as CityAPIViewSet
from apps.geo.views.nationalities import APIViewSet as NationalityAPIViewSet
from apps.org.views.job_types import APIViewSet as JobTypeAPIViewSet
from apps.org.views.job_subtypes import APIViewSet as JobSubtypeAPIViewSet


router = routers.DefaultRouter()

router.register(r"governorates", GovernorateAPIViewSet)
router.register(r"cities", CityAPIViewSet)
router.register(r"nationalities", NationalityAPIViewSet)
router.register(r"job-types", JobTypeAPIViewSet)
router.register(r"job-subtypes", JobSubtypeAPIViewSet)
