import pytest
from django.test import Client
from selectolax.parser import HTMLParser

from apps.org.models import JobSubtype
from tests.utils import is_template_used


@pytest.mark.django_db
def test_index_page_has_update_link_for_job_type(
    admin_client: Client,
    urls: dict[str, str],
    templates: dict[str, str],
    model: JobSubtype,
):
    path = urls["index"] + "?ordering=id"
    response = admin_client.get(path)
    parser = HTMLParser(response.content)
    obj = model.objects.all().order_by("id").first()
    job_type = parser.css_first("td[data-header='job type'] a")

    assert response.status_code == 200
    assert is_template_used(templates["index"], response)
    assert job_type is not None
    assert obj.job_type.get_update_url() in job_type.attributes["hx-get"]


@pytest.mark.django_db
def test_index_page_has_no_update_link_for_governorate_for_unauthorized_user(
    client: Client,
    urls: dict[str, str],
    templates: dict[str, str],
    model: JobSubtype,
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
    job_type = parser.css_first("td[data-header='job type'] a")

    assert response.status_code == 200
    assert is_template_used(templates["index"], response)
    assert job_type is None

    job_type = parser.css_first(
        "td[data-header='job type']",
    ).text(strip=True)

    assert obj.job_type.name == job_type
