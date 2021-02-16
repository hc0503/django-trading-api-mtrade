#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

class TestCoverageException(Exception):
    pass

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mtrade.settings')

    # Set up Coverage
    try:
        command = sys.argv[1]
    except IndexError:
        command = "help"

    running_tests = (command == 'test')
    if running_tests:
        from coverage import Coverage
        cov = Coverage()
        cov.erase()
        cov.start()

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

    # Finalize Coverage
    if running_tests:
        threshold = 80
        cov.stop()
        cov.save()
        covered = cov.report()
        if covered < threshold:
            raise TestCoverageException("Coverage is below {}, please update your tests.".format(threshold))

if __name__ == '__main__':
    main()
