# -*- coding: UTF-8 -*-
# Copyright 2013-2014 Luc Saffre
# This file is part of the Lino Faggio project.
# Lino Faggio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino Faggio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with Lino Faggio; if not, see <http://www.gnu.org/licenses/>.

"""
This is a real-world example of how the application developer
can provide automatic data migrations for :ref:`dpy`.

This module is used because a :ref:`faggio`
Site has :setting:`migration_module` set to ``"lino_faggio.migrate"``.

"""

import logging
logger = logging.getLogger(__name__)

import datetime
from decimal import Decimal
from django.conf import settings
from lino.core.dbutils import resolve_model
from lino.utils import mti
from lino.utils import dblogger
from lino import dd


def migrate_from_0_0_1(globals_dict):
    """
    - Renamed `countries.City` to `countries.Place`
    - removed field imode from contacts.Partner
    - renamed sales.PaymentTerm to vat.PaymentTerm
    """
    countries_Place = resolve_model("countries.Place")
    globals_dict.update(countries_City=countries_Place)

    globals_dict.update(
        sales_PaymentTerm=resolve_model("vat.PaymentTerm"))

    contacts_Partner = resolve_model("contacts.Partner")
    def create_contacts_partner(id, country_id, city_id, region_id, zip_code, name, addr1, street_prefix, street, street_no, street_box, addr2, language, email, url, phone, gsm, fax, remarks, invoicing_address_id, payment_term_id, vat_regime, imode_id):
        kw = dict()
        kw.update(id=id)
        kw.update(country_id=country_id)
        kw.update(city_id=city_id)
        kw.update(region_id=region_id)
        kw.update(zip_code=zip_code)
        kw.update(name=name)
        kw.update(addr1=addr1)
        kw.update(street_prefix=street_prefix)
        kw.update(street=street)
        kw.update(street_no=street_no)
        kw.update(street_box=street_box)
        kw.update(addr2=addr2)
        kw.update(language=language)
        kw.update(email=email)
        kw.update(url=url)
        kw.update(phone=phone)
        kw.update(gsm=gsm)
        kw.update(fax=fax)
        kw.update(remarks=remarks)
        kw.update(invoicing_address_id=invoicing_address_id)
        kw.update(payment_term_id=payment_term_id)
        kw.update(vat_regime=vat_regime)
        # kw.update(imode_id=imode_id)
        return contacts_Partner(**kw)
    globals_dict.update(create_contacts_partner=create_contacts_partner)

    return '0.0.2'


def migrate_from_0_0_2(globals_dict):
    "No changes that need explicit migration actions."
    return '0.0.3'
