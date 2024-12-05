#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from codeleap_network.settings import base as base_settings

def main():
    settings_definitions_based_on_debug = {
        True: 'codeleap_network.settings.local',
        False: 'codeleap_network.settings.production',
    }

    os.environ.setdefault(
        'DJANGO_SETTINGS_MODULE', 
        settings_definitions_based_on_debug[base_settings.DEBUG]
    )
    
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
