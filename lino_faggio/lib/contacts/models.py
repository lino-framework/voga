# Copyright 2013-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
The :xfile:`models` module for the :mod:`lino_faggio.contacts` app.

"""


from django.utils.translation import ugettext_lazy as _

from lino.modlib.contacts.models import *

from lino.modlib.sales import models as sales
from lino.modlib.beid.mixins import BeIdCardHolder


class Person(Person, BeIdCardHolder):
    pass


class MyPartnerDetail(PartnerDetail, sales.PartnerDetailMixin):

    main = 'general more sales ledger'

    #~ general = dd.Panel(PartnerDetail.main,label=_("General"))

    general = dd.Panel("""
    address_box:60 contact_box:30
    bottom_box
    """, label=_("General"))

    more = dd.Panel("""
    id language
    addr1 url
    #courses.CoursesByCompany
    """, label=_("More"))

    ledger = dd.Panel("""
    sales.InvoiceablesByPartner
    # ledger.InvoicesByPartner
    ledger.MovementsByPartner
    """, label=dd.plugins.ledger.verbose_name)

    bottom_box = """
    remarks
    """

    address_box = """
    name
    country region city zip_code:10
    street:25 street_no street_box
    addr2
    """

    contact_box = """
    mti_navigator
    email
    phone
    fax
    gsm
    """


class MyCompanyDetail(CompanyDetail, MyPartnerDetail):

    # main = 'general more ledger'

    more = dd.Panel("""
    id language type vat_id
    addr1 url
    rooms.BookingsByCompany lists.MembersByPartner
    notes.NotesByCompany
    """, label=_("More"))

    address_box = """
    prefix name
    country region city zip_code:10
    street:25 street_no street_box
    addr2
    """

    contact_box = dd.Panel("""
    mti_navigator
    email:40
    phone
    gsm
    fax
    """)  # ,label = _("Contact"))

    bottom_box = """
    remarks contacts.RolesByCompany
    """


class MyPersonDetail(PersonDetail, MyPartnerDetail):

    main = 'general sales ledger more'

    general = dd.Panel("""
    address_box contact_box
    remarks contacts.RolesByPerson
    """, label=_("General"))

    more = dd.Panel("""
    id language url
    addr1 addr2 national_id
    notes.NotesByPerson  lists.MembersByPartner
    """, label=_("More"))

    personal = 'is_pupil is_teacher'

    address_box = """
    last_name first_name:15 #title:10
    country region city zip_code:10
    #street_prefix street:25 street_no street_box
    gender birth_date age:10 personal
    """


class PupilDetail(MyPersonDetail):

    main = 'general courses sales ledger more'

    personal = 'pupil_type'

    courses = dd.Panel("""
    courses.SuggestedCoursesByPupil
    courses.EnrolmentsByPupil
    """, label=dd.plugins.courses.verbose_name)


class TeacherDetail(MyPersonDetail):
    main = MyPersonDetail.main + \
        " courses.EventsByTeacher courses.CoursesByTeacher"
    personal = 'teacher_type'


@dd.receiver(dd.post_analyze)
def customize_contacts(sender, **kw):
    site = sender
    site.modules.contacts.Persons.set_detail_layout(MyPersonDetail())
    site.modules.contacts.Companies.set_detail_layout(MyCompanyDetail())
    site.modules.contacts.Partners.set_detail_layout(MyPartnerDetail())
    site.modules.courses.Pupils.set_detail_layout(PupilDetail())
    site.modules.courses.Teachers.set_detail_layout(TeacherDetail())
