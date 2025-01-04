from .base import *


DEBUG = True

INSTALLED_APPS += [
    "silk",
]

MIDDLEWARE = [
    'silk.middleware.SilkyMiddleware',
    *MIDDLEWARE,
]

INTERNAL_IPS = [
    "127.0.0.1",
]