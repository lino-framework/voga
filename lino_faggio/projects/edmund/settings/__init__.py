# -*- coding: UTF-8 -*-

from __future__ import unicode_literals
from __future__ import print_function

import datetime

from lino_faggio.projects.base import *


class Site(Site):

    title = "Lino Faggio all'estone"
    languages = "et en"

    demo_fixtures = """std
    few_languages few_countries eesti few_cities
    euvatrates
    demo faggio demo2""".split()

    ignore_dates_before = None
    the_demo_date = datetime.date(2014, 9, 26)
    ignore_dates_after = datetime.date(2019, 05, 22)

    def setup_plugins(self):
        """
        Change the default value of certain plugin settings.
       
        """
        super(Site, self).setup_plugins()
        self.plugins.countries.configure(country_code='EE')
