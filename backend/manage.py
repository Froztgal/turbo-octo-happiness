import os
import sys
import django
from django.core.management import execute_from_command_line


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config")
    django.setup()

    # Models must be imported in ./database/models/__init__.py
    # python manage.py makemigrations database
    # python manage.py migrate database

    execute_from_command_line(sys.argv)
