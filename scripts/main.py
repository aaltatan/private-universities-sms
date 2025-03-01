from apps.org.models import Department


def run():
    for department in Department.objects.all():
        print(department)
