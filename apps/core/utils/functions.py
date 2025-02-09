import re


def increase_slug_by_one(slug: str) -> str:
    """
    increases the slug by one.
    """
    if not slug:
        return slug

    slug = slug.lower()
    pattern = re.compile(r"([^0-9]*)(\d+)$")
    match_obj = pattern.match(slug)

    if match_obj:
        number = int(match_obj.groups()[-1]) + 1
        string = match_obj.groups()[0]
        increased_slug = f"{string}{number}"
    else:
        increased_slug = f"{slug}1"

    return increased_slug


def dict_to_css(styles: dict[str, str]) -> str:
    styles = [f"{key}: {value}; " for key, value in styles.items()]
    return "".join(styles).strip()


def get_differences(from_: dict, to: dict) -> dict:
    """
    Returns the differences between two dictionaries.
    """
    differences: set = set(from_.items()) ^ set(to.items())

    before: dict = {}
    after: dict = {}

    for key, value in differences:
        diff = key, value
        if diff in from_.items():
            before[key] = value
        else:
            after[key] = value

    if differences:
        return {"before": before, "after": after}
    else:
        return {}
