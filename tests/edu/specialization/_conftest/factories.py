import factory

from apps.edu.models import Specialization


class SpecializationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Specialization
        django_get_or_create = ("name",)

    name = factory.Sequence(
        lambda n: "Specialization " + str(n + 1).rjust(3, "0"),
    )
    is_specialist = factory.Iterator([True, False])
    description = factory.Faker("text")