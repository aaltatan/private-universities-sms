from django.db import connection
from django.http import HttpResponse
from django.test import Client
from selectolax.parser import HTMLParser


def get_token_headers(client: Client, admin: bool = False) -> dict[str, str]:
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
    activities_btn = parser.css_first("a[aria-label='object activities']")
    export_btn = parser.css_first("a[aria-label^='export table']")

    return {
        "add_btn_exists": add_btn is not None,
        "delete_btn_exists": delete_btn is not None,
        "delete_all_btn_exists": delete_all_btn is not None,
        "edit_btn_exists": edit_btn is not None,
        "activities_btn_exists": activities_btn is not None,
        "export_btn_exists": export_btn is not None,
    }


def is_template_used(
    template_name: str, response: HttpResponse, used: bool = True
) -> bool:
    if used:
        return template_name in [t.name for t in response.templates]
    else:
        return template_name not in [t.name for t in response.templates]


def reset_sequence(model):
    table_name = model._meta.db_table
    with connection.cursor() as cursor:
        cursor.execute(
            f"UPDATE sqlite_sequence SET seq = (SELECT MAX(id) FROM {table_name}) WHERE name = '{table_name}';"
        )
