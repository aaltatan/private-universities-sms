from datetime import datetime
from typing import Literal

from django.db import connection
from django.http import HttpResponse
from django.test import Client
from selectolax.parser import HTMLParser


def get_token_headers(
    client: Client,
    admin: bool = False,
) -> dict[str, str]:
    response = client.post(
        "/api/token/",
        {
            "username": "admin" if admin else "user_with_no_perm",
            "password": "password",
        },
    )
    token = response.json()["access"]
    return {
        "Authorization": f"Bearer {token}",
    }


def parse_buttons(parser: HTMLParser) -> dict[str, bool]:
    add_btn = parser.css_first("[aria-label='create new object']")
    delete_btn = parser.css_first("a[aria-label='delete object']")
    delete_all_btn = parser.css_first("input[aria-label='delete all objects']")
    edit_btn = parser.css_first("a[aria-label='edit object']")
    export_btn = parser.css_first("a[aria-label^='export table']")

    return {
        "add_btn_exists": add_btn is not None,
        "delete_btn_exists": delete_btn is not None,
        "delete_all_btn_exists": delete_all_btn is not None,
        "edit_btn_exists": edit_btn is not None,
        "export_btn_exists": export_btn is not None,
    }


def is_template_used(
    template_name: str,
    response: HttpResponse,
    used: bool = True,
) -> bool:
    if used:
        return template_name in [t.name for t in response.templates]
    else:
        return template_name not in [t.name for t in response.templates]


def assert_export(
    admin_client: Client,
    urls: dict[str, str],
    headers_modal_GET: dict[str, str],
    filename: str,
    extension: Literal["xlsx", "csv", "json"],
) -> None:
    url = urls["index"] + f"?export=true&extension={extension}"

    content_types = {
        "xlsx": "application/vnd.ms-excel",
        "csv": "text/csv",
        "json": "application/json",
    }

    response = admin_client.get(url, headers=headers_modal_GET)

    assert response.status_code == 200
    assert "HX-Redirect" in response.headers

    url += "&redirected=true"
    response = admin_client.get(url, headers=headers_modal_GET)

    assert response.status_code == 200
    assert response.headers["Content-Type"] == content_types[extension]

    str_now_without_sec = datetime.now().strftime("%Y-%m-%d-%H-%M")
    filename_without_sec = f"{filename}-{str_now_without_sec}"

    assert filename_without_sec in response.headers["Content-Disposition"]


def reset_sequence(model):
    table_name = model._meta.db_table
    with connection.cursor() as cursor:
        cursor.execute(
            f"UPDATE sqlite_sequence SET seq = (SELECT MAX(id) FROM {table_name}) WHERE name = '{table_name}';"
        )
