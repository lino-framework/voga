# -*- coding: UTF-8 -*-
# Copyright 2016-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)
"""
Adds some demo data specific to Lino Voga à la Roger.

    legacy_id
    section

    is_lfv
    is_ckk
    is_raviva
    member_until


"""

from builtins import range
from lino.api import dd, rt
from lino.utils.cycler import Cycler

from lino_xl.lib.ledger.choicelists import CommonAccounts
from lino_xl.lib.ledger.utils import CREDIT

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
    fee_account = CommonAccounts.membership_fees.get_object()

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
                amount=fee_account.default_amount, dc=CREDIT)
            yield M(**kw)
        voucher.register(REQUEST)
        voucher.save()

