# -*- coding: UTF-8 -*-
# Copyright 2013 Luc Saffre
# License: BSD (see file COPYING for details)

"""
The :xfile:`models` module of the :mod:`lino_faggio.rooms` app.

"""

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from lino import dd, rt

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
