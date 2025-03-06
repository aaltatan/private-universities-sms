import factory


class GroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "org.Group"
        django_get_or_create = ("name",)

    name = factory.Sequence(lambda n: "Group " + str(n + 1).rjust(3, "0"))
    kind = factory.Iterator(["administrative", "academic"])
    description = factory.Faker("text")
