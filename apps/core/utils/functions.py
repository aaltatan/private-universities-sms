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
