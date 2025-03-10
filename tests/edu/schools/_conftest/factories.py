import factory

from tests.edu.school_kinds._conftest.factories import SchoolKindFactory
from tests.geo.nationalities._conftest.factories import NationalityFactory


class SchoolFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "edu.School"
        django_get_or_create = ("name",)

    name = factory.Sequence(
        lambda n: "School " + str(n + 1).rjust(3, "0"),
    )
    nationality = factory.SubFactory(NationalityFactory)
    kind = factory.SubFactory(SchoolKindFactory)
    email = factory.Sequence(
        lambda n: f"a.altatan-{n + 1}@gmail.com",
    )
    website = factory.Sequence(
        lambda n: f"https://google-{n + 1}.com",
    )
    phone = factory.Faker("phone_number")
    description = factory.Faker("text")
