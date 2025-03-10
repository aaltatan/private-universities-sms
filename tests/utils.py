from typing import Literal
from django.db import connection
from django.http import HttpResponse
from django.test import Client
from selectolax.parser import HTMLParser, Node


def get_management_form(
    app_label: str,
    initial_forms: int = 0,
    total_forms: int = 0,
    min_num_forms: int = 0,
    max_num_forms: int = 1000,
) -> dict[str, int]:
    return {
        f"{app_label}-INITIAL_FORMS": str(initial_forms),
        f"{app_label}-TOTAL_FORMS": str(total_forms),
        f"{app_label}-MIN_NUM_FORMS": str(min_num_forms),
        f"{app_label}-MAX_NUM_FORMS": str(max_num_forms),
    }


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


def is_option_selected(
    node: Node,
    option_text: str,
    child_selector: str = "option",
    attr: str = "selected",
) -> bool:
    selected: bool = False

    for option in node.css(child_selector):
        if attr in option.attributes:
            selected = option.text(strip=True).lower() == option_text.lower()

    return selected


def is_required_star_visible(
    form: Node,
    input_name: str = "name",
    *,
    input_type: Literal["input", "select", "textarea"] = "input",
) -> bool:
    required_star = form.css_first(
        f"div[role='group']:has({input_type}[name='{input_name}']) span[aria-label='required field']"
    )
    visible = required_star.attributes.get("aria-hidden") == "false"

    return visible


def get_nested_create_btn(
    form: Node,
    input_name: str = "name",
    *,
    input_type: Literal["input", "select", "textarea"] = "input",
) -> Node:
    return form.css_first(
        f"div[role='group']:has({input_type}[name='{input_name}']) div[aria-label='create nested object']"
    )


def get_nested_hx_path(input: Node) -> str:
    return input.css_first("button").attributes.get("hx-get")
