"""
The settings used for building `/docs` and `/userdocs`
"""
import datetime

from lino_faggio.settings import *


class Site(Site):

    title = "Lino Faggio demo"
    is_demo_site = True

    ignore_dates_before = None
    the_demo_date = datetime.date(2014, 06, 15)
    ignore_dates_after = datetime.date(2019, 05, 22)


SITE = Site(globals())
# the following line should not be active in a checked-in version
#~ DATABASES['default']['NAME'] = ':memory:'
