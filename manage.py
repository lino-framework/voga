#!/usr/bin/env python
# import logging
# logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    import sys
    import os
    os.environ['DJANGO_SETTINGS_MODULE'] = 'lino_voga.projects.docs.settings.demo'
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
