import sys
import os
import django
from django.core.management import execute_from_command_line

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings')
    django.setup()
    execute_from_command_line(sys.argv)
