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
from django.utils.translation import ugettext_lazy as _


from lino import dd
from lino import mixins
#~ from lino.models import SiteConfig

#~ from lino.modlib.contacts import models as contacts
#~ from lino.modlib.cal import models as cal

contacts = dd.resolve_app('contacts')
#~ cal = dd.resolve_app('cal')
#~ school = dd.resolve_app('school')


class Person(contacts.Person,mixins.Born):
    class Meta(contacts.Person.Meta):
        app_label = 'contacts'


class CompanyDetail(contacts.CompanyDetail):
    
    main = 'general more'
    
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
    
class PersonDetail(contacts.PersonDetail):
   
    #~ main = "contact outbox calendar"
    
    main = 'general more'
    
    general = dd.Panel("""
    box1 box2
    remarks contacts.RolesByPerson 
    """,label = _("General"))

    more = dd.Panel("""
    id language 
    addr1 url
    gender birth_date age:10 personal
    households.MembersByPerson
    """,label = _("More"))
    
    personal = 'is_pupil is_teacher'
    
    #~ main = dd.Panel("""
    #~ box1 box2
    #~ remarks contacts.RolesByPerson #households.MembersByPerson
    #~ """,label = _("Contact"))
    
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
    
    
    #~ def setup_handle(self,lh):
      
        #~ lh.contact.label = _("Contact")
        #~ lh.mails.label = _("Mails")


class PupilDetail(PersonDetail):
    
    main = "general more school.EnrolmentsByPupil"

    personal = ''
    
class TeacherDetail(PersonDetail):
    main = "general more school.EventsByTeacher school.CoursesByTeacher"
    personal = ''

#~ class Company(contacts.Partner,contacts.CompanyMixin):
    #~ class Meta(contacts.CompanyMixin.Meta):
        #~ app_label = 'contacts'
        #~ # see :doc:`/tickets/14`
        #~ verbose_name = _("Company")
        #~ verbose_name_plural = _("Companies")
        
#~ class Event(cal.Event):
    #~ class Meta(cal.Event.Meta):
        #~ app_label = 'cal'

#~ class Task(cal.Task):
    #~ class Meta(cal.Task.Meta):
        #~ app_label = 'cal'
        
        
#~ class EventDetail(cal.EventDetail):
#~ class EventDetail(dd.FormLayout):
    #~ main = "general more"
    
    #~ lesson = dd.Panel("""
    #~ owner start_date start_time end_time place 
    #~ school.PresencesByEvent
    #~ """,label=_("Lesson"))
    
  
    #~ event = dd.Panel("""
    #~ id:8 user priority access_class transparent #rset 
    #~ summary state workflow_buttons 
    #~ calendar created:20 modified:20 
    #~ description
    #~ cal.GuestsByEvent 
    #~ """,label=_("Event"))
    
    #~ main = "lesson event"

    #~ def setup_handle(self,lh):
      
        #~ lh.lesson.label = _("Lesson")
        #~ lh.event.label = 
        #~ lh.notes.label = _("Notes")

     
     
def site_setup(site):
    site.modules.contacts.Persons.set_detail_layout(PersonDetail())
    site.modules.contacts.Companies.set_detail_layout(CompanyDetail())
    site.modules.school.Pupils.set_detail_layout(PupilDetail())
    site.modules.school.Teachers.set_detail_layout(TeacherDetail())
    site.modules.contacts.Partners.set_detail_layout(bottom_box = """
    remarks 
    is_person is_company is_household
    """
)
    
    #~ site.modules.cal.Events.set_detail_layout(EventDetail())
    site.modules.cal.Events.set_detail_layout('general more')
    site.modules.cal.Events.add_detail_panel('general',"""
    calendar summary user project 
    start end 
    place priority access_class transparent #rset 
    owner workflow_buttons
    description cal.GuestsByEvent 
    """,_("General"))
    
    site.modules.cal.Events.add_detail_panel('more',"""
    id created:20 modified:20  
    outbox.MailsByController #postings.PostingsByController
    """,_("More"))
    
    
    
    # remove `project` field
    #~ site.modules.cal.Tasks.set_detail_layout("""
    #~ start_date workflow_buttons due_date done user id
    #~ summary 
    #~ calendar owner created:20 modified:20 user_modified  
    #~ description #notes.NotesByTask    
    #~ """)

    #~ site.modules.cal.Events.set_detail_layout("general more")
    
    
    site.modules.cal.Events.set_insert_layout("""
    summary 
    start end 
    calendar project 
    """,
    start="start_date start_time",
    end="end_date end_time",
    window_size=(60,'auto'))
    
