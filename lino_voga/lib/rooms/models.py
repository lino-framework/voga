# -*- coding: UTF-8 -*-
# Copyright 2013-2016 Luc Saffre
# This file is part of Lino Voga.
#
# Lino Voga is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Lino Voga is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with Lino Voga.  If not, see
# <http://www.gnu.org/licenses/>.

"""
The :xfile:`models` module of the :mod:`lino_voga.rooms` app.

"""

from __future__ import unicode_literals

from lino.utils.mti import get_child
from lino_xl.lib.rooms.models import *
from lino.api import rt
from lino_cosi.lib.auto.sales.mixins import Invoiceable

sales = dd.resolve_app('sales')


class Booking(Booking, Invoiceable):

    invoiceable_date_field = 'start_date'
    #~ invoiceable_partner_field = 'company'

    create_invoice = sales.CreateInvoice()

    @classmethod
    def get_invoiceables_for_partner(cls, partner, max_date):
        # company = partner.get_mti_child(rt.modules.contacts.Company)
        company = get_child(partner, rt.modules.contacts.Company)
        if company:
            qs = cls.objects.filter(company=company)
            qs = qs.filter(**{cls.invoiceable_date_field + '__lte': max_date})
            for obj in qs.order_by(cls.invoiceable_date_field):
                yield obj

    def get_invoiceable_product(self):
        if self.company and self.room:
            if self.get_invoicings().count() > 0:
                return
            # if self.company != settings.SITE.site_config.site_company:
            return self.room.fee

    #~ def get_invoiceable_title(self):
        #~ if self.organizer:
            #~ return unicode(self.room)

    def get_invoiceable_qty(self):
        return self.max_events or 1
