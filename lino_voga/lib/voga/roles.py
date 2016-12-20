# Copyright 2015-2016 Luc Saffre
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

See also :ref:`voga.specs.profiles`.

See also :attr:`lino.core.site.Site.user_types_module`.

"""

from lino.core.roles import UserRole, SiteAdmin, SiteStaff
from lino_xl.lib.contacts.roles import ContactsUser, ContactsStaff
from lino.modlib.office.roles import OfficeStaff, OfficeUser
from lino_cosi.lib.ledger.roles import LedgerUser, LedgerStaff
from lino_cosi.lib.sepa.roles import SepaStaff
from lino_cosi.lib.courses.roles import CoursesUser
from lino.modlib.plausibility.roles import PlausibilityUser


class SiteUser(CoursesUser, ContactsUser, OfficeUser, LedgerUser, PlausibilityUser):
    pass


class Secretary(SiteUser, SiteStaff, ContactsStaff):
    pass


class SiteAdmin(CoursesUser, SiteAdmin, OfficeStaff, LedgerStaff,
                SepaStaff, PlausibilityUser):
    pass


from django.utils.translation import ugettext_lazy as _
from lino.modlib.users.choicelists import UserTypes
UserTypes.clear()
add = UserTypes.add_item
add('000', _("Anonymous"), UserRole, name='anonymous', readonly=True)
add('100', _("User"), SiteUser, name='user')
add('200', _("Secretary"), Secretary, name='secretary')
add('900', _("Administrator"), SiteAdmin, name='admin')
