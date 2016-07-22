# -*- coding: UTF-8 -*-
"""
The base settings module for :mod:`lino_voga.projects.roger`.
"""

from __future__ import unicode_literals
from __future__ import print_function

from lino_voga.projects.base import *


class Site(Site):
    """
    The `Site` class for this module.
    """

    # default_ui = 'lino_extjs6.extjs6'

    title = "Lino Voga à la Roger"
    languages = "en de fr"

    demo_fixtures = """std few_languages few_countries euvatrates
    minimal_ledger demo voga demo_bookings payments demo2 checkdata""".split()

    def setup_plugins(self):
        """
        Change the default value of certain plugin settings.
       
        """
        super(Site, self).setup_plugins()
        self.plugins.countries.configure(hide_region=True)
        self.plugins.countries.configure(country_code='BE')
        self.plugins.ledger.configure(start_year=2014)
        self.plugins.ledger.configure(use_pcmn=True)

    def get_apps_modifiers(self, **kw):
        kw = super(Site, self).get_apps_modifiers(**kw)
        # alternative implementations:
        kw.update(courses='lino_voga.projects.roger.lib.courses')
        return kw
