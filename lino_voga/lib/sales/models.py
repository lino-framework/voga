# -*- coding: UTF-8 -*-
# Copyright 2016 Luc Saffre
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

"""The :xfile:`models.py` module for `lino_voga.lib.sales`.

"""

from __future__ import unicode_literals

from lino_cosi.lib.sales.models import *
from lino.api import _


class InvoiceItem(InvoiceItem):

    class Meta:
        app_label = 'sales'
        abstract = dd.is_abstract_model(__name__, 'InvoiceItem')
        verbose_name = _("Product invoice item")
        verbose_name_plural = _("Product invoice items")

    def full_clean(self):
        if self.invoiceable_id and not self.title:
            self.title = self.invoiceable.get_invoiceable_title()
            self.invoiceable.setup_invoice_item(self)
        super(InvoiceItem, self).full_clean()


InvoiceItems.detail_layout = dd.DetailLayout("""
seqno product discount
unit_price qty total_base total_vat total_incl
invoiceable title
description""", window_size=(80, 20))

# class InvoiceItems(InvoiceItems):

#     detail_layout = dd.DetailLayout("""
#     seqno product discount
#     unit_price qty total_base total_vat total_incl
#     invoiceable title
#     description""", window_size=(80, 20))

# class ItemsByInvoice(InvoiceItems):
