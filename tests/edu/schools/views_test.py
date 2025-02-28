import pytest
from django.test import Client
from selectolax.parser import HTMLParser

from apps.geo.models import City
from tests.utils import is_template_used


@pytest.mark.django_db
def test_index_page_has_update_link_for_nested_objects(
    admin_client: Client,
    urls: dict[str, str],
    templates: dict[str, str],
    model: City,
):
    path = urls["index"] + "?ordering=id"
    response = admin_client.get(path)
    parser = HTMLParser(response.content)
    obj = model.objects.all().order_by("id").first()
    nationality = parser.css_first("td[data-header='nationality'] a")
    kind = parser.css_first("td[data-header='kind'] a")

    assert response.status_code == 200
    assert is_template_used(templates["index"], response)
    assert nationality is not None
    assert kind is not None
    assert obj.nationality.get_update_url() in nationality.attributes["hx-get"]
    assert obj.nationality.get_update_url() in nationality.attributes["hx-get"]


@pytest.mark.django_db
def test_index_page_has_no_update_link_for_nested_objects_for_unauthorized_user(
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
    nationality = parser.css_first("td[data-header='nationality'] a")
    kind = parser.css_first("td[data-header='kind'] a")

    assert response.status_code == 200
    assert is_template_used(templates["index"], response)
    assert nationality is None
    assert kind is None

    nationality = parser.css_first(
        "td[data-header='nationality']",
    ).text(strip=True)
    kind = parser.css_first("td[data-header='kind']").text(strip=True)

    assert obj.nationality.name == nationality
    assert obj.kind.name == kind
