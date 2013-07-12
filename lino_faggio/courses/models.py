# -*- coding: UTF-8 -*-
## Copyright 2013 Luc Saffre
## This file is part of the Lino project.
## Lino is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino; if not, see <http://www.gnu.org/licenses/>.

"""
Deserves a docstring.
"""

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from lino import dd
#~ dd.extends_app('lino.modlib.courses',globals())
from lino.modlib.courses.models import *

sales = dd.resolve_app('sales')

class Course(Course,sales.Invoiceable):
    
    invoiceable_date_field = 'start_date'
    invoiceable_partner_field = 'company'
    
    def get_invoiceable_product(self): 
        #~ if self.organizer and self.room: 
        if self.company and self.room: 
            if self.company != settings.SITE.site_config.site_company: 
                return self.room.tariff
            
    #~ def get_invoiceable_title(self): 
        #~ if self.organizer: 
            #~ return unicode(self.room)

    def get_invoiceable_qty(self): 
        return self.max_events or 1

class CoursesByTopic(CoursesByTopic):
    column_names = "start_date:8 line:20 room__company__city:10 weekdays_text:10 times_text:10"
        

class ActiveCourses(ActiveCourses):
    column_names = 'info tariff max_places enrolments teacher company room'
    hide_sums = True

class CourseDetail(CourseDetail):     
    main = "general cal.EventsByController"
    general = dd.Panel("""
    line teacher start_date start_time room #slot state id:8
    max_places max_events end_date end_time every_unit every
    monday tuesday wednesday thursday friday saturday sunday
    company contact_person user calendar tariff
    courses.EnrolmentsByCourse
    """,label=_("General"))
    

@dd.receiver(dd.post_analyze)
def customize_courses(sender,**kw):
    site = sender
    site.modules.courses.Courses.set_detail_layout(CourseDetail())
    #~ site.modules.courses.ActiveCourses.column_names = 'info tariff max_places enrolments teacher company room'
    

