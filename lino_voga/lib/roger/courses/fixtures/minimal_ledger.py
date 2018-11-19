# -*- coding: UTF-8 -*-
# Copyright 2017-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

from lino.api import dd
from lino_xl.lib.sheets.choicelists import CommonItems
from lino_xl.lib.ledger.choicelists import CommonAccounts

def objects():
    obj = CommonAccounts.membership_fees.get_object()
    obj.default_amount = 15
    obj.needs_partner = True
    if dd.is_installed('sheets'):
        obj.sheet_item = CommonItems.sales.get_object()
    yield obj
    
