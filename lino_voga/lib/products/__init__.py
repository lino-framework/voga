# -*- coding: UTF-8 -*-
# Copyright 2016-2018 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""
The :ref:`voga` extension of :mod:`lino_xl.lib.products`.
"""

from lino_xl.lib.products import Plugin, _


class Plugin(Plugin):

    verbose_name = _("Fees")
    extends_models = ['Product', 'Category']

    def setup_main_menu(self, site, user_type, m):
        pass

    def setup_config_menu(self, site, user_type, m):
        m = m.add_menu(self.app_label, self.verbose_name)
        m.add_action('products.Products')
        m.add_action('products.Categories')

