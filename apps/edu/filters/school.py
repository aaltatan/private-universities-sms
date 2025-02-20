import django_filters as filters
from django.utils.translation import gettext_lazy as _

from apps.core.filters import (
    BaseNameDescriptionFilter,
    BaseQSearchFilter,
    FilterComboboxMixin,
    get_combobox_choices_filter,
    get_ordering_filter,
    get_text_filter,
)

from .. import models
from ..constants import schools as constants


class BaseSchoolFilter(BaseNameDescriptionFilter):
    is_governmental = filters.ChoiceFilter(
        label=_("is governmental").title(),
        choices=models.School.OwnershipChoices,
    )
    is_virtual = filters.ChoiceFilter(
        label=_("is virtual").title(),
        choices=models.School.VirtualChoices,
    )
    website = get_text_filter(
        label=_("website").title(),
        widget_type='url',
        placeholder=_("https://example.com"),
    )
    email = get_text_filter(
        label=_("email").title(),
        widget_type='email',
        placeholder=_("some-email@example.com"),
    )
    phone = get_text_filter(
        label=_("phone").title(),
        placeholder=_("phone number").title(),
    )

    class Meta:
        model = models.School
        fields = (
            "name",
            "nationality",
            "is_governmental",
            "is_virtual",
            "website",
            "email",
            "phone",
            "description",
        )


class APISchoolFilter(FilterComboboxMixin, BaseSchoolFilter):
    nationality = get_combobox_choices_filter(
        model=models.School,
        field_name="nationality__name",
        label=_("nationality"),
        api_filter=True,
    )


class SchoolFilter(
    FilterComboboxMixin,
    BaseQSearchFilter,
    BaseSchoolFilter,
):
    ordering = get_ordering_filter(constants.ORDERING_FIELDS)
    nationality = get_combobox_choices_filter(
        model=models.School,
        field_name="nationality__name",
        label=_("nationality"),
    )
