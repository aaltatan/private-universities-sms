from rest_framework import routers

# geo
from apps.geo.views.governorates import APIViewSet as GovernorateAPIViewSet
from apps.geo.views.cities import APIViewSet as CityAPIViewSet
from apps.geo.views.nationalities import APIViewSet as NationalityAPIViewSet
# org
from apps.org.views.job_types import APIViewSet as JobTypeAPIViewSet
from apps.org.views.job_subtypes import APIViewSet as JobSubtypeAPIViewSet
from apps.org.views.groups import APIViewSet as GroupAPIViewSet
from apps.org.views.cost_centers import APIViewSet as CostCenterAPIViewSet
from apps.org.views.positions import APIViewSet as PositionAPIViewSet
from apps.org.views.statuses import APIViewSet as StatusAPIViewSet


router = routers.DefaultRouter()

# geo
router.register(r"geo/governorates", GovernorateAPIViewSet)
router.register(r"geo/cities", CityAPIViewSet)
router.register(r"geo/nationalities", NationalityAPIViewSet)
# org
router.register(r"org/job-types", JobTypeAPIViewSet)
router.register(r"org/job-subtypes", JobSubtypeAPIViewSet)
router.register(r"org/groups", GroupAPIViewSet)
router.register(r"org/cost-centers", CostCenterAPIViewSet)
router.register(r"org/positions", PositionAPIViewSet)
router.register(r"org/statuses", StatusAPIViewSet)
