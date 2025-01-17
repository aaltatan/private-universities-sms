from .base import *

ALLOWED_HOSTS = config('ALLOWED_HOSTS').split(';')

STATIC_ROOT = BASE_DIR / "staticfiles"
