# Copyright 2016-2017 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)
"""
An extension of :mod:`lino_voga.lib.courses`

.. autosummary::
   :toctree:

    management.commands.eiche2lino

"""

from lino_voga.lib.courses import Plugin


class Plugin(Plugin):
    # see blog 20160409
    extends_models = ['Pupil', 'Enrolment', 'Line']
    # extends_models = ['Pupil', 'Course', 'Enrolment']
    # extends_models = ['Pupil', 'Course', 'Line']

    # membership_fee_account = '7100'
    # membership_fee_account = 'membership_fee'
    # membership_fee_account = None
    # """The reference of the general account where membership fees are
    # being booked.  Used by :class:`MemberChecker`.

    # """

    # def on_site_startup(self, site):
    #     from lino_xl.lib.ledger.accounts import MEMBERSHIP_FEE_ACCOUNT
    #     self.membership_fee_account = MEMBERSHIP_FEE_ACCOUNT
    #     super(Plugin, self).on_site_startup(site)
