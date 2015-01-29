"""
The settings used to build the docs
"""
import datetime
from lino_faggio.projects.base import *


class Site(Site):

    project_name = 'faggio_std'  # avoid name clash with
                                 # `lino/projects/docs`.

    languages = 'en'
    # languages = 'en de fr'
    title = "Lino Faggio Reference"

    ignore_dates_before = None
    the_demo_date = datetime.date(2014, 06, 15)
    ignore_dates_after = datetime.date(2019, 05, 22)

    def setup_plugins(self):
        super(Site, self).setup_plugins()
        self.plugins.countries.configure(country_code='BE')
