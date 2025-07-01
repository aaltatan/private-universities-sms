from apps.core.models import Activity


def run():
    Activity.objects.all().delete()
