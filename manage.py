#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
# from django_tor import run_with_tor
# from django.core.management.commands.runserver import Command as runserver

# if sys.argv[1] == 'runserver':
#     host, port = run_with_tor()
#     runserver.default_port = str(port)
#     from scam.settings import ALLOWED_HOSTS
#     ALLOWED_HOSTS.append(host)


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scam.settings')
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
