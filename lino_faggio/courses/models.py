# -*- coding: UTF-8 -*-
# Copyright 2013 Luc Saffre
# This file is part of the Lino project.
# Lino is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with Lino; if not, see <http://www.gnu.org/licenses/>.

"""
The :xfile:`models.py` module of the :mod:`lino_faggio.courses` app.

"""

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from lino import dd
#~ dd.extends_app('lino.modlib.courses',globals())
from lino.modlib.courses.models import *


class Teacher(Teacher):

    class Meta:
        verbose_name = _("Instructor")
        verbose_name_plural = _("Instructors")


class Pupil(Pupil):

    class Meta:
        verbose_name = _("Participant")
        verbose_name_plural = _("Participants")


class TeacherType(TeacherType):

    class Meta:
        verbose_name = _("Instructor Type")
        verbose_name_plural = _("Instructor Types")


class PupilType(PupilType):

    class Meta:
        verbose_name = _("Participant Type")
        verbose_name_plural = _("Participant Types")


class CoursesByTopic(CoursesByTopic):
    column_names = "start_date:8 line:20 room__company__city:10 weekdays_text:10 times_text:10"


class ActiveCourses(ActiveCourses):
    column_names = 'info max_places enrolments teacher room *'
    hide_sums = True


class CourseDetail(CourseDetail):
    main = "general more courses.EnrolmentsByCourse"
    general = dd.Panel("""
    line start_date start_time end_date end_time max_places
    teacher room #slot  state
    every_unit every max_events max_date
    monday tuesday wednesday thursday friday saturday sunday
    # cal.EventsByController
    courses.EventsByCourse
    """, label=_("General"))
    more = dd.Panel("""
    # company contact_person 
    user id
    sales.InvoicingsByInvoiceable
    """, label=_("More"))


@dd.receiver(dd.post_analyze)
def customize_courses(sender, **kw):
    site = sender
    site.modules.courses.Courses.set_detail_layout(CourseDetail())
    #~ site.modules.courses.Enrolments.set_insert_layout("""
    #~ request_date user
    #~ course pupil
    #~ tariff remark
    #~ """
    #~ )
    #~ site.modules.courses.ActiveCourses.column_names = 'info tariff max_places enrolments teacher company room'
