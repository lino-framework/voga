import datetime

from lino_voga.projects.roger.settings import *


class Site(Site):
    is_demo_site = True
    the_demo_date = datetime.date(2014, 05, 22)
    ignore_dates_after = datetime.date(2019, 05, 22)


SITE = Site(globals())
DEBUG = True

# the following line should not be active in a checked-in version
# DATABASES['default']['NAME'] = ':memory:'
