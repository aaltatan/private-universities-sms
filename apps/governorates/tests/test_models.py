from django.forms import ValidationError
from django.test import TestCase
from django.db.utils import IntegrityError

from ..models import Governorate


class GovernorateTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        Governorate.objects.create(name="محافظة حماه", description="حماه")
        Governorate.objects.create(name="محافظة حمص", description="حمص")
        Governorate.objects.create(name="محافظة ادلب", description="ادلب")
        Governorate.objects.create(name="محافظة المنيا", description="المنيا")

    def test_name_field(self):
        governorate = Governorate.objects.filter(name__contains="حماه").first()
        self.assertEqual(governorate.name, "محافظة حماه")
        governorate = Governorate.objects.filter(name__contains="حمص").first()
        self.assertEqual(governorate.name, "محافظة حمص")
        governorate = Governorate.objects.filter(name__contains="ادلب").first()
        self.assertEqual(governorate.name, "محافظة ادلب")
        governorate = Governorate.objects.filter(name__contains="المنيا").first()

    def test_length_of_the_queryset(self):
        self.assertEqual(Governorate.objects.count(), 4)

    def test_slug_field(self):
        governorate = Governorate.objects.filter(name__contains="حماه").first()
        self.assertEqual(governorate.slug, "محافظة-حماه")
        governorate = Governorate.objects.filter(name__contains="حمص").first()
        self.assertEqual(governorate.slug, "محافظة-حمص")
        governorate = Governorate.objects.filter(name__contains="ادلب").first()
        self.assertEqual(governorate.slug, "محافظة-ادلب")
        governorate = Governorate.objects.filter(name__contains="المنيا").first()
        self.assertEqual(governorate.slug, "محافظة-المنيا")

    def test_unique_name(self):
        with self.assertRaises(IntegrityError):
            Governorate.objects.create(name="محافظة حماه", description="حماه")

    def test_less_than_four_characters(self):
        with self.assertRaises(ValidationError):
            gov = Governorate.objects.create(name="ddd", description="حماه")
            gov.full_clean()
