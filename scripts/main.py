from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType



def run():
    perm = Permission.objects.get(
        codename="view_group",
        content_type=ContentType.objects.get(app_label="org", model="group"),
    )
    print(perm)
