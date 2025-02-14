import factory


class JobTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "org.JobType"
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


class JobSubtypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "org.JobSubtype"
        django_get_or_create = ("name",)

    name = factory.Sequence(lambda n: "City " + str(n + 1).rjust(3, "0"))
    job_type = factory.SubFactory(JobTypeFactory)
    description = factory.Faker("text")
