from apps.org.models import Department

from icecream import ic


def run():
    qs = Department.objects.filter(name__contains="رئاس")
    qs = Department.objects.get_queryset_descendants(qs)
    ic(qs)