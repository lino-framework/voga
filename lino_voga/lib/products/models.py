# -*- coding: UTF-8 -*-
# Copyright 2016-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""The :xfile:`models.py` module for `lino_voga.lib.products`.

In Lino Voga we don't call them "products" but "Fees".

And we make them less visible by moving them from the main menu to the
configuration menu.

"""

from __future__ import unicode_literals

from lino_xl.lib.products.models import *
from lino.api import _

ProductTypes.clear()
add = ProductTypes.add_item
add('100', _("Fees"), 'default', table_name="products.Products")


class ProductCat(ProductCat):
    """
    Currently this just changes the `verbose_name`.

    """
    class Meta(ProductCat.Meta):
        app_label = 'products'
        abstract = dd.is_abstract_model(__name__, 'ProductCat')
        verbose_name = _("Fee category")
        verbose_name_plural = _("Fee categories")


class Product(Product):
    """Adds two fields

    .. attribute:: number_of_events

        Number of calendar events paid per invoicing.

    .. attribute:: min_asset

        Minimum quantity required to trigger an invoice.
    

    """

    class Meta(Product.Meta):
        app_label = 'products'
        abstract = dd.is_abstract_model(__name__, 'Product')
        verbose_name = _("Fee")
        verbose_name_plural = _("Fees")

#     number_of_events = models.IntegerField(
#         _("Number of events"), null=True, blank=True,
#         help_text=_("Number of calendar events paid per invoicing."))

#     min_asset = models.IntegerField(
#         _("Invoice threshold"), blank=True, default=1,
#         help_text=_("Minimum quantity to pay in advance."))


class ProductDetail(ProductDetail):

    main = "general courses"
    
    general = dd.Panel("""
    id cat sales_price tariff
    # tariff__number_of_events:10 tariff__min_asset:10
    vat_class delivery_unit
    name
    description
    """, _("General"))

    courses = dd.Panel("""
    courses.EnrolmentsByFee
    courses.EnrolmentsByOption
    """, _("Enrolments"))


