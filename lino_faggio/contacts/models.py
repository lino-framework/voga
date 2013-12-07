## Copyright 2013 Luc Saffre
## This file is part of the Lino-Faggio project.
## Lino-Faggio is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino-Faggio is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino-Faggio; if not, see <http://www.gnu.org/licenses/>.

"""
The :xfile:`models` module for the :mod:`lino_faggio.contacts` app.

"""



from django.db import models
from django.db.models import loading
from django.utils.translation import ugettext_lazy as _


from lino.modlib.contacts.models import *

ledger = dd.resolve_app('ledger')

    
class Person(Person, mixins.Born):
    pass


class MyPartnerDetail(PartnerDetail):
    
    main = 'general more ledger'
    
    #~ general = dd.Panel(PartnerDetail.main,label=_("General"))
    
    general = dd.Panel("""
    address_box:60 contact_box:30
    bottom_box
    """,label = _("General"))
    
    more = dd.Panel("""
    id language 
    addr1 url
    #courses.CoursesByCompany
    rooms.BookingsByCompany
    """,label = _("More"))
    
    ledger = dd.Panel("""
    sales.InvoiceablesByPartner
    # ledger.InvoicesByPartner
    ledger.MovementsByPartner
    """, label=ledger.MODULE_LABEL)

    bottom_box = """
    remarks 
    is_person is_company #is_household
    """    
    
    address_box = """
    name
    country city zip_code:10
    street:25 street_no street_box
    addr2
    """
    
    contact_box = """
    email
    phone 
    fax
    gsm
    """
    
    

class MyCompanyDetail(CompanyDetail,MyPartnerDetail):
    
    main = 'general more ledger'
    
    more = dd.Panel("""
    id language type vat_id:12
    addr1 url
    rooms.BookingsByCompany
    notes.NotesByCompany
    """,label = _("More"))
    
    address_box = """
    prefix name
    country city zip_code:10
    street:25 street_no street_box
    addr2
    """
    
    contact_box = dd.Panel("""
    email:40 
    phone
    gsm 
    fax
    """) # ,label = _("Contact"))
    

    bottom_box = """
    remarks contacts.RolesByCompany
    """
    
    
    
    
    
class MyPersonDetail(PersonDetail,MyPartnerDetail):
   
    main = 'general more ledger'
    
    general = dd.Panel("""
    address_box contact_box
    remarks contacts.RolesByPerson 
    """,label = _("General"))

    more = dd.Panel("""
    id language 
    addr1 url
    gender birth_date age:10 personal
    notes.NotesByPerson
    """,label = _("More"))
    
    personal = 'is_pupil is_teacher'
    
    address_box = """
    last_name first_name:15 #title:10
    country city zip_code:10
    #street_prefix street:25 street_no street_box
    addr2:40
    """
    

class PupilDetail(MyPersonDetail):
    
    main = MyPersonDetail.main + " courses.EnrolmentsByPupil"
    personal = 'pupil_type'

    
class TeacherDetail(MyPersonDetail):
    main = MyPersonDetail.main + " courses.EventsByTeacher courses.CoursesByTeacher"
    personal = 'teacher_type'

        
     
@dd.receiver(dd.post_analyze)
def customize_contacts(sender,**kw):
    site = sender
    site.modules.contacts.Persons.set_detail_layout(MyPersonDetail())
    site.modules.contacts.Companies.set_detail_layout(MyCompanyDetail())
    site.modules.contacts.Partners.set_detail_layout(MyPartnerDetail())
    #~ site.modules.contacts.Partners.set_detail_layout(bottom_box = """
    #~ remarks 
    #~ is_person is_company #is_household
    #~ """)
    #~ site.modules.contacts.Partners.add_detail_tab("sales.InvoiceablesByPartner")
    site.modules.courses.Pupils.set_detail_layout(PupilDetail())
    site.modules.courses.Teachers.set_detail_layout(TeacherDetail())
    

