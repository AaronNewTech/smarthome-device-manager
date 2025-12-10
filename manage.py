#!/usr/bin/env python
"""Django's command-line utility for administrative tasks.

This file has a small convenience tweak: if you run

    python manage.py runserver

without specifying a port, Django will default to localhost:5555.

We do this by setting the default values on the runserver Command class
imported from django.core.management.commands.runserver. This is a
lightweight, widely-used technique suitable for local development.

run seed data file:
python3 manage.py loaddata serve
r/apps/devices/fixtures/sample_data.json
 --verbosity 2


"""

import os
import sys

# Set default runserver host/port for local development (when no args are provided)
try:
    from django.core.management.commands.runserver import Command as runserver
    # listen on localhost and default port 5555
    # Use 'localhost' so the server binds to the platform's localhost name.
    runserver.default_addr = 'localhost'
    # default_port is expected to be an int; set to 5555
    runserver.default_port = 5555
except Exception:
    # If Django is not installed or import fails, we silently continue; manage.py
    # will raise the normal ImportError when attempting to run commands.
    pass


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
