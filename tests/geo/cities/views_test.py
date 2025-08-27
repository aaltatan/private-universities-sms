import pytest
from django.test import Client
from selectolax.parser import HTMLParser

from apps.geo.models import City
from tests.utils import is_template_used


@pytest.mark.django_db
def test_index_page_has_update_link_for_governorate(
    admin_client: Client,
    urls: dict[str, str],
    templates: dict[str, str],
    model: City,
):
    path = urls["index"] + "?ordering=id"
    response = admin_client.get(path)
    parser = HTMLParser(response.content)
    obj = model.objects.all().order_by("id").first()
    governorate = parser.css_first("td[data-header='governorate'] a")

    assert response.status_code == 200
    assert is_template_used(templates["index"], response)
    assert governorate is not None
    assert obj.governorate.get_absolute_url() in governorate.attributes["hx-get"]


@pytest.mark.django_db
def test_index_page_has_no_update_link_for_governorate_for_unauthorized_user(
    client: Client,
    urls: dict[str, str],
    templates: dict[str, str],
    model: City,
    subapp_label: str,
):
    client.login(
        username=f"{subapp_label}_user_with_view_perm_only",
        password="password",
    )
    path = urls["index"] + "?ordering=id"
    response = client.get(path)
    parser = HTMLParser(response.content)
    obj = model.objects.all().order_by("id").first()
    governorate = parser.css_first("td[data-header='governorate'] a")

    assert response.status_code == 200
    assert is_template_used(templates["index"], response)
    assert governorate is None

    governorate = parser.css_first(
        "td[data-header='governorate']",
    ).text(strip=True)

    assert obj.governorate.name == governorate
