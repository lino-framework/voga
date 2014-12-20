# -*- coding: UTF-8 -*-

from __future__ import unicode_literals
from __future__ import print_function

import datetime

from lino_faggio.projects.base import *


class Site(Site):

    title = "Lino Faggio à la Roger"
    languages = "en de fr"

    demo_fixtures = """std few_languages few_countries euvatrates
    demo buche demo2""".split()

    def setup_plugins(self):
        """
        Change the default value of certain plugin settings.
       
        """
        self.plugins.contacts.configure(hide_region=True)
        self.plugins.vat.configure(country_code='BE')
        super(Site, self).setup_plugins()
