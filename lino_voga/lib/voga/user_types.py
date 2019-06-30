# Copyright 2015-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)
"""Defines the standard user roles for Lino Voga.

See also :ref:`voga.specs.profiles`.

See also :attr:`lino.core.site.Site.user_types_module`.

"""

from lino.core.roles import UserRole, SiteUser, SiteAdmin, SiteStaff, Explorer
from lino.modlib.office.roles import OfficeStaff, OfficeUser
from lino.modlib.about.roles import SiteSearcher
from lino_xl.lib.excerpts.roles import ExcerptsUser, ExcerptsStaff
from lino_xl.lib.contacts.roles import ContactsUser, ContactsStaff
from lino_xl.lib.ledger.roles import LedgerUser, VoucherSupervisor, LedgerStaff
from lino_xl.lib.notes.roles import NotesUser, NotesStaff
from lino_xl.lib.sepa.roles import SepaStaff
from lino_xl.lib.products.roles import ProductsStaff
from lino_xl.lib.courses.roles import CoursesTeacher, CoursesUser
from lino_xl.lib.cal.roles import GuestOperator
from lino.modlib.checkdata.roles import CheckdataUser


class Receptor(SiteUser, CoursesUser, ContactsUser, OfficeUser,
               NotesUser,
               LedgerUser, CheckdataUser, ExcerptsUser, SiteSearcher):
    pass


class Secretary(Receptor, SiteStaff, ContactsStaff, ExcerptsUser,
                VoucherSupervisor, ProductsStaff, Explorer, GuestOperator):
    pass


class Teacher(CoursesTeacher):  # , ExcerptsUser, OfficeUser):
    """Somebody who can just register presences of participants, i.e. mark
    them as absent or present.

    """
    pass


class SiteAdmin(SiteAdmin, CoursesUser, ContactsStaff, OfficeStaff,
                NotesStaff,
                LedgerStaff, SepaStaff, CheckdataUser, GuestOperator,
                ExcerptsStaff, ProductsStaff, Explorer, SiteSearcher):
    pass


from django.utils.translation import ugettext_lazy as _
from lino.modlib.users.choicelists import UserTypes
UserTypes.clear()
add = UserTypes.add_item
add('000', _("Anonymous"), UserRole, name='anonymous', readonly=True)
add('100', _("User"), Receptor, name='user')
add('200', _("Secretary"), Secretary, name='secretary')
add('300', _("Teacher"), Teacher, name='teacher')
add('900', _("Administrator"), SiteAdmin, name='admin')
