#!/usr/bin/env python
if __name__ == "__main__":

    import os
    os.environ['DJANGO_SETTINGS_MODULE'] = 'lino_faggio.settings.demo'

    #~ from django.conf import settings
    from lino_faggio.settings import demo

    from django.core.management import execute_manager

    execute_manager(demo)
    #~ execute_manager(settings)







