import factory


class GovernorateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "geo.Governorate"
        django_get_or_create = ("name",)

    name = factory.Iterator(
        [
            "محافظة حماه",
            "محافظة حمص",
            "محافظة دمشق",
            "محافظة ريف دمشق",
            "محافظة اللاذقية",
            "محافظة طرطوس",
            "محافظة ادلب",
            "محافظة دير الزور",
            "محافظة درعا",
            "محافظة حلب",
        ]
    )
    description = factory.Faker("text")


class CityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "geo.City"
        django_get_or_create = ("name",)

    name = factory.Sequence(lambda n: "City " + str(n + 1).rjust(3, "0"))
    governorate = factory.SubFactory(GovernorateFactory)
    description = factory.Faker("text")
