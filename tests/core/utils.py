from datetime import datetime
from typing import Literal

from django.test import Client
from selectolax.parser import HTMLParser


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

    str_now = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    filename = f"{filename}-{str_now}.{extension}"

    assert (
        response.headers["Content-Disposition"] == f'attachment; filename="{filename}"'
    )
