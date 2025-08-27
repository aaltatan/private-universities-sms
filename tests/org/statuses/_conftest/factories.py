import factory

from apps.org.models import Status


class StatusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Status
        django_get_or_create = ("name",)

    name = factory.Sequence(
        lambda n: "Status " + str(n + 1).rjust(3, "0"),
    )
    is_payable = factory.Iterator([True, False])
    is_separated = factory.Iterator([True, False])
    description = factory.Faker("text")
