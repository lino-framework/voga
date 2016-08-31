# Copyright 2015 Luc Saffre
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

"""Defines the standard user roles for Lino Voga.

See also :attr:`lino.core.site.Site.user_profiles_module`.

"""

from lino.core.roles import UserRole, SiteAdmin, SiteStaff
from lino_xl.lib.contacts.roles import ContactsUser
from lino.modlib.office.roles import OfficeStaff, OfficeUser
from lino_cosi.lib.ledger.roles import LedgerUser, LedgerStaff
from lino_cosi.lib.sepa.roles import SepaStaff
from lino.modlib.plausibility.roles import PlausibilityUser


class SiteUser(ContactsUser, OfficeUser, LedgerUser, PlausibilityUser):
    pass


class Secretary(SiteUser, SiteStaff):
    pass


class SiteAdmin(SiteAdmin, OfficeStaff, LedgerStaff, SepaStaff,
                PlausibilityUser):
    pass


from django.utils.translation import ugettext_lazy as _
from lino.modlib.users.choicelists import UserProfiles
UserProfiles.clear()
add = UserProfiles.add_item
add('000', _("Anonymous"), UserRole, name='anonymous', readonly=True)
add('100', _("User"), SiteUser, name='user')
add('200', _("Secretary"), Secretary, name='secretary')
add('900', _("Administrator"), SiteAdmin, name='admin')
