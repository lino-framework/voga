# -*- coding: UTF-8 -*-

from __future__ import unicode_literals
from __future__ import print_function

from lino_voga.projects.base import *


class Site(Site):

    title = "Lino Voga à la Roger"
    languages = "en de fr"

    demo_fixtures = """std few_languages few_countries euvatrates
    minimal_ledger demo demo_bookings buche demo2""".split()

    def setup_plugins(self):
        """
        Change the default value of certain plugin settings.
       
        """
        super(Site, self).setup_plugins()
        self.plugins.contacts.configure(hide_region=True)
        self.plugins.countries.configure(country_code='BE')
        self.plugins.ledger.configure(start_year=2014)

