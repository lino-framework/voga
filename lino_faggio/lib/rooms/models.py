# -*- coding: UTF-8 -*-
# Copyright 2013 Luc Saffre
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

"""
The :xfile:`models` module of the :mod:`lino_faggio.rooms` app.

"""

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from lino import dd

from lino.modlib.rooms.models import *

sales = dd.resolve_app('sales')


class Booking(Booking, sales.Invoiceable):

    invoiceable_date_field = 'start_date'
    #~ invoiceable_partner_field = 'company'

    create_invoice = sales.CreateInvoice()

    @classmethod
    def get_partner_filter(cls, partner):
        q = models.Q(company=partner, invoice__isnull=True)
        return q

    def get_invoiceable_product(self):
        #~ if self.organizer and self.room:
        if self.company and self.room:
            #~ if self.company != settings.SITE.site_config.site_company:
            return self.room.tariff

    #~ def get_invoiceable_title(self):
        #~ if self.organizer:
            #~ return unicode(self.room)

    def get_invoiceable_qty(self):
        return self.max_events or 1
