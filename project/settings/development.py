from .base import *


INSTALLED_APPS += [
    "silk",
]

MIDDLEWARE += [
    "silk.middleware.SilkyMiddleware",
]

INTERNAL_IPS = [
    "127.0.0.1",
]
