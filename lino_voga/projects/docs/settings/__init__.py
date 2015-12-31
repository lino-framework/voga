"""
The settings used to build the docs
"""
import datetime
from lino_voga.projects.base import *


class Site(Site):

    # avoid name clash with `lino/projects/docs`:
    project_name = 'voga_std'

    languages = 'en'
    # languages = 'en de fr'
    title = "Lino Voga Reference"

    ignore_dates_before = None
    the_demo_date = datetime.date(2014, 06, 15)
    ignore_dates_after = datetime.date(2019, 05, 22)

    def setup_plugins(self):
        super(Site, self).setup_plugins()
        self.plugins.countries.configure(country_code='BE')
        self.plugins.ledger.configure(start_year=2014)
