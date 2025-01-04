from content_settings.types.basic import SimpleInt
from content_settings.types.array import TypedStringsList


PER_PAGE: SimpleInt = SimpleInt(
    default="10",
    help="Number of items to show per page in list views.",
)

MESSAGES_TIMEOUT: SimpleInt = SimpleInt(
    default="7",
    help="Timeout for messages in seconds.",
)

PER_PAGE_ARRAY: TypedStringsList = TypedStringsList()
