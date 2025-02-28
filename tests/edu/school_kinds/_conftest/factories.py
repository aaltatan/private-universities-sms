import factory


class SchoolKindFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "edu.SchoolKind"
        django_get_or_create = ("name",)

    name = factory.Sequence(
        lambda n: "School " + str(n + 1).rjust(3, "0"),
    )
    is_governmental = factory.Iterator([True, False])
    is_virtual = factory.Iterator([True, False])
    description = factory.Faker("text")
