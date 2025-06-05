from typing import Literal

from django.utils.html import format_html

BADGE_COLOR = Literal["green", "orangered", "red", "blue", "lime", "black"]


def dict_to_css(styles: dict[str, str]) -> str:
    styles = [f"{key}: {value}; " for key, value in styles.items()]
    return "".join(styles).strip()


def dict_to_html_attributes(**kwargs: str) -> str:
    return " ".join(
        [f'{key.replace("_", "-")}="{value}"' for key, value in kwargs.items()]
    )


def badge_component(
    background_color: BADGE_COLOR, text: str, **attributes: dict[str, str]
) -> str:
    styles = {
        "color": "white",
        "border-radius": "0.25rem",
        "padding": "0.125rem 0.25rem",
        "font-size": "0.75rem",
        "text-transform": "capitalize",
        "font-weight": "bold",
    }
    styles["background-color"] = background_color
    attributes = dict_to_html_attributes(**attributes)
    return format_html(
        f'<div style="{dict_to_css(styles)}" {attributes}>{text}</div>',
    )
