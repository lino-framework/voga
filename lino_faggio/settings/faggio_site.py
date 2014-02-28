# -*- coding: UTF-8 -*-
# Copyright 2012-2014 Luc Saffre
# This file is part of the Lino project.
# Lino is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with Lino; if not, see <http://www.gnu.org/licenses/>.


from lino.projects.std.settings import *

from lino_faggio import SETUP_INFO

class Site(Site):
    version = SETUP_INFO['version']
    verbose_name = "Lino Faggio"
    url = SETUP_INFO['url']

    #~ help_url = "http://lino.saffre-rumma.net/az/index.html"

    migration_module = 'lino_faggio.migrate'

    userdocs_prefix = 'faggio.'

    demo_fixtures = 'std few_languages demo demo_bookings faggio demo2'.split()
    start_year = 2013

    ignore_dates_before = None

    user_model = 'users.User'

    languages = 'en de fr'

    use_eid_jslib = False

    show_internal_field_names = True

    def get_installed_apps(self):
        yield super(Site, self).get_installed_apps()
        yield 'django.contrib.contenttypes'
        yield 'lino.modlib.system'
        yield 'lino.modlib.users'
        yield 'lino.modlib.countries'
        yield 'lino_faggio.contacts'
        yield 'lino.modlib.lists'

        yield 'lino_faggio.courses'
        yield 'lino.modlib.extensible'
        yield 'lino_faggio.cal'
        yield 'lino_faggio.rooms'

        yield 'lino.modlib.products'
        yield 'lino.modlib.accounts'
        yield 'lino.modlib.ledger'
        yield 'lino.modlib.vat'
        #~ yield 'lino.modlib.declarations'
        #~ yield 'lino.modlib.sales'
        yield 'lino.modlib.auto.sales'
        yield 'lino.modlib.finan'

        #~ yield 'lino.modlib.households'
        yield 'lino.modlib.notes'
        yield 'lino.modlib.uploads'
        #~ yield 'lino.modlib.cal'

        yield 'lino.modlib.outbox'
        #~ yield 'lino.modlib.pages'
        #~ yield 'lino.modlib.courses'
        yield 'lino_faggio'

    def setup_choicelists(self):
        """
        This defines default user profiles for :mod:`lino_welfare`.
        """
        super(Site, self).setup_choicelists()

        #~ raise Exception(123)
        from lino import dd
        from django.utils.translation import ugettext_lazy as _
        dd.UserProfiles.reset('* office accounts')
        add = dd.UserProfiles.add_item

        add('000', _("Anonymous"),     '_ _ _', name='anonymous',
            readonly=True, authenticated=False)
        add('100', _("User"),          'U U U', name='user')
        add('900', _("Administrator"), 'A A A', name='admin')

        self.modules.vat.configure(default_vat_class='exempt')

    def get_admin_main_items(self, ar):
        yield self.modules.courses.ActiveCourses

    def setup_plugins(self):
        """
        Change the default value of certain plugin settings.

        - :setting:`accounts.ref_length` = 5
        - :setting:`humanlink.human_model` = 'pcsw.Client'
        
        """
        self.plugins.extensible.configure(calendar_start_hour=9)
        self.plugins.extensible.configure(calendar_end_hour=21)
        super(Site, self).setup_plugins()


