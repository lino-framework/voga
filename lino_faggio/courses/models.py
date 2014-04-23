# -*- coding: UTF-8 -*-
# Copyright 2013-2014 Luc Saffre
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
from lino.utils import mti

from lino.modlib.courses.models import *


class TeacherType(dd.Referrable, dd.BabelNamed, dd.Printable):

    class Meta:
        abstract = settings.SITE.is_abstract_model('courses.TeacherType')
        # verbose_name = _("Teacher type")
        # verbose_name_plural = _('Teacher types')
        verbose_name = _("Instructor Type")
        verbose_name_plural = _("Instructor Types")


class TeacherTypes(dd.Table):
    model = 'courses.TeacherType'
    required = dd.required(user_level='manager')
    detail_layout = """
    id name
    courses.TeachersByType
    """


class Teacher(Person):

    class Meta:
        abstract = settings.SITE.is_abstract_model('courses.Teacher')
        verbose_name = _("Instructor")
        verbose_name_plural = _("Instructors")

        # verbose_name = _("Teacher")
        # verbose_name_plural = _("Teachers")

    teacher_type = dd.ForeignKey('courses.TeacherType', blank=True, null=True)

    def __unicode__(self):
        return self.get_full_name(salutation=False)


class TeacherDetail(contacts.PersonDetail):
    general = dd.Panel(contacts.PersonDetail.main, label=_("General"))
    box5 = "remarks"
    main = "general courses.CoursesByTeacher \
    courses.EventsByTeacher cal.GuestsByPartner"


class Teachers(contacts.Persons):
    model = 'courses.Teacher'
    #~ detail_layout = TeacherDetail()
    column_names = 'name_column address_column teacher_type *'
    auto_fit_column_widths = True


class TeachersByType(Teachers):
    master_key = 'teacher_type'


class PupilType(dd.Referrable, dd.BabelNamed, dd.Printable):

    class Meta:
        abstract = settings.SITE.is_abstract_model('courses.PupilType')
        # verbose_name = _("Pupil type")
        # verbose_name_plural = _('Pupil types')
        verbose_name = _("Participant Type")
        verbose_name_plural = _("Participant Types")


class PupilTypes(dd.Table):
    model = 'courses.PupilType'
    required = dd.required(user_level='manager')
    detail_layout = """
    id name
    courses.PupilsByType
    """


class Pupil(Person):

    class Meta:
        abstract = settings.SITE.is_abstract_model('courses.Pupil')
        verbose_name = _("Participant")
        verbose_name_plural = _("Participants")
        # verbose_name = _("Pupil")
        # verbose_name_plural = _("Pupils")

    pupil_type = dd.ForeignKey('courses.PupilType', blank=True, null=True)

    def __unicode__(self):
        s = self.get_full_name(salutation=False)
        if self.pupil_type:
            s += " (%s)" % self.pupil_type.ref
        return s


class PupilDetail(contacts.PersonDetail):
    main = "general courses.EnrolmentsByPupil"

    general = dd.Panel(contacts.PersonDetail.main, label=_("General"))
    box5 = "remarks"

    #~ pupil = dd.Panel("""
    #~ EnrolmentsByPupil
    #~ """,label = _("Pupil"))

    #~ def setup_handle(self,lh):

        #~ lh.general.label = _("General")
        #~ lh.courses.label = _("School")
        #~ lh.notes.label = _("Notes")


class Pupils(contacts.Persons):
    model = 'courses.Pupil'
    #~ detail_layout = PupilDetail()
    column_names = 'name_column address_column pupil_type *'
    auto_fit_column_widths = True


class PupilsByType(Pupils):
    master_key = 'pupil_type'






class CoursesByTopic(CoursesByTopic):
    column_names = "start_date:8 line:20 \
    room__company__city:10 weekdays_text:10 times_text:10"


class ActiveCourses(ActiveCourses):
    column_names = 'info max_places enrolments teacher room *'
    hide_sums = True


class CourseDetail(CourseDetail):
    main = "general more courses.EnrolmentsByCourse"
    general = dd.Panel("""
    line start_date end_date start_time end_time max_places
    teacher room workflow_buttons
    every_unit every max_events max_date
    monday tuesday wednesday thursday friday saturday sunday
    cal.EventsByController
    # courses.EventsByCourse
    """, label=_("General"))
    more = dd.Panel("""
    # company contact_person 
    user id
    sales.InvoicingsByInvoiceable
    """, label=_("More"))


dd.inject_field(
    'contacts.Person',
    'is_teacher',
    mti.EnableChild(
        'courses.Teacher',
        verbose_name=_("is a teacher"),
        help_text=_("Whether this Person is also a Teacher.")))

dd.inject_field(
    'contacts.Person',
    'is_pupil',
    mti.EnableChild(
        'courses.Pupil',
        verbose_name=_("is a pupil"),
        help_text=_("Whether this Person is also a Pupil.")))




@dd.receiver(dd.post_analyze)
def customize_courses(sender, **kw):
    dd.modules.courses.Courses.set_detail_layout(CourseDetail())


def setup_main_menu(site, ui, profile, main):
    m = main.get_item("contacts")
    m.add_action('courses.Teachers')
    m.add_action('courses.Pupils')
    m = main.add_menu("courses", config.verbose_name)
    m.add_action(Courses)
    #~ m.add_action(Teachers)
    #~ m.add_action(Pupils)
    m.add_action(PendingRequestedEnrolments)
    m.add_action(PendingConfirmedEnrolments)



def setup_config_menu(site, ui, profile, m):
    m = m.add_menu("courses", config.verbose_name)
    #~ m.add_action(Rooms)
    m.add_action('courses.TeacherTypes')
    m.add_action('courses.PupilTypes')
    m.add_action(Topics)
    m.add_action(Lines)
    m.add_action(Slots)
