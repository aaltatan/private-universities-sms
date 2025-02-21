import factory

from tests.geo.nationalities._conftest.factories import NationalityFactory


class SchoolFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "edu.School"
        django_get_or_create = ("name",)

    name = factory.Sequence(
        lambda n: "School " + str(n + 1).rjust(3, "0"),
    )
    nationality = factory.SubFactory(NationalityFactory)
    is_governmental = factory.Iterator([True, False])
    is_virtual = factory.Iterator([True, False])
    website = factory.Faker("url")
    email = factory.Faker("email")
    phone = factory.Faker("phone_number")
    description = factory.Faker("text")
