from rest_framework import routers

# edu
from apps.edu.views.degrees import APIViewSet as DegreeAPIViewSet
from apps.edu.views.school_kinds import APIViewSet as SchoolKindAPIViewSet
from apps.edu.views.schools import APIViewSet as SchoolAPIViewSet
from apps.edu.views.specializations import APIViewSet as SpecializationAPIViewSet

# fin
from apps.fin.views.currencies import APIViewSet as CurrencyAPIViewSet

# geo
from apps.geo.views.cities import APIViewSet as CityAPIViewSet
from apps.geo.views.governorates import APIViewSet as GovernorateAPIViewSet
from apps.geo.views.nationalities import APIViewSet as NationalityAPIViewSet

# hr
from apps.hr.views.emails import APIViewSet as EmailAPIViewSet
from apps.hr.views.employees import APIViewSet as EmployeeAPIViewSet
from apps.hr.views.mobiles import APIViewSet as MobileAPIViewSet
from apps.hr.views.phones import APIViewSet as PhoneAPIViewSet

# org
from apps.org.views.cost_centers import APIViewSet as CostCenterAPIViewSet
from apps.org.views.groups import APIViewSet as GroupAPIViewSet
from apps.org.views.job_subtypes import APIViewSet as JobSubtypeAPIViewSet
from apps.org.views.job_types import APIViewSet as JobTypeAPIViewSet
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
# edu
router.register(r"edu/school-kinds", SchoolKindAPIViewSet)
router.register(r"edu/schools", SchoolAPIViewSet)
router.register(r"edu/specializations", SpecializationAPIViewSet)
router.register(r"edu/degrees", DegreeAPIViewSet)
# hr
router.register(r"hr/employees", EmployeeAPIViewSet)
router.register(r"hr/mobiles", MobileAPIViewSet)
router.register(r"hr/phones", PhoneAPIViewSet)
router.register(r"hr/emails", EmailAPIViewSet)
# fin
router.register(r"fin/currencies", CurrencyAPIViewSet)