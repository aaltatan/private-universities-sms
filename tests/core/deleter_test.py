from typing import Any, Literal

import pytest
from django.db.models import QuerySet

from apps.core.models import AbstractUniqueNameModel as Model
from apps.core.utils import Deleter


class CustomDeleter(Deleter[Model]):
    success_obj_msg = "success obj message"
    error_obj_msg = "error obj message"
    success_qs_msg = "success qs message"
    error_qs_msg = "error qs message"

    def check_obj_executing_possibility(self, obj: Model) -> bool:
        return False

    def check_queryset_executing_possibility(self, qs: QuerySet) -> bool:
        return False


class CustomMessagesDeleter(Deleter[Model]):
    success_obj_msg = "success obj message"
    error_obj_msg = "error obj message"
    success_qs_msg = "success qs message"
    error_qs_msg = "error qs message"


@pytest.mark.django_db
def test_deleter_class_with_obj_error_status(model: type[Model]):
    obj = model.objects.filter(name__contains="حماه").first()
    deleter: Deleter = Deleter(obj=obj)

    assert deleter.action() is None
    assert deleter.has_executed is False
    assert deleter.get_message() == "{} cannot be deleted.".format("محافظة حماه")
    assert model.objects.count() == 4


@pytest.mark.django_db
def test_deleter_class_with_obj_success_status(model: type[Model]):
    obj = model.objects.filter(name__contains="دلب").first()
    deleter: Deleter = Deleter(obj=obj)

    assert deleter.action() == (1, {"geo.Governorate": 1})
    assert deleter.has_executed is True
    assert deleter.get_message() == "{} has been deleted successfully.".format(
        "محافظة ادلب"
    )
    assert model.objects.count() == 3


@pytest.mark.django_db
def test_deleter_class_with_qs_error_status(model: type[Model]):
    qs = model.objects.all()
    deleter: Deleter = Deleter(queryset=qs)

    assert deleter.action() is None
    assert deleter.has_executed is False
    assert (
        deleter.get_message()
        == "selected objects CANNOT be deleted because they are related to other objects."
    )
    assert model.objects.count() == 4


@pytest.mark.django_db
def test_deleter_class_with_qs_error_status_2(model: type[Model]):
    qs = model.objects.filter(pk__in=[1, 2])
    deleter: Deleter = Deleter(queryset=qs)

    assert deleter.action() is None
    assert deleter.has_executed is False
    assert (
        deleter.get_message()
        == "selected objects CANNOT be deleted because they are related to other objects."
    )
    assert model.objects.count() == 4


@pytest.mark.django_db
def test_deleter_class_with_qs_success_status(model: type[Model]):
    qs = model.objects.filter(pk__in=[3, 4])
    deleter: Deleter = Deleter(queryset=qs)

    assert deleter.action() == (2, {"geo.Governorate": 2})
    assert deleter.has_executed is True
    assert deleter.get_message() == "2 selected objects have been deleted successfully."
    assert model.objects.count() == 2


@pytest.mark.django_db
@pytest.mark.parametrize(
    "filters,kind,deleted_object,has_deleted,message,count",
    [
        (
            {"name__contains": "حماه"},
            "obj",
            None,
            False,
            "error obj message",
            4,
        ),
        (
            {"pk__in": [1, 2, 3, 4]},
            "qs",
            None,
            False,
            "error qs message",
            4,
        ),
        (
            {"pk": 3},
            "obj",
            (1, {"geo.Governorate": 1}),
            True,
            "success obj message",
            3,
        ),
        (
            {"pk__in": [3, 4]},
            "qs",
            (2, {"geo.Governorate": 2}),
            True,
            "success qs message",
            2,
        ),
    ],
)
def test_deleter_class_with_obj_with_custom_message(
    model: type[Model],
    filters: dict[str, Any],
    kind: Literal["obj", "qs"],
    deleted_object: tuple[int, dict[str, int]] | None,
    has_deleted: bool,
    message: str,
    count: int,
):
    if kind == "obj":
        obj = model.objects.filter(**filters).first()
        deleter = CustomMessagesDeleter(obj=obj)
    else:
        qs = model.objects.filter(**filters)
        deleter = CustomMessagesDeleter(queryset=qs)

    if deleted_object is None:
        assert deleter.action() is None
    else:
        assert deleter.action() == deleted_object

    assert deleter.has_executed is has_deleted
    assert deleter.get_message() == message
    assert model.objects.count() == count


@pytest.mark.django_db
def test_deleter_class_with_obj_with_custom_checking(model: type[Model]):
    qs = model.objects.all()
    for obj in qs:
        deleter = CustomDeleter(obj=obj)

        assert deleter.action() is None
        assert deleter.has_executed is False
        assert deleter.get_message() == "error obj message"
        assert model.objects.count() == 4


@pytest.mark.django_db
def test_deleter_class_with_qs_with_custom_checking(model: type[Model]):
    qs = model.objects.all()
    deleter = CustomDeleter(queryset=qs)

    assert deleter.action() is None
    assert deleter.has_executed is False
    assert deleter.get_message() == "error qs message"
    assert model.objects.count() == 4


@pytest.mark.django_db
def test_deleter_class_when_provide_qs_and_object(model: type[Model]):
    class InvalidDeleter(Deleter):
        pass

    with pytest.raises(ValueError):
        InvalidDeleter(
            queryset=model.objects.all(),
            obj=model.objects.first(),
        )


@pytest.mark.django_db
def test_deleter_class_when_not_provide_qs_or_object(model: type[Model]):
    class InvalidDeleter(Deleter):
        pass

    with pytest.raises(ValueError):
        InvalidDeleter()


@pytest.mark.django_db
def test_deleter_class_when_provide_qs_not_instance_of_queryset(
    model: type[Model],
):
    class InvalidDeleter(Deleter):
        pass

    with pytest.raises(ValueError):
        InvalidDeleter(queryset=model.objects.all().first())
