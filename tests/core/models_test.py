import pytest

from apps.core.models import AbstractUniqueNameModel as Model


@pytest.mark.django_db
def test_slug_signal(model: type[Model]):
    names = [
        "abcdefghijklmnopqrstuvwxyz",
        "Abcdefghijklmnopqrstuvwxyz",
        "ABcdefghijklmnopqrstuvwxyz",
        "AbCDefghijklmnopqrstuvwxyz",
        "ABCdEFgHIJKLMNOPQRSTUVWXYZ",
        "ABCdEFgHIJKLMNOPQRSTUVWxYZ",
        "ABCdEFgHIJKLMNOPQRSTUVWxyz",
        "ABCdEFgHIJKLMNOPqRSTUVWxyz",
        "ABCdEFgHIJKLMnOPqRSTUVWxyz",
        "ABCdEFgHIJKLmnOPqRSTUVWxyz",
        "ABCdEFgHIJKLmnOPqRSTUVwxyz",
        "ABCdEFgHIJKLmnOPqRSTUvwxyz",
        "ABCdEFgHIJKLmnOPqRSTuvwxyz",
        "ABCdEFgHIJKLmnOPqRStuvwxyz",
        "ABCdEFgHIJKLmnOPqRstuvwxyz",
        "ABCdEFgHIJKLmnOPqrstuvwxyz",
        "ABCdEFgHIJKLmnOpqrstuvwxyz",
    ]
    names += [name.swapcase() for name in names]

    for idx, name in enumerate(names):
        obj = model.objects.create(name=name)
        if idx == 0:
            assert obj.slug == "abcdefghijklmnopqrstuvwxyz"
        else:
            assert obj.slug == f"abcdefghijklmnopqrstuvwxyz{idx}"

    names = [
        "google is",
        "google-is",
        "google----is",
        "google       is",
        "google       is   ",
        "   google       is   ",
    ]
    names += [name.swapcase() for name in names]

    for idx, name in enumerate(names):
        obj = model.objects.create(name=name)
        if idx == 0:
            assert obj.slug == "google-is"
        else:
            assert obj.slug == f"google-is{idx}"
