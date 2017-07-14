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

"""
Adds some demo data specific to Lino Voga à la Roger.

    legacy_id
    section

    is_lfv
    is_ckk
    is_raviva
    member_until


"""

from lino.api import dd, rt, _
from lino.utils.cycler import Cycler

from lino_voga.lib.courses.fixtures.demo import objects as lib_objects


def objects():

    yield lib_objects()

    SECTIONS = Cycler(rt.models.courses.Sections.objects())

    for obj in rt.models.courses.Pupil.objects.order_by('id'):
        if obj.id % 5 == 0:
            obj.is_lfv = True
        if obj.id % 6 == 0:
            obj.is_ckk = True
        if obj.id % 4 == 0:
            obj.section = SECTIONS.pop()
        elif obj.id % 10 != 0:
            obj.member_until = dd.demo_date().replace(month=12, day=31)
        yield obj
    Account = rt.models.accounts.Account
    try:
        fee_account = Account.get_by_ref(
            dd.plugins.courses.membership_fee_account)
        fee_account.default_amount = 15
        yield fee_account
    except Account.DoesNotExist:
        fee_account = Account(
            ref=dd.plugins.courses.membership_fee_account,
            type=rt.models.accounts.AccountTypes.incomes,
            default_amount=15,
            **dd.str2kw('name', _("Membership fee")))
        

    Journal = rt.models.ledger.Journal
    USERS = Cycler(rt.models.users.User.objects.all())
    MEMBERS = Cycler(rt.models.courses.Pupil.objects.all())

    jnl = Journal.objects.get(ref='CSH')
    membership_payments = [
        (1, 3),
        (2, 1),
        (10, 2),
        (11, 4),
        (12, 5),
    ]
    REQUEST = rt.login()

    for month, number in membership_payments:
        date = dd.demo_date().replace(month=month)
        voucher = jnl.create_voucher(
            user=USERS.pop(),
            voucher_date=date)
        yield voucher
        for i in range(number):
            M = jnl.voucher_type.get_items_model()
            kw = dict(voucher=voucher)
            kw.update(partner=MEMBERS.pop(), date=date, account=fee_account)
            kw.update(
                amount=fee_account.default_amount, dc=fee_account.type.dc)
            yield M(**kw)
        voucher.register(REQUEST)
        voucher.save()

