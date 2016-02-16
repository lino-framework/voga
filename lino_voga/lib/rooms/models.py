# -*- coding: UTF-8 -*-
# Copyright 2013-2016 Luc Saffre
# License: BSD (see file COPYING for details)

"""
The :xfile:`models` module of the :mod:`lino_voga.rooms` app.

"""

from __future__ import unicode_literals

from lino.utils.mti import get_child
from lino.modlib.rooms.models import *
from lino.api import rt
from lino_cosi.lib.auto.sales.mixins import Invoiceable

sales = dd.resolve_app('sales')


class Booking(Booking, Invoiceable):

    invoiceable_date_field = 'start_date'
    #~ invoiceable_partner_field = 'company'

    create_invoice = sales.CreateInvoice()

    @classmethod
    def get_invoiceables_for_partner(cls, partner, max_date=None):
        # company = partner.get_mti_child(rt.modules.contacts.Company)
        company = get_child(partner, rt.modules.contacts.Company)
        if company:
            return cls.objects.filter(company=company, invoice__isnull=True)

    @classmethod
    def unused_get_partner_filter(cls, partner):
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
