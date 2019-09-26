#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'testone.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # cmd = 'java -jar /Users/vanthink_test_ios/Downloads/selenium-server-standalone-3.11.0.jar -role hub'
    # os.popen(cmd)
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
