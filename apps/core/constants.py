from typing import Literal


PERMISSION = Literal["view", "add", "change", "delete", "export", "view_activity"]

MAX_PAGE_SIZE: int = 100

PER_PAGE: int = 10

MESSAGES_TIMEOUT: int = 7

PER_PAGE_ARRAY: int = [10, 20, 50, 100]
