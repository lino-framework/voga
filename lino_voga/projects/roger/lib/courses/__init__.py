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
An extension of :mod:`lino_voga.lib.courses`

.. autosummary::
   :toctree:

    management.commands.eiche2lino
    models
    desktop

"""

from lino_voga.lib.courses import Plugin


class Plugin(Plugin):
    # see blog 20160409
    extends_models = ['Pupil', 'Enrolment', 'Line']
    # extends_models = ['Pupil', 'Course', 'Enrolment']
    # extends_models = ['Pupil', 'Course', 'Line']

    # membership_fee_account = '7100'
    # membership_fee_account = 'membership_fee'
    membership_fee_account = None
    """The reference of the general account where membership fees are
    being booked.  Used by :class:`MemberChecker`.

    """

    def on_site_startup(self, site):
        from lino_xl.lib.ledger.accounts import MEMBERSHIP_FEE_ACCOUNT
        self.membership_fee_account = MEMBERSHIP_FEE_ACCOUNT
        super(Plugin, self).on_site_startup(site)
