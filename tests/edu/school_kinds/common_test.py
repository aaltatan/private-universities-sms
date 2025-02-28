import pytest

from tests import commons


@pytest.mark.django_db
class TestActions(commons.CommonActionsTests):
    pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class TestCreate(commons.CommonCreateTests):
    pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class TestDelete(commons.CommonDeleteTests):
    pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class TestExport(commons.CommonExportTests):
    pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class TestMixin(commons.CommonMixinTests):
    pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class TestPermissions(commons.CommonPermissionsTests):
    pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class TestQuerystring(commons.CommonQuerystringTests):
    pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class TestUpdate(commons.CommonUpdateTests):
    pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class TestViews(commons.CommonViewsTests):
    pytestmark = pytest.mark.django_db
