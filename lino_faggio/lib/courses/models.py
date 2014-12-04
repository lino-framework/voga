# -*- coding: UTF-8 -*-
# Copyright 2013-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
The :xfile:`models.py` module of the :mod:`lino_faggio.courses` app.

"""

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from lino import dd, rt
from lino.utils import mti

from lino.modlib.courses.models import *


class TeacherType(mixins.Referrable, mixins.BabelNamed, mixins.Printable):

    class Meta:
        abstract = dd.is_abstract_model(__name__, 'TeacherType')
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
        abstract = dd.is_abstract_model(__name__, 'Teacher')
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


class PupilType(mixins.Referrable, mixins.BabelNamed, mixins.Printable):

    class Meta:
        abstract = dd.is_abstract_model(__name__, 'PupilType')
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
        abstract = dd.is_abstract_model(__name__, 'Pupil')
        verbose_name = _("Participant")
        verbose_name_plural = _("Participants")
        # verbose_name = _("Pupil")
        # verbose_name_plural = _("Pupils")

    pupil_type = dd.ForeignKey('courses.PupilType', blank=True, null=True)

    suggested_courses = dd.ShowSlaveTable('courses.SuggestedCoursesByPupil')

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


# class ActiveCourses(ActiveCourses):
#     column_names = 'info max_places enrolments teacher line room *'
#     hide_sums = True


class CourseDetail(CourseDetail):
    main = "general events enrolments more"
    general = dd.Panel("""
    line teacher name workflow_buttons
    room start_date end_date start_time end_time
    # courses.EventsByCourse
    remark #OptionsByCourse
    """, label=_("General"))

    events = dd.Panel("""
    every_unit every max_date max_events
    monday tuesday wednesday thursday friday saturday sunday
    cal.EventsByController

    """, label=_("Events"))

    enrolments = dd.Panel("""
    max_places enrolments_until tariff
    EnrolmentsByCourse:40
    """, label=_("Enrolments"))

    more = dd.Panel("""
    # company contact_person
    user id events_text
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
    rt.modules.courses.Courses.set_detail_layout(CourseDetail())


def setup_main_menu(site, ui, profile, main):
    # m = main.get_item("contacts")
    m = main.add_menu("courses", config.verbose_name)
    m.add_action('courses.Pupils')
    m.add_action('courses.Teachers')
    m.add_separator()
    m.add_action('courses.Courses')
    m.add_action('courses.Lines')
    #~ m.add_action(Teachers)
    #~ m.add_action(Pupils)
    m.add_separator()
    m.add_action(PendingRequestedEnrolments)
    m.add_action(PendingConfirmedEnrolments)


def setup_config_menu(site, ui, profile, m):
    m = m.add_menu("courses", config.verbose_name)
    #~ m.add_action(Rooms)
    m.add_action('courses.TeacherTypes')
    m.add_action('courses.PupilTypes')
    m.add_action('courses.Topics')
    m.add_action('courses.Lines')
    m.add_action('courses.Slots')
