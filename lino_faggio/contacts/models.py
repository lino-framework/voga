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


from django.db import models
from django.db.models import loading
from django.utils.translation import ugettext_lazy as _


#~ from lino import dd
#~ from lino import mixins
#~ from lino.models import SiteConfig

#~ from lino.modlib.contacts import models as contacts
#~ from lino.modlib.cal import models as cal

#~ from lino.modlib.contacts.models import models as contacts
from lino.modlib.contacts.models import *

#~ print dd

#~ PartnerField = contacts.PartnerField

#~ contacts = dd.resolve_app('contacts')
ledger = dd.resolve_app('ledger')
#~ sales = dd.resolve_app('sales')
#~ cal = dd.resolve_app('cal')
#~ school = dd.resolve_app('school')

#~ print 20130607, loading.cache.postponed

    
class Person(Person,mixins.Born):
    pass


class MyCompanyDetail(CompanyDetail):
    
    main = 'general more sales.InvoiceablesByPartner ledger'
    
    general = dd.Panel("""
    address_box:60 contact_box:30
    bottom_box
    """,label = _("General"))
    
    more = dd.Panel("""
    id language type vat_id:12
    addr1 url
    school.CoursesByCompany
    """,label = _("More"))
    
    address_box = dd.Panel("""
    prefix name
    country city zip_code:10
    street:25 street_no street_box
    addr2
    """) # ,label = _("Address"))
    
    contact_box = dd.Panel("""
    email:40 
    phone
    gsm 
    fax
    """) # ,label = _("Contact"))
    

    bottom_box = """
    remarks contacts.RolesByCompany
    """
    
    ledger = dd.Panel("""
    ledger.InvoicesByPartner
    ledger.MovementsByPartner
    """,label=ledger.MODULE_LABEL)
    
    
class MyPersonDetail(PersonDetail):
   
    #~ main = "contact outbox calendar"
    
    main = 'general more sales.InvoiceablesByPartner ledger'
    
    general = dd.Panel("""
    box1 box2
    remarks contacts.RolesByPerson 
    """,label = _("General"))

    more = dd.Panel("""
    id language 
    addr1 url
    gender birth_date age:10 personal
    """,label = _("More"))
    
    personal = 'is_pupil is_teacher'
    
    box1 = """
    last_name first_name:15 #title:10
    country city zip_code:10
    #street_prefix street:25 street_no street_box
    addr2:40
    """
    
    box2 = """
    email
    phone 
    fax
    gsm
    """
    
    ledger = dd.Panel("""
    ledger.InvoicesByPartner
    ledger.MovementsByPartner
    """,label=ledger.MODULE_LABEL)
    


class PupilDetail(MyPersonDetail):
    
    main = MyPersonDetail.main + " school.EnrolmentsByPupil"
    personal = 'pupil_type'

    
class TeacherDetail(MyPersonDetail):
    main = MyPersonDetail.main + " school.EventsByTeacher school.CoursesByTeacher"
    personal = 'teacher_type'

        
     
@dd.receiver(dd.post_analyze)
def customize_contacts(sender,**kw):
    site = sender
    site.modules.contacts.Persons.set_detail_layout(MyPersonDetail())
    site.modules.contacts.Companies.set_detail_layout(MyCompanyDetail())
    site.modules.contacts.Partners.set_detail_layout(bottom_box = """
    remarks 
    is_person is_company #is_household
    """)
    site.modules.school.Pupils.set_detail_layout(PupilDetail())
    site.modules.school.Teachers.set_detail_layout(TeacherDetail())
    

