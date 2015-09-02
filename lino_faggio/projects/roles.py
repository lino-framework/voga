# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Defines the standard user roles for `lino.projects.docs`.

See also :attr:`lino.core.site.Site.user_profiles_module`.

"""

from lino.core.roles import UserRole, SiteAdmin, SiteStaff
from lino.modlib.office.roles import OfficeStaff, OfficeUser
from lino.modlib.ledger.roles import LedgerUser, LedgerStaff


class SiteUser(OfficeUser, LedgerUser):
    pass


class SiteAdmin(SiteAdmin, OfficeStaff, LedgerStaff):
    pass


class Developer(SiteStaff):
    pass


class SeniorDeveloper(Developer):
    pass

from django.utils.translation import ugettext_lazy as _
from lino.modlib.users.choicelists import UserProfiles
UserProfiles.clear()
add = UserProfiles.add_item
add('000', _("Anonymous"), UserRole, name='anonymous', readonly=True)
add('100', _("User"), SiteUser, name='user')
add('500', _("Developer"), Developer, name='developer')
add('510', _("Senior Developer"), SeniorDeveloper, name='senior')
add('900', _("Administrator"), SiteAdmin, name='admin')
