"""
The settings used to build the docs
"""
import datetime
from lino_faggio.projects.base import *


class Site(Site):

    languages = 'en de fr'
    title = "Lino Faggio Reference"

    ignore_dates_before = None
    the_demo_date = datetime.date(2014, 06, 15)
    ignore_dates_after = datetime.date(2019, 05, 22)

