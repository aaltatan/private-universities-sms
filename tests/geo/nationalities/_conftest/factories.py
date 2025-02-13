import factory

from apps.geo.models import Nationality


class NationalityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Nationality
        django_get_or_create = ("name",)

    name = factory.Sequence(
        lambda n: "Nationality " + str(n + 1).rjust(3, "0"),
    )
    is_local = factory.Iterator([True, False])
    description = factory.Faker("text")
