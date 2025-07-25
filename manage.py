#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hackathon_project.settings')
    
    # Enable debug mode for development
    if len(sys.argv) > 1 and sys.argv[1] == 'runserver':
        import logging
        logging.basicConfig(level=logging.INFO, format='%(levelname)s %(asctime)s %(name)s %(message)s')
        print("🚀 Starting Django server in DEBUG mode with comprehensive logging...")
    
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
