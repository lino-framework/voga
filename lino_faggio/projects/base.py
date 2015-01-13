# -*- coding: UTF-8 -*-
# Copyright 2012-2014 Luc Saffre
# License: BSD (see file COPYING for details)

from lino.projects.std.settings import *

from lino_faggio import SETUP_INFO


class Site(Site):
    version = SETUP_INFO['version']
    verbose_name = "Lino Faggio"
    url = SETUP_INFO['url']

    #~ help_url = "http://lino.saffre-rumma.net/az/index.html"

    migration_class = 'lino_faggio.migrate.Migrator'

    userdocs_prefix = 'faggio.'

    demo_fixtures = 'std demo demo_bookings buche faggio demo2'.split()
    start_year = 2013

    user_model = 'users.User'

    languages = 'en de et'

    show_internal_field_names = True

    def get_installed_apps(self):
        yield super(Site, self).get_installed_apps()
        yield 'lino.modlib.contenttypes'
        yield 'lino.modlib.system'
        yield 'lino.modlib.users'
        yield 'lino.modlib.countries'
        yield 'lino_faggio.lib.contacts'
        yield 'lino.modlib.lists'
        yield 'lino.modlib.beid'

        yield 'lino_faggio.lib.courses'
        yield 'lino.modlib.extensible'
        yield 'lino_faggio.lib.cal'
        yield 'lino_faggio.lib.rooms'

        yield 'lino.modlib.products'
        yield 'lino.modlib.accounts'
        yield 'lino.modlib.ledger'
        yield 'lino.modlib.vat'
        #~ yield 'lino.modlib.declarations'
        #~ yield 'lino.modlib.sales'
        yield 'lino.modlib.auto.sales'
        yield 'lino.modlib.finan'
        yield 'lino.modlib.iban'

        #~ yield 'lino.modlib.households'
        yield 'lino.modlib.notes'
        yield 'lino.modlib.uploads'
        #~ yield 'lino.modlib.cal'

        yield 'lino.modlib.outbox'
        yield 'lino.modlib.excerpts'
        #~ yield 'lino.modlib.pages'
        #~ yield 'lino.modlib.courses'
        yield 'lino_faggio'

        yield 'lino.modlib.appypod'
        yield 'lino.modlib.export_excel'

    def setup_choicelists(self):
        """
        This defines default user profiles for :ref:`faggio`.
        """
        super(Site, self).setup_choicelists()

        from lino.modlib.users.choicelists import UserProfiles
        from django.utils.translation import ugettext_lazy as _

        UserProfiles.reset('* office accounts')
        add = UserProfiles.add_item

        add('000', _("Anonymous"),     '_ _ _', name='anonymous',
            readonly=True, authenticated=False)
        add('100', _("User"),          'U U U', name='user')
        add('900', _("Administrator"), 'A A A', name='admin')

    def get_admin_main_items(self):
        yield self.modules.courses.DraftCourses
        # yield self.modules.courses.ActiveCourses

    def setup_plugins(self):
        """
        Change the default value of certain plugin settings.
       
        """
        self.plugins.extensible.configure(calendar_start_hour=9)
        self.plugins.extensible.configure(calendar_end_hour=21)
        self.plugins.vat.configure(default_vat_class='exempt')
        super(Site, self).setup_plugins()
