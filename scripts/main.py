from django.urls import reverse


def run():
    url = reverse("governorates:cities", kwargs={"slug": "محافظة-حماه"})

    print(url)