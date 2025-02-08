import factory


class GovernorateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "geo.Governorate"
        django_get_or_create = ("name",)

    name = factory.Iterator([
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
    ])
    description = factory.Faker("text")


class CityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "geo.City"
        django_get_or_create = ("name",)

    name = factory.Faker("name")
    governorate = factory.SubFactory(GovernorateFactory)
    description = factory.Faker("text")
