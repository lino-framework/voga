# -*- coding: UTF-8 -*-
# Copyright 2016-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""The :xfile:`models.py` module for `lino_voga.lib.sales`.

"""

from __future__ import unicode_literals

from lino_xl.lib.sales.models import *
from lino.api import _


class InvoiceDetail(InvoiceDetail):
    totals = dd.Panel("""
    #total_base #total_vat
    total_incl
    balance_before
    balance_to_pay
    workflow_buttons
    """, label=_("Totals"))


# class InvoiceItem(InvoiceItem):

#     class Meta:
#         app_label = 'sales'
#         abstract = dd.is_abstract_model(__name__, 'InvoiceItem')
#         verbose_name = _("Product invoice item")
#         verbose_name_plural = _("Product invoice items")


class InvoiceItemDetail(InvoiceItemDetail):

    main = """
    seqno product discount
    unit_price qty total_base total_vat total_incl
    title
    invoiceable_type:15 invoiceable_id:15 invoiceable:50
    description
    """
    

VatProductInvoice.print_items_table = ItemsByInvoicePrintNoQtyColumn
