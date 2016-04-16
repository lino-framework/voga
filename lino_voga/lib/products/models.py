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

"""The :xfile:`models.py` module for `lino_voga.lib.products`.

In Lino Voga we don't call them "products" but "tariffs".

And we make them less visible by moving them from the main menu to the
configuration menu.

"""

from __future__ import unicode_literals

from lino_xl.lib.products.models import *
from lino.api import _


class ProductCat(ProductCat):
    """
    Currently this just changes the `verbose_name`.

    """
    class Meta(ProductCat.Meta):
        app_label = 'products'
        abstract = dd.is_abstract_model(__name__, 'ProductCat')
        verbose_name = _("Tariff Category")
        verbose_name_plural = _("Tariff Categories")


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
        verbose_name = _("Tariff")
        verbose_name_plural = _("Tariffs")

    number_of_events = models.IntegerField(
        _("Number of events"), null=True, blank=True,
        help_text=_("Number of calendar events paid per invoicing."))

    min_asset = models.IntegerField(
        _("Invoice threshold"), blank=True, default=1,
        help_text=_("Minimum quantity to pay in advance."))


class ProductDetail(dd.DetailLayout):

    main = "general courses"
    general = dd.Panel("""
    id cat vat_class sales_price number_of_events:10 min_asset:10
    name
    description
    """, _("General"))

    courses = dd.Panel("""
    courses.EnrolmentsByFee
    courses.EnrolmentsByOption
    """, _("Enrolments"))


Products.detail_layout = ProductDetail()
