#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv


def main():
    """Run administrative tasks."""

    BASE_DIR = Path(__file__).resolve()
    dotenv_filepath = BASE_DIR / ".env"
    load_dotenv(dotenv_filepath)

    settings_module: Literal['development', 'deployment', 'testing'] = (
        "development" if os.getenv("DEBUG") == "1" else "deployment"
    )

    if 'test' in sys.argv:
        settings_module = "testing"

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"project.settings.{settings_module}")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
